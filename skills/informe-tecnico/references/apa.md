# Formato institucional con criterios APA 7

Guía verificada con APA Style el 28 de octubre de 2026. La séptima edición se aplica aquí como criterio de composición y atribución para informes y manuales. Conservar la voz y la finalidad definidas en [redaccion.md](redaccion.md).

## Perfil y límites

Usar `"format": {"profile": "institucional-apa"}` para un documento nuevo. La plantilla base lo incluye. El motor aplica las medidas de la tabla y registra los valores efectivos en el manifiesto. Cambiar un valor para atender un requisito institucional es una adaptación que debe quedar identificada en el paquete de trabajo.

| Elemento | Tratamiento del perfil |
| --- | --- |
| Cuerpo | 11 pt, alineación izquierda, margen derecho irregular. |
| Interlineado | 2,0: con cuerpo de 11 pt, distancia de 22 pt entre líneas. |
| Párrafos de texto | Primera línea a 1,27 cm; sin espacios adicionales antes o después. |
| Listas, títulos, celdas y notas de tablas/figuras | Sin sangría inicial de párrafo. Las listas utilizan sangría colgante propia. |
| Referencias | Doble interlineado y sangría francesa de 1,27 cm: primera línea al margen y siguientes desplazadas. |
| Citas en bloque | Desde 40 palabras, sin comillas envolventes; bloque a 1,27 cm del margen izquierdo. Los párrafos posteriores añaden 1,27 cm en su primera línea. |
| Títulos de sección | Nivel 1 centrado y en negrita; nivel 2 izquierdo y en negrita; nivel 3 izquierdo y en negrita cursiva. Se conserva la numeración técnica. |
| Tablas y figuras | Número en negrita y título en cursiva, encima del contenido; nota debajo cuando sea necesaria. |
| Celdas | Misma familia y tamaño del cuerpo; interlineado sencillo como excepción permitida. Puede configurarse a 1,5 o 2 si mejora la lectura. |

