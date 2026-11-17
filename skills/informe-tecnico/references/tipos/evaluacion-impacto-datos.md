# Evaluación de impacto en datos

Elegir `document.kind: "evaluacion-impacto-datos"` para evaluar, antes de construir o de cambiar un sistema, qué datos personales trata, qué riesgos corren las personas a quienes pertenecen y qué medidas los reducen. Sirve a cualquier proyecto con datos personales, no solo a uno de crédito ni de pagos. Empezar por `assets/ejemplo-evaluacion-impacto-datos.json`. Diagrama: no lleva. El flujo de los datos ya está dibujado en la descripción de arquitectura ([descripcion-arquitectura.md](descripcion-arquitectura.md)) y esta evaluación lo cita por su código; los datos que van a cada lugar caben en una tabla (ver «¿Necesita un diagrama?»).

**Contenido:** Decidir antes de redactar; Completar cada campo; Cómo se valoran los riesgos de las personas; Cómo se comprueba; Personalizar; Qué no inventar; Qué se elimina cuando algo no aplica; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

**Aviso: este documento no es asesoría legal.** Esta guía organiza información y valora riesgos. No afirma que un documento cumpla una ley local, no dice si la evaluación es obligatoria u opcional en un país y no sustituye a quien asesora a la entidad en materia legal. Todo campo normativo que no conste se escribe «Por confirmar con asesoría legal»: el marco normativo aplicable, la base de licitud, la autoridad de protección de datos, el delegado de protección de datos, la retención y las transferencias. Cada documento lleva este aviso, visible, en la información de referencia.

La estructura se orienta por los cuatro elementos que el apartado 7 del artículo 35 del Reglamento (UE) 2016/679 (RGPD) lista para una evaluación de impacto: descripción sistemática del tratamiento y de sus fines, necesidad y proporcionalidad, riesgos para los derechos y libertades de las personas, y medidas previstas. Esa orientación es todo lo que se toma: no se reproduce el texto del reglamento, no se declara conformidad con él y no se afirma de él nada más. El orden de los apartados es el del catálogo.

El PDF es compacto: título y contenido en la primera página, sin portada, de diez páginas en el ejemplo (tres en la variante breve). Tiene dos casillas de una sola marca: la conclusión del tamizaje y la decisión. El histórico de revisiones se imprime al final con `document.show_changes: true`. No hay bloque nuevo: los riesgos usan el bloque `risks`, cuyo esquema está en [risks.md](../contrato/risks.md), con otro vocabulario (ver «Cómo se valoran los riesgos de las personas»), y el resto son tablas y cuadrículas de campos. Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Variante breve.** Si el tamizaje concluye que la evaluación completa no es necesaria, el documento queda solo con los apartados 1, 2, 8 y 9. Ver «Qué se elimina cuando algo no aplica».

**Índices.** El ejemplo no los lleva: con diez páginas, `contents` alargaría la apertura sin cambiar la lectura. Conviene `document.indexes: ["contents"]` cuando la evaluación pasa de diez páginas, por muchos riesgos o por descripciones largas. `tables` cuenta la matriz y el resumen de riesgos, además de las tablas escritas. `figures` no se recomienda: el tipo no lleva figura.

## Decidir antes de redactar

