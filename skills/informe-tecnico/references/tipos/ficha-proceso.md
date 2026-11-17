# Ficha de proceso y mapa SIPOC

Elegir `document.kind: "ficha-proceso"`, código `FPR`, para explicar cómo trabaja una entidad: proveedores, entradas, proceso, salidas y clientes, con sus etapas, decisiones e indicadores. Partir de `assets/ejemplo-ficha-proceso.json`. Es formulario sin elección obligatoria. Lleva figura SIPOC y su equivalente textual. La estructura la fija el catálogo; no procede de un formulario empresarial ni reproduce una norma.

La muestra ocupa tres páginas: identificación y SIPOC en la primera; etapas, controles, roles y decisiones en la segunda; indicadores, firmas e histórico en la tercera. No lleva portada ni índices. Usa las medidas del perfil por omisión; una ficha que deba caber en dos páginas puede pedir `format.profile: "institucional"` (cuerpo de 10,5 pt, tablas de 9 pt). No hay ajuste automático de escala. El nombre del proceso aparece en el subtítulo; código y versión se repiten con el dueño en la información. Las firmas se organizan por función en tres columnas para conservar un espacio real de firma sin alargar la ficha.

## Decidir antes de redactar

Acordar el límite del proceso: qué lo dispara, dónde termina y qué rol responde de él. Distinguir un procedimiento propuesto de una práctica ya autorizada. El ejemplo «Gestión y entrega de proyectos tecnológicos» de la Entidad de demostración es genérico y usa roles, sin nombres de personas. Cita documentos del catálogo para enseñar qué registro deja cada etapa; no da por aceptadas las propuestas ni por ejecutadas las pruebas de esos ejemplos.

## Completar cada campo

1. **Información del proceso.** Nombre, código, versión, dueño por rol, objetivo, disparador y fin. Una función que nadie ha confirmado queda «Por confirmar»; no asignarla a una persona por suposición.
2. **Mapa SIPOC.** Figura de izquierda a derecha con cinco bloques: proveedores, entradas, proceso, salidas y clientes. Añadir una tabla que diga lo mismo en texto, con términos coincidentes. El proceso central se desarrolla en las etapas; los cinco bloques no representan cinco departamentos ni cinco fases cronológicas.
3. **Etapas.** Número, etapa, acción, rol y documento del catálogo por tipo y código. El ejemplo recorre solicitud, factibilidad, propuesta, aceptación, arranque, construcción, validación y entrega. La aceptación de una propuesta deja constancia en la misma propuesta; no exige inventar un acta nueva. Las siglas o roles abreviados deben ser reconocibles y coherentes con la tabla de decisiones.
4. **Controles y registros.** Qué documentos requieren aprobación, autoridad y evidencia, qué se congela y quién custodia. Aplicar [ciclo-de-vida.md](../ciclo-de-vida.md): cada documento cambia por su propia decisión, conservando las versiones anteriores. `vigente` requiere autorización documentada; `sustituido` identifica sucesor; `retirado` requiere fecha; `archivado` exige plazo y ubicación. El texto de una ficha no modifica los estados de otros archivos. Citar también los registros de apoyo sin repetir su contenido.
5. **Roles y decisiones.** Tabla de decisión, quién decide, a quién se consulta y a quién se informa. Usar roles de la entidad. Esta es una lectura breve de decisiones del proceso; la asignación por actividad de un proyecto vive en su alcance.
6. **Indicadores.** Nombre, qué mide, fórmula, meta, frecuencia y fuente. Un nombre de indicador no sustituye a su fórmula. Definir numerador, denominador, unidad y universo de conteo; con denominador cero escribir «No aplica». La meta puede ser «Por definir» hasta que el dueño la acuerde. El ejemplo propone dos porcentajes sin inventar mediciones: cobertura de entregas con evidencia y resolución de pendientes.
7. **Firmas e histórico.** Elaboración, revisión y aprobación por rol, espacios de firma y fechas pendientes. Una primera versión lleva una sola entrada de histórico. Identificar después a las personas autorizadas cuando consten.

## Cómo se comprueba

