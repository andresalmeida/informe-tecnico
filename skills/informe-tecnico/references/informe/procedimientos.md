# Procedimientos verificables y avisos

Leer al redactar tareas de un manual, instrucciones de operación o anexos de consulta. Estos bloques son opcionales: un informe descriptivo puede seguir usando párrafos, tablas y figuras. Los resultados de una actividad ya realizada pertenecen a su desarrollo/resultados, con la voz de [redaccion.md](redaccion.md).

## Procedimientos

Organizar cada procedimiento por una tarea reconocible: consultar un indicador, descargar un reporte o recuperar una sesión. Indicar rol y condiciones iniciales cuando cambien la ejecución. Cada paso tiene una acción concreta y un **resultado esperado observable**: una vista, un estado, un mensaje o un archivo. Nombrar los controles tal como aparecen en la interfaz y mantener una forma verbal uniforme. No imponer seis pasos ni una página por procedimiento.

El resultado esperado describe cómo reconocer que el paso funcionó. No es una afirmación de prueba realizada: no añadir marcas de aprobado, casillas preseleccionadas ni fechas de validación. Registrar una ejecución real y su evidencia por separado cuando el encargo lo requiera. El compilador verifica la estructura del bloque; no opera la aplicación ni comprueba sus resultados.

Añadir `on_failure` solo si se conoce qué hacer cuando no se obtiene el resultado. Explicar una acción concreta o una condición de parada; no inventar botones, reintentos, recuperación ni contactos. No documentar comandos a partir de suposiciones. Consultar la evidencia del sistema para permisos, límites, unidades y textos de controles; resolver las diferencias entre la versión documentada y el código o despliegue antes de publicar.

```json
{
  "type": "procedure",
  "id": "consulta-periodo",
  "title": "Consultar datos de un período",
  "role": "Usuario con permiso de consulta",
  "prerequisites": ["Sesión iniciada y vista de consulta abierta."],
  "steps": [
    {
      "action": "Seleccione el período y pulse Consultar.",
      "expected": "La cabecera muestra el período seleccionado y la tabla presenta sus registros.",
      "on_failure": "Si la cabecera conserva otro período, revise la selección antes de interpretar la tabla."
    }
  ]
}
```

Este ejemplo describe una interfaz ficticia. En un documento real se sustituyen sus condiciones y controles por los del sistema. El motor numera los procedimientos en orden de aparición, genera un índice condicional y permite `{{ref:consulta-periodo}}`; el ID es de composición y no se imprime como código documental. Cada paso conserva acción y resultado juntos cuando caben en una página. Un procedimiento extenso puede continuar en otra página sin reducir la fuente.

## Avisos

Usar `notice` cuando la información modifica una decisión o previene una consecuencia concreta. No añadir avisos para llenar espacio o adornar todas las secciones.

| `level` | Rótulo | Cuándo corresponde |
| --- | --- | --- |
| `note` | Nota | Aclaración necesaria para interpretar o ejecutar una tarea. |
| `caution` | Precaución | Riesgo de pérdida o alteración de datos, o daño a equipos. Describir la consecuencia y cómo evitarla. |
| `warning` | Advertencia | Riesgo para la integridad física de personas. Usar solo si el sistema o procedimiento realmente lo presenta. |

Una denegación de permisos o una consulta sin datos se explica como funcionamiento normal, salvo que tenga una consecuencia que justifique un aviso. En un sistema de información es habitual que no haya ninguna advertencia de riesgo físico.

```json
{
  "type": "notice",
  "level": "caution",
  "title": "Sustitución de datos",
  "text": "La importación sustituye los registros del período. Confirme el período y conserve una copia antes de continuar."
}
```

El ejemplo solo corresponde si esas condiciones y la copia están sustentadas. Para un aviso asociado a un paso, colocar `notice: {"level": "...", "title": "...", "text": "..."}` dentro del paso, sin `type`: el motor lo sitúa **antes** de la acción. Fuera de un procedimiento se usa el bloque completo. `title` es opcional; `level` y `text` son obligatorios.

Mantener los avisos breves, con condición, consecuencia y acción cuando corresponda. El rótulo siempre se imprime y conserva su significado en blanco y negro. Usar la tipografía y el interlineado del perfil activo; estas son convenciones del manual institucional, no requisitos de APA. La nota de una tabla o figura continúa usando su pie correspondiente. El bloque antiguo `note` se conserva para compatibilidad; no se convierte automáticamente en un aviso de riesgo.

La separación de acción/comprobación y la semántica de los avisos se inspiran en [NASA handbook](https://github.com/R44VC0RP/skills/blob/main/skills/nasa-handbook/references/style-guide.md), adaptadas a este motor. No se trasladan su tipografía retro, abreviaturas de vuelo ni ejemplos ficticios al sistema documentado.
