---
name: informe-tecnico
description: Crear y actualizar informes técnicos, manuales de sistemas y catálogos de datos con identidad institucional, control documental, índices automáticos y formato con criterios APA 7. Usar para documentación técnica formal y mantenible; no para propuestas comerciales ni presentaciones.
license: MIT
metadata:
  version: "0.4.0"
---

# Informe técnico institucional

Producir documentos técnicos listos para presentar a su destinatario, centrados en el sistema, el trabajo realizado o su uso. La identidad se configura; los datos se sustentan; la composición se verifica. Esta skill es una implementación propia inspirada en las referencias descritas en [fuentes.md](references/fuentes.md), no una norma ni una certificación.

## Composición con la skill de diagramas

`informe-tecnico` es la skill principal; `diagram-design` es una skill colaboradora instalada por separado. Cuando una sección necesita un esquema nuevo, cargar sus instrucciones y la referencia del tipo seleccionado, aplicar los tokens del informe y seguir [diagramas.md](references/diagramas.md). La principal proporciona propósito, evidencia, identidad y tamaño de impresión; la colaboradora produce HTML/SVG y su exportación estática. Después, la principal integra el activo como `figure`, resuelve referencias/índices y revisa el PDF.

Esta composición se ejecuta por el agente que lee ambas skills. El script Python recibe el activo terminado y no invoca skills por sí mismo. Un informe sin esquemas nuevos puede compilarse sin diagram-design. Si se necesita esa skill y falta, informar de la dependencia y resolver su instalación dentro del alcance autorizado o declarar una alternativa explícita. No copiar la skill externa dentro de esta ni atribuirle un esquema que no se haya producido con su flujo.

## Decidir antes de redactar

Leer los archivos suministrados y revisar páginas representativas si hay PDF. Distinguir entre **recomponer contenido existente**, **actualizar una edición** y **redactar desde evidencia**. Conservar los originales. No convertir automáticamente todo un PDF cuando el encargo solo pide una plantilla.

Identificar audiencia, uso y clase documental: informe técnico de actividad/entrega, manual de usuario/técnico/de operación, evaluación solicitada o catálogo/diccionario. Un encargo de «hacer un informe» produce por defecto un documento de presentación; no convertirlo en auditoría ni en relato de la investigación del agente. Leer [redaccion.md](references/redaccion.md) antes de redactar y [estructura.md](references/estructura.md) para seleccionar los módulos necesarios.

Para un informe nuevo, partir de `assets/plantilla-base.json`: introducción, objetivos, alcance, **4. Desarrollo técnico**, resultados/validación, conclusiones/recomendaciones y referencias. La faena principal y sus subsecciones pertenecen al capítulo 4. Los preliminares no consumen números de capítulo. Adaptar esta base cuando el usuario o una estructura institucional requieran otro orden.

Reutilizar logo, entidad, colores y metadatos proporcionados. Si faltan, avanzar con una identidad neutral explícita y estado Borrador; no inventar una entidad, responsable, fecha de aprobación o historial. Pedir únicamente los datos que bloqueen una entrega real. Separar la versión del documento, la del sistema descrito y la de esta skill.

## Formato institucional con criterios APA 7

Para documentos nuevos, usar `format.profile: "institucional-apa"` de la plantilla base y leer [apa.md](references/apa.md). Aplica doble interlineado, sangría inicial de 1,27 cm, alineación izquierda, referencias con sangría francesa, cursivas y títulos/notas de tablas y figuras. Mantiene la cabecera, portada, índices y márgenes institucionales; denominarlo **formato institucional con criterios APA 7**, no APA integral. Un encargo académico que exija APA estricto necesita adaptar también esas diferencias o elegir otro motor.

Las fuentes antiguas sin `format` conservan su maquetación. Al actualizar un informe, mantener su perfil salvo que se solicite la adaptación. Aplicar citas autor-fecha y referencias cuando se use material ajeno; conservar los códigos documentales dentro de su título o identificación. No inventar autores, fechas, DOI ni validaciones para completar una referencia. El formato APA no cambia la voz técnica ni convierte un informe de sistema en una revisión bibliográfica.

## Construir una fuente mantenible

Leer [contrato.md](references/contrato.md) para el esquema del motor y [composicion.md](references/composicion.md) para su tratamiento visual.

Para tareas de un manual o instrucciones de operación, leer [procedimientos.md](references/procedimientos.md). Los bloques opcionales `procedure` presentan condición inicial, acción y resultado esperado por paso; `notice` distingue nota, precaución para datos/equipos y advertencia para personas. Usarlos cuando aporten a la tarea, sin convertir resultados esperados en pruebas realizadas ni añadir avisos a todos los informes.

`assets/procedimientos-preview.png` muestra una página renderizada del perfil actual con un procedimiento y un aviso: usarla como referencia de escala y gramática, adaptando la identidad al encargo. La muestra anterior se conserva en `assets/ejemplo-preview.png`.