1. **Qué se evalúa y quién responde.** Un tratamiento o un sistema, con su responsable y sus encargados escritos **por rol** (por ejemplo, la jefatura de operaciones de reservas; el proveedor de la pasarela). Una persona con nombre aparece solo como firmante. Decir qué hace cada parte (decide la finalidad, captura la tarjeta) basta; si esa parte es responsable o encargada en el sentido de una norma depende del contrato y del marco aplicable, y queda «Por confirmar con asesoría legal».
2. **Con qué base se decide.** La decisión de más peso es la marca de «Conclusión y decisión». La base, de mayor a menor peso: el resumen de riesgos abiertos por nivel; las medidas, con su estado y su responsable; los campos normativos que siguen «Por confirmar con asesoría legal». Son criterios de trabajo de esta guía, no criterios legales: la entidad puede sustituirlos por los suyos. Lo que no cambia es que la marca se sostiene en esos tres datos y que la decisión es una propuesta del documento: su aprobación consta en las firmas.
   - **Continúa sin medidas adicionales.** El tamizaje concluyó que no hace falta la evaluación completa, o todos los riesgos abiertos están en el nivel más bajo de la matriz y ningún campo normativo sigue por confirmar.
   - **Continúa con medidas.** Hay riesgos abiertos por encima del nivel más bajo, y cada uno tiene al menos una medida prevista con responsable. Ningún campo normativo que condicione el diseño sigue por confirmar.
   - **Consultar a asesoría legal o a la autoridad.** Un campo normativo que condiciona el diseño sigue «Por confirmar con asesoría legal», o un riesgo del nivel más alto no baja con medidas propias. Es la marca que corresponde cuando falta la base: el documento no presenta como decidido lo que solo asesoría legal puede confirmar.
   - **No continúa hasta resolver.** Hay un riesgo abierto del nivel más alto sin medida prevista, o una medida que lo reduce y nadie asignó.

   Si se cumplen dos reglas a la vez, se marca la que más detiene (de menos a más: puede continuar, continúa con medidas, consultar, no continúa) y el texto de debajo nombra la otra. Las etiquetas se reescriben para la entidad (ver «Personalizar»), siempre con exactamente una marcada.
3. **Cuándo se hace y con qué se encadena.** Antes de construir o de cambiar el tratamiento, después de la descripción de arquitectura cuando existe (para citar su figura del flujo) y antes de pasar a producción. Cita por código la factibilidad, el alcance, las decisiones de arquitectura, el registro de riesgos del proyecto y, si hay decisiones automatizadas, la ficha de modelo ([ficha-modelo.md](ficha-modelo.md)), que a su vez cita esta evaluación. Al evaluar la factibilidad se anota si el proyecto trata datos personales (ver [factibilidad.md](factibilidad.md)); la respuesta abre esta evaluación.
4. **Tamizaje y variante breve.** El tamizaje decide si se redacta la evaluación completa. Lo contestan quienes conocen el tratamiento, con lo que consta en los documentos del proyecto.
5. **Quién firma.** Elabora quien redacta, revisa el delegado de protección de datos si la entidad lo designó (si no consta, «Por confirmar») y aprueba quien responde por el tratamiento, por su función. Las fechas de firma son «Pendiente».
6. **El código.** Usar el prefijo y la numeración de la entidad, con el tipo `EID` de [codigos.md](../codigos.md) (`DEMO-EID-01` en el ejemplo). Es `document.code` y aparece en el pie.

## Completar cada campo

La conclusión va primero dentro de cada campo. Un dato personal real no se escribe en el documento: ni nombres, ni correos, ni teléfonos, ni identificadores de las personas titulares. Se describen las categorías de datos.

