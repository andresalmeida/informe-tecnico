"""ADR semantics and rendering, without adding document-specific validation to the engine."""
import copy
import json
from datetime import date

import pdfplumber
from pypdf import PdfReader


def run_checks(example, checks, build, rejected_with):
    def load(name):return json.loads((example.parent/f'ejemplo-{name}.json').read_text())
    def find(source,key):return next(b for s in source['sections'] for b in s['blocks'] if b.get('id')==key)
    def fields(source):return [i for s in source['sections'] for b in s['blocks'] if b['type']=='fields' for i in b['items']]
    def state(source):return next(i for i in fields(source) if i['label']=='Estado')
    def values(source):return {i['label']:i.get('value') for i in fields(source)}
    def semantic(source,known):
        vals=values(source)
        if state(source)['selected']=='Sustituida':
            assert vals.get('Sustituida por') in known and vals['Sustituida por']!=source['document']['code']
        if vals.get('Sustituye a'):
            assert vals['Sustituye a'] in known and vals['Sustituye a']!=source['document']['code']
    source=load('decision-arquitectura');fac=load('informe-factibilidad');scope=load('alcance-proyecto');risk=load('registro-riesgos')
    result,pdf=build('decision-arquitectura',source)
    assert result['pages']==2
    assert date.fromisoformat(fac['document']['date'])<date.fromisoformat(source['document']['date'])<date.fromisoformat(scope['document']['date'])
    encoded=json.dumps(source,ensure_ascii=False)
    assert all(code in encoded for code in ('DEMO-REQ-014',fac['document']['code'],risk['document']['code']))
    assert '50 cobros y 10 reembolsos' in encoded
    risks=next(b for s in risk['sections'] for b in s['blocks'] if b['type']=='risks')['items']
    assert next(r for r in risks if r['id']=='R-07')['state']=='Cerrado'
    for code in ('R-04','R-05','R-07'):assert any(r['id']==code for r in risks)
    assert state(source)['selected']=='Aceptada' and len(state(source)['options'])==4
    alternatives=find(source,'alternativas')['rows']
    assert len(alternatives)>=2
    decision=next(s for s in source['sections'] if s['id']=='decision')['blocks'][0]['text'].lower()
    assert alternatives[0][0].lower() in decision
    assert 'Sustituye a' not in values(source) and 'Sustituida por' not in values(source)
    semantic(source,{source['document']['code']})
    assert PdfReader(pdf).metadata.author=='Entidad de demostración'
    with pdfplumber.open(pdf) as printed:
        texts=[' '.join((p.extract_text() or '').split()) for p in printed.pages]
        boxes=[r for p in printed.pages for r in p.rects if abs(r['width']-9)<.01 and abs(r['height']-9)<.01]
        diagonals=[l for p in printed.pages for l in p.lines if abs(l['width']-5.2)<.01 and abs(l['height']-5.2)<.01]
        assert len(boxes)==4 and len(diagonals)==2
        bold=''.join(c['text'] for p in printed.pages for c in p.chars if 'Bold' in c['fontname'])
        assert 'Aceptada' in bold
        destinations={e['id']:e['page'] for e in result['entries']}
        for key in ('alternativas','firmas'):
            table=find(source,key)
            page=printed.pages[destinations[key]-1]
            left=21*72/25.4
            width=(page.width-2*left)*table['widths'][0]/sum(table['widths'])
            column=' '.join((page.crop((left,0,left+width,page.height)).extract_text() or '').split())
            assert all(' '.join(r[0].split()) in column for r in table['rows'])
        assert destinations['firmas']==result['pages'] and 'Histórico de revisiones' in texts[-1]
    checks.append({'case':'adr-aceptada-cadena-y-una-marca','pages':result['pages']})
    for logo in (False,True):
        custom=copy.deepcopy(source)
        custom['brand'].update(entity='Organización de prueba',unit='Oficina de Proyectos',accent='#7A2E1D')
        custom['document'].update(code='ACME-ADR-07',paper='Letter')
        if logo:custom['brand']['logo']='test-logo.png'
        custom_result,custom_pdf=build('adr-identidad-'+str(logo),custom)
        assert custom_result['paper']=='Letter'
        assert any(a['path']=='test-logo.png' for a in custom_result['assets'])==logo
        checks.append({'case':'adr-identidad','logo':logo,'pages':custom_result['pages']})
    personalized=copy.deepcopy(source)
    state(personalized).update(options=['En estudio','Adoptada','Descartada','Reemplazada'],selected='Adoptada')
    _,custom_pdf=build('adr-etiquetas-propias',personalized)
    assert 'Adoptada' in ' '.join(p.extract_text() for p in PdfReader(custom_pdf).pages)
    checks.append({'case':'adr-estado-personalizable'})
    # The fixture creates both documents in memory; no nonexistent successor is added to the catalog.
    replaced=copy.deepcopy(source);successor=copy.deepcopy(source)
    successor['document']['code']='DEMO-ADR-02'
    next(i for i in fields(successor) if i['label']=='N.º de decisión')['value']='DEMO-ADR-02'
    state(replaced)['selected']='Sustituida'
    next(b for s in replaced['sections'] for b in s['blocks'] if b['type']=='fields')['items'].append(
        {'label':'Sustituida por','value':successor['document']['code']})
    next(b for s in successor['sections'] for b in s['blocks'] if b['type']=='fields')['items'].append(
        {'label':'Sustituye a','value':source['document']['code']})
    known={source['document']['code'],successor['document']['code']}
    semantic(replaced,known);semantic(successor,known)
    build('adr-sustituida-con-codigo',replaced)
    missing=copy.deepcopy(replaced)
    for s in missing['sections']:
        for b in s['blocks']:
            if b['type']=='fields':b['items']=[i for i in b['items'] if i['label']!='Sustituida por']
    try:semantic(missing,known)
    except AssertionError:pass
    else:raise AssertionError('Una decisión sustituida requiere el código sucesor')
    checks.append({'case':'adr-sustitucion-con-codigos-reciprocos-y-control-de-ausencia'})
    indexed=copy.deepcopy(source);indexed['document']['indexes']=['contents']
    _,indexed_pdf=build('adr-indice-opcional',indexed)
    assert 'Contenido' in PdfReader(indexed_pdf).pages[0].extract_text()
    checks.append({'case':'adr-indice-opcional'})
    for name,change,message in [
        ('sin-estado',lambda s:state(s).update(value='Propuesta'), 'usar value o options'),
        ('estado-sin-marca',lambda s:state(s).pop('selected'),'selected debe ser exactamente una'),
        ('estado-doble',lambda s:state(s).update(selected=['Aceptada','Propuesta']),'multiple: true'),
        ('estado-ajeno',lambda s:state(s).update(selected='Otro'),'selected debe ser exactamente una'),
    ]:
        broken=copy.deepcopy(source);change(broken);rejected_with('adr-'+name,broken,message)
    no_choice=copy.deepcopy(source)
    item=state(no_choice);item.clear();item.update(label='Estado',value='Por confirmar')
    rejected_with('adr-sin-eleccion-global',no_choice,'decision-arquitectura requiere el estado marcado')
    multiple=copy.deepcopy(source);state(multiple).update(multiple=True,selected=['Aceptada'])
    rejected_with('adr-marca-multiple-no-sustituye-estado',multiple,'decision-arquitectura requiere el estado marcado')