- Guardar contenido, identidad, fecha efectiva y revisión en un JSON editable. `assets/ejemplo.json` es una demostración ficticia, no hechos reutilizables sobre el usuario.
- Asignar identificadores estables a secciones, tablas y figuras. Referenciar con `{{ref:identificador}}`; no escribir números de página ni índices manuales. Conservar identificadores de catálogo existentes aunque se inserten otros nuevos.
- Sustentar afirmaciones en las fuentes disponibles y conservar su localización en los archivos de trabajo. En el documento presentar referencias reconocibles por título o código existente (por ejemplo, `AA_Act9_4`, apartado 3), sin rutas personales del equipo, hashes, nombres de temporales ni códigos de captura inventados como bibliografía. Mostrar archivos, tablas de base de datos o rutas operativas solo cuando ayuden a comprender o ejecutar el procedimiento solicitado. Distinguir un resultado realizado de una previsión sin llenar el cuerpo de advertencias de auditoría.
- Registrar cambios reales: versión, fecha efectiva, resumen, responsable y objetos afectados. Para una actualización, comparar con la edición anterior antes de redactar el historial. No cambiar la fecha por el mero hecho de exportar.
- Repetir encabezados de tablas, conservar códigos como texto y usar unidades explícitas. Un dato desconocido no equivale a cero. No modificar términos técnicos por estética.
- Añadir una figura solo si explica relaciones, estados o secuencias. Para esquemas nuevos de arquitectura, flujo, secuencia o datos, usar preferentemente la skill instalada `diagram-design`: leer su entrada, el tipo elegido y [diagramas.md](references/diagramas.md), que define el traspaso de identidad, fuente editable y salida estática al informe. No inventar arquitectura a partir de un catálogo.

## Renderizar

El motor de referencia usa Python 3, `reportlab`, `pypdf` y `pdfplumber`; las figuras SVG externas requieren `svglib`. Resolver el Python del entorno y usar las dependencias disponibles antes de instalar nada. No descargar fuentes ni logos por defecto.

```sh
python3 <skill>/scripts/build_report.py <documento.json> --output <informe.pdf>
python3 <skill>/scripts/check_report.py <informe.pdf>
```

El motor genera portada, encabezado institucional, fecha/versión/estado, `Página X de Y`, historial, contenido, índices condicionales de tablas/figuras/procedimientos, marcadores, referencias internas y manifiesto `.manifest.json`. Compila hasta estabilizar índices y total. Falla si una fila no cabe o un objeto carece de referencia; no reduce la letra silenciosamente.

Para un DOCX solicitado explícitamente, usar campos nativos de tabla de contenido, títulos y referencias cruzadas, además de PAGE/NUMPAGES en encabezados/pies. Recalcular los campos con una herramienta compatible y exportar/revisar el resultado. El motor incluido produce PDF, no DOCX. No entregar una maqueta de texto plano como equivalente editable.

## Comprobar y entregar

1. Revisar la redacción con [redaccion.md](references/redaccion.md): el destinatario debe leer sobre el sistema o la actividad, sin reconstruir cómo trabajó el agente. Comprobar también títulos, pies, historial, referencias e índices: sin rutas de trabajo, notación `§`, etiquetas como `$1.2` ni marcadores sin resolver. En el perfil APA, comprobar correspondencia entre citas y referencias, orden alfabético, cursivas y sangrías; el motor no valida esos hechos bibliográficos.
2. Ejecutar el comprobador: tamaño de papel, total de páginas, metadatos repetidos, destinos de índices, enlaces, texto fuera de márgenes y mínimo tipográfico. Es una comprobación parcial, no demuestra corrección técnica ni accesibilidad PDF/UA.
3. Renderizar **todas** las páginas con Poppler o un renderizador disponible. Revisar portada, historial, índices, texto, figuras, cada corte de tabla y última página. Abrir las imágenes; un comando exitoso no demuestra buena composición. Comprobar que no haya saltos consecutivos que produzcan una página solo con cabecera y pie.
4. Corregir colisiones, filas cortadas, títulos huérfanos y rótulos ilegibles. Redistribuir columnas, dividir figuras o usar una hoja apaisada justificada en otro motor antes de reducir tamaños. Tras cambios que afecten al flujo, recompilar y revisar los cortes nuevos.
5. Entregar PDF y fuente editable con los activos necesarios. Mantener inventarios, hashes, notas de revisión y localizadores personales en archivos de trabajo separados del documento de presentación. Resumir los pendientes que afecten realmente a la entrega, sin inventar validaciones ni aprobaciones.

Al modificar el motor, comprobar un documento que atraviese varias páginas de tabla, una referencia cruzada, índices que cambien al insertar contenido y un segundo perfil gráfico. No crear pruebas que solo comparen frases de esta skill.

`python3 <skill>/scripts/self_test.py` ejecuta esas comprobaciones con datos sintéticos y también rechaza IDs duplicados, referencias inexistentes y filas que no caben. Requiere Pillow además de las dependencias del motor.
