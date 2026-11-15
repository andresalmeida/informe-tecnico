"""Optional document lifecycle: strict metadata, visible print mark and PDF checks."""
import re
from datetime import date
from xml.sax.saxutils import escape

LABELS = {'borrador':'Borrador','en-revision':'En revisión','vigente':'Vigente',
          'sustituido':'Sustituido','retirado':'Retirado','archivado':'Archivado'}
INACTIVE = frozenset(('sustituido','retirado','archivado'))
RELEASED = frozenset(('vigente',*INACTIVE))
BAND_TOP_MM, BAND_BOTTOM_MM = 48, 56
UNIT = 72/25.4


def require(condition, message):
    if not condition:raise ValueError('lifecycle: '+message)


def iso_date(value, field):
    require(isinstance(value,str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}',value) is not None,
            field+' debe ser una fecha YYYY-MM-DD')
    try:return date.fromisoformat(value)
    except ValueError:raise ValueError('lifecycle: '+field+' debe ser una fecha válida YYYY-MM-DD') from None


def document_code(value, field):
    require(isinstance(value,str) and re.fullmatch(r'[A-Z]{2,5}-[A-Z]{3}-\d{2,}',value) is not None,
            field+' debe usar PREFIJO-TIPO-NN, con prefijo de 2 a 5 letras mayúsculas y número de al menos dos cifras')


def version_parts(value, field):
    require(isinstance(value,str) and re.fullmatch(r'[0-9]+(?:\.[0-9]+)*',value) is not None,
            field+' debe ser texto con partes numéricas separadas por punto, por ejemplo "0.2"')
    parts=[int(part) for part in value.split('.')]
    while len(parts)>1 and parts[-1]==0:parts.pop()
    return tuple(parts)


def successor_label(block):
    label=block['superseded_by']
    if 'superseded_by_version' in block:label+=' versión '+block['superseded_by_version']
    return label


def validate_lifecycle(document):
    if 'lifecycle' not in document:return
    block=document['lifecycle']
    require(isinstance(block,dict),'debe ser un objeto con state; omitir el bloque si no se usa')
    allowed={'state','frozen_on','supersedes','superseded_by','superseded_by_version','retire_on','retention'}
    require(not set(block)-allowed,'quitar campos no admitidos: '+', '.join(sorted(set(block)-allowed)))
    state=block.get('state')
    require(isinstance(state,str) and state in LABELS,'state debe ser borrador, en-revision, vigente, sustituido, retirado o archivado')
    current=iso_date(document.get('date'),'document.date')
    if 'frozen_on' in block:
        require(state in RELEASED,'frozen_on solo se admite en vigente, sustituido, retirado o archivado')
        frozen=iso_date(block['frozen_on'],'frozen_on')
        require(frozen<=current,'frozen_on no puede ser posterior a document.date')
    if 'supersedes' in block:
        require(state in RELEASED,'supersedes solo se admite desde vigente; en un borrador citar el antecedente en el contenido')
        codes=block['supersedes']
        require(isinstance(codes,list) and bool(codes),'supersedes debe ser una lista no vacía de códigos')
        for code in codes:document_code(code,'supersedes')
        require(len(set(codes))==len(codes),'supersedes no admite códigos repetidos')
        require(document['code'] not in codes,'supersedes no puede citar el código del propio documento')
    if state=='sustituido':
        require('superseded_by' in block,'sustituido requiere superseded_by con el código sucesor')
    if 'superseded_by_version' in block:
        require('superseded_by' in block,'superseded_by_version requiere superseded_by con el código sucesor')
        version_parts(block['superseded_by_version'],'superseded_by_version')
    if 'superseded_by' in block:
        require(state in ('sustituido','archivado'),'superseded_by solo se admite en sustituido o archivado')
        document_code(block['superseded_by'],'superseded_by')
        if block['superseded_by']==document['code']:
            require('superseded_by_version' in block,
                    'con el mismo código, indicar superseded_by_version con una versión mayor que document.version')
            target=version_parts(block['superseded_by_version'],'superseded_by_version')
            current_version=version_parts(document['version'],'document.version')
            require(target!=current_version,'superseded_by_version debe ser distinta de document.version y mayor, por ejemplo "0.2" después de "0.1"')
            require(target>current_version,'superseded_by_version debe ser mayor que document.version; comparar las partes numéricas')
        require(block['superseded_by'] not in block.get('supersedes',[]),'el sucesor no puede estar también en supersedes')
    if state=='retirado':require('retire_on' in block,'retirado requiere retire_on con la fecha efectiva')
    if 'retire_on' in block:
        require(state in ('vigente','retirado','archivado'),'retire_on solo se admite en vigente, retirado o archivado')
        retired=iso_date(block['retire_on'],'retire_on')
        if 'frozen_on' in block:require(retired>=iso_date(block['frozen_on'],'frozen_on'),'retire_on no puede ser anterior a frozen_on')
        if state=='vigente':require(retired>current,'en vigente, retire_on debe ser posterior a document.date; si el retiro ya ocurrió usar retirado')
        else:require(retired<=current,'en retirado o archivado, retire_on no puede ser posterior a document.date')
    if state=='archivado':require('retention' in block,'archivado requiere retention con period y location')
    if 'retention' in block:
        require(state=='archivado','retention solo se admite en archivado')
        retention=block['retention']
        require(isinstance(retention,dict) and not set(retention)-{'period','location'},'retention debe contener solo period y location')
        for key in ('period','location'):
            require(isinstance(retention.get(key),str) and bool(retention[key].strip()),'retention.'+key+' debe indicar '+('por cuánto tiempo se conserva' if key=='period' else 'dónde se conserva'))


