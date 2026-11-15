"""The compact process card preserves its map, records and measurement definitions."""
import copy
import json
import xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader
import pdfplumber


def run_checks(example, root, checks, build, rejected_with):
    source=json.loads((example.parent/'ejemplo-ficha-proceso.json').read_text())
    def block(name):return next(b for s in source['sections'] for b in s['blocks'] if b.get('id')==name)
    result,pdf=build('ficha-proceso',source)
    assert result['pages']==2
    entries={e['id']:e['page'] for e in result['entries']}
    assert entries['sipoc-mapa']==entries['flujo']==1
    assert entries['responsabilidad']==entries['medidas']==2
    stage=block('flujo')['rows']
    assert [r[0] for r in stage]==list(map(str,range(1,9)))
    kinds=['registro-requerimientos','informe-factibilidad','propuesta-servicio','propuesta-servicio',
           'alcance-proyecto','especificacion-requisitos','plan-pruebas','acta-entrega']
    for row,kind in zip(stage,kinds):
        record=json.loads((example.parent/f'ejemplo-{kind}.json').read_text())
        assert record['document']['code'] in row[4]
    svg=ET.parse(example.parent/'diagrams/sipoc-proyectos.svg').getroot()
    svg_text=' '.join(svg.itertext())
    for value in block('sipoc-texto')['headers']+block('sipoc-texto')['rows'][0]:
        assert value in ' '.join(svg_text.split()),value
    ns={'s':'http://www.w3.org/2000/svg'}
    nodes=[r for r in svg.findall('s:rect',ns) if r.get('width')=='104']
    assert len(nodes)==5 and [float(r.attrib['x']) for r in nodes]==[8,128,248,368,488]
    assert len(svg.findall('s:path',ns))==4
    with Image.open(example.parent/'diagrams/sipoc-proyectos.png') as im:
        assert im.width==1800 and abs(im.height-300)<=3
    assert any(a['path']=='diagrams/sipoc-proyectos.png' for a in result['assets'])
    assert block('medidas')['rows'][0][2]=='100 × entregas con evidencia / entregas totales'
    assert block('medidas')['rows'][1][2]=='100 × pendientes cerrados / pendientes registrados'
    with pdfplumber.open(pdf) as printed:
        for entry in result['entries']:
            if entry['kind']!='table':continue
            table=block(entry['id']);page=printed.pages[entry['page']-1];left=21*72/25.4
            right=left+(page.width-2*left)*table['widths'][0]/sum(table['widths'])
            text=page.crop((left,58*72/25.4,right,page.height-20*72/25.4)).extract_text() or ''
            for row in table['rows']:
                assert ' '.join(row[0].split()) in ' '.join(text.split())
        last=printed.pages[-1].extract_text() or ''
        assert 'Denominador cero: No aplica.' in ' '.join(last.split())
        assert 'Histórico de revisiones' in last and last.count('Fecha: Pendiente')==3
        assert len(printed.pages[0].images)==1
    checks.append({'case':'ficha-proceso-dos-paginas-sipoc-registros-formulas','pages':2})
    for logo in (False,True):
        value=copy.deepcopy(source)
        value['brand'].update(entity='Organización de prueba',unit='Oficina de procesos',accent='#7A2E1D')
        value['document'].update(code='ACME-FPR-02',paper='Letter')
        # Identity of an external figure belongs to the source asset, separately from report styling.
        if logo:value['brand']['logo']='test-logo.png'
        custom,_=build('proceso-logo' if logo else 'proceso-sin-logo',value)
        assert custom['paper']=='Letter'
        checks.append({'case':'proceso-personalizado','logo':logo,'pages':custom['pages']})
    value=copy.deepcopy(source);value['document']['indexes']=['contents','tables','figures']
    indexed,_=build('proceso-indices',value);assert indexed['pages']>2
    checks.append({'case':'proceso-indices'})
    value=copy.deepcopy(source)
    value['sections'][0]['blocks'].append({'type':'fields','items':[{'label':'Prueba','options':['A','B'],'selected':'C'}]})
    rejected_with('proceso-eleccion-invalida',value,'exactamente una de las options')
