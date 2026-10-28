# Informe técnico institucional

Skill para crear informes técnicos, manuales de sistemas y catálogos de datos con una identidad configurable y control documental mantenible.

![Página de la muestra: desarrollo técnico y esquema de revisión](skills/informe-tecnico/assets/ejemplo-preview.png)

[Ver la muestra en PDF](docs/muestra-informe-tecnico.pdf) · [Leer la skill](skills/informe-tecnico/SKILL.md) · [Ver la plantilla base](skills/informe-tecnico/assets/plantilla-base.json)

Versión 0.3.0: [muestra del perfil institucional con criterios APA 7](docs/muestra-perfil-apa.pdf) · [fuente editable](skills/informe-tecnico/assets/ejemplo-apa.json) · [criterios y fuentes oficiales](skills/informe-tecnico/references/apa.md).

## Qué resuelve

- Entidad, logo, colores, líneas y marco configurables.
- Cabecera con fecha de actualización, versión y «Página X de Y»; entidad y paginación comparten el mismo separador vertical.
- Historial de cambios con identificadores estables y referencias enlazadas.
- Contenido e índices de tablas y figuras calculados al compilar.
- Tablas multipágina con títulos y encabezados repetidos.
- Figuras con fuente editable, número, pie y destino en el índice.
- Comprobación estructural del PDF y pruebas de regresión del motor.
- Redacción de presentación adaptada a informes y manuales, con referencias por nombre o código documental. Las rutas personales y la trazabilidad de autoría quedan en archivos de trabajo.
- Perfil institucional con criterios APA 7: interlineado doble, sangría inicial, referencias con sangría francesa, cursivas y presentación de tablas y figuras.

La muestra es ficticia. Los documentos institucionales que orientaron el diseño se describen en [fuentes](skills/informe-tecnico/references/fuentes.md); sus PDF y logos originales no forman parte del repositorio.

## Instalar en Codex

Pide al agente:

> Instala la skill informe-tecnico desde https://github.com/andresalmeida/informe-tecnico, ruta skills/informe-tecnico. Instala también diagram-design desde https://github.com/cathrynlavery/diagram-design, ruta skills/diagram-design, para crear los esquemas.

El instalador de skills de Codex también admite estos comandos, ejecutados en un entorno con Python y acceso a GitHub:

```sh
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo andresalmeida/informe-tecnico --path skills/informe-tecnico

python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo cathrynlavery/diagram-design --path skills/diagram-design
```

Las skills instaladas estarán disponibles en el siguiente turno de Codex. Si ya existe una instalación, revisa las diferencias antes de actualizarla.

## Uso

```text
Usa $informe-tecnico para preparar un informe sobre [tema] a partir de mis
archivos. Usa la identidad de [entidad] y coloca el trabajo principal en el
capítulo 4. Para los esquemas necesarios, aplica $diagram-design con los
mismos colores y tipografía.
```

La estructura base comprende preliminares y siete capítulos:

1. Introducción.
2. Objetivos.
3. Alcance.
4. **Desarrollo técnico:** el trabajo principal, dividido en 4.1, 4.2, etc.
5. Resultados.
6. Conclusiones y recomendaciones.
7. Referencias.

Los módulos se adaptan al tipo de documento y a las estructuras institucionales que deban preservarse. Consulta la [guía de estructura](skills/informe-tecnico/references/estructura.md).

La [guía de redacción](skills/informe-tecnico/references/redaccion.md) distingue un informe de actividad, un manual y una evaluación solicitada. El documento describe el sistema y el trabajo realizado con lenguaje técnico; no narra cómo lo investigó el agente. Las comprobaciones y los pendientes conservan su estado real.

## Formato con criterios APA 7

Los documentos nuevos parten de `format.profile: "institucional-apa"`: cuerpo de 11 pt, interlineado 2,0, sangría inicial de 1,27 cm y referencias con sangría francesa de 1,27 cm. Los títulos de tabla/figura se colocan encima, con número en negrita y título en cursiva. Las tablas usan líneas horizontales mínimas y celdas con interlineado sencillo.