1. **Información de referencia.** Una frase de apertura con la decisión propuesta y lo que falta por confirmar, y el aviso de que el documento no es asesoría legal (una `note`). Después, una cuadrícula con el número de evaluación (el código del documento) y la fecha, y otra con el sistema o proyecto, el responsable del tratamiento (por rol), los encargados (por rol), el delegado de protección de datos («Por confirmar» si no consta), el marco normativo aplicable, la autoridad de protección de datos y los documentos relacionados por código. El marco y la autoridad son «Por confirmar con asesoría legal» mientras nadie los confirme.
2. **Tamizaje.** Una tabla con siete preguntas: ¿trata datos personales?, ¿datos sensibles o de menores?, ¿a gran escala?, ¿hay perfilamiento o decisiones automatizadas con efectos sobre las personas?, ¿datos de personas vulnerables?, ¿transfiere datos fuera del país?, ¿usa tecnología nueva sobre datos personales? Cada respuesta es «Sí», «No» o «Por confirmar», con lo que la sostiene. Una respuesta que ningún documento sostiene es «Por confirmar», no «No». Si lo confirmado cubre solo una parte (por ejemplo, el alojamiento pero no el acceso remoto del soporte), la respuesta sigue «Por confirmar» y la base dice qué parte se confirmó. La conclusión es una casilla de una sola marca: evaluación completa necesaria, no necesaria o por confirmar. Regla: la pregunta 1 en No hace innecesaria la evaluación; un Sí entre las preguntas 2 y 7 la hace necesaria; con la pregunta 1 en Sí y las demás en No, no es necesaria; en cualquier otro caso la conclusión es por confirmar y la evaluación completa se elabora igualmente. La regla es de esta guía y no dice si la evaluación es obligatoria en un país. La entidad puede añadir preguntas y entonces actualiza la regla en el propio documento.
3. **Descripción del tratamiento.** Una tabla de los datos (qué dato, quién lo da, dónde queda, quién accede) y una cuadrícula con la finalidad, los titulares, el volumen aproximado, los encargados y terceros, el flujo, la retención y supresión y las transferencias. El flujo cita la figura de la descripción de arquitectura por el código del documento, el título y el número de la figura de la versión citada; `{{ref:id}}` enlaza solo objetos de este documento. El volumen que ningún documento da es «Por estimar». La retención y las transferencias que no constan son «Por confirmar con asesoría legal».
4. **Necesidad y proporcionalidad.** Por qué esos datos y no menos, con el uso de cada uno; las alternativas menos intrusivas (minimización, anonimización, datos sintéticos o de prueba) y cuáles se adoptan; la base de licitud («Por confirmar con asesoría legal» si nadie la confirmó); cómo se informa a las personas titulares; cómo ejercen los derechos que reconozca el marco aplicable (por ejemplo, acceso, rectificación u oposición) y quién los atiende; y, si hay decisiones automatizadas, la intervención humana. Si no las hay, «No aplica».
5. **Análisis de riesgos del tratamiento.** El apartado agrupa los criterios y la matriz, las fichas de riesgos para las personas titulares (5.1) y el resumen de abiertos (5.2). Un solo bloque `risks`, con la escala, la matriz, una ficha por riesgo y el resumen de los abiertos. Antes del bloque, un párrafo con la conclusión (cuántos riesgos, cuántos abiertos, el nivel más alto) y la declaración de quién valoró la probabilidad y el impacto y que se leen sin contar las medidas previstas ni pendientes. Ver «Cómo se valoran los riesgos de las personas».
6. **Medidas y salvaguardas.** Una tabla con la medida (con su código M-nn), el riesgo que reduce (su `{{ref:id}}`), el responsable por rol y el estado: **Implementada** (ya funciona y consta cómo se comprobó), **Prevista** (decidida y asignada, aún sin construir) o **Pendiente** (falta decidirla, asignarla o confirmarla con asesoría legal). Cada riesgo abierto tiene al menos una medida, y cada medida cita un riesgo del documento. Antes de construir, ninguna medida técnica está implementada.
7. **Supervisión humana y decisiones automatizadas.** Si no hay decisiones automatizadas con efectos sobre las personas, un solo campo con «No aplica» y la razón, y se elimina el detalle. Si las hay: quién decide en cada caso (por rol), cómo se impugna una decisión y la ficha de modelo por su código.
8. **Conclusión y decisión.** Un párrafo con la propuesta, lo que se consulta si la marca es consultar y el nivel más alto abierto. Después, una cuadrícula con la decisión (una sola marca), el riesgo residual y la fecha de revisión. El **riesgo residual** es el nivel más alto de los riesgos abiertos del resumen; mientras las medidas no estén implementadas, «con las medidas aplicadas» es «Por estimar». La fecha de revisión es posterior a la del documento y anterior al paso a producción; la que nadie fijó es «Por confirmar». Si esta es la revisión previa al paso y la siguiente no tiene fecha, queda «Por confirmar» con la condición que la dispara (por ejemplo, la respuesta de asesoría legal). Ninguna marca de la decisión autoriza o impide por sí sola el paso a producción: lo decide quien responde del tratamiento, y el documento lo dice.
9. **Firmas de responsabilidad e histórico.** Una fila por función (elaboró, revisó, aprobó) con nombre, cargo, espacio de firma y fecha. El histórico sale de `changes`: un documento nuevo lleva una sola entrada, versión `0.1`, «Primera versión.»

