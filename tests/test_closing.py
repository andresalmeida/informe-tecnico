"""A real pagination failure: history must travel with the final signature table."""
import copy
import json

import pdfplumber
from pypdf import PdfReader


def run_checks(example, root, checks, build):
    base=json.loads((example.parent/'ejemplo-acta-reunion.json').read_text())
    base['document'].update(version='0.1',show_changes=True)
    base['changes']=base['changes'][:1]
    signatures={'type':'table','id':'firmas','title':'Firmas de responsabilidad',
                'headers':['Rol','Nombre','Firma','Fecha'],
                'rows':[['Elabora','Persona de demostración','\n________________','Pendiente'],
                        ['Revisa','Por confirmar','\n________________','Pendiente'],
                        ['Aprueba','Por confirmar','\n________________','Pendiente']]}
    base['sections']=[
        {'id':'cuerpo','title':'Contenido','blocks':[
            {'type':'paragraph','text':f'Párrafo de demostración {i}: contenido previo al cierre.'}
            for i in range(12)]},
        {'id':'responsabilidad','title':'Responsabilidad','blocks':[
            signatures,{'type':'paragraph','text':'Remitido a la unidad de demostración. Fecha de remisión: Pendiente.'}]}]
    for name, profile, paper in [('institucional','institucional','A4'),('apa-carta','institucional-apa','Letter')]:
        value=copy.deepcopy(base)
        value['format']['profile']=profile
        value['document']['paper']=paper
        result,pdf=build('cierre-unidad-'+name,value)
        with pdfplumber.open(pdf) as printed:
            last=printed.pages[-1]
            body=last.crop((21*72/25.4,58*72/25.4,last.width-21*72/25.4,last.height-25*72/25.4)).extract_text() or ''
            alone=body.startswith('Histórico de revisiones')
            if profile=='institucional':
                assert not alone
                for text in ['Responsabilidad','Elabora','Revisa','Aprueba','Remitido','Histórico de revisiones']:
                    assert text in body,text
            elif not alone:
                for text in ['Responsabilidad','Elabora','Revisa','Aprueba','Remitido','Histórico de revisiones']:
                    assert text in body,text
        positions={e['id']:e['page'] for e in result['entries']}
        # In the default profile the history may go alone, but the signatures never split from their section.
        assert positions['responsabilidad']==positions['firmas']>=result['pages']-(1 if profile!='institucional' else 0)
        if profile=='institucional':assert result['pages']==2
        checks.append({'case':'cierre-unidad-'+name,'pages':result['pages']})
    # With little room left (at most 40 % of the page), the default profile still moves the whole closing together.
    value=copy.deepcopy(base)
    value['format']['profile']='institucional-apa'
    value['document']['paper']='Letter'
    value['sections'][0]['blocks'].extend(
        {'type':'paragraph','text':f'Párrafo adicional de demostración {i}: contenido previo al cierre.'} for i in range(5))
    result,pdf=build('cierre-hueco-chico-apa',value)
    with pdfplumber.open(pdf) as printed:
        last=printed.pages[-1]
        body=last.crop((21*72/25.4,58*72/25.4,last.width-21*72/25.4,last.height-25*72/25.4)).extract_text() or ''
    assert not body.startswith('Histórico de revisiones') and 'Elabora' in body and 'Histórico de revisiones' in body
    checks.append({'case':'cierre-hueco-chico-apa','pages':result['pages']})
    value=copy.deepcopy(base)
    value['sections'][0]['blocks'].extend(
        {'type':'paragraph','text':f'Contenido adicional de demostración {i}.'} for i in range(6))
    for row in value['sections'][-1]['blocks'][0]['rows']:row[2]=''
    result,pdf=build('cierre-firmas-sin-lineas',value)
    text=PdfReader(pdf).pages[-1].extract_text() or ''
    assert 'Elabora' in text and 'Revisa' in text and 'Histórico de revisiones' in text
    checks.append({'case':'cierre-firmas-sin-lineas','pages':result['pages']})
    value=copy.deepcopy(base)
    value['sections'][-1]['blocks'].pop()
    result,pdf=build('cierre-sin-remision',value)
    text=PdfReader(pdf).pages[-1].extract_text() or ''
    assert 'Elabora' in text and 'Histórico de revisiones' in text
    checks.append({'case':'cierre-sin-remision','pages':result['pages']})
    value=copy.deepcopy(base)
    value['changes']=[{'version':f'0.{i}','date':'2026-11-03',
                      'summary':f'Revisión sintética {i} para comprobar un histórico mayor que una página.',
                      'author':'Equipo de demostración'} for i in range(1,46)]
    value['document']['version']='0.45'
    result,pdf=build('cierre-historico-mayor-que-pagina',value)
    text=' '.join(p.extract_text() or '' for p in PdfReader(pdf).pages)
    assert result['pages']>=3 and all(f'Revisión sintética {i}' in text for i in range(1,46))
    checks.append({'case':'cierre-historico-mayor-que-pagina','pages':result['pages']})
    value=copy.deepcopy(base)
    value['sections'][-1]['blocks'].append({'type':'pagebreak'})
    result,pdf=build('cierre-respeta-salto-explicito',value)
    with pdfplumber.open(pdf) as printed:
        last=printed.pages[-1]
        body=last.crop((21*72/25.4,58*72/25.4,last.width-21*72/25.4,last.height-25*72/25.4)).extract_text() or ''
        assert body.startswith('Histórico de revisiones')
    checks.append({'case':'cierre-respeta-salto-explicito','pages':result['pages']})
