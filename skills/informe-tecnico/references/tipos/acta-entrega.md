# Acta de entrega y recepción

Elegir `document.kind: "acta-entrega"` para registrar qué se entrega, a quién y en qué estado se recibe. Partir de `assets/ejemplo-acta-entrega.json`. El acta identifica el inventario y su comprobación; la conformidad depende de la evidencia y de la decisión de quien acepta. Va después del alcance y puede citar la capacitación. Diagrama: no; el inventario, las comprobaciones y las firmas resuelven la finalidad del documento.

El PDF comienza con título y contenido en la primera página, sin portada. La cabecera, el pie, los marcadores y las referencias funcionan como en los informes. Usar `document.show_changes: true` para imprimir al final el histórico, conservando `changes` en la fuente. Los índices son opcionales; no se recomiendan para un acta breve. Si una entidad exige un formato oficial, trabajar sobre una copia y conservar sus campos y cláusulas, verificando que lo declarado tenga respaldo.

La muestra ocupa cuatro páginas: información general en la 1; inventario y capacitación en la 2; observaciones, frase de estado y firmas de aceptación en la 3; responsabilidad e histórico en la 4. El inventario pasa entero a la página 2 y la segunda tabla de firmas a la 4, dejando huecos al pie en las páginas anteriores. Es el compromiso de mantener las tablas completas sin reducir la letra ni añadir relleno. Las variantes sin observaciones o sin capacitación de la prueba ocupan tres páginas.

La entrega del ejemplo cierra la cadena de documentos del módulo de pagos: requerimiento, factibilidad, alcance, plan de pruebas, capacitación y entrega. El acta de reunión es otro ejemplo independiente. El esquema de los bloques está en [secciones.md](../contrato/secciones.md); el código se elige con [codigos.md](../codigos.md).

## Decidir antes de redactar

Identificar el objeto, la versión o identificación de cada entregable, las partes que entregan y reciben, el líder de proyecto y la fecha efectiva. Conservar el código, fecha, versión y estado del documento; indicar en el cuerpo la fecha del hecho si difiere de la revisión. Los responsables y cargos vienen de los documentos del proyecto, sin asignar funciones nuevas por suposición.

Una entrega comunicada, una recepción para revisión, una conformidad y una firma son hechos distintos. Abrir con el estado documentado. Si la revisión sigue abierta, precisar las comprobaciones pendientes, quién las hace y quién decide la conformidad. Los plazos solo se anotan cuando consten.

La decisión de mayor peso es la conformidad y el cierre. Cuenta como respaldo el alcance aprobado y su inventario, las pruebas de aceptación firmadas como satisfactorias y el registro que acredita la ausencia de pendientes e incidencias abiertas. No basta que el software haya sido entregado ni que exista un plan de pruebas. Elegir la variante de cierre de acuerdo con esa evidencia.

## Completar cada campo