## Cómo se valoran los riesgos de las personas

El tipo no crea un bloque: reutiliza `risks`, que el registro de riesgos del proyecto ([registro-riesgos.md](registro-riesgos.md)) ya usa para otro fin. Lo que cambia es lo que se escribe, no el bloque.

- **Qué es el riesgo.** Un riesgo de la evaluación es de las personas titulares de los datos, no del proyecto. La causa dice por qué puede ocurrir, el evento qué le pasa a los datos y la consecuencia qué sufre la persona. El **impacto** mide lo que sufre la persona, no lo que cuesta al proyecto. El responsable es un rol.
- **Qué se personaliza.** Los títulos (`matrix_title`, `register_title`, `summary_title`, `summary_table_title`), las etiquetas de la escala y las celdas de la matriz, `responses` y `states`. El ejemplo usa probabilidad Remota, Posible y Probable; impacto Leve, Importante y Grave; niveles Bajo, Medio, Alto y Muy alto; respuestas Reducir, Evitar, Aceptar y Consultar a asesoría legal; y estados Abierto, En reducción, Ocurrido y Cerrado. Al reemplazar `states`, hay que indicar `open_states`: el motor rechaza el documento si falta.
- **Qué no se personaliza.** Los rótulos fijos del bloque: «Probabilidad», «Impacto», «Causa», «Evento», «Consecuencia», «Respuesta», «Estado», «Responsable», «Acción», «Nivel», «Abiertos», «Cuáles», «Total de abiertos» y las frases que encabezan la matriz y las respuestas. Escribir el contenido de cada campo para que esos rótulos lean bien con otro vocabulario.
- **Identificadores propios.** Con otro prefijo (`RD-01` en el ejemplo) para no confundirlos con los `R-nn` del registro de riesgos del proyecto. Un riesgo que coincide con uno del registro cita su código y el del documento, como texto, en la causa o en la acción: `{{ref:id}}` enlaza solo ids de este documento.
- **Cómo se lee el nivel.** La probabilidad y el impacto de cada ficha se valoran sin contar las medidas previstas ni pendientes. Un riesgo está «Abierto» mientras ninguna de sus medidas esté prevista o implementada, pasa a «En reducción» cuando alguna lo está y a «Cerrado» cuando el dato deja de recogerse (por ejemplo, la tarjeta no pasa por los servidores propios) o cuando su medida está implementada y comprobada. Quien responde por la protección de datos decide la matriz y las valoraciones: mientras no lo confirme, el párrafo de apertura lo dice («valoración del equipo, por confirmar»). El motor aplica la celda escrita y no sabe de datos personales.

## Cómo se comprueba

- **Origen.** Cada dato y cada riesgo remiten a un documento citado o a un hecho observado. Un volumen o una cifra sin fuente es «Por estimar».
- **Tamizaje.** La conclusión marcada es la que da la regla con las respuestas de la tabla. Un «No» sin documento que lo sostenga es un «Por confirmar» mal escrito.
- **Riesgos y medidas.** Cada riesgo abierto tiene al menos una medida; cada medida cita un riesgo que existe; el estado de cada riesgo sigue el estado de sus medidas; el riesgo residual es el nivel más alto del resumen; un riesgo cerrado dice por qué.
- **Decisión.** La marca sigue la regla del apartado «Con qué base se decide» y el texto de debajo nombra lo que falta. Si un campo normativo sigue por confirmar, la marca no es «Continúa sin medidas adicionales».
- **Lenguaje.** Buscar «cumple», «conforme», «legal», «obligatorio» y «no requiere». Cada aparición está en el aviso o en un campo «Por confirmar con asesoría legal». Ningún apartado afirma que el tratamiento es lícito ni que la evaluación es obligatoria u opcional.
- **Fechas.** El documento es posterior a la descripción de arquitectura que cita y anterior a la construcción; la fecha de revisión es posterior a la del documento.
- **Coherencia.** El número de evaluación coincide con el código del documento; los roles, los códigos y los nombres de los firmantes coinciden con los de la cadena de documentos.