El proveedor produce la entrada, el proceso transforma lo recibido y sus salidas llegan al cliente indicado. La figura y la tabla expresan exactamente esa relación. Las ocho etapas tienen un responsable y un registro reconocible; comprobar la existencia de cada código antes de citarlo en un proceso real. Una referencia al catálogo sirve de ejemplo, sin convertir los documentos pendientes en aprobados.

Cada indicador debe permitir calcular el mismo resultado con los mismos datos. «Entregas con evidencia» cuenta las que tienen registradas sus comprobaciones de aceptación; «pendientes» se cuenta por identificador de seguimiento. Definir en el uso real período de corte y criterios de inclusión con el dueño del proceso. El motor imprime las fórmulas y no consulta los registros ni calcula mediciones; no hay un bloque nuevo en el contrato.

## Personalizar y tratar lo pendiente

Cambiar identidad, código, papel A4 o Letter, dueño, roles, fuentes y fórmulas. El logo es PNG o JPEG relativo al JSON. Seguir [pendientes-y-estado.md](../pendientes-y-estado.md) y [codigos.md](../codigos.md). No inventar aprobaciones, firmas, metas, mediciones o cumplimiento de una norma. Conservar las condiciones y la evidencia que determinan la conformidad.

No se omiten figura, tabla equivalente, etapas ni fórmulas para acortar la ficha. Los índices son opcionales del motor, pero no se recomiendan aquí; la prueba cubre su activación. Más registros o textos más largos pueden superar las tres páginas: resumir a una acción por etapa, revisar los anchos y separar el detalle en documentos referenciados. La personalización en Letter puede necesitar esa revisión de composición. No reducir toda la figura o la letra para forzar el límite.

## Diagrama: qué agrega y cómo producirlo

La figura añade la relación proveedor → entrada → transformación → salida → cliente de un proceso de la entidad. Las figuras anteriores de la cadena describen el módulo de pagos; esta responde a otra pregunta. Seguir [diagramas.md](../diagramas.md), con identidad del JSON y fuentes locales. El ejemplo conserva `diagrams/sipoc-proyectos.html`, SVG y PNG a 3x. Se usó el flujo mínimo de `diagram-design`, referencia flowchart adaptada a cinco bloques de izquierda a derecha por el encargo. No contiene decisiones ni ramas. La validación se ejecutó sin red y las exportaciones con sus helpers; el verificador de geometría no está instalado, por lo que los conectores se revisaron visualmente.

El viewBox es 600 × 100; los textos de 12 unidades quedan aproximadamente en 9,5 pt al ancho de 168 mm. Solo el proceso central lleva acento; texto y flechas conservan contraste sobre blanco. La figura, su fuente y el subtítulo declaran la demostración. No altera el estilo compartido de la instalación.

## Redacción y entrega

Aplicar Minto: propósito y límite del proceso primero. Aplicar unicorntext: quitar relleno manteniendo acciones, responsabilidades y fórmulas. Los criterios están incorporados; si el usuario invoca las skills hermanas, leer además sus instrucciones.

Verificar dependencias: `python3 -c "import reportlab, pypdf, pdfplumber, PIL"`. Si faltan, usar un entorno virtual externo con `reportlab>=4.4,<5`, `pypdf>=6,<7`, `pdfplumber>=0.11,<1` y `Pillow>=11,<13`. Desde la carpeta instalada, con ese intérprete:

```sh
python3 scripts/build_report.py assets/ejemplo-ficha-proceso.json --output proceso.pdf
python3 scripts/check_report.py proceso.pdf
pdftoppm -r 80 -png proceso.pdf proceso
```

Abrir todas las páginas y un recorte de la figura a 150 ppp. Revisar cinco bloques legibles, flechas con destino claro, equivalencia textual, ocho etapas, fórmulas y firmas completas con histórico en la última página. Si falta Poppler, renderizar con `pdfplumber.open('proceso.pdf').pages` y `page.to_image(resolution=80)`. Entregar PDF, manifiesto obligatorio, JSON, fuente HTML/SVG y PNG integrado.
