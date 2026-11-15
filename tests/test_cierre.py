"""Check the closure against evidence already present in the catalog."""
import copy
import json
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pypdf import PdfReader
import pdfplumber


def run_checks(example, root, checks, build, rejected_with):
    assets = example.parent
    source = json.loads((assets/'ejemplo-informe-cierre.json').read_text())
    def block(name):
        return next(b for s in source['sections'] for b in s['blocks'] if b.get('id') == name)
    result, pdf = build('informe-cierre', source)
    assert result['pages'] == 4
    pages = [p.extract_text() or '' for p in PdfReader(pdf).pages]
    assert 'Entregado con pendientes' in ' '.join(pages)
    assert 'sin ejecutar' in ' '.join(pages)
    assert 'Firmas de responsabilidad' in pages[-1] and 'Histórico de revisiones' in pages[-1]
    assert 'Rafael Mena' in pages[-1] and 'Lucía Ferrer' in pages[-1]
    ent = json.loads((assets/'ejemplo-acta-entrega.json').read_text())
    inventory = next(b for s in ent['sections'] for b in s['blocks'] if b.get('id') == 'entregables')
    assert [r[:2] for r in block('inventario')['rows']] == [r[:2] for r in inventory['rows']]
    assert date.fromisoformat(source['document']['date']) > date.fromisoformat(ent['document']['date'])
    assert (date(2027, 1, 17)-date(2026, 11, 23)).days+1 == 8*7
    for row in block('variaciones')['rows']:
        estimated, actual = map(Decimal, row[1:3])
        assert Decimal(row[3]) == actual-estimated
        percent = (100*(actual-estimated)/estimated).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        assert Decimal(row[4].replace(' %','').replace(',','.')) == percent
    fac = (assets/'ejemplo-informe-factibilidad.json').read_text()
    assert '50' in fac and '7' in fac
    assert all(not b.get('options') for s in source['sections'] for b in s['blocks'])
    with pdfplumber.open(pdf) as printed:
        # Each row of these short tables remains intact and every table stays on one page.
        for entry in result['entries']:
            if entry['id'] in ('inventario','variaciones','aprendizajes','pendientes','firmas'):
                table = block(entry['id'])
                page = printed.pages[entry['page']-1]
                left = 21*72/25.4
                right = left+(page.width-2*left)*table['widths'][0]/sum(table['widths'])
                text = page.crop((left,58*72/25.4,right,page.height-20*72/25.4)).extract_text() or ''
                for row in table['rows']:
                    assert ' '.join(row[0].split()) in ' '.join(text.split())
    checks.append({'case':'informe-cierre-evidencia-variaciones-tablas','pages':result['pages']})
    for logo in (False, True):
        value = copy.deepcopy(source)
        value['brand'].update(entity='Organización de prueba', unit='Oficina de cierre', accent='#7A2E1D')
        value['document'].update(code='ACME-CIE-02', paper='Letter')
        if logo: value['brand']['logo'] = 'test-logo.png'
        customized, _ = build('cierre-logo' if logo else 'cierre-sin-logo', value)
        assert customized['paper'] == 'Letter'
        checks.append({'case':'cierre-personalizado','logo':logo})
    value = copy.deepcopy(source)
    value['document']['indexes'] = ['contents', 'tables']
    indexed, _ = build('cierre-indices', value)
    assert indexed['pages'] > result['pages']
    checks.append({'case':'cierre-indices'})
    value = copy.deepcopy(source)
    value['sections'][0]['blocks'].append({'type':'fields','items':[{'label':'Prueba','options':['A','B'],'selected':'C'}]})
    rejected_with('cierre-eleccion-invalida',value,'exactamente una de las options')
