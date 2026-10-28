# Figuras y esquemas

Elegir por la pregunta: límites y componentes → arquitectura/contexto; decisiones → flujo; intercambio temporal → secuencia; entidades y cardinalidad → ER; cambios de estado → estados; responsables y entregas → carriles. Una lista de atributos corresponde a una tabla.

Herramienta preferida para esquemas nuevos: [diagram-design](https://github.com/cathrynlavery/diagram-design). Es una skill externa que se instala por separado, no una biblioteca de Python ni un motor invocado automáticamente por `build_report.py`. La skill del informe decide cuándo hace falta una figura, usa diagram-design para crearla y entrega el activo terminado al compilador.

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