Se conservan identidad, cabecera, portada, índices, márgenes institucionales y capítulos numerados. Es una adaptación para informes, no un formato académico APA integral. La [guía APA](skills/informe-tecnico/references/apa.md) identifica las diferencias y la atribución autor-fecha. Las fuentes antiguas sin `format` mantienen su composición; `profile: "institucional"` permite elegir expresamente el perfil original.

Los nuevos bloques `reference` y `quotation`, y los tramos `runs` para cursivas/negritas, están descritos en el [contrato](skills/informe-tecnico/references/contrato.md). El motor compone las entradas que se le suministran; la selección y verificación de autores, fechas y citas siguen siendo trabajo de autoría.

## Una skill coordina la otra

`informe-tecnico` y `diagram-design` se instalan por separado. El agente que aplica la principal carga la colaboradora cuando necesita crear un esquema:

| Paso | Responsable | Resultado |
| --- | --- | --- |
| Definir qué explicar y con qué evidencia | informe-tecnico | Propósito, datos, identidad y escala de impresión |
| Elegir representación y componer el esquema | diagram-design | HTML con SVG, validación y exportación estática |
| Integrar y comprobar el documento | informe-tecnico | Figura numerada, pie, referencias, índice y PDF revisado |

La integración es una instrucción de composición para el agente. El script `build_report.py` incorpora archivos terminados; no ejecuta otra skill ni instala dependencias automáticamente. La [guía de diagramas](skills/informe-tecnico/references/diagramas.md) define el flujo completo.

Para un informe que ya dispone de sus figuras, o que solo necesita texto y tablas, el motor PDF funciona sin diagram-design. Al cambiar de identidad gráfica, también se regeneran los esquemas externos desde su fuente editable.

## Ejecutar el motor sin el agente

Requiere Python 3.10 o posterior. Desde la raíz del repositorio:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python skills/informe-tecnico/scripts/build_report.py \
  skills/informe-tecnico/assets/ejemplo.json \
  --output output/muestra.pdf

python skills/informe-tecnico/scripts/check_report.py output/muestra.pdf
python skills/informe-tecnico/scripts/self_test.py
```

El motor genera el PDF y un manifiesto de compilación. Para crear un informe propio, copia `plantilla-base.json`, completa la identidad, los metadatos, el historial y el contenido, y conserva los activos junto a la fuente. Los campos obligatorios vacíos deben completarse antes de compilar.

La muestra incluye un esquema exportado a PNG para imprimir y sus fuentes HTML/SVG editables. Integrar otros SVG directamente requiere el paquete opcional `svglib` y revisión de su compatibilidad. Crear o regenerar esquemas con diagram-design usa sus herramientas y requisitos propios.

## Comprobaciones y límites

Las pruebas comprueban continuación de tablas, desplazamiento de destinos al crecer el índice, conservación de números de catálogo, ceros iniciales, otro perfil gráfico/papel y rechazo de referencias desconocidas, IDs duplicados, filas excesivas y cabeceras desalineadas.

La regresión APA mide en el PDF la sangría de 36 pt y la distancia de 22 pt entre líneas, la sangría francesa y el bloque de cita, además de cursivas, título sobre la imagen y continuación de tablas. No certifica cumplimiento APA integral ni exactitud de las referencias.

El motor incluido produce PDF A4/Carta en vertical. El contenido se mantiene en JSON editable; no genera DOCX. Las comprobaciones automáticas no verifican los hechos técnicos, las aprobaciones institucionales ni la conformidad PDF/UA. La entrega requiere abrir las páginas renderizadas y revisar su composición.

## Licencia y atribuciones

[MIT](LICENSE). El scaffold del ejemplo de diagrama conserva la [licencia y atribución de diagram-design](skills/informe-tecnico/assets/diagrams/LICENSE-diagram-design.txt). Las referencias de diseño y las decisiones de adaptación se conservan en [fuentes.md](skills/informe-tecnico/references/fuentes.md).
