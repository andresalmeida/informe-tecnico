# Traspaso a operación

Elegir `document.kind: "traspaso-operacion"` para el paso a producción: quién opera lo entregado, cómo se comprueba y cómo se vuelve atrás si falla. Empezar por `assets/ejemplo-traspaso-operacion.json`. Diagrama: no lleva. La ventana y la reversa caben en el texto.

**Contenido:** Decidir antes de redactar; Completar cada campo; Cómo se comprueba un traspaso; Personalizar; Qué no inventar; Texto de lo pendiente; Bloques opcionales; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

No hay bloque nuevo: las tablas y las fichas de campos bastan. No se reproduce el texto de un formulario ajeno. El orden de los apartados es el del catálogo.

El PDF es compacto: título y contenido en la primera página, sin portada, de cuatro páginas en el ejemplo. El histórico de revisiones se imprime al final con `document.show_changes: true`. No exige casilla. Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Índices.** El ejemplo no los lleva: con cuatro páginas, `contents` alargaría la apertura sin cambiar la lectura. Conviene `document.indexes: ["contents"]` cuando el traspaso pasa de siete páginas. `tables` lista las tablas que el documento traiga. `figures` no se recomienda.

## Decidir antes de redactar

1. **Qué se traspasa y en qué ventana.** Sistema, versión desplegada, fecha, ventana y entorno. La ventana del ejemplo es la semana del 04/01/2027 al 10/01/2027, la de DEMO-ALC-01 y de R-08. La fecha del documento es la de DEMO-ENT-01, el 08/01/2027. En otro proyecto el traspaso puede escribirse antes del paso a producción, con todas las comprobaciones en Pendiente: su fecha es entonces anterior a la ventana y a la entrega. El resultado de la verificación posterior se registra en una versión nueva del mismo traspaso, no en un documento aparte.
2. **Qué ya está hecho y qué no.** Una comprobación sin evidencia queda en Pendiente. No se escribe un resultado de una prueba que DEMO-ATP-01 todavía no ejecutó. R-05 sigue pendiente.
3. **Dónde viven los secretos.** El documento dice cómo se entregan los accesos y dónde se guardan. No se escriben claves, tokens ni secretos. Si la herramienta del depósito no consta, queda Por confirmar.
4. **Quién firma.** Quien entrega y quien recibe, con los nombres de la cadena. La fecha de firma es Pendiente mientras la conformidad de la entrega no conste.

## Completar cada campo

La conclusión va primero dentro de cada campo.

1. **Información de referencia.** Sistema, versión, fecha, ventana, entorno y documentos por código. La versión de plataforma que la arquitectura deja abierta sigue Por confirmar.
2. **Qué pasa a operación.** Componentes y quién responde de cada uno después del paso. Lo que queda fuera del módulo, como la pasarela, se nombra como fuera.
3. **Quién opera y quién da soporte.** Roles, horario, vía de contacto y límites. El horario que no consta es Por confirmar. El soporte no incluye lo que el alcance dejó fuera.
4. **Verificación posterior.** Comprobación, método y resultado. El resultado de partida es Pendiente.
5. **Plan de reversa.** Condición que lo dispara, pasos, tiempo máximo y quién decide. El tiempo que nadie fijó es Por confirmar.
6. **Monitoreo y alertas.** Qué se vigila. El umbral que no consta es Por confirmar. No se inventa una cifra.
7. **Accesos.** Cómo se entregan y dónde se guardan, sin copiar el secreto.
8. **Pendientes conocidos y soporte posterior.** Los mismos pendientes que ya trae la entrega, más los riesgos abiertos que frenan el paso. La fecha de fin del soporte, si no consta, es Por confirmar.
9. **Firmas.** Entrega y recepción. Fechas en Pendiente.

Los códigos siguen [codigos.md](../codigos.md). Este tipo usa `TRA`.

## Cómo se comprueba un traspaso

- **Ventana.** La ventana cae en la semana escrita en el alcance y en el plan. La fecha del documento coincide con la entrega cuando el traspaso se escribe al entregar; si se escribió antes del paso, es anterior a la ventana.
- **Resultados.** Cada fila de comprobación que no tiene evidencia dice Pendiente. Los casos citados existen en el plan de pruebas y, si allí no están ejecutados, aquí tampoco.
- **Riesgos.** R-05 y R-08 se citan con el estado del registro.
- **Secretos.** El PDF no contiene una clave, un token ni un secreto. El lugar donde se guardan está nombrado o en Por confirmar.
- **Pendientes.** Coinciden con los de la entrega: casos sin ejecutar, constancia de capacitación y versiones por confirmar.

## Personalizar

Se cambian `brand.entity`, `brand.unit`, `brand.accent` y, si hace falta, `brand.logo`. El código sigue el prefijo de la entidad. `paper` admite `A4` y `Letter`. El horario, la vía y el depósito de secretos son los de la entidad.

## Qué no inventar

- Un resultado de comprobación, una firma o una fecha de conformidad que no conste.
- Una clave, un token, una contraseña o un secreto, ni un ejemplo disfrazado de ellos.
- Un umbral de alerta numérico que la operación no fijó.
- Una versión de plataforma distinta de la que los documentos anteriores dejan en Por confirmar.

## Texto de lo pendiente

Pendiente, Por confirmar y Por estimar están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Situación | Qué escribir |
|---|---|
| Comprobación sin evidencia | Pendiente, en el resultado |
| Horario, vía, umbral o fin del soporte sin acordar | Por confirmar |
| Secreto | No se escribe. Se nombra el depósito, o Por confirmar si no consta |
| Firma | Pendiente |

## Bloques opcionales

- **Sin tabla de comprobaciones.** Si todavía no hay una lista de comprobaciones, se quita la tabla y el párrafo dice que el resultado está pendiente. No se rellena con filas vacías de resultado.
- **Sin índice.** El ejemplo no lleva `document.indexes`.

## ¿Necesita un diagrama?

No. Quién opera, qué se comprueba y cómo se vuelve atrás caben en las tablas y en la lista de la reversa. La arquitectura del sistema ya está dibujada en la factibilidad y en el alcance.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** La apertura dice la ventana, la entrega y que las comprobaciones siguen pendientes. El resto sostiene esa frase.
- **`unicorntext`.** Revisar los límites del soporte y los accesos: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las frases de trámite. Conservar fechas, códigos y las palabras Pendiente y Por confirmar.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py traspaso.json --output traspaso.pdf
python3 <skill>/scripts/check_report.py traspaso.pdf
pdftoppm -r 80 -png traspaso.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('traspaso.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que cada resultado siga en Pendiente, que no aparezca un secreto y que el histórico comparta página con las firmas. Entregar el PDF, su manifiesto `.manifest.json` y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. Una tabla que cabe en una página no se parte, salvo que moverla dejara más del 40 % de la página en blanco: entonces se parte entre filas, con su título y encabezado repetidos y al menos tres filas en cada página.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

Los saltos medidos de la muestra:

- La página 2 reúne el soporte, la verificación y la reversa. Las cuatro comprobaciones quedan en Pendiente y la tabla no se parte.
- La página 3 cierra con el soporte posterior. El hueco queda por debajo de un tercio.
- La página 4 reúne firmas e histórico. Debajo queda espacio libre: es el final del documento. El espacio de firma queda cerca del nombre.
