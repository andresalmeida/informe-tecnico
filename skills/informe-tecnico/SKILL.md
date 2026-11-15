---
name: informe-tecnico
description: Redacta y compila en PDF documentos técnicos y de gestión de proyectos con la identidad de una entidad (nombre, logo, colores, código): informes, manuales, actas, factibilidad, propuestas, alcance, requisitos, pruebas, riesgos, cambios, traspasos, cierres, evaluaciones de impacto en datos y fichas de modelo y de proceso. Usar cuando se pida cualquiera de esos documentos, un informe o manual con formato institucional o criterios APA 7, o un acta de reunión en Word.
license: MIT
metadata:
  version: "0.8.0"
---

# Informe técnico institucional

Produce documentos listos para presentar a su destinatario. La identidad se configura, los datos se sustentan y la composición se verifica. Es una implementación propia, orientada por las referencias de [fuentes.md](references/fuentes.md); no es una norma ni una certificación.

## Elegir el documento

Producir el documento que se pide. Ningún proyecto usa todo el catálogo. Ante un encargo general («arma la documentación del proyecto»), proponer los del núcleo (acta de reunión, factibilidad, propuesta, alcance, plan de pruebas y acta de entrega), preguntar por los demás según la condición del proyecto (datos personales, un modelo, una baja) y no generar el catálogo entero. Qué va en cada fase y cuáles son indispensables: [flujo-proyecto.md](references/flujo-proyecto.md). Si el entorno trae más de una copia de esta skill, usar la de mayor `metadata.version` y avisar de que las otras están desactualizadas.

| `document.kind` | Cuándo | Guía | JSON de partida (`assets/`) |
|---|---|---|---|
| `informe` | Informe técnico, manual o catálogo de un sistema | [informe.md](references/informe/informe.md) | `plantilla-base.json` |
| `acta-reunion` | Lo tratado y acordado en una sesión. PDF por omisión; también se exporta a Word | [acta-reunion.md](references/tipos/acta-reunion.md) | `ejemplo-acta-reunion.json` |
| `registro-requerimientos` | Constancia de un pedido recibido, antes de evaluarlo | [registro-requerimientos.md](references/tipos/registro-requerimientos.md) | `ejemplo-registro-requerimientos.json` |
| `informe-factibilidad` | Evaluar si una propuesta técnica es viable, con recursos y tiempo (con índices para un comité: `ejemplo-informe-factibilidad-completo.json`) | [factibilidad.md](references/tipos/factibilidad.md) | `ejemplo-informe-factibilidad.json` |
| `registro-riesgos` | Seguir los riesgos de un proyecto, con el nivel calculado desde la matriz | [registro-riesgos.md](references/tipos/registro-riesgos.md) | `ejemplo-registro-riesgos.json` |
| `evaluacion-impacto-datos` | Qué datos personales trata un sistema y qué riesgos corren sus titulares. No es asesoría legal | [evaluacion-impacto-datos.md](references/tipos/evaluacion-impacto-datos.md) | `ejemplo-evaluacion-impacto-datos.json` |
| `propuesta-servicio` | Proponer a quien contrata qué se hace, en qué plazo y por cuánto, tras la factibilidad | [propuesta-servicio.md](references/tipos/propuesta-servicio.md) | `ejemplo-propuesta-servicio.json` |
| `alcance-proyecto` | Fijar qué se construye y quién lo acepta, una vez aprobada la propuesta | [alcance-proyecto.md](references/tipos/alcance-proyecto.md) | `ejemplo-alcance-proyecto.json` |
| `especificacion-requisitos` | Qué debe hacer y cumplir un sistema, cada requisito trazado a su origen y a su prueba | [especificacion-requisitos.md](references/tipos/especificacion-requisitos.md) | `ejemplo-especificacion-requisitos.json` |
| `decision-arquitectura` | Una decisión (ADR) con contexto, opciones, razones y consecuencias | [decision-arquitectura.md](references/tipos/decision-arquitectura.md) | `ejemplo-decision-arquitectura.json` |
| `descripcion-arquitectura` | Vistas del sistema para operarlo, revisarlo o extenderlo; lleva figuras | [descripcion-arquitectura.md](references/tipos/descripcion-arquitectura.md) | `ejemplo-descripcion-arquitectura.json` |
| `plan-proyecto` | Qué se entrega, en qué hitos y con qué esfuerzo (EDT), para un equipo pequeño | [plan-proyecto.md](references/tipos/plan-proyecto.md) | `ejemplo-plan-proyecto.json` |
| `plan-pruebas` | Plan y registro de pruebas de aceptación (ATP), con el certificado | [plan-pruebas.md](references/tipos/plan-pruebas.md) | `ejemplo-plan-pruebas.json` |
| `solicitud-cambio` | Cambio sobre un documento ya aprobado o una propuesta ya aceptada, con su impacto y la decisión | [solicitud-cambio.md](references/tipos/solicitud-cambio.md) | `ejemplo-solicitud-cambio.json` |
| `acta-capacitacion` | Constancia de una capacitación dada a quienes usarán un sistema entregado | [acta-capacitacion.md](references/tipos/acta-capacitacion.md) | `ejemplo-acta-capacitacion.json` |
| `traspaso-operacion` | Paso a producción: quién opera, cómo se comprueba y cómo se vuelve atrás | [traspaso-operacion.md](references/tipos/traspaso-operacion.md) | `ejemplo-traspaso-operacion.json` |
| `acta-entrega` | Entrega y recepción: qué se entregó, a quién y con qué estado de conformidad | [acta-entrega.md](references/tipos/acta-entrega.md) | `ejemplo-acta-entrega.json` |
| `notas-version` | Qué cambia en una versión entregada | [notas-version.md](references/tipos/notas-version.md) | `ejemplo-notas-version.json` |
| `informe-cierre` | Balance interno de un proyecto | [informe-cierre.md](references/tipos/informe-cierre.md) | `ejemplo-informe-cierre.json` |
| `acta-baja` | Retirada de un sistema, procedimiento o documentos, con autorización | [acta-baja.md](references/tipos/acta-baja.md) | `ejemplo-acta-baja.json` |
| `ficha-modelo` | Acompañar un modelo estadístico o de aprendizaje automático | [ficha-modelo.md](references/tipos/ficha-modelo.md) | `ejemplo-ficha-modelo.json` |
| `ficha-proceso` | Cómo trabaja un proceso de la entidad (SIPOC), en una o dos páginas | [ficha-proceso.md](references/tipos/ficha-proceso.md) | `ejemplo-ficha-proceso.json` |
| dossier | El usuario pide un «dossier», «informe-dossier», «modo nasa dossier» o «flow NASA» | [dossier.md](references/tipos/dossier.md) | no usa el motor JSON |

