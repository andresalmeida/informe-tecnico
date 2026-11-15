# Lo pendiente, el estado y las fechas en los tipos de formulario

Esta guía vale para `informe-factibilidad`, `registro-requerimientos`, `alcance-proyecto` y los tipos de formulario que se añadan. Cada guía de tipo conserva sus filas propias. Aquí está lo común: cómo se escribe lo que falta, quién puede firmar, qué estado y qué fecha lleva el documento y qué historial lleva uno nuevo.

## Palabras para lo que falta

Lo que no consta se escribe siempre con la misma palabra, según el caso:

| Dato | Texto |
|---|---|
| Fecha de firma, de aprobación o de remisión que aún no ocurrió | Pendiente |
| Estado de algo aún no cumplido (por ejemplo, una condición de la aprobación) | Pendiente |
| Nombre o cargo de una persona que nadie ha confirmado | Por confirmar |
| Valor que depende de otro equipo o de una decisión | Por confirmar con (área) |
| Cifra de esfuerzo, plazo o recurso sin estimar | Por estimar |
| Umbral o criterio que nadie ha acordado | Propuesto, por confirmar con (área) |
| Identificador de tarea o de solicitud que el tablero aún no asignó (notas de versión, solicitud de cambio) | Por registrar |
| Dato que no aplica al caso | No aplica |
| Sección o bloque opcional sin ningún dato | Se elimina entero; los apartados siguientes se renumeran solos |

La palabra va en el campo y no dentro de una oración. Para los umbrales de una lista, la frase que la introduce lleva la marca: «Umbrales propuestos, por confirmar con atención al socio:». Una estimación propia se rotula como tal donde aparece (en el título de la tabla, en el total o en el criterio), con la palabra «estimado» o «estimación».

## Quién puede firmar o ser responsable

Se nombra a quien el encargo o los documentos citados identifican por su función: quien solicita, quien recibe o registra, quien lidera el proyecto y quien elabora el documento. Quien revisa o aprueba y no consta lleva «Por confirmar» en nombre y cargo. Tampoco se asigna una persona a una función que el encargo no le dio: el patrocinador, el responsable o el momento de una condición de la aprobación y el código de una propuesta que no constan se escriben «Por confirmar», aunque haya una persona verosímil.

## Estado del documento

`document.status` es el estado: «Borrador» mientras faltan datos o firmas, y «En revisión» al circular. «Demostración» es solo para los ejemplos que trae la skill. Un documento pedido sobre un escenario que el usuario declara ficticio es un borrador, y además lo dice en el subtítulo («Ejemplo ficticio») y con el rótulo «Diagrama demostrativo» dentro de su figura y en la fuente de esta. Si el usuario no declara el escenario como ficticio, no se rotula así.

## Fechas

- Las fechas se escriben `dd/mm/aaaa`. Un rango se escribe «del 08/02/2027 al 18/04/2027», sin raya entre las fechas.
- `document.date` es la fecha de la última acción que el documento registra: en un registro, la de asignación; en un alcance, la de elaboración o de la última revisión. Si el encargo no da ninguna, es la de elaboración, que es la del día en que se redacta.
- Las fechas de recepción, registro y asignación siguen ese orden y no superan la fecha del documento.
- Un documento no afirma una aprobación con fecha anterior a la última versión del documento aprobado.

## Aceptación comunicada y firma

Que quien contrata comunique su aceptación (por ejemplo, el encargo dice que aceptó el 03/02/2027) no es una firma ni autoriza los compromisos internos de quien ofrece. El documento que la recoge escribe la aceptación comunicada con su fecha y su origen, deja la fecha de firma en «Pendiente» y no se usa para marcar vigente ni aprobado un documento que nadie aprobó. Tampoco se corrige hacia atrás el documento ya fechado: la aceptación consta en el documento posterior.

## Versiones de un documento

Un documento sigue en `0.x` y en «Borrador» o «En revisión» mientras no conste su aprobación. La versión `1.0` se asigna cuando consta esa aprobación; no por la fecha ni por el número de revisiones. Una versión nueva de un borrador conserva el código y sube la versión.

## Historial de un documento nuevo

`changes` es obligatorio. Un documento nuevo lleva una sola entrada: versión `0.1`, la fecha de elaboración, el resumen «Primera versión.» y quien redacta como responsable. No se fabrican versiones anteriores. Los ejemplos de la skill traen varias versiones porque son demostraciones de un historial.

## Datos que da quien solicita

Una cifra que da el solicitante (un tiempo de espera, un volumen) se atribuye a quien la da («según la solicitante») y no se presenta como medición del equipo. Si es la única base del resultado esperado, se cita como situación actual y la meta se deja para la evaluación. La necesidad se apoya en la solicitud original citada por quien la hizo y su fecha, sin inventar un documento adjunto.

## Ciclo de vida opcional

Cuando se use `document.lifecycle`, seguir [ciclo-de-vida.md](ciclo-de-vida.md). Su estado gobierna el pie y las bandas; `document.status` conserva el contexto editorial de la fuente y los metadatos. No declarar vigente, retirado o archivado por disponer de una plantilla: la decisión debe constar. Una baja o un cierre todavía pendientes conservan su condición de borrador. Las fechas de congelación, retiro y conservación solo se completan con evidencia o como simulación explícita del ejemplo.
