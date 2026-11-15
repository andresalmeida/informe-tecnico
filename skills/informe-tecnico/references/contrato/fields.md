### Bloque `fields`

Cuadrícula de etiqueta y valor para fichas de referencia, decisiones y totales. Cada elemento de `items` es de uno de tres tipos y admite únicamente estas claves:

- Valor: `label` y `value`, ambos textos no vacíos. Admite `{{ref:id}}` y saltos de línea.
- Elección: `label`, `options` (2 a 6 textos distintos y no vacíos) y `selected`, que debe ser exactamente una de las `options`. Cada opción se dibuja como una casilla vectorial, con una cruz y negrita en la elegida. Una elección de una sola marca no existe sin marca ni con dos: el motor rechaza `selected` ausente, nulo, fuera de `options` o con más de un valor (si es una lista, el mensaje remite a `multiple`). `value` y `options` no se combinan en un elemento. Una elección también cabe en una cuadrícula de dos columnas: sus casillas se apilan en la celda de valor.
- Elección múltiple: lo mismo que la elección, más `"multiple": true`, y `selected` es una lista con cero o más de las `options`, sin repetir. Cada marcada se dibuja con la misma casilla, con su cruz y su negrita; las demás quedan vacías. Sirve para una lista de comprobación, como los materiales entregados. Una lista vacía (`[]`) declara que no se marcó ninguna y es válida; `selected` ausente, nulo, un texto, una opción que no figura en `options` o una opción repetida se rechazan con un mensaje que nombra el campo. `multiple` solo acompaña a `options` y debe ser booleano; `"multiple": false` equivale a omitirlo y conserva la regla de una sola marca. Una elección múltiple no cuenta como la elección marcada que exige un tipo de formulario (la viabilidad, el tipo o la modalidad): esa sigue siendo de una sola marca.

Con `columns: 1` cada elemento ocupa una fila (etiqueta al 24 % del ancho). Con `columns: 2` se colocan dos pares etiqueta y valor por fila; un último elemento impar ocupa el ancho restante. Una cuadrícula no se parte entre páginas si cabe en una; en los tipos de formulario, si el bloque siguiente es una tabla, una lista o un párrafo, la mantiene junto a él. El motor rechaza claves desconocidas en el bloque o en un elemento, `columns` distinto de 1 o 2, listas vacías o de más de 16 elementos y textos vacíos.

```json
{"type": "fields", "columns": 2, "items": [
  {"label": "N.º de informe", "value": "DEMO-FAC-01"},
  {"label": "Fecha de elaboración", "value": "09/11/2026"}
]}
{"type": "fields", "items": [
  {"label": "Viabilidad técnica",
   "options": ["Factible", "Factible con observaciones", "No factible"],
   "selected": "Factible con observaciones"},
  {"label": "Materiales entregados",
   "options": ["Manual", "Ficha técnica", "Presentación"],
   "multiple": true,
   "selected": ["Manual", "Presentación"]}
]}
```

La marca es gráfica: el texto extraído del PDF no distingue la opción elegida, que solo se reconoce por la cruz y la negrita. No usar una elección para registrar una aprobación que no conste. Para el contenido que debe llevar cada campo, ver [factibilidad.md](../tipos/factibilidad.md), [registro-requerimientos.md](../tipos/registro-requerimientos.md), [alcance-proyecto.md](../tipos/alcance-proyecto.md), [acta-capacitacion.md](../tipos/acta-capacitacion.md), [plan-pruebas.md](../tipos/plan-pruebas.md), [registro-riesgos.md](../tipos/registro-riesgos.md), [propuesta-servicio.md](../tipos/propuesta-servicio.md), [decision-arquitectura.md](../tipos/decision-arquitectura.md), [descripcion-arquitectura.md](../tipos/descripcion-arquitectura.md), [especificacion-requisitos.md](../tipos/especificacion-requisitos.md), [ficha-modelo.md](../tipos/ficha-modelo.md), [evaluacion-impacto-datos.md](../tipos/evaluacion-impacto-datos.md), [informe-cierre.md](../tipos/informe-cierre.md), [acta-baja.md](../tipos/acta-baja.md), [ficha-proceso.md](../tipos/ficha-proceso.md), [solicitud-cambio.md](../tipos/solicitud-cambio.md), [plan-proyecto.md](../tipos/plan-proyecto.md), [traspaso-operacion.md](../tipos/traspaso-operacion.md) y [notas-version.md](../tipos/notas-version.md).