def status_label(document):
    block=document.get('lifecycle')
    if not block:return document['status']
    label=LABELS[block['state']]
    if 'superseded_by_version' in block:
        label+=(' por ' if block['state']=='sustituido' else '; sustituido por ')+successor_label(block)
    return label


def band_message(document):
    block=document.get('lifecycle')
    if not block:return None
    state=block['state']
    printed=lambda value:date.fromisoformat(value).strftime('%d/%m/%Y')
    if state=='sustituido':
        return f"Documento sustituido por {successor_label(block)} desde {printed(document['date'])}. No usar para decidir."
    if state=='retirado':
        return f"Documento retirado desde {printed(block['retire_on'])}. No usar para decidir."
    if state=='archivado':
        successor=f" Sustituido por {successor_label(block)}." if block.get('superseded_by') else ''
        return f"Documento archivado desde {printed(document['date'])}.{successor} No usar para decidir."
    if state=='vigente' and block.get('retire_on'):
        return f"Documento vigente. Retiro programado para {printed(block['retire_on'])}."
    return None


def draw_lifecycle_band(canvas, doc, document, styles):
    message=band_message(document)
    if message is None:return
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
    y=doc.pagesize[1]-BAND_BOTTOM_MM*UNIT
    h=(BAND_BOTTOM_MM-BAND_TOP_MM)*UNIT
    inactive=document['lifecycle']['state'] in INACTIVE
    style=ParagraphStyle('lifecycle-band',fontName=styles['h1' if inactive else 'cell'].fontName,
                         fontSize=9,leading=10,textColor=colors.black)
    paragraph=Paragraph(escape(message),style)
    _,height=paragraph.wrap(doc.width-12,h-4)
    require(height<=h-4,'la banda no cabe; acortar la identificación del sucesor (código o versión) sin reducir la letra')
    canvas.saveState()
    canvas.setFillColor(colors.white);canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(.8 if inactive else .5)
    canvas.rect(doc.leftMargin,y,doc.width,h,stroke=1,fill=1)
    paragraph.drawOn(canvas,doc.leftMargin+6,y+(h-height)/2)
    canvas.restoreState()


def check_lifecycle_page(page, document):
    """Check the actual header-gap text and border, rather than a mention in the body."""
    message=band_message(document)
    if message is None:return []
    left=21*UNIT;top=BAND_TOP_MM*UNIT;bottom=BAND_BOTTOM_MM*UNIT
    actual=' '.join((page.crop((left,top,page.width-left,bottom)).extract_text() or '').split())
    errors=[]
    if ' '.join(message.split()) not in actual:errors.append('Banda de ciclo de vida ausente o incorrecta')
    bordered=any(abs(r['x0']-left)<.6 and abs(r['x1']-(page.width-left))<.6
                 and abs(r['top']-top)<.6 and abs(r['bottom']-bottom)<.6
                 and r.get('stroke') and r.get('stroking_color') in (0,(0,0,0),[0,0,0])
                 for r in page.rects)
    if not bordered:errors.append('Banda de ciclo de vida sin borde negro')
    return errors
