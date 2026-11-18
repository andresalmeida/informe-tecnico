# Propuesta de servicio

Elegir `document.kind: "propuesta-servicio"` para la propuesta técnico-económica que recibe quien contrata: qué se propone, en cuánto tiempo, a qué costo y qué se necesita de su parte. Empezar por `assets/ejemplo-propuesta-servicio.json`. Diagrama: no lleva. La solución de un módulo cabe en un párrafo y en la tabla de entregables; la arquitectura y el perímetro viven en los documentos internos.

**Contenido:** Decidir antes de redactar; Qué se queda en la factibilidad; Voz; Completar cada campo; Cómo se comprueba una propuesta; Personalizar; Qué no inventar; Qué se elimina cuando algo no aplica; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

Va después del informe de factibilidad ([factibilidad.md](factibilidad.md)), que es interno, y antes del alcance ([alcance-proyecto.md](alcance-proyecto.md)). Cita el registro de riesgos ([registro-riesgos.md](registro-riesgos.md)) por su código cuando un riesgo cambia una fecha o una decisión de quien contrata. El orden de los apartados es el del catálogo.

El PDF es compacto: título y contenido en la primera página, sin portada, de cinco páginas en el ejemplo. No tiene casillas. El histórico de revisiones se imprime al final con `document.show_changes: true`. El esquema del bloque `quote` está en [quote.md](../contrato/quote.md). Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Índices.** El ejemplo no los lleva: con cinco páginas, `contents` alargaría la apertura sin cambiar la lectura. Conviene `document.indexes: ["contents"]` cuando la propuesta pasa de siete páginas. `tables` y `figures` no se recomiendan: las tablas son los entregables, el cronograma, los aportes, la cotización y la aceptación, y el tipo no lleva figura.

## Decidir antes de redactar

1. **Qué se propone y para quién.** Quien lee es la parte solicitante. El texto dice qué recibe, en qué plazo, por cuánto y qué se le pide. La evaluación interna no se le reenvía.
2. **Con qué base se propone.** Este tipo no tiene casillas: su regla en el motor es la de un formulario sin elecciones (`form: True`, sin `choice`). La decisión de más peso es el conjunto de lo que se ofrece, el plazo, la inversión total y lo que se pide a la parte solicitante. La sostiene la factibilidad, en lo que puede salir de la entidad. Si la factibilidad quedó en «Pendiente de evidencia», la propuesta puede emitirse solo como borrador condicionado: cada prerrequisito sin evidencia consta como condición en «Lo que necesitamos» y en los supuestos, la propuesta no presenta la viabilidad como confirmada y la autorización de quien compromete a la entidad sigue «Pendiente». Lo que la factibilidad sostiene es el plazo de calendario, los entregables, las exclusiones y los criterios con los que la parte solicitante aceptará el resultado. Lo que la factibilidad no resolvió queda «Por confirmar» o «Por estimar».
3. **Quiénes aceptan.** Las dos partes firman. La fecha de aceptación de un documento nuevo es «Pendiente». La fecha hasta la que vale la propuesta es otra: la pone la entidad y tiene que ser posterior a `document.date`.
4. **El código.** Usar el prefijo y la numeración de la entidad (`DEMO-PRO-01` en el ejemplo). Es `document.code` y aparece en el pie.

## Qué se queda en la factibilidad

La factibilidad es interna. La propuesta no la copia. Se queda allí, y no se traslada:

- El esfuerzo en días-persona y el desglose por rol.
- Los recursos del equipo y los perfiles externos con su dedicación.
- Los márgenes y cualquier cifra que sirva para calcular el precio por dentro.
- La viabilidad marcada y el detalle de la arquitectura (componentes, protocolos, nombres internos de servicios).
- Los riesgos que no cambian una fecha ni una decisión de quien contrata. Esos siguen en el registro.

La propuesta da el plazo en tiempo de calendario, los entregables, la inversión ya calculada y lo que se pide a la parte solicitante.

## Voz

Se escribe para quien contrata. Sin jerga interna y sin códigos que esa persona no tenga: el de su requerimiento sí, el del registro de riesgos cuando se cita un riesgo que le afecta, y el de la propuesta. Un código de trabajo interno, si hace falta identificar la evaluación, va una sola vez en la referencia y no se explica en el cuerpo.

## Completar cada campo

La conclusión va primero dentro de cada campo.