El acta de reunión se exporta a Word con `scripts/build_acta_docx.py`; el comando está en [acta-reunion.md](references/tipos/acta-reunion.md#acta-de-reunión-en-word). Si el usuario aporta un formato obligatorio, trabajar sobre una copia y conservar su estructura. Todos los tipos de proyecto usan `format.profile: "institucional"`; el perfil APA es solo del informe. Cada guía dice si su tipo lleva figura; para un esquema nuevo, usar la skill `diagram-design` y seguir [diagramas.md](references/diagramas.md).

## Leer solo lo necesario

Cada tipo lee su guía, [pendientes-y-estado.md](references/pendientes-y-estado.md) (cómo se escribe lo que falta, quién firma, estado y fechas), [contrato/raiz.md](references/contrato/raiz.md), [contrato/secciones.md](references/contrato/secciones.md) y el archivo del bloque que use el tipo (`references/contrato/fields.md`, `risks.md`, `quote.md`, `requirements.md`, `impact.md`, `wbs.md` o `testcase.md`). Además:

- [codigos.md](references/codigos.md), para asignar `document.code` y citar otros documentos.
- [ciclo-de-vida.md](references/ciclo-de-vida.md), si se declara `document.lifecycle` o se retira o sustituye una copia.
- [diagramas.md](references/diagramas.md), solo si el tipo lleva figura.
- [redaccion.md](references/informe/redaccion.md), [estructura.md](references/informe/estructura.md), [apa.md](references/informe/apa.md) y [composicion.md](references/informe/composicion.md) son del informe y el manual; los demás tipos no los leen.

## Reglas para todos los tipos

- **Identidad.** Va en `brand` del JSON (`entity`, `unit`, `accent`, `logo`; ver [contrato/raiz.md](references/contrato/raiz.md)). Reutilizar logo, entidad, colores y metadatos que dé el usuario. Si faltan, usar una identidad neutral explícita y el estado Borrador. No inventar una entidad, un responsable, una fecha de aprobación ni un historial. Pedir solo los datos que bloqueen una entrega real. Separar la versión del documento, la del sistema descrito y la de esta skill.
- **No inventar.** Ni firmas, ni aprobaciones, ni resultados de pruebas, ni cifras, ni nombres. Lo que falta se escribe con las palabras de [pendientes-y-estado.md](references/pendientes-y-estado.md). Los ejemplos son ficticios y no se reutilizan como hechos.
- **Fuente editable.** El contenido, la identidad, la fecha efectiva y la revisión viven en un JSON. Secciones, tablas, figuras y casos llevan identificadores estables; se referencian con `{{ref:identificador}}`, sin números de página ni índices manuales. Un dato desconocido no equivale a cero. Un `changes` registra cambios reales (versión, fecha, resumen, responsable, objetos afectados); no se cambia la fecha por exportar.
- **Revisar un documento que ya existe.** Una versión nueva conserva el código, sube `document.version` y añade una fila a `changes` con la fecha y los objetos afectados; la fila anterior no se toca. Se cita como «SRO-ALC-01, versión 0.2». No hace falta `document.lifecycle` salvo que conste la decisión de dejar la copia anterior fuera de uso. Antes de que quien contrata acepte una propuesta, un cambio es una versión nueva de ella; después de aceptada, es una solicitud de cambio. Una prueba que falla sobre lo ya acordado se corrige y se repite: no es un cambio ni una cotización nueva.
- **Ciclo de vida.** Opcional. Sustituido, retirado y archivado llevan una banda en cada página. Una fecha o un rótulo no acredita la autorización de un cambio de estado.
- **Redacción.** El destinatario lee sobre el sistema o la actividad, sin reconstruir cómo trabajó el agente. Ni rutas de trabajo, ni hashes, ni localizadores personales en el documento. Cada guía incorpora la pirámide de Minto (la conclusión primero, después las razones y la evidencia) y la revisión de estilo de unicorntext (sin relleno, sin el contraste «no es X sino Y» ni enumeraciones por costumbre); las skills `minto-pyramid` y `unicorntext` solo se cargan si el usuario las invoca. Los esquemas nuevos los produce `diagram-design`, con la identidad del documento.

## Renderizar

El motor usa Python 3, `reportlab`, `pypdf` y `pdfplumber`; las figuras SVG externas requieren `svglib`. Comprobarlas con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, crear un entorno virtual fuera de la carpeta de la skill y de la de entrega (por ejemplo, en `~/.cache`): `python3 -m venv <carpeta> && <carpeta>/bin/python -m pip install "reportlab>=4.4,<5" "pypdf>=6,<7" "pdfplumber>=0.11,<1" "Pillow>=11,<13"`, más `svglib` si hay figuras SVG; y usar ese intérprete. Sin una dependencia, los scripts terminan con código 2 y un mensaje que dice qué instalar. Con `PYTHONDONTWRITEBYTECODE=1` no dejan `__pycache__` dentro de la skill. Los scripts de `diagram-design` pueden necesitar otro intérprete (por ejemplo, uno con Playwright). No descargar fuentes ni logos por defecto.

```sh
python3 <skill>/scripts/build_report.py <documento.json> --output <documento.pdf>
python3 <skill>/scripts/check_report.py <documento.pdf>
```

El motor genera portada, encabezado institucional, fecha, versión y estado, `Página X de Y`, historial, contenido, índices condicionales, marcadores, referencias internas y un manifiesto `.manifest.json`. Compila hasta estabilizar índices y total. Falla si una fila no cabe o un objeto carece de referencia; no reduce la letra en silencio. Para otros documentos Word, usar un flujo de autoría DOCX con estilos nativos y campos de página recalculados.

## Comprobar y entregar

1. Ejecutar el comprobador: papel, total de páginas, metadatos, destinos de índices, enlaces, texto fuera de márgenes y mínimo tipográfico. Es una comprobación parcial; no demuestra corrección técnica ni accesibilidad PDF/UA.
2. Renderizar **todas** las páginas con Poppler o un renderizador disponible y abrirlas: portada, historial, índices, figuras, cada corte de tabla y la última página. Un comando exitoso no demuestra buena composición. Ninguna página debe quedar solo con cabecera y pie ni con el histórico solo.
3. Corregir colisiones, filas cortadas, títulos huérfanos y rótulos ilegibles redistribuyendo columnas o acortando texto antes de reducir tamaños. Tras cada cambio, recompilar y revisar los cortes nuevos.
4. Entregar el PDF con su manifiesto (el comprobador lo exige junto al PDF) y la fuente editable con sus activos. Mantener inventarios, hashes y notas de revisión en archivos de trabajo, fuera del documento. Resumir los pendientes que afecten a la entrega, sin inventar validaciones ni aprobaciones.
