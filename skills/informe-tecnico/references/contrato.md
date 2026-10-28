# Contrato del motor de referencia

## Ejecución y entregables

Ejecutar `scripts/build_report.py fuente.json --output informe.pdf` con Python 3 y reportlab. La fuente contiene datos UTF-8, no código ejecutable ni HTML: el motor escapa el marcado. Genera PDF y `informe.manifest.json` con hash de fuente, activos y PDF, páginas, pasadas y destinos. `scripts/check_report.py informe.pdf` exige ese manifiesto y usa pypdf/pdfplumber. Una fuente modificada exige recompilar; el PDF no se actualiza solo.

`assets/ejemplo.json` muestra el esquema completo. Rutas de logo, fuentes y figuras se resuelven respecto al JSON, no al directorio desde donde se ejecuta. Empaquetar esos archivos junto con la fuente.

Los campos `id` y `path` son datos de composición; no se convierten en referencias bibliográficas. Los textos `source`, `description`, títulos, celdas, historial y metadatos de presentación sí se imprimen: redactarlos para el destinatario según [redaccion.md](redaccion.md). Conservar localizadores del equipo y hashes en archivos de trabajo o manifiestos, fuera de esos textos visibles.

`assets/plantilla-base.json` permite comenzar un informe con el capítulo 4 reservado al desarrollo técnico. Sus campos vacíos de identidad/metadatos y su historial vacío deben completarse con evidencia real antes de compilar; el motor los rechaza mientras falten. Los bloques de contenido vacíos son espacios de autoría: rellenarlos o eliminar las subsecciones que no correspondan, no entregar capítulos sin desarrollar. La muestra completa es un documento distinto, de demostración.

Cambiar `brand` actualiza la composición del informe; no recolorea una imagen externa ya exportada. Si cambia la identidad, regenerar también los esquemas desde su HTML/SVG con los nuevos tokens antes de compilar.

## Raíz

- `schema_version`: entero 1.
- `brand`: `entity` obligatorio; `unit`, `accent` hexadecimal, `ink`, `rule`, `border` en puntos, `frame` booleano y `logo` opcionales. Sin logo se muestra el nombre tipográficamente. `fonts` opcional es un objeto con rutas TTF `normal` y `bold`; incluir ambas y verificar licencia y cobertura de caracteres.
- `document`: `title`, `code`, `version`, `date` ISO YYYY-MM-DD y `status` obligatorios como cadenas. Opcionales: `short_title` para cabecera, `subtitle`, `author`, `notice`, `control_note`, `paper` (`A4` o `Letter`, predeterminado A4). La versión es texto, no número decimal.
- `changes`: lista no vacía de cambios. Cada elemento tiene `version`, `date`, `summary`, `author` y opcional `affects` como lista de IDs actuales. Para historial no localizado usar explicación textual, no fabricar un destino. No hay aprobaciones automáticas.
- `sections`: lista no vacía de secciones en orden de lectura.

## Secciones y bloques

Cada sección tiene `id`, `title`, `level` (1,2,3; predeterminado 1), `blocks` y opcional `new_page`. No saltar niveles. La numeración se calcula por jerarquía. Los IDs empiezan con letra y continúan con letras ASCII, dígitos, guion o guion bajo; son únicos en todo el documento.

Bloques admitidos:

| type | Campos |
| --- | --- |
| paragraph | `text` |
| list | `items` (lista de texto), `ordered` opcional |
| note | `text`, `label` opcional |
| pagebreak | Sin otros campos |
| table | `id`, `title`, `headers`, `rows`; opcionales `widths`, `source`, `number` |
| figure | `id`, `title`, `description`, `source`; `nodes` para flujo simple **o** `path` para SVG/imagen; `max_height_mm` y `number` opcionales |

`headers` y cada fila deben tener la misma longitud. `widths` contiene pesos positivos, uno por columna. Una celda es texto; `null` se muestra «No informado». Códigos con cero inicial deben ser cadenas. Una fila demasiado alta falla: reorganizar el contenido, no reducir automáticamente la fuente. La fuente de una tabla se coloca al final, y su título y encabezados se repiten al partirla.

`number` conserva el número publicado de un catálogo (por ejemplo `"136"`); no renumerar catálogos heredados. Para tablas nuevas en un catálogo usar números explícitos que no colisionen. Si se omite, se usa el ordinal de aparición. Numeración de tablas y figuras independiente.

`{{ref:id}}` dentro de textos, celdas e historial se transforma en el título/número del objeto y un enlace al destino. Un ID inexistente detiene la compilación. No admite enlaces externos ni estilo en línea en este motor.

El flujo nativo admite 2-5 nodos de texto y flechas lineales. SVG externos requieren `svglib` y compatibilidad con sus funciones. No usar diagramas animados dentro del PDF. Conservar la fuente vectorial editable.

## Alcance real

El motor implementa A4/Carta en vertical, portada, control de cambios, contenido, índices condicionales, encabezado/pie, marcadores y tablas simples con filas no divisibles. No implementa DOCX, numeración romana, tablas anidadas, fórmulas, mezcla de orientaciones, firmas electrónicas, control de acceso ni PDF/UA. Las cabeceras y pies demasiado largos fallan con mensaje en vez de solaparse. Para un documento con otras necesidades elegir un motor apropiado manteniendo los mismos invariantes.
