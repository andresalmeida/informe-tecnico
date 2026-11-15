### Bloque `impact`

Tabla de antes y después. Cada elemento de `rows` lleva `aspect` (texto no vacío), `before`, `after` y `unit` (texto no vacío). `before` y `after` son un número, hasta 2 decimales, o exactamente `Por estimar`. La diferencia es el después menos el antes. Si uno de los dos es `Por estimar`, la diferencia impresa es `Por estimar`. El motor no suma las filas: las unidades pueden ser distintas.

Esos resultados no se escriben. `difference`, `diferencia` y `delta`, en el bloque o en una fila, se rechazan con un mensaje que dice que se quiten. También se rechaza un valor que no es número ni `Por estimar`, más de 2 decimales, una lista fuera de 1 a 12 filas y campos desconocidos.

La tabla tiene cinco columnas: aspecto, antes, después, diferencia y unidad. Un `{{ref:id}}` apunta a esa tabla. El formato de número usa coma decimal y punto de miles, con medio hacia arriba, y no consulta el idioma del sistema. Para cuándo una fila queda en `Por estimar` y qué decisión deja el compromiso quieto, ver [solicitud-cambio.md](../tipos/solicitud-cambio.md).
