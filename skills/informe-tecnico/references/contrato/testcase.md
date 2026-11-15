### Bloque `testcase`

Ficha repetible de prueba de aceptación. Se admite en todos los tipos sin cambiar su composición anterior. Requiere `id` único con la sintaxis común, `title`, `description`, `preconditions`, `expected`, `responsible` y `observations`, todos textos no vacíos. Se referencia con `{{ref:id}}`; el rótulo «Caso ID. Título» incluye el identificador suministrado y no consume la numeración de tablas ni procedimientos. El destino y el marcador se registran solo en el primer fragmento. No tiene índice impreso propio.

`steps` es una lista no vacía, sin límite fijo de cantidad, con `task`, `activity`, `expected` y `actual`, todos textos no vacíos. El motor numera los pasos desde 1. Antes de ejecutar, escribir «Pendiente» en `actual`; después, registrar lo observado y localizar su evidencia. No valida la verdad de ese contenido.

`options` contiene exactamente tres textos distintos no vacíos. `executed` es booleano, falso por omisión. Con `executed: false`, `selected` se omite o es `null`, y todas las casillas quedan vacías. Con `executed: true`, `selected` es una cadena idéntica a exactamente una opción; esa casilla lleva una cruz vectorial y su texto en negrita. No se admite una lista de marcas, una cadena vacía, una opción inexistente, una selección sin ejecución ni ejecución sin selección. Esto es independiente de `fields`, que sigue exigiendo una marca siempre.

```json
{"type": "testcase", "id": "CP-01", "title": "Confirmación de pago",
 "description": "Verifica el criterio acordado para la reserva de prueba.",
 "preconditions": "Reserva pendiente en la pasarela de pruebas.",
 "expected": "Una confirmación de pago vincula una sola reserva.",
 "steps": [{"task": "Confirmar", "activity": "Enviar la confirmación de prueba.",
            "expected": "La reserva queda confirmada.", "actual": "Pendiente"}],
 "options": ["Conforme", "Conforme con observaciones", "No conforme"],
 "executed": false, "responsible": "Por confirmar", "observations": "Pendiente de ejecución."}
```

Una ficha que cabe en una página se mantiene entera. Si supera el alto útil, se divide entre filas de pasos y repite título, descripción, precondiciones, resultado esperado y encabezados de pasos. Resultado, responsable y observaciones permanecen junto al último paso. Una fila nunca se divide; si la cabecera repetida y un paso (más el cierre en el último) superan la página, falla con el ID, el número de paso y una indicación de acortar la ficha, dividir la actividad o reducir observaciones. No reduce automáticamente la tipografía. La cantidad de pasos es libre, pero la cabecera repetida y el cierre tienen que caber con un paso. Los rótulos fijos de la ficha son españoles; se personalizan los tres textos de resultado, sin controles de firma electrónica.

`validate_testcase` rechaza claves desconocidas en ficha y pasos, campos vacíos, pasos ausentes o vacíos, opciones repetidas o distintas de tres y estados o selecciones inválidos. La cobertura de criterios, la evidencia, las fechas y la coherencia con el certificado se revisan con [plan-pruebas.md](../tipos/plan-pruebas.md).
