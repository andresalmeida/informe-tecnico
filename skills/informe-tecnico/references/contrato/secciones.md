## Secciones y bloques

`document.kind` admite `informe` (predeterminado), `acta-entrega`, `acta-reunion`, `informe-factibilidad`, `registro-requerimientos`, `alcance-proyecto`, `acta-capacitacion`, `plan-pruebas`, `registro-riesgos`, `propuesta-servicio`, `decision-arquitectura`, `descripcion-arquitectura`, `especificacion-requisitos`, `ficha-modelo`, `evaluacion-impacto-datos`, `informe-cierre`, `acta-baja`, `ficha-proceso`, `solicitud-cambio`, `plan-proyecto`, `traspaso-operacion` y `notas-version`. Los veintiún tipos compactos comienzan con el título y el contenido en la primera página. Usan cabecera, pie, marcadores, referencias y tablas del mismo motor. El historial permanece en `changes` (se imprime solo con `show_changes`) y los índices impresos son del `informe`; los tipos de formulario los admiten como opción (`document.indexes`, abajo). La elección de `format` es independiente. Para ejemplos y pautas de contenido, consultar [acta-entrega.md](../tipos/acta-entrega.md), [acta-reunion.md](../tipos/acta-reunion.md), [factibilidad.md](../tipos/factibilidad.md), [registro-requerimientos.md](../tipos/registro-requerimientos.md), [alcance-proyecto.md](../tipos/alcance-proyecto.md), [acta-capacitacion.md](../tipos/acta-capacitacion.md), [plan-pruebas.md](../tipos/plan-pruebas.md), [registro-riesgos.md](../tipos/registro-riesgos.md), [propuesta-servicio.md](../tipos/propuesta-servicio.md), [decision-arquitectura.md](../tipos/decision-arquitectura.md), [descripcion-arquitectura.md](../tipos/descripcion-arquitectura.md), [especificacion-requisitos.md](../tipos/especificacion-requisitos.md), [ficha-modelo.md](../tipos/ficha-modelo.md), [evaluacion-impacto-datos.md](../tipos/evaluacion-impacto-datos.md), [informe-cierre.md](../tipos/informe-cierre.md), [acta-baja.md](../tipos/acta-baja.md), [ficha-proceso.md](../tipos/ficha-proceso.md), [solicitud-cambio.md](../tipos/solicitud-cambio.md), [plan-proyecto.md](../tipos/plan-proyecto.md), [traspaso-operacion.md](../tipos/traspaso-operacion.md) y [notas-version.md](../tipos/notas-version.md).

`acta-entrega`, `acta-reunion`, `informe-factibilidad`, `registro-requerimientos`, `alcance-proyecto`, `acta-capacitacion`, `plan-pruebas`, `registro-riesgos`, `propuesta-servicio`, `decision-arquitectura`, `descripcion-arquitectura`, `especificacion-requisitos`, `ficha-modelo`, `evaluacion-impacto-datos`, `informe-cierre`, `acta-baja`, `ficha-proceso`, `solicitud-cambio`, `plan-proyecto`, `traspaso-operacion` y `notas-version` añaden un diseño de formulario: filas de tabla más densas, tablas y cuadrículas de campos que se mantienen enteras cuando caben en una página, y listas con sangría francesa que no dejan un solo elemento a un lado del salto. Una tabla o una cuadrícula se mantiene con el párrafo o la lista que la sigue (una leyenda, una nota), de modo que no queden en páginas distintas. `informe-factibilidad`, `registro-requerimientos`, `acta-capacitacion`, `decision-arquitectura`, `ficha-modelo`, `evaluacion-impacto-datos` y `solicitud-cambio` exigen al menos una elección marcada de una sola marca en la fuente (un elemento `fields` con `options` y `selected` de un solo valor, no una elección múltiple) y el motor rechaza la fuente que no la tiene, con un mensaje que dice qué añadir. En el informe de factibilidad es la viabilidad; en el registro, el tipo de requerimiento o la prioridad, para que no se registre un requerimiento sin clasificar; en el acta de capacitación, la modalidad (presencial o virtual); en el ADR, el estado; en la ficha de modelo, el estado del modelo; en la evaluación de impacto en datos, la decisión (la conclusión del tamizaje también es una casilla de una sola marca y la regla se cumple con cualquiera de las dos, de modo que comprobar que están las dos corresponde a quien redacta); en la solicitud de cambio, la decisión. La relación Sustituida por del ADR se comprueba en el contenido, sin una validación específica del motor. Los materiales entregados del acta son una elección múltiple y pueden quedar sin ninguna marca. El alcance del proyecto no tiene elecciones y no exige ninguna: su decisión de más peso, qué entra y qué queda fuera, se escribe en el texto y la sostiene la guía. El plan de pruebas tampoco exige una elección global: cada `testcase` ejecutado exige una marca y cada caso sin ejecutar queda sin marca. El registro de riesgos tampoco exige elección: el nivel de cada riesgo lo calcula el bloque `risks` y la guía dice quién decide la matriz. La propuesta de servicio tampoco: lo que se ofrece, el plazo y la inversión se escriben, y el total lo calcula el bloque `quote`. La descripción de arquitectura no exige elección global: su lista de decisiones se escribe y cita códigos existentes. La especificación de requisitos tampoco: los requisitos se escriben y la matriz de trazabilidad la calcula el bloque `requirements`. El informe de cierre, el acta de baja y la ficha de proceso no exigen elección global; sus decisiones y evidencias se escriben con bloques existentes. El plan de proyecto tampoco: la EDT se escribe y los totales los calcula el bloque `wbs`. El traspaso a operación y las notas de versión tampoco exigen elección: las comprobaciones y el estado de las pruebas se escriben. El `informe` conserva su composición.

