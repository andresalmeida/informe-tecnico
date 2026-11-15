# Mapa de uso: qué documento va en cada fase de un proyecto

El catálogo tiene más de veinte tipos, y un proyecto no los usa todos. Esta guía dice cuáles se usan en cada fase, cuáles son indispensables y quién ve cada uno. Es genérica: sirve a un encargo interno o a uno para un cliente, de software o de otro tipo.

## El hilo

Un compromiso nace en la propuesta y viaja por todo el proyecto: se vuelve requisito, tarea, caso de prueba y línea del acta de entrega con la versión que se entregó. Cada documento enlaza al anterior por su código y registra algo distinto. Así el compromiso se escribe una vez y no cinco. Los códigos siguen [codigos.md](codigos.md).

## Tres niveles de uso

- **Núcleo:** casi todo proyecto los necesita.
- **Frecuente:** la mayoría de los proyectos medianos los usa.
- **Según el caso:** solo si el proyecto tiene esa condición (datos personales, un modelo, una baja).

Un proyecto pequeño puede quedarse con el núcleo: acta de reunión, factibilidad, propuesta, alcance, plan de pruebas y acta de entrega.

## Por fase

| Fase | Qué ocurre | Documentos del catálogo |
|---|---|---|
| 1. Levantamiento | Se entiende el pedido, quién lo usará y qué resultado espera. | **Núcleo:** [acta de reunión](tipos/acta-reunion.md). **Frecuente:** [registro de requerimientos](tipos/registro-requerimientos.md). |
| 2. Factibilidad interna | Se decide si se puede asumir, con qué esfuerzo y con qué riesgos. | **Núcleo:** [informe de factibilidad](tipos/factibilidad.md). **Frecuente:** [registro de riesgos](tipos/registro-riesgos.md). **Según el caso:** [evaluación de impacto en datos](tipos/evaluacion-impacto-datos.md), si el proyecto trata datos personales. |
| 3. Propuesta y aceptación | Se ofrece qué se entrega, en cuánto tiempo y a qué costo, y quien contrata acepta. | **Núcleo:** [propuesta de servicio](tipos/propuesta-servicio.md). |
| 4. Arranque y planificación | Se fija el compromiso y se detalla cómo se cumplirá. | **Núcleo:** [alcance del proyecto](tipos/alcance-proyecto.md), [plan de pruebas](tipos/plan-pruebas.md). **Frecuente:** [especificación de requisitos](tipos/especificacion-requisitos.md), [descripción de arquitectura](tipos/descripcion-arquitectura.md), [decisión de arquitectura](tipos/decision-arquitectura.md). **Según el caso:** [plan de proyecto](tipos/plan-proyecto.md), [ficha de modelo](tipos/ficha-modelo.md). |
| 5. Construcción | Se construye y se mide el avance. Lo que cambia lo prometido se tramita aparte. | **Frecuente:** [solicitud de cambio](tipos/solicitud-cambio.md); el registro de riesgos sigue vivo. |
| 6. Validación | La parte designada comprueba la versión contra lo acordado. | **Núcleo:** el [plan de pruebas](tipos/plan-pruebas.md) recoge resultados y certificado. |
| 7. Entrega y cierre | Se entrega, se traspasa a quien opera y se cierra. | **Núcleo:** [acta de entrega](tipos/acta-entrega.md). **Frecuente:** [acta de capacitación](tipos/acta-capacitacion.md), [traspaso a operación](tipos/traspaso-operacion.md), [informe de cierre](tipos/informe-cierre.md). |
| 8. Operación y evolución | El sistema opera y se publican versiones nuevas. Cada cambio de lo acordado vuelve a pasar por la solicitud de cambio. | **Frecuente:** [notas de versión](tipos/notas-version.md) de cada versión que se publica y [solicitud de cambio](tipos/solicitud-cambio.md); el registro de riesgos sigue vivo. **Según el caso:** un nuevo [traspaso a operación](tipos/traspaso-operacion.md) si cambia quién opera, y la revisión de la [evaluación de impacto en datos](tipos/evaluacion-impacto-datos.md) si cambian los datos. |
| 9. Retiro | Se deja de usar un sistema, un módulo o un procedimiento. | **Según el caso:** [acta de baja](tipos/acta-baja.md), solo cuando alguien con autoridad decidió retirar. |

Las fases 1 a 7 se recorren una vez; la 8 se repite con cada versión, y la 9 puede no ocurrir nunca. Dos tipos quedan fuera de las fases porque no son de un proyecto. La [ficha de proceso](tipos/ficha-proceso.md) describe cómo trabaja una entidad un proceso (proveedores, entradas, etapas, salidas y clientes) y se hace una vez por proceso, no por proyecto. Los [informes y manuales](informe/informe.md) cubren la documentación que no sigue este flujo.