APA prescribe doble interlineado sin espacios extra entre párrafos y admite excepciones para las celdas y el interior de imágenes. La alineación izquierda y ambas sangrías proceden de sus reglas de párrafo. No simular sangrías mediante espacios o tabulaciones escritos en el texto. Fuentes: [interlineado](https://apastyle.apa.org/style-grammar-guidelines/paper-format/line-spacing) y [párrafos](https://apastyle.apa.org/style-grammar-guidelines/paper-format/paragraph-format).

La plantilla conserva cabecera con logo, control de cambios, portada propia, índices, capítulos numerados y márgenes de cuerpo de 21 mm laterales, 58 mm superior y 25 mm inferior. Los preliminares, índices, encabezados y pies mantienen sus estilos institucionales compactos. Estas son diferencias deliberadas respecto de un trabajo académico APA. APA indica márgenes de 2,54 cm; no presentar los márgenes institucionales como una medida APA. Fuente: [márgenes](https://apastyle.apa.org/style-grammar-guidelines/paper-format/margins).

Por defecto se usa Helvetica integrada, como familia sans serif institucional. APA admite varias familias y ofrece, entre otros ejemplos, Arial de 11 pt, Calibri de 11 pt, Aptos de 12 pt y Times New Roman de 12 pt. Si el destinatario exige una fuente concreta, proporcionar sus TTF con licencia adecuada y ajustar `body_size_pt`; el interlineado se calcula sobre ese tamaño. Para el perfil APA con fuentes externas se requieren variantes normal, negrita, cursiva y negrita cursiva. No distribuir fuentes comerciales sin autorización. Fuente: [fuentes tipográficas](https://apastyle.apa.org/style-grammar-guidelines/paper-format/font).

## Citas y referencias documentales

Cuando se atribuya una idea, utilizar autor y año, con correspondencia en la lista de referencias. En español puede integrarse la cita en la oración: «Pérez (2026) describe…», o entre paréntesis: «… (Pérez, 2026)». Para dos autores, usar sus apellidos; para tres o más, el primer apellido y «et al.», atendiendo a las desambiguaciones. El código de un informe identifica el documento; no reemplaza los datos de atribución. Fuente: [sistema autor-fecha](https://apastyle.apa.org/style-grammar-guidelines/citations/basic-principles/author-date).

Para un manual o informe, recuperar autor personal o institucional, fecha, título, versión o código pertinente y entidad editora o localizador recuperable. Verificar esos datos en el propio documento; el propietario de la carpeta no se convierte por ello en autor. Si autor y editor son la misma entidad, evitar duplicar el editor. Cuando falten datos, aplicar el tratamiento APA correspondiente: título en posición de autor cuando no se conoce, y fecha desconocida identificada expresamente. No deducir la publicación a partir de la fecha de modificación del archivo. Fuentes: [elementos de una referencia](https://apastyle.apa.org/style-grammar-guidelines/references/elements-list-entry) y [datos faltantes](https://apastyle.apa.org/style-grammar-guidelines/references/missing-information).

Conservar códigos existentes dentro del título o identificación, por ejemplo «Manual de operación (ENT-IT-04)». Omitir las rutas personales de lectura y los códigos nuevos del agente. Si un informe de sistema no utiliza fuentes externas, no añadir citas decorativas a cada explicación del propio funcionamiento.

Ordenar las referencias alfabéticamente por autor o por el título que lo sustituya; resolver obras del mismo autor y año mediante sufijos coherentes con las citas. Las comunicaciones no recuperables no se convierten automáticamente en entradas bibliográficas. Mantener DOI como enlace `https://doi.org/...` cuando exista y no añadir un punto después de DOI o URL. Las entradas no son una lista numerada ni una tabla. Fuentes: [principios de las referencias](https://apastyle.apa.org/style-grammar-guidelines/references/basic-principles) y [orden alfabético](https://apastyle.apa.org/instructional-aids/creating-reference-list.pdf).

El bloque `reference` implementa la sangría francesa. El agente prepara y comprueba la entrada bibliográfica; el motor no busca autores, ordena entradas, genera citas autor-fecha ni comprueba su correspondencia. Usar `runs` para cursivas reales en títulos de obras independientes o en los elementos que correspondan; el texto no admite HTML libre. Ver [contrato.md](contrato.md).

## Citas textuales

Preferir una paráfrasis fiel cuando la literalidad no sea necesaria. Las citas menores de 40 palabras se integran entre comillas en un párrafo con autor, año y localizador. Para 40 o más, usar `quotation` con el texto íntegro y `citation` con autor, año y página o localizador adecuado. La cita va después de la puntuación final del bloque, sin añadir otro punto al final. El motor no corrige la fidelidad de la transcripción ni los permisos de reproducción. Fuente: [citas textuales](https://apastyle.apa.org/style-grammar-guidelines/citations/quotations).

## Tablas, figuras y revisión

Mencionar cada tabla o figura en el texto antes de presentarla. El perfil coloca número y título arriba, y utiliza líneas horizontales mínimas en tablas, sin retícula vertical ni sombreado decorativo. Los encabezados y el título de tabla se repiten al continuar en otra página. Las notas explican unidades, abreviaturas y procedencia cuando sean necesarias. Para una reproducción o adaptación ajena, incluir la atribución pertinente; «elaboración propia» no convierte material ajeno en propio. Fuentes: [tablas](https://apastyle.apa.org/style-grammar-guidelines/tables-figures/tables) y [figuras](https://apastyle.apa.org/style-grammar-guidelines/tables-figures/figures).

El gráfico debe seguir siendo legible a su tamaño de impresión. Revisar también fuentes incrustadas, cursivas, saltos de página, sangrías francesas de entradas largas y filas de continuación. Las pruebas del motor miden sangría e interlineado en el PDF, pero no constituyen certificación APA integral.
