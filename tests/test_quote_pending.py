"""Known prices with an unknown tax remain a usable before-tax quotation."""
import copy
import json
import sys
from decimal import Decimal
from pathlib import Path

from pypdf import PdfReader

_scripts = Path(__file__).resolve().parents[1] / "skills" / "informe-tecnico" / "scripts"
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from build_report import validate_quote


def run_checks(example, root, checks, build, rejected_with):
    sample=json.loads((example.parent/'ejemplo-propuesta-servicio.json').read_text())
    quote=next(b for s in sample['sections'] for b in s['blocks'] if b['type']=='quote')
    value={key:copy.deepcopy(sample[key]) for key in ('schema_version','brand','document','format','changes')}
    value['document'].update(title='Cotización de demostración',short_title='Cotización',show_changes=False)
    quote['tax_rate']=None
    value['sections']=[{'id':'inversion','title':'Inversión','blocks':[
        {'type':'paragraph','text':'Precios de demostración. La entidad todavía debe confirmar el impuesto.'},quote]}]
    def printed(pdf):return ' '.join(' '.join(p.extract_text() or '' for p in PdfReader(pdf).pages).split())
    for name,profile,paper,tax_name in [('predeterminado','institucional','A4',None),
                                         ('nombre-propio-carta','institucional','Letter','Tributo de demostración')]:
        source=copy.deepcopy(value)
        source['format']['profile']=profile;source['document']['paper']=paper
        if tax_name is None:source['sections'][0]['blocks'][1].pop('tax_name',None)
        else:source['sections'][0]['blocks'][1]['tax_name']=tax_name
        checked=copy.deepcopy(source['sections'][0]['blocks'][1]);validate_quote(checked)
        assert checked['_subtotal']==checked['_total']==Decimal('23100.00')
        assert checked['_rate'] is None and checked['_tax'] is None
        result,pdf=build('cotizacion-impuesto-pendiente-'+name,source)
        text=printed(pdf)
        assert 'Total antes de impuestos (USD)' in text and 'Por confirmar' in text
        assert (tax_name or 'Impuesto') in text and '23.100,00' in text
        assert '0 %' not in text and '26.565,00' not in text
        checks.append({'case':'cotizacion-impuesto-pendiente-'+name,'pages':result['pages']})
    source=copy.deepcopy(value);source['sections'][0]['blocks'][1]['tax_rate']=0
    result,pdf=build('cotizacion-tasa-cero-explicita',source)
    text=printed(pdf)
    assert 'Impuesto, 0 %' in text and 'Total (USD)' in text and 'antes de impuestos' not in text
    checks.append({'case':'cotizacion-tasa-cero-explicita'})
    source=copy.deepcopy(value)
    source['sections'][0]['blocks'][1]['items']=[{'concept':'Ajuste de demostración','quantity':0.5,'unit_price':0.01}]
    result,pdf=build('cotizacion-pendiente-redondeo',source)
    assert '0,01' in printed(pdf) and 'Por confirmar' in printed(pdf)
    checks.append({'case':'cotizacion-pendiente-redondeo'})
    source=copy.deepcopy(value);source['sections'][0]['blocks'][1].pop('tax_rate')
    rejected_with('cotizacion-sin-clave-tasa',source,'por ejemplo "tax_rate": 0.15 o "tax_rate": null')
    source=copy.deepcopy(value);source['sections'][0]['blocks'][1]['tax_rate']='null'
    rejected_with('cotizacion-null-debe-ser-nulo-json',source,'tax_rate no es un número ni null')
    source=copy.deepcopy(value);source['sections'][0]['blocks'][1]['tax_rate']=False
    rejected_with('cotizacion-tasa-booleana',source,'tax_rate no es un número ni null')
    source=copy.deepcopy(value);source['sections'][0]['blocks'][1]['total']=23100
    rejected_with('cotizacion-pendiente-total-manual',source,'quitar total')
