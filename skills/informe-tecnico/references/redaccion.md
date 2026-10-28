# Redacción para documentos de presentación

El destinatario necesita entender el sistema, el trabajo y sus resultados. La lectura de archivos, las herramientas utilizadas por el agente y la preparación del paquete son actividades de autoría; no constituyen por sí mismas el tema del informe.

## Elegir la voz por finalidad

| Documento solicitado | Voz y contenido |
| --- | --- |
| Informe técnico de actividad o entrega | Redacción impersonal, principalmente en pasado para trabajo realizado: «Se implementó…», «Se configuró…», «Se elaboró…». Describir componente, acción, alcance y resultado concreto. Usar presente para el funcionamiento vigente. |
| Manual de usuario u operación | Presente para capacidades y reglas: «El sistema permite…». Pasos directos y uniformes: «Seleccione la institución», «Pulse Guardar». Explicar condición inicial, acción y resultado; evitar convertir cada instrucción en un relato de implementación. |
| Evaluación o auditoría solicitada | Método, muestra, hallazgos, pruebas y limitaciones proporcionados al encargo. Este tono requiere que esa sea la finalidad del documento. |

No reemplazar mecánicamente cualquier verbo por «se validó». Reservar esa expresión para una comprobación efectivamente realizada y precisar su objeto: «Se verificó la apertura del formulario enviado en modo de consulta». La existencia de una captura o un botón no demuestra la ejecución de una importación, un despliegue o una aprobación.

Cuando una parte siga pendiente, expresarlo con lenguaje de proyecto una vez en el lugar pertinente: «El despliegue definitivo está previsto para el 4 de noviembre». Mantener esa condición coherente en resultados y conclusiones. No repetir en cada figura fórmulas como «no acredita», «no certifica» o «no se ejecutó durante esta revisión» salvo que sean necesarias para entender un resultado de evaluación solicitado.

## Separar el documento de los archivos de trabajo

En el documento de presentación:

- Explicar el sistema, los componentes implementados, el procedimiento o los resultados de la actividad.
- Citar otros informes y manuales por su nombre o código documental existente. Usar «AA_Act9_4, apartado 3» o «Manual de usuario SIGC - Administrador, Importación de datos». Añadir fecha, versión o página cuando ayude a localizar el contenido.
- Usar fuentes de datos cuando sean pertinentes para una métrica: «Fuente: OpenAlex y registros institucionales; corte: octubre de 2026». En un informe de implementación no es obligatorio añadir bibliografía para cada descripción del propio sistema.
- Identificar una tabla o columna de base de datos solo si ese nivel de detalle pertenece al encargo. Una URL de acceso al sistema es pertinente para un manual; la carpeta personal donde se leyó su código no lo es.
- Escribir pies que expliquen la función o la lectura de la figura. Incluir entorno y fecha de captura donde importen, sin convertir el pie en un inventario de archivos.

En archivos de trabajo o un anexo de trazabilidad pedido expresamente:

- Guardar rutas como `/Volumes/...`, `/Users/...`, carpetas temporales y nombres de medios extraídos del DOCX.
- Conservar hashes, registros de consulta, método de extracción, recortes y correspondencia entre IDs internos y fuentes.
- Mantener dudas editoriales, discrepancias entre versiones y pruebas pendientes que todavía deban resolverse durante la autoría. Trasladar al documento solo su consecuencia relevante para el sistema o la entrega.

La trazabilidad no se elimina: se conserva sin obligar al lector del informe a navegar por el equipo del autor. No publicar fuentes privadas al actualizar el repositorio de la skill.

## Ejemplos de edición

| Evitar en un informe de actividad | Redacción adecuada según el hecho sustentado |
| --- | --- |
| «Se leyeron tres DOCX y se extrajeron 45 imágenes.» | «Se elaboró la documentación de usuario para los roles Usuario, Administrador y SuperAdministrador.» Si los manuales ya existían y solo se consolidaron, escribir «Se consolidó la guía de navegación a partir de los manuales por rol». |
| «En la sesión revisada se observó un menú con cuatro entradas.» | «El menú Gestión reúne Benchmarking IES, Búsqueda de publicaciones, Formulario IES e Importar». |
| «El solicitante informa que se desplegaría ahí mismo.» | «El despliegue definitivo se realizará en la dirección de acceso actual, una vez concluida la depuración de la base». |
| «La imagen no acredita envío de correo ni creación realizada durante esta revisión.» | «El formulario de alta permite definir los datos de la cuenta, su rol y la IES asignada». Conservar la prueba de envío pendiente en el registro de trabajo o en el estado de entrega, si afecta al resultado. |
| «Fuente: [R3], image7.png, extraída sin modificar.» | «Fuente: Manual de usuario SIGC - SuperAdministrador». Si es una captura propia, «SIGC, ambiente de pruebas, 28/10/2026». |

No afirmar «se implementó», «se realizó» o «se validó» únicamente para dar apariencia de cierre. El estado real prevalece sobre la forma verbal.

## Etiquetas y referencias legibles

- Usar «apartado 1.2», «sección 4.3», «Tabla 2» y «Figura 5». Omitir el símbolo de sección `§`, que puede confundirse con un signo monetario, y etiquetas como `$1.2`.
- Conservar códigos oficiales como `AA_Act9_4` o los identificadores existentes de un catálogo. No sustituirlos por un sistema nuevo `[R1]`, `M07` o `N19` en el texto presentado, salvo que el destinatario haya solicitado ese registro de evidencias.
- Numerar secciones, figuras y tablas automáticamente mediante los IDs internos y `{{ref:id}}`. El resultado impreso debe mostrar el nombre y el número, nunca el token, un ID de programación, Markdown sin interpretar ni una instrucción de la plantilla.
- Evitar repetir la finalidad de cada capítulo, comentar cómo se escribió el documento o llenar las conclusiones de instrucciones al agente.

Antes de entregar, leer de corrido portada, introducción, desarrollo, resultados, pies y referencias. Si el lector aprende más sobre la revisión del agente que sobre el sistema, reescribir el contenido antes de exportar.
