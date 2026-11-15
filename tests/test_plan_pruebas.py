"""Checks for acceptance cases, called by self_test with its shared build helpers."""
import copy
import json
from datetime import date

import pdfplumber
from pypdf import PdfReader


def run_checks(example, checks, build, rejected_with):
    source = json.loads((example.parent/'ejemplo-plan-pruebas.json').read_text())
    scope = json.loads((example.parent/'ejemplo-alcance-proyecto.json').read_text())
    def cases(value):
        return [b for s in value['sections'] for b in s.get('blocks', []) if b['type'] == 'testcase']
    def find(value, key):
        return next(b for s in value['sections'] for b in s.get('blocks', []) if b.get('id') == key)
    def texts(pdf):
        return [' '.join((p.extract_text() or '').split()) for p in PdfReader(pdf).pages]
    def marks(pdf):
        with pdfplumber.open(pdf) as printed:
            boxes = sum(sum(abs(r['width']-9)<.01 and abs(r['height']-9)<.01 for r in p.rects) for p in printed.pages)
            diagonals = sum(sum(abs(l['width']-5.2)<.01 and abs(l['height']-5.2)<.01 for l in p.lines) for p in printed.pages)
        return boxes, diagonals//2
    plan, pdf = build('plan-pruebas', source)
    assert plan['pages'] == 8, plan['pages']
    assert marks(pdf) == (15, 0), marks(pdf)
    pages = texts(pdf)
    destinations = {e['id']:e['page'] for e in plan['entries']}
    for case in cases(source):
        page = pages[destinations[case['id']]-1]
        assert f"Caso {case['id']}. {case['title']}" in page
        assert case['observations'] in page and 'Responsable de' in page
        assert all(step['task'] in page for step in case['steps'])
    for key in ('partes', 'firmas'):
        page = pages[destinations[key]-1]
        assert all(row[0].split('\n')[0] in page for row in find(source,key)['rows'])
    assert destinations['firmas'] == plan['pages']
    assert 'Histórico de revisiones' in pages[-1] and 'Estado del certificado' in '\n'.join(pages)
    assert PdfReader(pdf).metadata.author == 'Entidad de demostración'
    assert 'DEMO-ATP-01' in PdfReader(pdf).metadata.subject
    assert not any(a['path'].startswith('/') for a in plan['assets'])
    checks.append({'case':'plan-pruebas-sin-ejecutar', 'pages':plan['pages'], 'boxes':15, 'marks':0})

    # Every criterion is preserved, including thresholds, and at least one case covers it.
    criteria = next(b for s in scope['sections'] if s['id']=='criterios' for b in s['blocks'] if b['type']=='list')['items']
    assert len(cases(source)) >= len(criteria) == 5
    for criterion in criteria:
        case = next(c for c in cases(source) if criterion in c['description'])
        assert case['title'] == criterion.split(': ')[0]
        assert case['expected'] == criterion.split(': ',1)[1]
    encoded = json.dumps(source,ensure_ascii=False)
    for key in ('DEMO-FAC-01','DEMO-REQ-014',scope['document']['code'], 'Soledad Paredes', 'Iván Salas',
                'Marta Quiroga', 'Diego Arce', 'Rafael Mena', 'Lucía Ferrer'):
        assert key in encoded and key in json.dumps(scope,ensure_ascii=False), key
    for key in ('partes','firmas'):
        assert find(source,key)['rows'][1:] == find(scope,key)['rows'][1:]
    assert date.fromisoformat(source['document']['date']) > date.fromisoformat(scope['document']['date'])
    checks.append({'case':'plan-coherente-con-alcance', 'criteria':len(criteria)})

    executed = copy.deepcopy(source)
    case = cases(executed)[0]
    case.update(executed=True, selected='Aceptado', options=['Aceptado','Con reparos','Rechazado'],
                observations='Resultado sintético de demostración: se adjunta evidencia de prueba.')
    for step in case['steps']:
        step['actual'] = 'Resultado sintético: 98 de 100 pagos confirmados bajo 5 segundos; registro de prueba.'
    _, marked_pdf = build('plan-con-resultado', executed)
    assert marks(marked_pdf) == (15,1), marks(marked_pdf)
    with pdfplumber.open(marked_pdf) as printed:
        bold_text = ''.join(c['text'] for pg in printed.pages for c in pg.chars if 'Bold' in c['fontname'])
        assert 'Aceptado' in bold_text, bold_text
    checks.append({'case':'plan-una-marca-y-negrita', 'marks':1})

    # Optional executed and selected have a defined unexecuted default, and null is allowed.
    omitted = copy.deepcopy(source)
    for case in cases(omitted):
        case.pop('executed')
        case['selected'] = None
    _, omitted_pdf = build('plan-estado-por-omision', omitted)
    assert marks(omitted_pdf) == (15,0)
    indexed = copy.deepcopy(source)
    indexed['document']['indexes'] = ['contents']
    indexed_result, indexed_pdf = build('plan-con-indice', indexed)
    assert 'Contenido' in texts(indexed_pdf)[0]
    assert any(e['kind']=='testcase' for e in indexed_result['entries'])
    checks.append({'case':'plan-opciones-de-estado-e-indice'})

    report = copy.deepcopy(source)
    report['document'].update(kind='informe', show_changes=False)
    report['format']['profile'] = 'institucional-apa'
    report['sections'] = [{'id':'casos','title':'Casos de aceptación','blocks':[
        {'type':'paragraph','text':'Ver {{ref:CP-01}}.'}, copy.deepcopy(cases(source)[0])]}]
    report_result, report_pdf = build('testcase-en-informe-apa', report)
    assert report_result['reference_labels']['CP-01'] == 'Caso CP-01. Rendimiento'
    assert marks(report_pdf) == (3,0)
    checks.append({'case':'testcase-en-informe-apa'})

    for logo in (False, True):
        custom = copy.deepcopy(executed)
        custom['brand'].update(entity='Organización de prueba', unit='Oficina de Proyectos', accent='#7A2E1D')
        custom['document'].update(code='ACME-ATP-07',paper='Letter')
        if logo:
            custom['brand']['logo'] = 'test-logo.png'
        result, custom_pdf = build('plan-personalizado-'+str(logo), custom)
        assert result['paper']=='Letter' and 'ACME-ATP-07' in texts(custom_pdf)[0]
        assert any(a['path']=='test-logo.png' for a in result['assets']) == logo
        assert ('Organización de prueba' in texts(custom_pdf)[0]) != logo
        checks.append({'case':'plan-personalizado', 'logo':logo})

    # Two modules can contain independently addressable cases without a fixed count limit.
    multiple = copy.deepcopy(source)
    extra = copy.deepcopy(cases(multiple)[0]); extra['id']='CP-06'
    multiple['sections'].insert(-3, {'id':'otro-modulo','title':'Otro módulo','level':2,
                                    'blocks':[{'type':'paragraph','text':'Repetición: {{ref:CP-06}}.'},extra]})
    multi, _ = build('plan-varios-modulos',multiple)
    assert all(key in multi['labels'] for key in ('CP-01','CP-06'))

    # An oversized case repeats the complete header and cuts only between step rows.
    long_case = copy.deepcopy(cases(executed)[0])
    long_case['steps'] = [dict(task=f'Tarea{i:03}', activity=f'Actividad{i:03}: enviar el pago de prueba.',
                               expected=f'Esperado{i:03}: confirmación única.', actual=f'Real{i:03}: evidencia sintética.')
                          for i in range(1,61)]
    long_source = copy.deepcopy(source)
    long_source['sections']=[{'id':'largo','title':'Caso extenso','blocks':[long_case]}]
    long_result, long_pdf = build('plan-caso-multipagina',long_source)
    long_pages = texts(long_pdf)
    assert long_result['pages'] > 2
    assert len([e for e in long_result['entries'] if e['id']==long_case['id']]) == 1
    for page in long_pages:
        assert f"Caso {long_case['id']}. {long_case['title']}" in page
        assert 'Precondiciones' in page and 'Resultado esperado' in page and 'Resultado real' in page
        assert 'Criterio 1 de DEMO-ALC-01' in page
    for i in range(1,61):
        containing=[p for p in long_pages if f'Tarea{i:03}' in p]
        assert len(containing)==1
        assert all(token in containing[0] for token in (f'Actividad{i:03}',f'Esperado{i:03}',f'Real{i:03}'))
    assert 'Tarea060' in long_pages[-1] and 'Resultado del caso' in long_pages[-1]
    assert all('Resultado del caso' not in pg for pg in long_pages[:-1])
    assert marks(long_pdf) == (3,1), marks(long_pdf)
    checks.append({'case':'plan-cabecera-repetida-y-cierre-con-ultimo-paso','pages':long_result['pages']})

    # Moving short cases near a page boundary must never split one that fits a page.
    for filler in (0,8,16):
        padded = copy.deepcopy(source)
        one = copy.deepcopy(cases(padded)[0])
        padded['sections']=[{'id':'relleno','title':'Preparación', 'blocks':
                            [{'type':'paragraph','text':f'Preparación {i}.'} for i in range(filler)]+[one]}]
        whole, whole_pdf = build('plan-caso-entero-'+str(filler),padded)
        one_page=texts(whole_pdf)[next(e['page']-1 for e in whole['entries'] if e['id']==one['id'])]
        assert one['observations'] in one_page and all(s['task'] in one_page for s in one['steps'])
    checks.append({'case':'plan-ficha-entera-si-cabe'})

    variants = [
        ('campo-desconocido',lambda c:c.update(extra=True),'quitar campos no admitidos'),
        ('titulo-vacio',lambda c:c.update(title=' '),'testcase.title'),
        ('pasos-vacios',lambda c:c.update(steps=[]),'añadir al menos un paso'),
        ('pasos-nulos',lambda c:c.update(steps=None),'añadir al menos un paso'),
        ('paso-desconocido',lambda c:c['steps'][0].update(extra='x'),'usar solo task'),
        ('resultado-real-vacio',lambda c:c['steps'][0].update(actual=''),'testcase.steps[1].actual'),
        ('dos-opciones',lambda c:c.update(options=['A','B']),'exactamente tres textos'),
        ('opciones-repetidas',lambda c:c.update(options=['A','A','B']),'textos distintos'),
        ('opcion-vacia',lambda c:c.update(options=['A','B','']),'testcase.options'),
        ('ejecuted-texto',lambda c:c.update(executed='true'),'usar true o false'),
        ('ejecuted-numero',lambda c:c.update(executed=1),'usar true o false'),
        ('marca-sin-ejecucion',lambda c:c.update(selected=c['options'][0]),'omitir o usar null'),
        ('marca-vacia',lambda c:c.update(selected=''),'omitir o usar null'),
        ('ejecutado-sin-marca',lambda c:c.update(executed=True),'exactamente una de las options'),
        ('ejecutado-dos-marcas',lambda c:c.update(executed=True,selected=c['options'][:2]),'exactamente una de las options'),
        ('ejecutado-marca-ajena',lambda c:c.update(executed=True,selected='Ajena'),'exactamente una de las options'),
        ('id-invalido',lambda c:c.update(id='1 caso'),'ID no válido'),
        ('ficha-desbordada',lambda c:c.update(description='Texto muy largo. '*500),'acortar la ficha'),
        ('paso-desbordado',lambda c:c['steps'][0].update(activity='Actividad muy larga. '*500),'dividir la actividad'),
        ('cierre-desbordado',lambda c:c.update(observations='Observación larga. '*500),'reducir las observaciones'),
    ]
    for name,mutate,message in variants:
        broken=copy.deepcopy(source); mutate(cases(broken)[0])
        rejected_with('plan-'+name,broken,message)
    for key in ('id','description','preconditions','expected','responsible','observations'):
        broken=copy.deepcopy(source); cases(broken)[0][key]=''
        rejected_with('plan-vacio-'+key,broken,'testcase.'+key)
    duplicate=copy.deepcopy(source); cases(duplicate)[1]['id']=cases(duplicate)[0]['id']
    rejected_with('plan-id-duplicado',duplicate,'ID duplicado')
    missing=copy.deepcopy(source); cases(missing)[0]['description']='Ver {{ref:no-existe}}.'
    rejected_with('plan-referencia-inexistente',missing,'Referencia desconocida')
    # Existing fields choices still cannot be unmarked, even in a plan.
    fields=copy.deepcopy(source)
    fields['sections'][0]['blocks'][0]['items'].append({'label':'Decisión','options':['A','B']})
    rejected_with('plan-fields-sigue-exigiendo-marca',fields,'selected debe ser exactamente una')
