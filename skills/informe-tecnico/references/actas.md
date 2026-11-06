# Actas institucionales

Elegir `document.kind: "acta-entrega"` para registrar una entrega y su recepción, o `"acta-reunion"` para registrar lo tratado y acordado. Empezar por el ejemplo editable del tipo correspondiente en `assets/`. Conservar el código, la fecha, la versión y el estado del documento. Indicar la fecha del hecho en el cuerpo cuando difiera de la fecha de revisión.

El PDF genérico empieza con el título y el contenido en la primera página. La cabecera, el pie, los marcadores y las referencias internas funcionan como en los informes. Mantener las revisiones en `changes` en la fuente editable. Usar el perfil `institucional` de los ejemplos para una composición compacta. Cuando la entidad exija un formato oficial, usar una copia de ese formato, conservar sus campos y cláusulas y verificar la salida en el formato solicitado.

## Entrega y recepción

1. Identificar el objeto, la fecha efectiva, el área requirente y las partes que entregan y reciben. Abrir con el estado documentado de la entrega y la recepción.
2. Referir la solicitud o antecedente aplicable y resumir el trabajo realizado. Identificar las funcionalidades cuando sean parte del alcance entregado.
3. Inventariar los entregables con versión, código o localizador utilizable. Separar el criterio de comprobación del resultado observado. Si la revisión sigue abierta, registrar observaciones, pendientes y sus responsables y plazos cuando consten.
4. Registrar la conformidad únicamente cuando conste. Una entrega comunicada, una recepción para revisión, una conformidad y una firma son hechos distintos. Si se requiere firma, reservar espacio en blanco e identificar cada rol. Mantener las firmas en la misma página cuando quepan juntas.

Si el formato institucional incluye una declaración fija de conformidad, comprobar su respaldo antes de producir una versión lista para firma. Cuando falte, preparar un borrador e identificar la decisión pendiente con el solicitante. Los roles y la redacción del formato institucional prevalecen sobre el ejemplo genérico.

## Reunión

1. **Ficha y asistencia.** Identificar proyecto, objetivo, fecha, hora, lugar o modalidad. Registrar los asistentes y ausentes que consten, con su función o área cuando aporte contexto. Distinguir el estado de aprobación de esta acta de la revisión de un acta anterior.
2. **Orden del día.** Enumerar los temas en el orden efectivo y asignarles identificadores breves como `T01`. Incluir revisión del acta anterior y otros asuntos cuando hayan formado parte de la sesión.
3. **Desarrollo por punto.** Usar el mismo identificador de agenda para resumir lo tratado y registrar su resultado. Distinguir información, propuesta, decisión y asunto pendiente. Cuando un tema derive en una tarea, indicar su identificador de acuerdo para localizarla en el seguimiento. Atribuir una intervención solo cuando aporte precisión al registro.
4. **Resultados y acuerdos.** Registrar cada compromiso una sola vez, con identificador, punto de origen, acción, responsable y plazo. Una decisión que no requiera una acción puede quedar en el desarrollo. Si el acuerdo consta y falta la asignación o el plazo, indicar «Por definir». Una propuesta sin resolver permanece entre los asuntos pendientes.
5. **Cierre y anexos.** Registrar la próxima reunión cuando esté acordada, con fecha, hora y propósito si constan. Indicar quién elaboró el acta y su estado de aprobación cuando corresponda. Identificar los anexos incorporados o entregados por separado y vincularlos desde el punto o acuerdo pertinente.

En sesiones breves se pueden reunir la agenda y el desarrollo en una tabla con una fila por punto. Cuando haya varios temas, acuerdos o anexos, separar las secciones como en el ejemplo de dos páginas. En ambos casos, la lectura debe permitir pasar de cada tema a su resultado y, cuando corresponda, a la acción de seguimiento.

## Acta de reunión en Word

Usar `document.kind` igual a `acta-reunion` y `format.profile` igual a `institucional`. El exportador genera un `.docx` con tablas y texto editables, referencias internas y campos de página. Admite párrafos, listas, tablas y saltos de página. Usar un logo PNG o JPEG cuando se requiera. La fuente JSON sirve para regenerar el documento y los cambios manuales en Word se conservan en el archivo Word.

Desde la raíz del repositorio, instalar las dependencias y ejecutar el exportador sobre una copia de la fuente:

```sh
python -m pip install -r requirements.txt python-docx
python skills/informe-tecnico/scripts/build_acta_docx.py acta.json --output acta.docx
```

Abrir el Word o renderizarlo para comprobar la paginación, las tablas y los saltos. Si se exige un formato oficial de Word, preparar el acta sobre una copia de ese formato.

## Criterios de redacción y cierre

- Minto orienta la lectura. Presentar primero el estado de recepción o la decisión del punto tratado y después el antecedente necesario. Conservar el orden oficial de una plantilla obligatoria.
- Unicorntext orienta la revisión. Quitar frases de trámite y repeticiones que no aporten, manteniendo responsables, condiciones, plazos y terminología técnica.
- Del enfoque NASA se toma la comprobación antes del cierre. En una entrega, cada verificación identifica el elemento y el resultado observable. En una reunión, un tercero debe poder localizar cada compromiso y saber quién lo atiende y para cuándo, o qué dato queda por definir.
- Usar tablas para inventarios y acuerdos. Mantener encabezados repetidos si una tabla continúa y revisar los cortes de página. Para estas actas el flujo habitual se resuelve con texto y tablas.

La estructura de entrega se orientó con el formato institucional F04-PRO-GTI-GPT-003 facilitado como referencia. Para reuniones se tomó el patrón de agenda, acuerdos y seguimiento de [IT Process Wiki](https://wiki.es.it-processmaps.com/index.php/Gesti%C3%B3n_de_proyectos_-_Plantilla:_Acta_de_la_reuni%C3%B3n). Las muestras contienen situaciones ficticias y redacción propia.
