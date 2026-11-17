"""Lifecycle metadata and visible marks, including independent negative PDF checks."""
import copy
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pdfplumber
from pypdf import PdfReader

_scripts = Path(__file__).resolve().parents[1] / "skills" / "informe-tecnico" / "scripts"
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

import build_report
from check_report import check
from lifecycle import LABELS, BAND_TOP_MM, BAND_BOTTOM_MM, UNIT, band_message


def run_checks(example, root, checks, build, rejected_with):
    source=json.loads((example.parent/'ejemplo-propuesta-servicio.json').read_text())
    for state in LABELS:
        value=copy.deepcopy(source)
        value['document'].update(date='2026-11-13',status='Demostración',show_status_in_footer=False)
        block={'state':state}
        if state=='sustituido':block['superseded_by']='DEMO-PRO-02'
        if state=='retirado':block.update(retire_on='2026-11-12',frozen_on='2026-11-11')
        if state=='archivado':block.update(retention={'period':'Dos años, simulación','location':'Archivo de demostración'},superseded_by='DEMO-PRO-02')
        if state=='vigente':block.update(frozen_on='2026-11-11',supersedes=['DEMO-PRO-00'])
        value['document']['lifecycle']=block
        result,pdf=build('lifecycle-'+state,value)
        assert result['lifecycle']==result['document']['lifecycle']==block
        assert result['pages']>=3
        with pdfplumber.open(pdf) as printed:
            for page in printed.pages:
                footer=page.crop((page.width/2,page.height-18*UNIT,page.width,page.height)).extract_text() or ''
                assert LABELS[state] in footer,(state,footer)
                if state in ('sustituido','retirado','archivado'):
                    band=page.crop((21*UNIT,BAND_TOP_MM*UNIT,page.width-21*UNIT,BAND_BOTTOM_MM*UNIT))
                    text=' '.join((band.extract_text() or '').split())
                    assert 'No usar para decidir.' in text
                    assert ('12/11/2026' if state=='retirado' else '13/11/2026') in text
                    assert page.rects
        checks.append({'case':'lifecycle-estado-'+state,'pages':result['pages']})
    sunset=json.loads((example.parent/'ejemplo-propuesta-retiro-programado.json').read_text())
    result,pdf=build('lifecycle-retiro-programado',sunset)
    assert result['pages']==1
    assert 'Retiro programado para 11/12/2026' in PdfReader(pdf).pages[0].extract_text()
    checks.append({'case':'lifecycle-sunset-discreto','pages':1})
    replaced=json.loads((example.parent/'ejemplo-propuesta-sustituida.json').read_text())
    result,pdf=build('lifecycle-propuesta-sustituida',replaced)
    assert result['pages']==5 and result['document']['version']=='0.1'
    assert result['lifecycle']['superseded_by']=='DEMO-PRO-01'
    assert result['lifecycle']['superseded_by_version']=='0.2'
    assert len(replaced['changes'])==len({row['version'] for row in replaced['changes']})
    assert result['document']['code']==source['document']['code']
    checks.append({'case':'lifecycle-ejemplo-conserva-propuesta-01','pages':5})

    def raw(name,value):
        path=root/(name+'.json');path.write_text(json.dumps(value,ensure_ascii=False))
        pdf=root/(name+'.pdf');build_report.compile_report(path,pdf);return pdf
    real_draw=build_report.draw_lifecycle_band
    def skip_second(canvas,doc,document,styles):
        if doc.page!=2:real_draw(canvas,doc,document,styles)
    with patch('build_report.draw_lifecycle_band',skip_second):
        incomplete=raw('lifecycle-falta-banda-pagina-2',replaced)
    invalid=check(incomplete)
    assert not invalid['ok'] and any('Banda de ciclo de vida' in e and 'página 2' in e for e in invalid['errors'])
    def text_only(canvas,doc,document,styles):
        canvas.saveState();canvas.setFillColorRGB(0,0,0);canvas.setFont('Helvetica-Bold',9)
        canvas.drawString(doc.leftMargin+6,doc.pagesize[1]-52*UNIT,band_message(document));canvas.restoreState()
    with patch('build_report.draw_lifecycle_band',text_only):
        unbordered=raw('lifecycle-texto-sin-borde',replaced)
    invalid=check(unbordered)
    assert not invalid['ok'] and any('sin borde negro' in e for e in invalid['errors'])
    manifest=incomplete.with_suffix('.manifest.json')
    metadata=json.loads(manifest.read_text());metadata['lifecycle']={'state':'retirado','retire_on':'2026-11-12'}
    manifest.write_text(json.dumps(metadata,ensure_ascii=False))
    assert any('distinto' in e for e in check(incomplete)['errors'])
    checks.append({'case':'lifecycle-comprobador-detecta-ausencia-borde-y-manifiesto-incoherente'})

    # Two profiles/papers and a long body exercise the shared page hook beyond the proposal sample.
    alternate=json.loads((example.parent/'ejemplo-apa.json').read_text())
    alternate['document'].update(lifecycle={'state':'retirado','retire_on':alternate['document']['date']},paper='Letter')
    result,pdf=build('lifecycle-apa-carta',alternate)
    assert result['paper']=='Letter' and result['lifecycle']['state']=='retirado'
    checks.append({'case':'lifecycle-apa-carta','pages':result['pages']})

    variants=[
        ('nulo',None,'debe ser un objeto'),
        ('sin-estado',{'frozen_on':'2026-11-10'},'state debe ser'),
        ('desconocido',{'state':'publicado'},'state debe ser'),
        ('campo-desconocido',{'state':'borrador','label':'Alias'},'quitar campos no admitidos'),
        ('sustituido-sin-codigo',{'state':'sustituido'},'requiere superseded_by'),
        ('codigo-invalido',{'state':'sustituido','superseded_by':'cualquier código'},'superseded_by debe usar'),
        ('sucesor-propio',{'state':'sustituido','superseded_by':'DEMO-PRO-01'},'indicar superseded_by_version'),
        ('sucesor-en-vigente',{'state':'vigente','superseded_by':'DEMO-PRO-02'},'solo se admite en sustituido'),
        ('retirado-sin-fecha',{'state':'retirado'},'requiere retire_on'),
        ('fecha-no-iso',{'state':'retirado','retire_on':'12/11/2026'},'retire_on debe ser una fecha YYYY-MM-DD'),
        ('fecha-compacta',{'state':'retirado','retire_on':'20261112'},'retire_on debe ser una fecha YYYY-MM-DD'),
        ('fecha-imposible',{'state':'retirado','retire_on':'2026-02-30'},'retire_on debe ser una fecha válida'),
        ('retiro-antes-congelar',{'state':'retirado','retire_on':'2026-11-10','frozen_on':'2026-11-11'},'anterior a frozen_on'),
        ('retiro-futuro-en-retirado',{'state':'retirado','retire_on':'2027-01-01'},'no puede ser posterior a document.date'),
        ('sunset-ya-paso',{'state':'vigente','retire_on':'2026-11-10'},'debe ser posterior a document.date'),
        ('retiro-en-borrador',{'state':'borrador','retire_on':'2026-11-12'},'retire_on solo se admite'),
        ('congelar-borrador',{'state':'borrador','frozen_on':'2026-11-10'},'frozen_on solo se admite'),
        ('congelacion-futura',{'state':'vigente','frozen_on':'2027-01-01'},'frozen_on no puede ser posterior'),
        ('archivo-sin-conservacion',{'state':'archivado'},'requiere retention'),
        ('conservacion-texto',{'state':'archivado','retention':'Dos años'},'solo period y location'),
        ('conservacion-sin-plazo',{'state':'archivado','retention':{'location':'Archivo'}},'retention.period'),
        ('conservacion-sin-lugar',{'state':'archivado','retention':{'period':'Dos años'}},'retention.location'),
        ('conservacion-vacia',{'state':'archivado','retention':{'period':' ','location':'Archivo'}},'retention.period'),
        ('conservacion-ajena',{'state':'vigente','retention':{'period':'Dos años','location':'Archivo'}},'retention solo se admite'),
        ('conservacion-otra-clave',{'state':'archivado','retention':{'period':'Dos años','location':'Archivo','extra':True}},'solo period y location'),
        ('predecesores-texto',{'state':'vigente','supersedes':'DEMO-PRO-00'},'lista no vacía'),
        ('predecesores-vacios',{'state':'vigente','supersedes':[]},'lista no vacía'),
        ('predecesor-repetido',{'state':'vigente','supersedes':['DEMO-PRO-00','DEMO-PRO-00']},'códigos repetidos'),
        ('predecesor-invalido',{'state':'vigente','supersedes':['incorrecto']},'supersedes debe usar'),
        ('predecesor-propio',{'state':'vigente','supersedes':['DEMO-PRO-01']},'no puede citar el código del propio'),
        ('predecesor-borrador',{'state':'borrador','supersedes':['DEMO-PRO-00']},'supersedes solo se admite'),
        ('ciclo-relaciones',{'state':'sustituido','supersedes':['DEMO-PRO-02'],'superseded_by':'DEMO-PRO-02'},'sucesor no puede estar también'),
    ]
    for name,block,message in variants:
        broken=copy.deepcopy(source);broken['document'].update(date='2026-11-13',lifecycle=block)
        rejected_with('lifecycle-'+name,broken,message)


    # A revision preserves its code; another document may optionally identify its version.
    for name, code, current, target in [
        ('revision-mismo-codigo','DEMO-PRO-01','0.1','0.2'),
        ('comparacion-numerica','DEMO-PRO-01','1.9','1.10'),
        ('partes-adicionales','DEMO-PRO-01','1','1.0.1'),
        ('otro-codigo-sin-version','DEMO-PRO-02','0.1',None),
        ('otro-codigo-con-version','DEMO-PRO-02','0.1','0.2')]:
        value=copy.deepcopy(source)
        block={'state':'sustituido','superseded_by':code}
        if target is not None:block['superseded_by_version']=target
        value['document'].update(version=current,date='2026-11-13',lifecycle=block)
        result,pdf=build('lifecycle-'+name,value)
        assert result['lifecycle']==result['document']['lifecycle']==block
        with pdfplumber.open(pdf) as printed:
            for page in printed.pages:
                if target is not None:
                    expected='Sustituido por '+code+' versión '+target
                    footer=page.crop((page.width/2,page.height-18*UNIT,page.width,page.height))
                    assert expected in ' '.join((footer.extract_text() or '').split())
                    assert (code+' versión '+target) in ' '.join((page.crop((21*UNIT,BAND_TOP_MM*UNIT,page.width-21*UNIT,BAND_BOTTOM_MM*UNIT)).extract_text() or '').split())
        checks.append({'case':'lifecycle-'+name,'pages':result['pages']})

    for name, target, message in [
        ('version-igual','0.1','distinta de document.version'),
        ('version-equivalente','0.1.0','distinta de document.version'),
        ('version-menor','0.0','mayor que document.version'),
        ('version-con-letras','v0.2','partes numéricas'),
        ('version-vacia','','partes numéricas'),
        ('version-numero',0.2,'partes numéricas'),
        ('version-nula',None,'partes numéricas')]:
        value=copy.deepcopy(source)
        value['document']['lifecycle']={'state':'sustituido','superseded_by':'DEMO-PRO-01','superseded_by_version':target}
        rejected_with('lifecycle-'+name,value,message)
    value=copy.deepcopy(source)
    value['document']['lifecycle']={'state':'borrador','superseded_by_version':'0.2'}
    rejected_with('lifecycle-version-sin-sucesor',value,'superseded_by_version requiere superseded_by')
    value=copy.deepcopy(source)
    value['document'].update(version='v0.1',lifecycle={'state':'sustituido','superseded_by':'DEMO-PRO-01','superseded_by_version':'0.2'})
    rejected_with('lifecycle-version-actual-no-numerica',value,'document.version debe ser texto con partes numéricas')

    versioned=copy.deepcopy(replaced)
    versioned['document']['lifecycle'].update(state='archivado',retention={'period':'Dos años, demostración','location':'Archivo de demostración'})
    result,pdf=build('lifecycle-archivo-con-version-sucesora',versioned)
    assert 'versión 0.2' in PdfReader(pdf).pages[0].extract_text()
    checks.append({'case':'lifecycle-archivo-con-version-sucesora'})
    # A manifest cannot silently replace the successor version while keeping the old PDF band.
    metadata=json.loads(pdf.with_suffix('.manifest.json').read_text())
    metadata['lifecycle']['superseded_by_version']='0.3'
    metadata['document']['lifecycle']['superseded_by_version']='0.3'
    pdf.with_suffix('.manifest.json').write_text(json.dumps(metadata,ensure_ascii=False))
    invalid=check(pdf)
    assert not invalid['ok'] and any('Banda de ciclo de vida' in e for e in invalid['errors'])
    checks.append({'case':'lifecycle-comprobador-version-sucesora-discrepante'})