## Personalizar

- `brand.entity`, `brand.unit` (pie de página), `brand.accent` y `brand.logo` (PNG o JPEG con ruta relativa al JSON; sin logo se imprime el nombre de la entidad). `brand.fonts` solo con licencia verificada.
- `document.code` con el prefijo propio, `document.short_title` para la cabecera y `document.paper` (`A4` o `Letter`).
- Las etiquetas de la decisión y de la conclusión del tamizaje: se reescriben con las palabras de la entidad, siempre con exactamente una marcada. El motor exige al menos una elección de una sola marca; que estén las dos casillas lo comprueba quien redacta.
- La escala, la matriz, `responses` y `states` del bloque de riesgos, y las preguntas del tamizaje.
- Los rótulos de las partes: «titulares» por «personas afectadas» o «pacientes», «responsable del tratamiento» y «encargados» por los términos de la entidad.
- Responsable del tratamiento, encargados, delegado y firmantes.

## Qué no inventar

Marco normativo, autoridad, base de licitud, delegado, retención y transferencias que no consten. El volumen de personas o de registros. Una respuesta del tamizaje que ningún documento sostiene. Una medida implementada que nadie construyó ni comprobó. Aprobaciones, firmas y fechas de firma. Nombres de firmantes que no consten. Un dato personal real. Que el tratamiento sea lícito, que cumpla una norma o que la evaluación sea obligatoria u opcional.

Las palabras para lo que falta (Pendiente, Por confirmar, Por estimar, Propuesto), quién puede firmar, el estado del documento, las fechas y el historial de un documento nuevo están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Dato | Texto |
|---|---|
| Marco, autoridad, base de licitud, retención o transferencias que no constan | Por confirmar con asesoría legal |
| Delegado de protección de datos que nadie designó | Por confirmar |
| Volumen de personas o de registros sin fuente | Por estimar |
| Respuesta del tamizaje que ningún documento sostiene | Por confirmar |
| Medida sin decidir, sin responsable o a la espera de asesoría legal | Pendiente, con el responsable «Por confirmar» si nadie lo asignó |
| Nivel del riesgo con las medidas aplicadas, antes de aplicarlas | Por estimar |
| Fecha de revisión que nadie fijó | Por confirmar |
| Apartado que no aplica al caso (decisiones automatizadas) | No aplica |

## Qué se elimina cuando algo no aplica

- **Variante breve.** Con la conclusión del tamizaje «Evaluación completa no necesaria», se eliminan los apartados 3 a 7 (descripción, necesidad, riesgos, medidas y supervisión) y quedan el 1, el 2, el 8 y el 9, que el motor renumera (el documento pasa a cuatro apartados). Se reescriben las frases que hablaban de la evaluación completa: la apertura del 1, que en el documento completo propone la decisión, y la del 2, que concluye el tamizaje. En el 2 se conservan la tabla y su regla. En el 8, la decisión es «Continúa sin medidas adicionales», el riesgo residual dice «No aplica» y el párrafo de apertura no cita ningún apartado eliminado: el motor rechaza una referencia `{{ref:id}}` a un id que ya no existe.
- **Sin decisiones automatizadas.** El apartado 7 se queda con un campo que dice «No aplica» y la razón. Se quitan el «quién decide», el «cómo se impugna» y la ficha de modelo, y el apartado 4 remite a «No aplica» en «Intervención humana». Si las hay, el apartado 7 lleva esos tres campos y el 4 describe la intervención humana.
- **Otros campos sin dato.** Un campo que no aplica se escribe «No aplica» y se conserva; no se elimina un campo de la información de referencia ni del tratamiento.

