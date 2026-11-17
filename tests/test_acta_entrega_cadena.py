"""Validate the delivery example and its links to the payment project chain."""
import copy
import json
from datetime import date, datetime, timedelta

import pdfplumber
from pypdf import PdfReader


def run_checks(example, checks, build, rejected_with):
    def load(kind):
        return json.loads((example.parent/f'ejemplo-{kind}.json').read_text())
    def block(source, key):
        return next(b for s in source['sections'] for b in s.get('blocks',[]) if b.get('id')==key)
    def section(source,key):
        return next(s for s in source['sections'] if s['id']==key)
    def item(source,label):
        return next(i for s in source['sections'] for b in s['blocks'] if b['type']=='fields'
                    for i in b['items'] if i['label']==label)
    def pages(pdf):
        return [' '.join((p.extract_text() or '').split()) for p in PdfReader(pdf).pages]
    def marks(pdf):
        with pdfplumber.open(pdf) as printed:
            boxes=sum(abs(r['width']-9)<.01 and abs(r['height']-9)<.01 for pg in printed.pages for r in pg.rects)
            diagonals=sum(abs(l['width']-5.2)<.01 and abs(l['height']-5.2)<.01 for pg in printed.pages for l in pg.lines)
        return boxes,diagonals//2

    source=load('acta-entrega'); scope=load('alcance-proyecto'); training=load('acta-capacitacion')
    atp=load('plan-pruebas'); feasibility=load('informe-factibilidad'); request=load('registro-requerimientos')
    result,pdf=build('entrega-cadena',source)
    text_pages=pages(pdf); text=' '.join(text_pages)
    assert result['pages']==3,result['pages']
    assert source['document']['show_changes'] is True
    assert marks(pdf)==(2,1),marks(pdf)
    with pdfplumber.open(pdf) as printed:
        bold=''.join(c['text'] for pg in printed.pages for c in pg.chars if 'Bold' in c['fontname'])
        assert 'Con capacitación' in bold
    assert PdfReader(pdf).metadata.author=='Entidad de demostración'
    assert 'DEMO-ENT-01' in PdfReader(pdf).metadata.subject
    assert 'Atlas' not in json.dumps(source,ensure_ascii=False)
    assert 'Conforme' not in [o for s in source['sections'] for b in s['blocks'] if b['type']=='fields'
                              for i in b['items'] for o in i.get('options',[])]
    checks.append({'case':'entrega-cadena','pages':result['pages'],'boxes':2,'marks':1})

    inventory=block(source,'entregables'); deliverables=block(scope,'entregas')['rows']
    assert inventory['headers']==['Ítem','Entregable','Formato o ubicación','Comprobación y observaciones']
    assert [r[:2] for r in inventory['rows']]==[r[:2] for r in deliverables]
    assert [r[0] for r in inventory['rows']]==['E1','E2','E3','E4','E5']
    assert all('Por confirmar' in r[2] for r in inventory['rows'])
    assert all('Criterio:' in r[3] and 'Resultado: Pendiente' in r[3] for r in inventory['rows'][:4])
    assert 'Constancia de ejecución y firmas pendientes' in inventory['rows'][-1][3]
    assert not any(s['id'] in ('recepcion','antecedentes') for s in source['sections'])
    information=section(source,'informacion')
    assert len([b for b in information['blocks'] if b['type']=='paragraph'])==1
    checks.append({'case':'entrega-inventario-E1-a-E5-e-informacion-fundida'})

    encoded=json.dumps(source,ensure_ascii=False)
    for previous in (scope,training,atp,feasibility,request):
        assert previous['document']['code'] in encoded
    assert item(source,'N.º de acta')['value']==source['document']['code']=='DEMO-ENT-01'
    assert item(source,'Alcance asociado')['value']==scope['document']['code']
    assert item(source,'Pruebas de aceptación')['value']==atp['document']['code']
    assert item(source,'Capacitación')['selected']=='Con capacitación'
    assert item(source,'Acta de capacitación N.º')['value']==training['document']['code']
    assert item(source,'Fecha')['value']==item(training,'Fecha de capacitación')['value']=='07/01/2027'
    assert block(source,'partes')['rows']==block(scope,'partes')['rows']
    assert block(source,'firmas')['rows']==block(training,'firmas')['rows']
    for role in ('Parte solicitante','Equipo ejecutor','Líder de proyecto'):
        assert item(source,role)['value']==item(training,role)['value']
    checks.append({'case':'entrega-codigos-personas-y-capacitacion-coherentes'})

    dmy=lambda value:datetime.strptime(value,'%d/%m/%Y').date()
    start=dmy(item(scope,'Inicio propuesto')['value']); end=dmy(item(scope,'Fin propuesto')['value'])
    training_date=dmy(item(source,'Fecha')['value']); delivery=dmy(item(source,'Fecha de entrega')['value'])
    assert (end-start).days+1==7*7
    assert end-timedelta(days=6)<=training_date<delivery<=end
    assert date.fromisoformat(scope['document']['date'])<date.fromisoformat(atp['document']['date'])<start
    assert delivery==date.fromisoformat(source['document']['date'])
    assert '7 semanas, con 50 días-persona' in item(scope,'Tiempo total estimado')['value']
    assert block(scope,'fases')['rows'][-1][1]=='1 semana' and 'E5' in block(scope,'fases')['rows'][-1][2]
    for row in block(scope,'responsables')['rows']:
        assert sum(mark in ('A','R/A') for mark in row[1:])==1
        assert any(mark in ('R','R/A') for mark in row[1:])
    checks.append({'case':'entrega-fechas-dentro-de-siete-semanas','delivery':str(delivery)})

    cases=[b for s in atp['sections'] for b in s['blocks'] if b['type']=='testcase']
    assert len(cases)==5 and all(not c.get('executed',False) and c.get('selected') is None for c in cases)
    closing=section(source,'conformidad')['blocks'][0]['text']
    assert 'sin ejecutar' in closing and 'certificado de aceptación está pendiente' in closing
    assert 'Soledad Paredes, jefa de operaciones de reservas, decidirá' in closing
    assert 'satisfactorias' not in encoded.lower()
    checks.append({'case':'entrega-frase-de-estado-con-ATP-pendiente'})

    destinations={e['id']:e['page'] for e in result['entries']}
    for key in ('entregables','pendientes','partes','firmas'):
        first=destinations[key]-1
        page=' '.join(text_pages[first:first+2])  # a table may continue on the next page
        rows=block(source,key)['rows']
        assert all(' '.join(row[0].split()) in page for row in rows),(key,page)
    assert destinations['firmas']==result['pages']
    assert 'Histórico de revisiones' in text_pages[-1]
    assert all('Pendiente'==r[-1] for r in block(source,'firmas')['rows'])
    assert block(source,'partes')['rows'][-1][1:]==['Pendiente','Pendiente']
    with pdfplumber.open(pdf) as printed:
        words=printed.pages[destinations['entregables']-1].extract_words()
        assert any(w['text']=='Ítem' for w in words),'El encabezado Ítem debe caber sin partirse'
    checks.append({'case':'entrega-tablas-enteras-y-firmas-al-cierre'})

    no_notes=copy.deepcopy(source)
    no_notes['sections']=[s for s in no_notes['sections'] if s['id']!='observaciones']
    section(no_notes,'conformidad')['blocks'][0]['text']=closing.replace('y del tratamiento de los pendientes de {{ref:pendientes}}','y de la revisión documentada')
    no_notes_result,no_notes_pdf=build('entrega-sin-observaciones',no_notes)
    assert 'pendientes' not in no_notes_result['labels']
    assert 'Observaciones generales' not in ' '.join(pages(no_notes_pdf))
    assert 'sin ejecutar' in ' '.join(pages(no_notes_pdf))
    checks.append({'case':'entrega-sin-observaciones-generales','pages':no_notes_result['pages']})

    # A partial delivery without the session still preserves E5 as a pending commitment.
    no_training=copy.deepcopy(source)
    section(no_training,'capacitacion')['blocks']=[{'type':'fields','items':[
        {'label':'Capacitación','options':['Con capacitación','Sin capacitación'],'selected':'Sin capacitación'}]},
        {'type':'paragraph','text':'Entrega parcial: capacitación E5 pendiente de programación; no se presenta acta de sesión.'}]
    block(no_training,'entregables')['rows'].pop()
    block(no_training,'pendientes')['rows'][1][0]='Programar y realizar la capacitación E5 comprometida en el alcance.'
    section(no_training,'informacion')['blocks'][-1]['text']='Se reciben E1 a E4 para revisión; E5 permanece pendiente bajo DEMO-ALC-01.'
    section(no_training,'conformidad')['blocks'][0]['text']=closing.replace('E1 a E5','E1 a E4')
    no_training_result,no_training_pdf=build('entrega-sin-capacitacion',no_training)
    no_training_text=' '.join(pages(no_training_pdf))
    assert 'DEMO-CAP-01' not in no_training_text and '07/01/2027' not in no_training_text
    assert 'Sin capacitación' in no_training_text and 'E5 pendiente' in no_training_text
    assert marks(no_training_pdf)==(2,1)
    checks.append({'case':'entrega-sin-capacitacion-parcial','pages':no_training_result['pages']})

    for logo in (False,True):
        custom=copy.deepcopy(source)
        custom['brand'].update(entity='Organización de prueba',unit='Oficina de Proyectos',accent='#7A2E1D')
        custom['document'].update(code='ACME-ENT-07',paper='Letter',status='En revisión')
        item(custom,'N.º de acta')['value']='ACME-ENT-07'
        block(custom,'firmas')['rows'][0][1]='Persona de prueba\nCargo de prueba'
        if logo:
            custom['brand']['logo']='test-logo.png'
        custom_result,custom_pdf=build('entrega-identidad-'+str(logo),custom)
        custom_text=pages(custom_pdf)
        assert custom_result['paper']=='Letter' and 'ACME-ENT-07' in custom_text[0]
        assert 'Persona de prueba' in ' '.join(custom_text)
        assert any(a['path']=='test-logo.png' for a in custom_result['assets'])==logo
        assert ('Organización de prueba' in custom_text[0])!=logo
        checks.append({'case':'entrega-personalizada','logo':logo,'pages':custom_result['pages']})

    indexed=copy.deepcopy(source);indexed['document']['indexes']=['contents']
    _,indexed_pdf=build('entrega-con-indice',indexed)
    assert 'Contenido' in pages(indexed_pdf)[0]
    checks.append({'case':'entrega-indice-opcional'})
    legacy=copy.deepcopy(source)
    legacy['document']['show_changes']=False
    legacy['sections']=[{'id':'entrega','title':'Recepción','blocks':[{'type':'paragraph','text':'Recepción para revisión. Conformidad pendiente.'}]}]
    legacy_result,legacy_pdf=build('entrega-anterior-sin-eleccion',legacy)
    assert legacy_result['pages']==1 and 'Histórico de revisiones' not in ' '.join(pages(legacy_pdf))
    checks.append({'case':'entrega-sin-eleccion-global-sigue-admitida'})

    for name,mutate,message in [
        ('sin-marca',lambda v:item(v,'Capacitación').pop('selected'),'selected debe ser exactamente una'),
        ('dos-marcas',lambda v:item(v,'Capacitación').update(selected=['Con capacitación','Sin capacitación']),'multiple: true'),
        ('marca-ajena',lambda v:item(v,'Capacitación').update(selected='Ambas'),'selected debe ser exactamente una'),
        ('campo-vacio',lambda v:item(v,'Fecha').update(value=''),'fields.value'),
        ('fila-incompleta',lambda v:block(v,'entregables')['rows'][0].pop(),'Fila con número de columnas incorrecto'),
        ('id-duplicado',lambda v:block(v,'entregables').update(id='informacion'),'ID duplicado'),
    ]:
        broken=copy.deepcopy(source);mutate(broken)
        rejected_with('entrega-'+name,broken,message)