1. **Información general.** Una cuadrícula con proyecto, parte solicitante, equipo ejecutor y líder. Otra con número del acta, fecha de entrega, alcance asociado y pruebas de aceptación. Añadir un párrafo que abra con el estado de entrega y recepción, resuma el antecedente y el trabajo y enlace el inventario. La ubicación del acta de capacitación se desarrolla en su apartado, sin convertir una cita en una certificación.
2. **Entregables y comprobación.** Tabla de cuatro columnas: ítem, entregable, formato o ubicación y comprobación y observaciones. Reutilizar E1, E2 y los demás códigos del alcance. Indicar versión, código o localizador utilizable en el entregable o en su ubicación. Separar dentro de la última celda «Criterio: …» y «Resultado: …» cuando se documente una comprobación. Una tarea por hacer se registra como pendiente. Si no consta la ubicación o la versión, escribir «Por confirmar con (responsable)», sin inventar rutas o versiones. La capacitación es E5 en el ejemplo porque el alcance la compromete.
3. **Capacitación realizada.** Una elección `fields` de una sola marca con `Con capacitación` o `Sin capacitación`. Con la primera, añadir fecha y «Acta de capacitación N.º» a partir del registro que consta. Los códigos entre documentos son texto; `{{ref:id}}` enlaza objetos del mismo JSON. Si la constancia está sin firmar, decirlo; no presentarla como certificación completada. Con «Sin capacitación», quitar fecha, número y la oración que cite una sesión realizada, e indicar el motivo. Si sigue comprometida, queda como pendiente y no se cuenta como entregada. Si no aplica o no se requirió, citar la base de esa decisión. La elección no modifica por sí sola el alcance.
4. **Observaciones generales.** Apartado opcional. Registrar observaciones y pendientes con responsable y plazo cuando consten; si no hay datos propios, quitar el apartado entero y las referencias que lo llamen. No afirmar que no hay pendientes solo por omitirlo.
5. **Conformidad y cierre.** Aplicar una de las dos variantes de abajo. No añadir casillas de conformidad.
6. **Firmas de aceptación.** Una tabla con las dos partes y filas para nombre y cargo, firma y fecha. Dejar el espacio de firma en blanco y las fechas pendientes mientras no se produzcan. Los nombres en una tabla preparada para firma no acreditan aceptación.
7. **Firmas de responsabilidad.** Elaboración, revisión y aprobación del documento, con nombre, cargo, espacio de firma y fecha. La tabla cierra el cuerpo antes del histórico.

### Conformidad y cierre

**Declaración de conformidad.** Solo cuando consten el alcance aprobado, las pruebas firmadas como satisfactorias y la ausencia de pendientes e incidencias abiertas. Citar el código de cada documento que respalde esos hechos. Ejemplo de redacción condicional: «Se completaron y entregaron los elementos del alcance [código del alcance aprobado]. Las pruebas de aceptación [código y revisión] fueron satisfactorias y están firmadas. El registro de cierre [código] confirma que no quedan pendientes ni incidencias abiertas. La parte solicitante expresa su conformidad y se acuerda el cierre». Sustituir los marcadores con documentos existentes antes de usarla; este texto no describe el JSON de demostración.

**Frase de estado.** Cuando falte cualquiera de esas bases, indicar qué se entregó, qué falta, qué decisión se espera y de quién. El ejemplo entrega E1 a E5 para revisión el 08/01/2027. DEMO-ATP-01 tiene todos los casos sin ejecutar y el certificado pendiente; por eso espera la decisión de Soledad Paredes y conserva pendientes la conformidad, el cierre y las firmas.

No se añade una casilla «Conforme» o «Conforme con observaciones». Si el código que respalda una declaración no consta, escribir «Por confirmar» y mantener la decisión pendiente. Para un documento real con respaldo insuficiente, el estado es Borrador; «Demostración» queda reservado a los ejemplos de la skill. Un formato institucional con una declaración fija requiere comprobar esos hechos antes de preparar una versión lista para firma. Si faltan, preparar un borrador e identificar la decisión pendiente. Los roles y la estructura obligatoria de la entidad se conservan.

## Cómo se comprueba

Comparar el inventario con el alcance. Cada ítem entregado conserva su código y nombre; identificar las entregas parciales y lo que queda pendiente, sin omitir compromisos. La fecha de entrega sigue a la capacitación si se declara realizada antes de entregar y es compatible con el cronograma. En el ejemplo, la capacitación del 07/01/2027 y la entrega del 08/01/2027 caen en la implementación propuesta del 04/01/2027 al 10/01/2027. Ese calendario no acredita ejecución ni autoriza la puesta en producción.

Comprobar que los nombres y cargos coincidan entre documentos; que el número de acta sea `document.code`; que el número y la fecha de capacitación sean los de su acta; y que ningún resultado diga «satisfactorio» cuando el ATP esté pendiente. En cada comprobación distinguir el criterio del resultado observado y localizar su evidencia. Un criterio sin observación todavía no es una prueba realizada.

## Personalizar