1. **Resumen.** Pocas oraciones: qué se propone, el plazo, la inversión total y qué se pide a la parte solicitante. El total es el que imprime el bloque `quote`, con la misma moneda y los mismos separadores. Si la inversión está por estimar, el resumen lo dice y no inventa una cifra.
2. **Necesidad y objetivo.** Qué pidió la parte solicitante, con la fecha y el código del requerimiento, y el objetivo de esta propuesta en una frase.
3. **Solución propuesta.** Qué ocurre, en el lenguaje de quien contrata, desde que pide el servicio hasta que lo recibe. Si más adelante se añade una figura, se llama desde aquí con `{{ref:id}}`.
4. **Alcance y exclusiones.** Una frase con lo que entra y lo que queda fuera, y una tabla de entregables con lo que la parte solicitante recibe. Los criterios con los que aceptará el resultado van después, medibles, tomados de la factibilidad en lenguaje llano.
5. **Cronograma.** Fases con duración en tiempo de calendario y, en cada fase que dependa de la parte solicitante, el hito que le toca. El total de las fases que no se solapan es el plazo del resumen. Aquí no hay días-persona.
6. **Lo que necesitamos de la parte solicitante.** Accesos, personas, decisiones y fechas. Cada fila dice qué se pide, para cuándo y el estado. Lo que nadie ha confirmado está en «Por confirmar».
7. **Supuestos y riesgos relevantes.** Solo los que cambian una fecha o una decisión de quien contrata. El apartado cita el registro de riesgos por su código. Un riesgo interno que no le pide nada no se copia.
8. **Inversión.** Un bloque `quote`. Quien redacta escribe el concepto, la cantidad y el precio unitario de cada línea, la tasa (`tax_rate`, una fracción entre 0 y 1, o `null` si la entidad aún no la define) y la moneda. El motor calcula el importe de cada línea, el subtotal, el impuesto y el total. No se escribe ninguno de esos resultados: si aparecen `subtotal`, `tax`, `total`, `amount` o `importe`, el motor rechaza el documento. La tasa es un dato de la entidad. La skill no afirma una norma tributaria: el nombre va en `tax_name` con las palabras de la entidad. Los separadores se configuran con `decimal` (`","` o `"."`, por omisión la coma) y `thousands` (`"."`, `","`, un espacio o vacío, por omisión el punto). El motor no consulta el idioma del sistema. El párrafo anterior a la tabla dice el total con las mismas cifras que la tabla, y declara que son de demostración cuando el ejemplo lo es. Con `tax_rate: null`, esa cifra es el total antes de impuestos y así se rotula.
9. **Condiciones.** Validez de la propuesta, forma de pago y garantía. Las escribe la entidad. Esta guía no las redacta como consejo legal ni como cláusula modelo. Lo que no consta es «Por confirmar». En un ejemplo, el texto de pago y de garantía se rotula como demostración.
10. **Aceptación.** Tabla de las dos partes, con nombre, cargo, espacio de firma y fecha de aceptación. Esa fecha es «Pendiente» mientras no hayan firmado. En el mismo apartado, o en las condiciones, queda la fecha hasta la que vale la propuesta.

## Cómo se comprueba una propuesta

- **Lo que no viaja.** El PDF no contiene días-persona, márgenes ni el desglose de esfuerzo de la factibilidad.
- **Cifras.** El total del resumen es el total de la cotización. Cada importe es cantidad por precio unitario, el subtotal es la suma, el impuesto es el subtotal por la tasa y el total es subtotal más impuesto. Una cifra distinta es un texto escrito a mano: se borra y se deja el bloque `quote`.
- **Plazo.** La suma de las fases que no se solapan es el plazo del resumen, en las mismas unidades.
- **Precios.** Cada precio sale de una tarifa o una estimación de la entidad. Si no consta, la línea no se inventa: se omite y el párrafo dice «Por estimar».
- **Fechas.** La factibilidad, luego esta propuesta (`document.date`), luego el alcance. La validez es posterior a la fecha del documento. La aceptación no tiene fecha mientras siga en «Pendiente».
- **Riesgos.** Cada riesgo del apartado afecta a quien contrata y el código del registro es el del registro vivo.
- **Coherencia.** El código del documento coincide con el de la propuesta, los nombres y cargos con los de los documentos de la cadena, y las exclusiones con las de la factibilidad.

## Personalizar

- `brand.entity`, `brand.unit`, `brand.accent` y `brand.logo` (ruta relativa al JSON; sin logo se imprime el nombre). `brand.fonts` solo con licencia verificada.
- `document.code`, `document.short_title` y `document.paper` (`A4` o `Letter`).
- Rótulos de las partes. «Parte solicitante» y «equipo ejecutor» se reemplazan por los de la entidad.
- Moneda, `tax_name`, `tax_rate`, `decimal` y `thousands`.
- Condiciones de pago y de garantía, con el texto de la entidad. Firmantes.

## Qué no inventar

