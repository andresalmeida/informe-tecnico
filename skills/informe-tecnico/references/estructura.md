# Estructura según finalidad

El núcleo documental comprende identidad, código, título, versión, fecha efectiva, estado, control de cambios y navegación. Portada e índices se dimensionan al documento: para una ficha de dos páginas puede bastar el encabezado. El motor de referencia usa portada e historial explícitos para informes extensos.

## Plantilla base y lugar del trabajo técnico

Los preliminares no son capítulos: portada, control de cambios, contenido e índices de tablas/figuras. Para un informe técnico nuevo, usar esta base salvo una estructura institucional obligatoria o una instrucción distinta del usuario:

| Capítulo | Función |
| --- | --- |
| 1. Introducción | Problema, contexto y propósito del documento. |
| 2. Objetivos | Objetivo general y objetivos específicos comprobables. |
| 3. Alcance | Qué se estudia, límites, exclusiones y restricciones. |
| **4. Desarrollo técnico** | El trabajo principal: método y fuentes, análisis, solución o descripción técnica, tablas, figuras, cálculos y procedimientos aplicables. Organizar como 4.1, 4.2, etc. |
| 5. Resultados | Entregables, comportamiento obtenido y comprobaciones realizadas. Añadir evaluación o validación cuando forme parte del encargo. |
| 6. Conclusiones y recomendaciones | Respuestas a los objetivos y acciones justificadas. No repetir el desarrollo. |
| 7. Referencias | Fuentes y documentos relacionados con versión/localización. |
| Anexos, cuando proceda | Evidencia extensa o detalle auxiliar; no esconder allí información necesaria para comprender el trabajo. |

El capítulo 4 es un contenedor de contenido, no un formulario fijo de cuatro campos. Un análisis de infraestructura puede usar 4.1 Método, 4.2 Diagnóstico, 4.3 Propuesta y 4.4 Implementación. Un manual puede usar 4.1 Arquitectura, 4.2 Datos e interfaces, 4.3 Instalación y 4.4 Operación/diagnóstico. Un catálogo puede usar 4.1 Convenciones y 4.2 Fichas/tablas. Elegir subsecciones a partir de la evidencia; no crear secciones vacías para completar la lista.

`assets/plantilla-base.json` es la fuente inicial para un informe nuevo. Sus campos vacíos de identidad documental y revisión se completan con datos reales antes de compilar. Los bloques vacíos se rellenan o se eliminan según el alcance. `assets/ejemplo.json` demuestra la misma jerarquía aplicada a la propia plantilla: la explicación del modelo, las convenciones, el catálogo y el procedimiento aparecen dentro del capítulo 4.

Si el documento es breve o su finalidad exige otro orden, ajustar la estructura y explicar esa decisión. No forzar el capítulo 4 al migrar un manual regulado cuyo orden deba preservarse.

## Informe de evaluación

Introducción con problema y contexto; objetivo general y específicos comprobables; alcance y exclusiones; método, fuentes y restricciones; desarrollo técnico; resultados y evidencia; conclusiones que respondan a objetivos; recomendaciones con responsable/plazo solo si se conocen; referencias y anexos necesarios. No confundir recomendaciones con resultados medidos.

## Informe técnico de actividad o entrega

Describir lo implementado, configurado o elaborado, su funcionamiento y los resultados de la actividad con voz impersonal. El desarrollo se ocupa del sistema y sus entregables. No usar como estructura predeterminada un inventario de fuentes revisadas, hallazgos editoriales de manuales ni una matriz de pruebas pendientes. Conservar esos registros en los archivos de trabajo; incluir únicamente el estado pendiente que afecte a la entrega. Aplicar [redaccion.md](redaccion.md).

## Manual de usuario

Organizar la guía por tareas y por rol cuando cambie el alcance de acceso. Explicar entrada al sistema, navegación, consultas, operaciones e interpretación de resultados con pasos directos, controles identificables y resultado esperado. Las fuentes sirven para sustentar la guía; el texto no relata su lectura ni su extracción. Incluir referencias documentales cuando aporten contexto sin duplicar los manuales existentes.

## Manual técnico y de operación

Introducción y propósito; audiencia; objetivos; alcance; términos necesarios; descripción del sistema; requisitos y versiones; arquitectura y componentes; modelo/diccionario de datos; interfaces; instalación, configuración y despliegue; operación y mantenimiento; diagnóstico y recuperación; referencias/anexos. Incluir solamente módulos aplicables. Es suficiente referenciar arquitectura existente si duplicarla introduce divergencias.

Un procedimiento operativo útil precisa condición inicial, permisos/requisitos, pasos, resultado esperado, comprobación y recuperación cuando exista. Los comandos deben proceder de evidencia y no ejecutarse sobre un sistema real por el hecho de documentarlos.

## Catálogo o diccionario

Propósito, ámbito, convenciones, reglas generales y fichas tabulares. Por ficha: ID estable, nombre, definición, código, tipo/longitud cuando se conozcan, dominio permitido, unidad, obligatoriedad, vigencia y fuente. No inventar columnas de esquema ausentes. Las bajas llevan estado explícito; no se borra silenciosamente su significado histórico.

## Control de cambios

Usar fecha ISO en la fuente y una presentación local uniforme. La fecha corresponde a la revisión del documento. Una nueva exportación no crea una nueva revisión. No imponer SemVer a una entidad que ya usa 14.3 u otra convención.

Cada cambio debe identificar lo que cambió y el objeto estable afectado. Una página histórica puede preservarse como dato histórico con versión explícita; no se trata como localizador actual. Las referencias de la edición vigente se derivan de los destinos de la compilación.

Campos de aprobación son opcionales: registrar el acto real, no firmantes ficticios ni casillas aprobadas por defecto. Si falta evidencia, mostrar Borrador o Pendiente de validación.

## Redacción sin relleno

Preferir «El archivo se rechaza si el código no pertenece al catálogo» a «La solución robusta garantiza una gestión integral». Usar actor, condición, acción y efecto. No abrir cada sección anunciando lo que se verá. No resumir de nuevo cada tabla en prosa ni concluir cada capítulo con elogios al sistema. Los objetivos no deben prometer capacidades que las fuentes no demuestran.