## ¿Necesita un diagrama?

No. La pregunta de la evaluación es qué datos personales hay, adónde van y qué riesgo corren las personas. Lo primero cabe en la tabla de datos y en la cuadrícula del tratamiento; lo último lo responde la matriz impresa desde los mismos datos que usa el cálculo. El flujo de los datos entre componentes ya está en la descripción de arquitectura, y una figura nueva repetiría esa vista. Si no existe una descripción de arquitectura y los datos personales pasan por varios sistemas, se puede añadir una figura de flujo con [diagramas.md](../diagramas.md) y se dice aquí.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** Abrir cada apartado con la conclusión: en la referencia, la decisión propuesta; en el tamizaje, su conclusión y por qué; en los riesgos, cuántos hay y el nivel más alto; en la conclusión, la marca y lo que falta. Se conserva el orden de los apartados.
- **`unicorntext`.** Revisar la apertura, las causas, las alternativas y la conclusión: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las frases de trámite. Conservar las etiquetas de la escala, los códigos, las palabras «Por confirmar con asesoría legal», «Por estimar» y «Pendiente», y las fechas.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py evaluacion.json --output evaluacion.pdf
python3 <skill>/scripts/check_report.py evaluacion.pdf
pdftoppm -r 80 -png evaluacion.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('evaluacion.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que cada casilla tenga una sola cruz (la conclusión del tamizaje y la decisión), que ninguna tabla ni ficha de riesgo quede partida, que el nivel de cada ficha sea la celda de la matriz, que el resumen no cuente un riesgo cerrado y que las firmas queden enteras, con el histórico, en el cierre. Entregar el PDF, su manifiesto `.manifest.json` (el comprobador lo exige junto al PDF) y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. Una tabla o una ficha que cabe en una página no se parte. Los defectos habituales son:

- **Hueco al pie de una página**, porque una ficha de riesgo o una tabla entera pasó a la siguiente. Se corrige cuando una frase de más lo causa, acortando el texto de la ficha o de la fila; un hueco de hasta un tercio de página es un compromiso del diseño y se acepta.
- **Una página final con solo el histórico de revisiones.** El motor agrupa las firmas, la remisión y el histórico cuando caben juntos en una página, así que el caso ya no debería darse. Si aparece (el cierre no cabe en una página o hay un `new_page` escrito antes del histórico), se corrige acortando una sección anterior. Poner `new_page: true` en una sección suele empeorarlo.
- **Un apartado cuyo párrafo de apertura queda en una página y su tabla en la siguiente.** El motor mantiene la tabla entera; se acepta si el hueco queda por debajo de un tercio.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

En la muestra medida (A4):

- La página 1 reúne la información de referencia con el aviso y abre el tamizaje. La tabla de preguntas pasa entera a la 2 y deja un hueco de cerca de un quinto.
- La página 2 cierra con la apertura de la descripción; su tabla de datos abre la 3. La página 4 abre con la cuadrícula de necesidad y proporcionalidad y cierra con la matriz de niveles.
- Las páginas 5 y 6 llevan las seis fichas de riesgo, tres por página. Cada ficha se mantiene entera, de modo que quedan huecos de menos de un cuarto de página al pie.
- La página 7 reúne el resumen por nivel y la tabla de medidas, entera.
- La página 8 reúne la supervisión, la conclusión, las firmas y el histórico, con poco margen: una frase más en esos apartados lleva el histórico a una novena página solo.
- La variante breve tiene tres páginas: la información de referencia con el inicio del tamizaje, la tabla del tamizaje con la decisión, y las firmas con el histórico. Con papel Carta, el ejemplo completo ocupa diez.
