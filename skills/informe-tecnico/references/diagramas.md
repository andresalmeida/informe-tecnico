# Figuras y esquemas

Elegir por la pregunta: límites y componentes → arquitectura/contexto; decisiones → flujo; intercambio temporal → secuencia; entidades y cardinalidad → ER; cambios de estado → estados; responsables y entregas → carriles. Una lista de atributos corresponde a una tabla.

Herramienta preferida para esquemas nuevos: [diagram-design](https://github.com/cathrynlavery/diagram-design). Es una skill externa que se instala por separado, no una biblioteca de Python ni un motor invocado automáticamente por `build_report.py`. La skill del informe decide cuándo hace falta una figura, usa diagram-design para crearla y entrega el activo terminado al compilador.

El `plan-pruebas` no lleva diagrama: sus fichas y referencias a los criterios del alcance expresan qué se comprueba y con qué resultado, sin repetir la arquitectura.

## Integración

1. Resolver la instalación de `diagram-design` en el catálogo de skills o en la carpeta personal. Leer su `SKILL.md`, la referencia del tipo elegido y, para exportar, `references/export.md`. Si está ausente, indicarlo; no afirmar que un dibujo nativo procede de esa skill.
2. Obtener la identidad del JSON activo: `paper=#FFFFFF`, `ink=brand.ink`, `accent=brand.accent`, reglas y tipografía del documento. Usar esos datos como fuente del proceso de personalización de diagram-design, respetando su resolución de perfiles y autorizaciones existentes. Reutilizar las decisiones de identidad ya expresadas por el usuario. No alterar un perfil de otro cliente ni la apariencia compartida de una instalación para un solo informe.
3. Elegir tipo, tamaño y detalle para la pregunta técnica; comunicar la decisión. Conservar HTML con SVG en línea como fuente editable. Para impresión, generar un estado completo estático y usar fuentes del sistema o locales que no dependan de red.
4. Ejecutar el `scripts/self_check.py` de diagram-design sobre el HTML (añadir `--offline` para este flujo). Exportar con sus helpers a SVG o PNG cuando el encargo requiera integrar el esquema al PDF. Conservar la fuente HTML junto al activo; no copiar solo una captura sin su fuente.
5. Usar un bloque `figure` con `path`, `id`, `title`, `description` y `source`; el motor del informe asigna número, índice, referencia y pie. Preferir SVG si el renderizador compatible está disponible y se verifica. PNG a 3x es una alternativa de impresión; verificar tamaño de texto después de escalar al ancho de columna. Un SVG guardado no demuestra que se haya incrustado vectorialmente en el PDF.
6. Revisar el resultado integrado a tamaño de impresión: el comprobador del diagrama no conoce la escala final del informe. Registrar como demostrativo o propuesto lo que no describa un sistema real.

Si diagram-design no puede usarse con las herramientas disponibles, resolver un esquema sencillo con SVG/Mermaid exportado o con el flujo nativo e informar de esa elección. El flujo lineal del motor es una alternativa mínima; no reemplaza la selección y revisión de un esquema complejo.

Antes de dibujar, escribir qué evidencia representa cada nodo/enlace y qué aprenderá el lector. Etiquetar relaciones no obvias. No añadir puertos, tecnologías o cardinalidades que no aparezcan en la evidencia. No confundir una propuesta con el sistema desplegado.

Para PDF: una composición estática sobre blanco, sin red; conservar SVG o fuente de diagrama editable; texto legible al ancho impreso, conectores que no crucen rótulos, flechas con destino claro, 1-2 focos de atención. Reemplazar animaciones por estados o pasos rotulados. Si no cabe, dividir por tema o cambiar orientación, no reducir todo a letra de 5 pt.

El motor trae un diagrama lineal nativo de 2-5 pasos para flujos simples. Para arquitectura, ER y casos complejos usar `path` con SVG/PNG externo: el flujo simple no representa cardinalidades ni ramas. PNG solo a resolución suficiente; preferir SVG sin `foreignObject`, scripts ni fuentes remotas. El render con `svglib` exige comprobar fidelidad visual; algunos filtros SVG no son compatibles.

La muestra revisada incluye `assets/diagrams/ciclo-revision.html`, creado aplicando diagram-design, su SVG exportado y un PNG de impresión. El JSON integra el PNG para no requerir un renderizador SVG adicional. La fuente identifica el carácter demostrativo y conserva la editabilidad.

El ejemplo de informe de factibilidad añade `assets/diagrams/arquitectura-pagos.html` (tipo arquitectura, sistema ficticio), con su SVG y su PNG a 3x. Su ancho de 584 unidades se escala a la columna de 168 mm, de modo que los rótulos miden unos 8 pt y los nombres de nodo unos 10 pt. Los criterios para decidir si un informe de factibilidad lleva figura están en [factibilidad.md](tipos/factibilidad.md#necesita-un-diagrama). El ejemplo de alcance del proyecto añade `assets/diagrams/alcance-pagos.html` (tipo arquitectura con una zona de límite, sistema ficticio), con su SVG y su PNG a 3x. Su ancho de 588 unidades se escala a la columna de 168 mm, de modo que los rótulos miden unos 8 pt y los nombres de nodo unos 10 pt. No repite la arquitectura de la factibilidad: marca el perímetro (qué se construye, qué se ajusta, qué queda fuera y qué se excluye) con los códigos de la tabla de entregables. El criterio para decidir si un alcance lleva figura está en [alcance-proyecto.md](tipos/alcance-proyecto.md#necesita-un-diagrama). El registro de requerimientos no lleva figura; la razón está en [registro-requerimientos.md](tipos/registro-requerimientos.md#diagrama). El acta de capacitación tampoco: registra asistencia, contenidos y firmas, y el sistema ya está dibujado en la factibilidad y en el alcance; la razón está en [acta-capacitacion.md](tipos/acta-capacitacion.md#necesita-un-diagrama). El registro de riesgos no lleva figura: la matriz es la lectura del nivel, y el criterio está en [registro-riesgos.md](tipos/registro-riesgos.md#necesita-un-diagrama). La propuesta de servicio no lleva figura: la secuencia cabe en un párrafo, y la arquitectura y el perímetro ya están en otros documentos de la cadena. El criterio está en [propuesta-servicio.md](tipos/propuesta-servicio.md#necesita-un-diagrama). La especificación de requisitos no lleva figura: la ficha y la matriz son la lectura, y el criterio está en [especificacion-requisitos.md](tipos/especificacion-requisitos.md#necesita-un-diagrama). La ficha de modelo no lleva figura: quién decide y qué cifra caben en el texto y en las tablas. El criterio está en [ficha-modelo.md](tipos/ficha-modelo.md#necesita-un-diagrama). La evaluación de impacto en datos no lleva figura: el flujo de los datos ya está en la descripción de arquitectura y se cita por su código, y la matriz de riesgos es la lectura. El criterio está en [evaluacion-impacto-datos.md](tipos/evaluacion-impacto-datos.md#necesita-un-diagrama). La solicitud de cambio no lleva figura: el antes y el después caben en la tabla de impacto, y el criterio está en [solicitud-cambio.md](tipos/solicitud-cambio.md#necesita-un-diagrama). El plan de proyecto no lleva figura: la EDT es la lectura, y el criterio está en [plan-proyecto.md](tipos/plan-proyecto.md#necesita-un-diagrama). El traspaso a operación no lleva figura: la ventana y la reversa caben en el texto, y el criterio está en [traspaso-operacion.md](tipos/traspaso-operacion.md#necesita-un-diagrama). Las notas de versión no llevan figura: el resumen y la tabla de cambios son la lectura, y el criterio está en [notas-version.md](tipos/notas-version.md#necesita-un-diagrama).

El ADR `decision-arquitectura` no lleva figura: la comparación de opciones y sus consecuencias explica por qué se eligió la solución. `descripcion-arquitectura` sí lleva dos figuras: `contexto-arquitectura-pagos` añade actores y sistemas vecinos sin descomponer el módulo; `componentes-frontera-pagos` añade la captura de tarjeta en el dominio de la pasarela y el bloqueo de esa ruta antes de los servidores propios. Son composiciones nuevas, distintas de la factibilidad y del perímetro. Se siguió el flujo mínimo documentado de `diagram-design`, con HTML editable, validación sin red, exportación SVG con fuentes de sistema y PNG a 3x. Los viewBox son 600 × 352 y 600 × 496; las figuras se imprimen al ancho de columna y la segunda ocupa una página propia para conservar los rótulos. El verificador de geometría no está en la instalación y los conectores se revisaron a mano. Ver [descripcion-arquitectura.md](tipos/descripcion-arquitectura.md).

## Comandos y medidas

Los scripts de `diagram-design` se ejecutan desde su carpeta de instalación:

```sh
python3 <diagram-design>/scripts/self_check.py --offline esquema.html
python3 <diagram-design>/scripts/export_svg.py esquema.html esquema.svg --system-fonts
python3 <diagram-design>/scripts/export_png.py esquema.html esquema.png 3
```

La exportación a PNG usa Playwright, que debe estar disponible en el intérprete que ejecuta el script; si falta, exportar solo a SVG o decirlo en la entrega.

Medidas para una columna de 168 mm (476 pt):

- **Ancho.** Un `viewBox` de 580 a 600 unidades escala a unos 0,81 pt por unidad: rótulos de 10 unidades salen de unos 8 pt impresos y nombres de nodo de 12 unidades, de unos 10 pt. El preset de documento en línea de `diagram-design` mide 960 unidades de ancho y dejaría los rótulos en unos 5 pt: elegir el ancho antes de dibujar.
- **Alto.** Un bloque de figura con su pie mide el alto de la figura más unos 75 pt. En un documento compacto, unos 90 mm de figura o menos; una figura más alta pasa entera a la página siguiente y deja un hueco.
- **Contraste.** El trazo de los nodos externos o secundarios debe llegar a 3:1 sobre blanco; la opacidad predeterminada de la skin puede no alcanzarlo.

Tokens. `diagram-design` pide confirmar los tokens antes de dibujar. Los del documento son la identidad del JSON activo (`paper` blanco, `brand.ink`, `brand.accent`): si el encargo ya fija esa identidad, usarlos y decirlo en la entrega; si no, preguntar.

Geometría. El verificador de conectores (`verify-geometry.py`) existe en el repositorio fuente de `diagram-design` y puede faltar en la instalación. Si falta, revisar a mano que ningún conector cruce rótulos ni nodos y que cada flecha tenga un destino claro, y decirlo en la entrega.

Qué agrega. Cuando un documento anterior de la cadena ya dibuja el mismo sistema, la figura nueva responde a otra pregunta de lectura (por ejemplo, el perímetro del alcance frente a la arquitectura de la factibilidad). Si repetiría la misma figura, no se hace.

Otros puntos que cuestan tiempo si se descubren en medio del trabajo:

- **Intérpretes.** Los scripts de `diagram-design` pueden necesitar otro intérprete que el motor (por ejemplo, uno con Playwright, mientras el motor corre en un entorno con `reportlab`). Ejecutar cada script con el intérprete que tenga sus dependencias. La skill suele estar en la carpeta de skills del agente (por ejemplo, `~/.claude/skills/diagram-design` o `~/.codex/skills/diagram-design`).
- **Tokens por omisión.** Si el JSON no trae `brand.ink`, `brand.rule` o `brand.accent`, el motor usa `#17232F`, `#CED6DD` y `#155D86`. Esos son los valores del esquema. No se edita el `style-guide.md` de la instalación para un solo documento: los tokens se escriben en el HTML del esquema.
- **Tipografía.** Helvetica para los nombres y Courier para los subrótulos, como en los ejemplos de `assets/diagrams/`: son fuentes del sistema y no dependen de la red. Las fuentes remotas de la skill no se usan en un PDF.
- **Punto de partida.** Para un esquema de arquitectura, partir de `assets/diagrams/arquitectura-pagos.html` o de `alcance-pagos.html` y cambiar nodos, textos y tokens cuesta mucho menos que escribir el HTML desde cero. Las reglas de dibujo siguen siendo las de `diagram-design`.
- **Flujo completo y flujo mínimo.** El completo incluye la plantilla, los perfiles y la confirmación previa de `diagram-design`. El mínimo es su `SKILL.md`, la referencia del tipo, `export.md`, `self_check.py` y la exportación. Con el mínimo, decirlo en la entrega y no escribir «hecho con diagram-design» sin ese matiz.

## Cierre, baja y proceso

El `informe-cierre` no lleva figura: el balance y el traspaso de pendientes se leen en tablas. El `acta-baja` tampoco: el perímetro, las dependencias y la verificación no requieren repetir la arquitectura del sistema.

La `ficha-proceso` lleva `sipoc-proyectos`: cinco bloques de izquierda a derecha, con tabla equivalente. Agrega la relación de quien aporta la necesidad con quien recibe la entrega, frente a las vistas del módulo de pagos de otros tipos. El ejemplo sigue el flujo mínimo de `diagram-design` con la referencia flowchart adaptada al SIPOC del encargo, identidad del JSON, HTML editable, validación offline, SVG con fuentes del sistema y PNG a 3x. El viewBox es 600 × 100 y la letra de 12 unidades se imprime aproximadamente a 9,5 pt. Se revisaron a mano los cuatro conectores porque no está instalado el verificador de geometría. Ver [ficha-proceso.md](tipos/ficha-proceso.md).
