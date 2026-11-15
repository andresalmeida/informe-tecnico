### Bloque `wbs`

Estructura de desglose del trabajo. `nodes` es una lista de paquetes. Cada paquete lleva `id` y `title`. Una rama lleva `children`, una lista no vacía de paquetes. Una hoja lleva `effort`: un número mayor o igual que cero, hasta 2 decimales, o exactamente `Por estimar`. No se admiten las dos cosas a la vez, ni un paquete sin ninguna. Hasta 4 niveles y 40 paquetes. `unit` es la unidad del esfuerzo; si se omite, es días-persona.

El total de una rama es la suma del esfuerzo numérico de sus hojas. `Por estimar` se imprime y no entra en la suma. El total general es esa misma suma. `total` y `subtotal`, en el bloque o en un paquete, se rechazan con un mensaje que dice que se quiten. También se rechaza un id repetido o inválido, un esfuerzo negativo, más de 2 decimales, una rama sin hijos y campos desconocidos.

La tabla tiene identificador, paquete con sangría por nivel y esfuerzo. La fila final es el total general. Un `{{ref:id}}` apunta a esa tabla. El formato de número usa coma decimal y punto de miles, y no consulta el idioma del sistema. Para qué hojas se estiman y cuál queda fuera de la suma, ver [plan-proyecto.md](../tipos/plan-proyecto.md).
