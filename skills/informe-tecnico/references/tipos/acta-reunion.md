# Acta de reunión

Elegir `document.kind: "acta-reunion"` para registrar lo tratado y acordado. Empezar por `assets/ejemplo-acta-reunion.json`. Conservar código, fecha, versión y estado; indicar la fecha de la sesión en el cuerpo si difiere de la revisión. El ejemplo del Proyecto Atlas es independiente de la cadena del módulo de pagos que muestra el acta de entrega.

El PDF empieza con título y contenido en la primera página. La cabecera, el pie, los marcadores y las referencias funcionan como en los informes. Mantener las revisiones en `changes` en la fuente editable. Usar el perfil `institucional` para una composición compacta; el ejemplo tiene dos páginas. Cuando la entidad exija un formato oficial, usar una copia y conservar sus campos y cláusulas, verificando la salida en el formato solicitado. El esquema está en [secciones.md](../contrato/secciones.md).

## Completar el acta de reunión

1. **Ficha y asistencia.** Identificar proyecto, objetivo, fecha, hora, lugar o modalidad. Registrar los asistentes y ausentes que consten, con su función o área cuando aporte contexto. Distinguir el estado de aprobación de esta acta de la revisión de un acta anterior.
2. **Orden del día.** Enumerar los temas en el orden efectivo y asignarles identificadores breves como `T01`. Incluir revisión del acta anterior y otros asuntos cuando hayan formado parte de la sesión.
3. **Desarrollo por punto.** Usar el mismo identificador de agenda para resumir lo tratado y registrar su resultado. Distinguir información, propuesta, decisión y asunto pendiente. Cuando un tema derive en una tarea, indicar su identificador de acuerdo para localizarla en el seguimiento. Atribuir una intervención solo cuando aporte precisión al registro.
4. **Resultados y acuerdos.** Registrar cada compromiso una sola vez, con identificador, punto de origen, acción, responsable y plazo. Una decisión que no requiera una acción puede quedar en el desarrollo. Si el acuerdo consta y falta la asignación o el plazo, indicar «Por confirmar», como en [pendientes-y-estado.md](../pendientes-y-estado.md). Una acción que el equipo propone y nadie acordó va rotulada como propuesta en el título de la tabla. Una propuesta sin resolver permanece entre los asuntos pendientes.
5. **Cierre y anexos.** Registrar la próxima reunión cuando esté acordada, con fecha, hora y propósito si constan. Indicar quién elaboró el acta y su estado de aprobación cuando corresponda. Identificar los anexos incorporados o entregados por separado y vincularlos desde el punto o acuerdo pertinente.

En sesiones breves se pueden reunir la agenda y el desarrollo en una tabla con una fila por punto. Cuando haya varios temas, acuerdos o anexos, separar las secciones como en el ejemplo de dos páginas. En ambos casos, la lectura debe permitir pasar de cada tema a su resultado y, cuando corresponda, a la acción de seguimiento.

## Acta de reunión en Word

Usar `document.kind` igual a `acta-reunion` y `format.profile` igual a `institucional`. El exportador genera un `.docx` con tablas y texto editables, referencias internas y campos de página. Admite párrafos, listas, tablas y saltos de página. Usar un logo PNG o JPEG cuando se requiera. La fuente JSON sirve para regenerar el documento y los cambios manuales en Word se conservan en el archivo Word.

Con el intérprete del entorno de la skill, comprobar `python3 -c "import docx"`; si falta, instalar `python-docx`. Ejecutar el exportador sobre una copia de la fuente:

```sh
python3 -m pip install python-docx
python3 <skill>/scripts/build_acta_docx.py acta.json --output acta.docx
```

Abrir el Word o renderizarlo para comprobar la paginación, las tablas y los saltos. Si se exige un formato oficial de Word, preparar el acta sobre una copia de ese formato.

## Criterios de redacción y cierre

- Minto orienta la lectura: presentar primero la decisión del punto tratado y después el antecedente necesario. Conservar el orden oficial de una plantilla obligatoria.
- Unicorntext orienta la revisión: quitar frases de trámite y repeticiones que no aporten, manteniendo responsables, condiciones, plazos y terminología técnica.
- Del enfoque NASA se toma la comprobación antes del cierre: un tercero debe poder localizar cada compromiso y saber quién lo atiende y para cuándo, o qué dato queda por definir.
- Usar tablas para inventarios y acuerdos. Mantener encabezados repetidos si una tabla continúa y revisar los cortes de página. El flujo habitual se resuelve con texto y tablas, sin diagrama.

## Comprobar y entregar el PDF

Resolver el intérprete y las dependencias según `SKILL.md`, compilar con `python3 <skill>/scripts/build_report.py acta.json --output acta.pdf` y comprobar con `python3 <skill>/scripts/check_report.py acta.pdf`. Renderizar todas las páginas a 80 ppp y abrirlas para revisar tablas, saltos y vínculos entre agenda, resultados y acuerdos. Entregar el PDF, su manifiesto y la fuente editable con sus activos. Para Word, seguir el apartado anterior y revisar también su paginación.

Para reuniones se tomó el patrón de agenda, acuerdos y seguimiento de [IT Process Wiki](https://wiki.es.it-processmaps.com/index.php/Gesti%C3%B3n_de_proyectos_-_Plantilla:_Acta_de_la_reuni%C3%B3n). La muestra contiene una situación ficticia y redacción propia.
