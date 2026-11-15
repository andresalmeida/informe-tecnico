"""A proposed retirement cannot silently become a completed operational event."""
import copy
import json
from datetime import date
from pypdf import PdfReader
import pdfplumber


def run_checks(example, root, checks, build, rejected_with):
    source = json.loads((example.parent/'ejemplo-acta-baja.json').read_text())
    def block(value, name):
        return next(b for s in value['sections'] for b in s['blocks'] if b.get('id') == name)
    result, pdf = build('acta-baja', source)
    assert result['pages'] == 4
    text = ' '.join((' '.join(p.extract_text() or '' for p in PdfReader(pdf).pages)).split())
    assert 'Baja prevista, sin ejecutar.' in text
    assert 'No consta puesta en producción.' in text
    assert source['document']['lifecycle'] == {'state':'borrador'}
    assert {r[1] for r in block(source,'afectados')['rows']} == {'retirado','archivado'}
    assert all(r[2] == 'Pendiente' for r in block(source,'afectados')['rows'])
    assert 'Documento heredado sin código' in text
    req = (example.parent/'ejemplo-registro-requerimientos.json').read_text()
    assert 'el cobro se coordina por teléfono' in req
    ent = json.loads((example.parent/'ejemplo-acta-entrega.json').read_text())
    assert date(2027,1,20) > date.fromisoformat(source['document']['date']) > date.fromisoformat(ent['document']['date'])
    for code, name in [('DEMO-CIE-01','informe-cierre'),('DEMO-ALC-01','alcance-proyecto'),('DEMO-ARQ-01','descripcion-arquitectura'),('DEMO-ERS-01','especificacion-requisitos')]:
        assert json.loads((example.parent/f'ejemplo-{name}.json').read_text())['document']['code'] == code
        assert code in text
    with pdfplumber.open(pdf) as printed:
        for entry in result['entries']:
            if entry['kind'] != 'table' or entry['id'] == 'revision-history': continue
            table = block(source,entry['id'])
            page = printed.pages[entry['page']-1]
            left = 21*72/25.4
            right = left+(page.width-2*left)*table['widths'][0]/sum(table['widths'])
            first = page.crop((left,58*72/25.4,right,page.height-20*72/25.4)).extract_text() or ''
            for row in table['rows']:
                assert ' '.join(row[0].split()) in ' '.join(first.split())
        last = printed.pages[-1].extract_text()
        assert 'Rafael Mena' in last and 'Lucía Ferrer' in last and 'Histórico de revisiones' in last
    checks.append({'case':'acta-baja-propuesta-coherente-tablas','pages':result['pages']})
    for logo in (False,True):
        value=copy.deepcopy(source)
        value['brand'].update(entity='Organización de prueba',unit='Oficina de operaciones',accent='#7A2E1D')
        value['document'].update(code='ACME-BAJ-02',paper='Letter')
        if logo:value['brand']['logo']='test-logo.png'
        custom,_=build('baja-logo' if logo else 'baja-sin-logo',value)
        assert custom['paper']=='Letter'
        checks.append({'case':'baja-personalizada','logo':logo})
    value=copy.deepcopy(source);del value['document']['lifecycle']
    plain,_=build('baja-sin-ciclo',value)
    assert 'lifecycle' not in plain
    checks.append({'case':'baja-sin-ciclo'})
    value=copy.deepcopy(source);value['document']['indexes']=['contents','tables']
    indexed,_=build('baja-indices',value);assert indexed['pages']>result['pages']
    checks.append({'case':'baja-indices'})
    value=copy.deepcopy(source)
    block(value,'pasos')['rows'].extend([[f'Paso de prueba {n}','Por confirmar','Resultado: Pendiente.','Rol de prueba'] for n in range(5,45)])
    expanded,expanded_pdf=build('baja-plan-extenso',value)
    pages=[p.extract_text() or '' for p in PdfReader(expanded_pdf).pages]
    assert sum('Plan propuesto y evidencia de baja' in p for p in pages)>=2
    assert any('Paso de prueba 44' in p and 'Plan propuesto y evidencia de baja' in p for p in pages)
    checks.append({'case':'baja-plan-extenso','pages':expanded['pages']})
    value=copy.deepcopy(source)
    value['sections'][0]['blocks'].append({'type':'fields','items':[{'label':'Prueba','options':['A','B'],'selected':'C'}]})
    rejected_with('baja-eleccion-invalida',value,'exactamente una de las options')
