# Notas de versión

Elegir `document.kind: "notas-version"` para decir qué cambia en una versión ya entregada. Empezar por `assets/ejemplo-notas-version.json`. Usa `format.profile: "institucional"`, como los demás tipos compactos: el perfil APA es solo del `informe`. Diagrama: no lleva. El resumen y la tabla de cambios son la lectura.

No hay bloque nuevo. No se reproduce el texto de unas notas ajenas. El orden de los apartados es el del catálogo. Las firmas de esta entrega viven en el acta y en el traspaso: estas notas no piden otra firma.

El PDF es compacto: título y contenido en la primera página, sin portada, de dos páginas en el ejemplo. El histórico de revisiones se imprime al final con `document.show_changes: true`. No exige casilla. Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Índices.** El ejemplo no los lleva: con dos páginas, `contents` alargaría la apertura sin cambiar la lectura. Conviene `document.indexes: ["contents"]` cuando las notas pasan de siete páginas. `figures` no se recomienda.

## Decidir antes de redactar

1. **Qué versión es.** El número de la versión, la fecha y quién publica. En el ejemplo es la 1.0.0 del 08/01/2027, la misma fecha de DEMO-ENT-01 y de DEMO-TRA-01. La versión de la plataforma que sigue abierta queda Por confirmar.
2. **Qué entra y qué no.** El resumen dice lo más importante primero. Un pedido diferido, como DEMO-SCM-01, se nombra y no aparece en la tabla de cambios.
3. **De dónde sale cada cambio.** Cada fila lleva el tipo (nuevo, mejorado, corregido o retirado) y el identificador que lo originó: una tarea del tablero o una solicitud de cambio. Si el tablero todavía no tiene número, se escribe Por registrar.
4. **Qué sigue abierto.** Los problemas conocidos citan un riesgo o un pendiente que ya existe. El estado de las pruebas cita el plan por código y no adelanta un caso sin ejecutar.

## Completar cada campo

La conclusión va primero dentro de cada campo.

1. **Versión y fecha.** Producto, versión, fecha, quién publica y documentos relacionados por código.
2. **Cambios.** Una tabla con tipo, cambio y origen. Un tipo sin filas no se imprime.
3. **Compatibilidad y actualización.** Con qué sigue funcionando, qué no admite y los pasos para actualizar. El paso que depende de una ventana ya escrita cita esa ventana.
4. **Problemas conocidos.** Problema, dónde consta y estado. Solo códigos que existen.
5. **Estado de las pruebas.** El plan por código y una fila por caso, con el estado que ese plan trae.

Los códigos siguen [codigos.md](../codigos.md). Este tipo usa `NOV`.

## Cómo se comprueba unas notas

- **Fecha.** Coincide con la entrega de esa versión y no es anterior a la fecha del traspaso que la cita. Si el traspaso se escribió antes del paso a producción, las notas pueden ser posteriores a su fecha.
- **Origen.** Cada código citado existe. Una tarea sin número dice Por registrar y no se inventa el identificador.
- **Pedido diferido.** No se lista como cambio entregado.
- **Pruebas.** Si el plan tiene el caso sin ejecutar, la nota dice sin ejecutar. El certificado sigue pendiente.
- **Problemas.** El estado de cada riesgo es el del registro.

## Personalizar

Se cambian `brand.entity`, `brand.unit`, `brand.accent` y, si hace falta, `brand.logo`. El código sigue el prefijo de la entidad. `paper` admite `A4` y `Letter`. Los nombres de tipo de cambio pueden ser los de la entidad, con tal de que cada fila diga uno.

## Qué no inventar

- Una tarea, un caso ejecutado o un problema que los documentos anteriores no traen.
- Una firma de aceptación. Esas firmas están en la entrega y en el traspaso, y allí siguen en Pendiente.
- Una versión de plataforma distinta de Por confirmar.

## Texto de lo pendiente

Pendiente, Por confirmar y Por estimar están en [pendientes-y-estado.md](../pendientes-y-estado.md). Por registrar es el hueco de este tipo y de la solicitud de cambio: un número que todavía no existe.

| Situación | Qué escribir |
|---|---|
| Tarea del tablero sin número | Por registrar |
| Caso sin ejecutar | Sin ejecutar, y el certificado en Pendiente |
| Versión de plataforma o de API sin confirmar | Por confirmar |
| Problema de un riesgo abierto | El estado que trae el registro |

## Bloques opcionales

- **Sin un tipo de cambio.** No se añade una fila vacía de mejorado, corregido o retirado. Se quita la frase que los nombra si más adelante la versión sí los trae.
- **Sin apartado de problemas.** Si no hay ninguno citado, se quita el apartado. No se deja una tabla vacía.

## ¿Necesita un diagrama?

No. Lo que entra en la versión, lo que queda fuera y el estado de las pruebas caben en el resumen y en las tablas. El sistema ya está dibujado en otros documentos de la cadena.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** La primera frase dice qué entrega la versión y qué no entra. La tabla y los problemas sostienen esa frase.
- **`unicorntext`.** Revisar el resumen y la compatibilidad: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las frases de trámite. Conservar el número de versión, los códigos y las palabras Pendiente y Por confirmar.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py notas.json --output notas.pdf
python3 <skill>/scripts/check_report.py notas.pdf
pdftoppm -r 80 -png notas.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('notas.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que el resumen coincida con la tabla y que un caso sin ejecutar no aparezca como superado. Entregar el PDF, su manifiesto `.manifest.json` y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

Los saltos medidos de la muestra:

- La página 1 cierra con la tabla de cambios. El hueco queda por debajo de un tercio.
- La página 2 reúne la compatibilidad, los problemas, el estado de las pruebas y el histórico. El histórico no queda solo. Estas notas no llevan tabla de firmas: las firmas están en la entrega y en el traspaso.