Precios, tasas y monedas que la entidad no dio. El ejemplo trae cifras de demostración y lo dice en el apartado de inversión: no se reutilizan como tarifa. Condiciones de pago, garantía o validez que la entidad no haya definido: van en «Por confirmar», y esta guía no las propone como cláusula. Firmas y fechas de aceptación. Un margen o un día-persona para «explicar» el precio. Un riesgo que el registro no tenga. La aceptación de la parte solicitante.

Las palabras para lo que falta (Pendiente, Por confirmar, Por estimar, Propuesto), quién puede firmar, el estado del documento, las fechas y el historial de un documento nuevo están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Dato | Texto |
|---|---|
| Fecha de aceptación aún no ocurrida | Pendiente |
| Precio o plazo sin estimar | Por estimar, y la línea de cotización no se inventa |
| Decisión, acceso o persona que la parte solicitante no ha confirmado | Por confirmar |
| Forma de pago o garantía que la entidad no ha definido | Por confirmar |
| Tasa que la entidad no ha indicado | Usar `tax_rate: null` en `quote`: impuesto «Por confirmar» y «Total antes de impuestos». No usar tasa cero para representar un impuesto desconocido; la clave no se omite. |

## Qué se elimina cuando algo no aplica

- **Sin precio todavía.** Se quita el bloque `quote` y el total del resumen. El apartado de inversión queda en un párrafo: «Por estimar». Los apartados siguientes se renumeran solos.
- **Sin un concepto.** Se omite esa línea. Si el concepto existe y el precio no, el párrafo lo nombra como «Por estimar» y la tabla no lleva una fila con cero para rellenar el hueco. El cero es un concepto sin cargo, y se usa solo cuando la entidad dice que no se cobra.

## ¿Necesita un diagrama?

No. Quien contrata tiene que ver qué recibe, en qué plazo y por cuánto. Eso lo dan el párrafo de la solución, la tabla de entregables y la cotización. La arquitectura del módulo está en la factibilidad y el perímetro en el alcance, que son otros documentos. Una figura de esta propuesta repetiría una de esas lecturas. Si una propuesta futura necesita un esquema de otra cosa, se añade con [diagramas.md](../diagramas.md) y se dice aquí.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** El resumen abre con lo que se propone, el plazo, el total y lo que se pide. Cada apartado siguiente sostiene una parte de esa frase. Se conserva el orden de los apartados.
- **`unicorntext`.** Revisar el resumen, la solución y las condiciones: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las frases de trámite. Conservar plazos, precios, exclusiones, nombres y el rótulo de demostración de las cifras.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py propuesta.json --output propuesta.pdf
python3 <skill>/scripts/check_report.py propuesta.pdf
pdftoppm -r 80 -png propuesta.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('propuesta.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que la cotización esté entera, que el total del resumen coincida con el de la tabla, que la tabla de aceptación quede entera y que el histórico no ocupe una página solo. Entregar el PDF, su manifiesto `.manifest.json` y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. Una tabla que cabe en una página no se parte, salvo que moverla dejara más del 35 % de la página en blanco: entonces se parte entre filas, con su título y encabezado repetidos y al menos tres filas en cada página. Los defectos habituales son:

- **Hueco al pie de una página**, porque una tabla, una ficha o una figura entera pasó a la siguiente. No se corrige recortando texto, juntando filas ni quitando datos: el contenido manda y el número de páginas no es una meta. El motor parte una tabla entre filas cuando moverla dejaría más del 35 % de la página en blanco; una ficha o una figura se queda entera. Un hueco así no se arregla: solo se reporta si estorba la lectura.
- **El título de un apartado al pie y su tabla en la página siguiente.** Se acorta el apartado anterior o se mueve la frase que presenta la tabla para que quede debajo de ella: el motor mantiene la tabla con el párrafo que la sigue.
- **Una página final con solo el histórico de revisiones.** Es posible: si las firmas, la remisión y el histórico no caben juntos y moverlos dejaría más del 35 % de la página en blanco, el histórico va solo en la última página. No se corrige acortando secciones anteriores ni con `new_page`.

En la muestra medida:

- La página 1 cierra con el apartado de alcance y deja un hueco, porque la tabla de entregables no cabe debajo. El título no queda solo: lleva su párrafo.
- La página 2 cierra con el título del apartado 6 y la frase de los aportes, y deja un hueco, porque esa tabla abre la página 3. Meter la tabla en la 2 empujaría la cotización y separaría el total de sus líneas.
- La cotización queda entera en la página 3, con subtotal, impuesto y total.
- La página 4 reúne condiciones, aceptación e histórico. La fecha de aceptación sigue en Pendiente.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.