## Quién ve cada documento

- **Internos de quien ofrece:** factibilidad, registro de riesgos, plan de proyecto, informe de cierre y la evaluación de impacto en datos. Traen esfuerzo, márgenes y riesgos del equipo. A quien contrata le llega solo lo que cambia su decisión, dentro de la propuesta.
- **Para quien contrata y se firman o aprueban:** propuesta, alcance, plan de pruebas, actas, traspaso y notas de versión.
- **Para ambos:** especificación de requisitos, solicitud de cambio y descripción de arquitectura, según lo que se acuerde compartir.

## Tres decisiones distintas

Pueden tomarlas tres personas distintas y se registran en documentos distintos:

1. **«Podemos ofrecer»:** la decide quien ofrece, en la factibilidad.
2. **«Acepto esta oferta»:** la decide quien contrata, al aceptar la propuesta.
3. **«Esto cumple lo acordado»:** la confirma quien valida, en el plan de pruebas y el acta de entrega.

Aceptar una condición no es cumplirla. Si la propuesta depende de algo pendiente, solo arranca el trabajo que no depende de ello.

## Versiones y cambios

No todos los documentos pasan a la versión siguiente juntos. Las reglas completas están en [ciclo-de-vida.md](ciclo-de-vida.md); en corto:

- Antes de que quien contrata acepte la propuesta, un cambio da una versión nueva de la propuesta. La anterior se marca como sustituida si ya circuló; un borrador que nunca salió no necesita la marca, y el ciclo de vida solo se declara cuando consta la decisión de dejar la copia fuera de uso.
- Después de aceptarla, un cambio se tramita como solicitud de cambio y no entra al compromiso hasta que se acuerda. Si cambia la viabilidad, se vuelve a la factibilidad.
- Si una prueba falla sobre lo ya acordado, es una corrección, no un cambio ni una nueva cotización.

## Cuándo no producir un documento

- **Ficha de modelo:** solo si el sistema incluye un modelo estadístico o de aprendizaje automático. Un registro de eventos con reportes no lo es.
- **Acta de baja:** solo si alguien con autoridad decidió retirar algo. Una pregunta («¿hay que dar de baja el Excel?») no es esa decisión, y una baja en borrador sobre algo que nadie decidió retirar inventaría el retiro.
- **Solicitud de cambio:** nunca para un defecto sobre lo ya acordado; eso es una corrección.
- **Cuando ningún tipo del catálogo cubre el momento**, decirlo y no forzar el tipo más parecido.

## Cuando falta un documento anterior

Los proyectos arrancan sin todos los documentos. Estas son las salidas honestas, para no inventar:

| Situación | Qué se escribe |
|---|---|
| La factibilidad dice que hay datos personales y la evaluación de impacto aún no existe | El código de la evaluación queda «Por confirmar»; la evaluación, al emitirse, cita la factibilidad ([codigos.md](codigos.md)). |
| La factibilidad no tiene evidencia (sin entorno, sin muestra) | Viabilidad «Pendiente de evidencia». La propuesta puede emitirse solo como borrador condicionado ([propuesta-servicio.md](tipos/propuesta-servicio.md)). |
| La especificación de requisitos se escribe antes que el plan de pruebas | Los casos van «Por definir», el estado queda «Propuesto» y no se escribe un código de prueba que no existe ([especificacion-requisitos.md](tipos/especificacion-requisitos.md)). |
| Quien contrata comunica que aceptó y no hay firma | Se registra la aceptación comunicada con fecha y origen; la firma queda «Pendiente» ([pendientes-y-estado.md](pendientes-y-estado.md)). |
| La cotización no tiene tasa de impuesto | Ver `quote` en [quote.md](contrato/quote.md): el impuesto queda «Por confirmar» en vez de una tasa supuesta. |
| Quien pide da cifras (usuarios, plazo deseado) antes de cualquier estimación | Se anotan atribuidas a quien las dio; la estimación es de la factibilidad ([registro-requerimientos.md](tipos/registro-requerimientos.md)). |

## Revisión con ojos nuevos

Dos momentos piden una lectura de alguien sin el contexto. Antes de construir, un agente o una persona que no conoce el proyecto lee los documentos de arranque y dice lo que no entiende. Antes de enviar, lee la propuesta como la leería quien contrata. Si el plugin elephant-goldfish está instalado, hace ese trabajo; si no, basta un agente nuevo con el documento y la pregunta «¿qué no se entiende?».

## Cómo empezar

1. Elegir las fases que aplican y, de cada una, los documentos del núcleo.
2. Añadir los frecuentes cuando el proyecto lo pida y los demás solo ante su condición.
3. Asignar los códigos según [codigos.md](codigos.md) y citar cada documento desde el siguiente.
4. Redactar cada documento con la guía de su tipo.