Cambiar `brand.entity`, `brand.unit`, `brand.accent` y `brand.logo` (PNG/JPEG relativo al JSON), así como `document.code`, `paper` (`A4` o `Letter`), firmantes, opciones de capacitación y localizadores de entrega. Los rótulos «parte solicitante» y «equipo ejecutor» son genéricos y se reemplazan por los de la entidad. Mantener los identificadores de entregables acordados; no copiarlos de otro proyecto. Una nueva revisión conserva su código y cambia su versión.

## Qué no inventar

Aplicar [pendientes-y-estado.md](../pendientes-y-estado.md) para nombres y cargos no confirmados, estado, fechas de firma e historial de un documento nuevo. Lo propio de la entrega:

| Dato | Tratamiento |
|---|---|
| Comprobación de un entregable sin ejecutar | Resultado: Pendiente |
| Conformidad sin evidencia completa | Frase de estado, con decisión pendiente y responsable |
| Ubicación o versión sin confirmar | Por confirmar con (responsable) |
| Sesión citada con constancia sin firmar | Explicitar que la constancia y sus firmas están pendientes |
| Capacitación comprometida que aún no se realizó | Sin capacitación; mantenerla como pendiente del alcance |

No inventar recepción, pruebas satisfactorias, ausencia de incidencias, versiones, rutas, firmas ni aprobaciones. El motor valida estructura y elecciones; no comprueba que los hechos de las celdas sean verdaderos.

## Qué se elimina cuando algo no aplica

- **Sin capacitación:** conservar la elección con una sola marca, quitar fecha y número y cualquier afirmación de una sesión realizada. Ajustar el inventario si la entrega es parcial e indicar lo que sigue pendiente.
- **Sin observaciones generales:** quitar el apartado y sus referencias. En el ejemplo también se reemplaza la llamada a `{{ref:pendientes}}` de la frase de cierre por una referencia textual a la revisión pendiente; la conformidad permanece pendiente porque el ATP no está ejecutado.
- **Sin índices:** omitir `document.indexes`.

## ¿Necesita un diagrama?

No. El acta permite revisar qué se entregó y qué se comprobó mediante el inventario, los resultados y las firmas. La arquitectura y el perímetro se consultan en la factibilidad o el alcance, sin repetir sus figuras.

## Revisar la redacción con las skills hermanas

Aplicar los criterios incorporados de Minto: estado de recepción o decisión primero y después el antecedente necesario, conservando el orden de una plantilla obligatoria. Aplicar el criterio de unicorntext: quitar frases de trámite y repeticiones sin perder responsables, condiciones, plazos y términos técnicos. Del enfoque NASA se conserva la comprobación antes del cierre: cada verificación identifica el elemento y el resultado observable. Estos criterios no requieren instalar las skills hermanas; si el usuario las invoca, aplicar además las instrucciones disponibles.

## Comprobar y entregar

Comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber, PIL"`. Si faltan paquetes, seguir `SKILL.md`: entorno virtual fuera de la entrega con `reportlab>=4.4,<5`, `pypdf>=6,<7`, `pdfplumber>=0.11,<1` y `Pillow>=11,<13`. Usar su intérprete:

```sh
python3 <skill>/scripts/build_report.py acta.json --output acta.pdf
python3 <skill>/scripts/check_report.py acta.pdf
pdftoppm -r 80 -png acta.pdf pagina
```

Sin Poppler: `python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i,p in enumerate(pdfplumber.open('acta.pdf').pages,1)]"`.

Abrir todas las páginas. Comprobar que la opción de capacitación tenga una sola cruz y negrita, que no exista una casilla de conformidad, que las tablas que caben permanezcan enteras y que cada tabla de firmas esté completa, con responsabilidad e histórico al cierre. Revisar los cortes y rótulos: una tabla entera puede dejar un hueco al pie si no cabe en el resto. No reducir la letra ni rellenar el documento para ocuparlo. Si el histórico queda solo en una página, revisar la extensión del contenido anterior. Entregar PDF, manifiesto `.manifest.json` (obligatorio para el comprobador), fuente JSON y activos necesarios.