Los tipos de formulario fijan además tres convenciones por defecto, que no dependen de quien redacta:

- **Numeración con punto.** Los títulos se imprimen como `1. Título` y `2.1. Título`, también en los índices, los marcadores y las referencias `{{ref:id}}`. Solo el `informe` sigue por ahora con `1 Título`.
- **Mayúscula de los títulos** (`heading_case`). `sentence`, el valor por defecto, pone en mayúscula solo la primera letra y deja el resto tal como lo escribió el autor. `title` pone mayúscula de título en los títulos de sección, el título del documento, `short_title` y los encabezados fijos (el histórico y los índices de tablas y figuras): los conectores cortos quedan en minúscula salvo al inicio o tras dos puntos, y se respetan las siglas, la mayúscula interior y las palabras con dígitos. No afecta a títulos de tablas y figuras, al subtítulo ni al cuerpo. Vale para todos los tipos, también para el informe. La numeración de los títulos lleva punto en todos: «1. Título», «2.1. Título».
- **Índices opcionales.** `document.indexes` es una lista, sin repetir, con `contents` (contenido), `tables` (índice de tablas) y `figures` (índice de figuras). Se imprimen bajo el título, en ese orden, con las páginas calculadas al compilar. Pedir `tables` o `figures` sin tablas o sin figuras en el documento, o usar la opción en el `informe` (que ya trae los suyos), es un error. Un bloque `risks` cuenta como tablas: imprime la matriz y el resumen. Un bloque `quote` también: imprime la cotización. Un bloque `requirements` con `matrix: true` también: imprime la matriz de trazabilidad. Un bloque `impact` también: imprime la tabla de antes y después. Un bloque `wbs` también: imprime la estructura de desglose.

Cada sección tiene `id`, `title`, `level` (1,2,3; predeterminado 1), `blocks` y opcional `new_page`. No saltar niveles. La numeración se calcula por jerarquía. Los IDs empiezan con letra y continúan con letras ASCII, dígitos, guion o guion bajo; son únicos en todo el documento.

Bloques admitidos:

| type | Campos |
| --- | --- |
| paragraph | `text` o `runs`; `indent: false` opcional para excepciones de párrafo sin sangría |
| reference | `text` o `runs`; aplica sangría francesa y espaciado del perfil |
| quotation | `text` de al menos 40 palabras y `citation` con atribución/localizador; párrafos separados por una línea en blanco |
| list | `items` (lista de texto), `ordered` opcional |
| note | `text`, `label` opcional |
| notice | `level` (`note`, `caution`, `warning`), `text`; `title` opcional |
| procedure | `id`, `title`, `steps` no vacía; `role` y `prerequisites` (lista de texto) opcionales |
| pagebreak | Sin otros campos |
| testcase | `id`, `title`, `description`, `preconditions`, `expected`, `steps`, `options`, `responsible`, `observations`; `executed` y `selected` opcionales |
| fields | `items` (1 a 16); `columns` opcional (1 o 2, predeterminado 1) |
| table | `id`, `title`, `headers`, `rows`; opcionales `widths`, `source`, `number` |
| figure | `id`, `title`, `description`, `source`; `nodes` para flujo simple **o** `path` para SVG/imagen; `max_height_mm` y `number` opcionales |
| risks | `id`, `scale`, `items`. Opcionales: `responses`, `states`, `open_states`, `summary_id`, `matrix_title`, `register_title`, `summary_title`, `summary_table_title` |
| quote | `id`, `title`, `currency`, `tax_rate`, `items` (`concept`, `quantity`, `unit_price`). Opcionales: `tax_name`, `decimal`, `thousands` |
| requirements | Con `items`: `id` e `items` (`id`, `statement`, `priority`, `source`, `method`, `tests`, `deliverable`, `state`). Opcionales: `priorities`, `methods`, `states`, `verified_states`. Con `matrix: true`: `id` y `title`, sin `items` |

`headers` y cada fila deben tener la misma longitud. Un encabezado puede ser una cadena vacía y deja su celda de cabecera sin texto (la tabla de aceptación de `alcance-proyecto` lo usa en la columna de rótulos). `widths` contiene pesos positivos, uno por columna. Una celda es texto; `null` se muestra «No informado» y una cadena vacía deja la celda en blanco (la usan las filas de asistentes y la hoja de evaluación de `acta-capacitacion`, que se llenan a mano). Códigos con cero inicial deben ser cadenas. Una fila demasiado alta falla: reorganizar el contenido, no reducir automáticamente la fuente. La fuente de una tabla se coloca al final, y su título y encabezados se repiten al partirla.

**Espacio de firma.** En una tabla, una celda vacía de la columna «Firma» (o de la fila «Firma», en las de dos partes) reserva altura para firmar, a mano o con firma electrónica; no se escribe una raya ni guiones bajos. Una celda con texto («No asistió») se imprime tal cual.

Cada elemento de `procedure.steps` requiere `action` y `expected` como textos no vacíos. Admite `on_failure` (texto) y `notice` (objeto con `level`, `text` y `title` opcional, sin `type`); el aviso se imprime antes de la acción. No admite campos de aprobación o ejecución como `checked` o `status`. Los procedimientos reciben numeración automática independiente, destino enlazable e índice condicional. Sus referencias APA muestran «Procedimiento 1»; el índice conserva el título completo. Véase [procedimientos.md](../informe/procedimientos.md) para semántica y ejemplo. Los nuevos bloques rechazan campos desconocidos; `note` mantiene su comportamiento anterior.

`runs` es una lista de tramos `{ "text": "...", "italic": true, "bold": false }`; las marcas de estilo son opcionales y booleanas. Utilizar `text` o `runs`, sin mezclarlos. El contenido se escapa: no se aceptan etiquetas HTML libres. Ejemplo de referencia con título en cursiva:

```json
{
  "type": "reference",
  "runs": [
    {"text": "Entidad de demostración. (2026). "},
    {"text": "Manual de operación del sistema", "italic": true},
    {"text": " (ENT-IT-04)."}
  ]
}
```

El ejemplo es ficticio. En documentos reales, verificar datos, orden alfabético y correspondencia autor-fecha antes de compilar. El bloque no genera automáticamente autores ni citas.

`number` conserva el número publicado de un catálogo (por ejemplo `"136"`); no renumerar catálogos heredados. Para tablas nuevas en un catálogo usar números explícitos que no colisionen. Si se omite, se usa el ordinal de aparición. Numeración de tablas y figuras independiente.

`{{ref:id}}` dentro de textos, celdas e historial se transforma en el título/número del objeto y un enlace al destino. Un ID inexistente detiene la compilación. No admite enlaces externos ni HTML libre en este motor.

En el perfil `institucional-apa`, las llamadas a tablas y figuras muestran solo «Tabla 1» o «Figura 2»; sus títulos completos permanecen en los índices. El manifiesto conserva `labels` para navegación y `reference_labels` para el texto de las llamadas. Las cursivas y negritas controladas de `runs` constituyen la excepción al texto plano; no equivalen a HTML libre.

El flujo nativo admite 2-5 nodos de texto y flechas lineales. SVG externos requieren `svglib` y compatibilidad con sus funciones. No usar diagramas animados dentro del PDF. Conservar la fuente vectorial editable.
