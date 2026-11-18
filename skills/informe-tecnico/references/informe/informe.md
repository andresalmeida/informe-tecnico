# Informe, manual o catálogo

Elegir `document.kind: "informe"` (es el valor por omisión) para explicar un sistema, documentar un trabajo, presentar resultados, escribir un manual de usuario, técnico o de operación, o un catálogo o diccionario de datos. Partir de `assets/plantilla-base.json`. Esta guía reúne lo que solo vale para este tipo; lo común a todos los tipos está en [SKILL.md](../../SKILL.md).

**Leer:** [redaccion.md](redaccion.md), [estructura.md](estructura.md), [apa.md](apa.md), [contrato.md](../contrato.md) y [composicion.md](composicion.md); [procedimientos.md](procedimientos.md) si hay pasos.

**Contenido:** antes de redactar, estructura base, formato del informe, procedimientos y avisos, fuente y evidencia, comprobar.

## Antes de redactar

Leer los archivos suministrados y revisar páginas representativas si hay PDF. Distinguir entre **recomponer contenido existente**, **actualizar una edición** y **redactar desde evidencia**. Conservar los originales. No convertir automáticamente todo un PDF cuando el encargo solo pide una plantilla.

Identificar audiencia, uso y clase documental: informe técnico de actividad o entrega, manual de usuario, técnico o de operación, evaluación solicitada, o catálogo o diccionario. Un encargo de «hacer un informe» produce por defecto un documento de presentación; no convertirlo en auditoría ni en relato de la investigación del agente. Leer [redaccion.md](redaccion.md) antes de redactar y [estructura.md](estructura.md) para seleccionar los módulos necesarios.

## Estructura base

Para un informe nuevo, partir de `assets/plantilla-base.json`: introducción, objetivos, alcance, **4. Desarrollo técnico**, resultados y validación, conclusiones y recomendaciones, y referencias. El trabajo principal y sus subsecciones pertenecen al capítulo 4. Los preliminares no consumen números de capítulo. Adaptar esta base cuando el usuario o una estructura institucional requieran otro orden.

## Formato del informe

Un informe nuevo parte de `assets/plantilla-base.json`, con `format.profile: "institucional-apa"`, el mismo perfil de todos los tipos: cuerpo justificado con sangría en la primera línea, interlineado 1,5, tablas y figuras con su rótulo y su nota, referencias con sangría francesa, títulos a la izquierda con numeración «1. Título» y mayúscula de oración. Con `format.heading_case: "title"` los títulos llevan mayúscula en cada palabra. Leer [apa.md](apa.md) para las medidas y los criterios de citas y referencias.

**Composición compacta.** `format.profile: "institucional"` da el aspecto anterior: interlineado sencillo, sin sangría ni justificado, tablas con cabecera de color. Se usa cuando el documento debe ocupar pocas páginas.

**APA estricto, solo si se exige.** El perfil mantiene la cabecera, la portada, los índices, los márgenes institucionales y los títulos a la izquierda; denominarlo **formato institucional con criterios APA 7**, no APA integral. Un encargo académico que exija doble interlineado y alineación izquierda fija `line_spacing: 2` y `justify: false`; si además exige títulos centrados o márgenes de 2,54 cm, el motor no lo cubre y hay que elegir otro.

Una fuente anterior sin `format` se compila con el perfil por omisión; para conservar su aspecto compacto, añadir `"profile": "institucional"`. Al actualizar un informe cuyo JSON fija `format.profile: "institucional"` (de una versión anterior), preguntar si pasa al perfil por omisión antes de compilar; un valor fijado a propósito se mantiene. Aplicar citas autor-fecha y referencias cuando se use material ajeno; conservar los códigos documentales dentro de su título o identificación. No inventar autores, fechas, DOI ni validaciones para completar una referencia. El formato APA no cambia la voz técnica ni convierte un informe de sistema en una revisión bibliográfica.

## Procedimientos y avisos

Para tareas de un manual o instrucciones de operación, leer [procedimientos.md](procedimientos.md). Los bloques opcionales `procedure` presentan condición inicial, acción y resultado esperado por paso; `notice` distingue nota, precaución para datos o equipos y advertencia para personas. Usarlos cuando aporten a la tarea, sin convertir resultados esperados en pruebas realizadas ni añadir avisos a todos los informes.

`assets/procedimientos-preview.png` muestra una página renderizada con un procedimiento y un aviso: usarla como referencia de escala y gramática, adaptando la identidad al encargo. La muestra del perfil original se conserva en `assets/ejemplo-preview.png`.

## Fuente y evidencia

- `assets/ejemplo.json` es una demostración ficticia, no hechos reutilizables sobre el usuario.
- Sustentar las afirmaciones en las fuentes disponibles y conservar su localización en los archivos de trabajo. En el documento, presentar referencias reconocibles por título o código existente (por ejemplo, `DOC-04`, apartado 3), sin rutas personales del equipo, hashes, nombres de temporales ni códigos de captura inventados como bibliografía.
- Mostrar archivos, tablas de base de datos o rutas operativas solo cuando ayuden a comprender o ejecutar el procedimiento solicitado.
- Distinguir un resultado realizado de una previsión, sin llenar el cuerpo de advertencias de auditoría.
- Añadir una figura solo si explica relaciones, estados o secuencias. Para esquemas nuevos de arquitectura, flujo, secuencia o datos, seguir [diagramas.md](../diagramas.md). No inventar arquitectura a partir de un catálogo.
- Repetir los encabezados de las tablas, conservar los códigos como texto y usar unidades explícitas. No modificar términos técnicos por estética.

## Comprobar

Además de la comprobación general de `SKILL.md`: revisar la redacción con [redaccion.md](redaccion.md); el destinatario debe leer sobre el sistema o la actividad, sin reconstruir cómo trabajó el agente. Comprobar títulos, pies, historial, referencias e índices: sin rutas de trabajo, notación `§`, etiquetas como `$1.2` ni marcadores sin resolver. En el perfil APA, comprobar la correspondencia entre citas y referencias, el orden alfabético, las cursivas y las sangrías; el motor no valida esos hechos bibliográficos.
