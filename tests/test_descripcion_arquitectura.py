"""Architecture views preserve the chain's codes, criteria, dates and pending evidence."""
import copy
import json
import re
from datetime import date
from xml.etree import ElementTree as ET

import pdfplumber
from PIL import Image
from pypdf import PdfReader


def run_checks(example, checks, build, rejected_with):
    assets=example.parent
    def load(kind):return json.loads((assets/f'ejemplo-{kind}.json').read_text())
    def block(source,key):return next(b for s in source['sections'] for b in s['blocks'] if b.get('id')==key)
    def field(source,label):return next(i for s in source['sections'] for b in s['blocks'] if b['type']=='fields' for i in b['items'] if i['label']==label)
    source=load('descripcion-arquitectura');adr=load('decision-arquitectura');scope=load('alcance-proyecto');atp=load('plan-pruebas');risks=load('registro-riesgos');delivery=load('acta-entrega')
    result,pdf=build('descripcion-arquitectura',source)
    assert result['pages']==10,result['pages']
    assert source['document']['indexes']==['contents','figures']
    assert date.fromisoformat(scope['document']['date'])<date.fromisoformat(source['document']['date'])<date.fromisoformat(delivery['document']['date'])
    assert field(source,'Versión del sistema')['value']=='Por confirmar con Iván Salas'
    assert 'Pendiente' in field(source,'Naturaleza del corte')['value']
    assert not any('options' in i for s in source['sections'] for b in s['blocks'] if b['type']=='fields' for i in b['items'])
    assert PdfReader(pdf).metadata.author=='Entidad de demostración'
    assert source['document']['code'] in PdfReader(pdf).metadata.subject
    checks.append({'case':'arq-descripcion-con-dos-indices','pages':result['pages']})

    # Every document, risk and test-case code must resolve to an example, including the first ADR.
    known={json.loads(p.read_text())['document']['code'] for p in assets.glob('ejemplo*.json')}
    encoded=json.dumps(source,ensure_ascii=False)
    assert set(re.findall(r'\bDEMO-[A-Z]{3}-\d+\b',encoded))<=known
    risk_items=next(b for s in risks['sections'] for b in s['blocks'] if b['type']=='risks')['items']
    by_risk={r['id']:r for r in risk_items}
    assert set(re.findall(r'\bR-\d{2}\b',encoded))<=set(by_risk)
    cases={b['id']:b for s in atp['sections'] for b in s['blocks'] if b['type']=='testcase'}
    assert set(re.findall(r'\bCP-\d{2}\b',encoded))==set(cases)
    decision=block(source,'decisiones-adr')['rows'][0]
    assert decision[0]==adr['document']['code'] and decision[1]==field(adr,'Título')['value']
    assert decision[2].startswith(field(adr,'Estado')['selected'])
    for row in block(source,'riesgos-arquitectura')['rows']:
        risk=by_risk[row[0]]
        assert row[1:]==[risk['event'],risk['state'],risk['owner']]
    criteria=next(b for s in scope['sections'] if s['id']=='criterios' for b in s['blocks'] if b['type']=='list')['items']
    for i,(row,criterion) in enumerate(zip(block(source,'calidad-criterios')['rows'],criteria),1):
        label,expected=criterion.split(': ',1)
        assert row[:2]==[label,expected]
        assert cases[f'CP-0{i}']['title']==label and cases[f'CP-0{i}']['expected']==expected
        assert f"{atp['document']['code']} / CP-0{i}" in row[3] and 'Pendiente' in row[3]
        assert not cases[f'CP-0{i}'].get('executed',False)
    assert len(block(source,'calidad-criterios')['rows'])==len(criteria)==5
    assert block(source,'firmas')['rows']==block(scope,'firmas')['rows']
    checks.append({'case':'arq-todos-los-codigos-resuelven-y-criterios-conservados','risks':len(by_risk),'cases':len(cases)})

    figures=[b for s in source['sections'] for b in s['blocks'] if b['type']=='figure']
    assert len(figures)==2 and {f['id'] for f in figures}=={'contexto-sistema','frontera-tarjeta'}
    for f in figures:
        image=assets/f['path'];svg=image.with_suffix('.svg');html=image.with_suffix('.html')
        root=ET.fromstring(svg.read_text());view=list(map(float,root.attrib['viewBox'].split()))
        assert root.attrib['role']=='img'
        ids={el.attrib.get('id') for el in root.iter()}
        assert set(root.attrib['aria-labelledby'].split())<=ids
        # Browser screenshot bounds round fractional layout positions to CSS pixels.
        with Image.open(image) as raster:
            assert all(abs(actual-expected*3)<=3 for actual,expected in zip(raster.size,view[2:]))
        assert 'fonts.googleapis' not in html.read_text()
        assert 'DIAGRAMA DEMOSTRATIVO' in svg.read_text()
        assert 'Diagrama demostrativo' in f['source']
    assert set(a['path'] for a in result['assets'])==set(f['path'] for f in figures)
    assert all(not a['path'].startswith('/') for a in result['assets'])
    checks.append({'case':'arq-figuras-accesibles-y-exportaciones-3x','figures':2})

    with pdfplumber.open(pdf) as printed:
        destinations={e['id']:e['page'] for e in result['entries']}
        first=' '.join((printed.pages[0].extract_text() or '').split())
        assert 'Contenido' in first and 'Índice de figuras' in first
        for entry in result['entries']:
            if entry['kind'] in ('section','figure'):
                label=' '.join(entry['label'].split())
                assert re.search(re.escape(label)+r'\s*(?:\.\s*)+'+str(entry['page'])+r'\b',first),(label,entry['page'])
        for table in [b for s in source['sections'] for b in s['blocks'] if b['type']=='table']:
            page=printed.pages[destinations[table['id']]-1]
            left=21*72/25.4;width=(page.width-2*left)*table['widths'][0]/sum(table['widths'])
            column=' '.join((page.crop((left,0,left+width,page.height)).extract_text() or '').split())
            assert all(' '.join(row[0].split()) in column for row in table['rows']),table['id']
        assert destinations['firmas']==result['pages']
        assert 'Histórico de revisiones' in printed.pages[-1].extract_text()
        assert destinations['contexto-sistema']!=destinations['frontera-tarjeta']
        assert any(w['text']=='Compatibilidad' for w in printed.pages[destinations['calidad-criterios']-1].extract_words())
        assert any(w['text']=='Riesgo' for w in printed.pages[destinations['riesgos-arquitectura']-1].extract_words())
    checks.append({'case':'arq-indices-con-destinos-y-tablas-enteras'})

    no_index=copy.deepcopy(source);no_index['document'].pop('indexes')
    no_index_result,no_index_pdf=build('arq-sin-indices',no_index)
    assert 'Contenido' not in PdfReader(no_index_pdf).pages[0].extract_text()
    assert no_index_result['pages']<result['pages']
    checks.append({'case':'arq-indices-opcionales','without_indexes':no_index_result['pages']})
    for logo in (False,True):
        custom=copy.deepcopy(source)
        custom['brand'].update(entity='Organización de prueba',unit='Oficina de Proyectos')
        # The embedded figures keep the same palette; recoloring requires regenerating their sources.
        custom['document'].update(code='ACME-ARQ-07',paper='Letter')
        if logo:custom['brand']['logo']='test-logo.png'
        custom_result,custom_pdf=build('arq-identidad-'+str(logo),custom)
        assert custom_result['paper']=='Letter'
        assert any(a['path']=='test-logo.png' for a in custom_result['assets'])==logo
        assert ('Organización de prueba' in PdfReader(custom_pdf).pages[0].extract_text())!=logo
        checks.append({'case':'arq-identidad','logo':logo,'pages':custom_result['pages']})
    broken=copy.deepcopy(source)
    broken['sections'][0]['blocks'][0]['items'].append({'label':'Revisión','options':['Inicial','Final'],'selected':'Ajena'})
    rejected_with('arq-eleccion-invalida-sigue-rechazada',broken,'selected debe ser exactamente una')
    broken=copy.deepcopy(source);block(broken,'frontera-tarjeta')['id']='contexto-sistema'
    rejected_with('arq-figura-duplicada',broken,'ID duplicado')
