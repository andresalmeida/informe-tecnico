# Registro de riesgos

Elegir `document.kind: "registro-riesgos"` para llevar el registro vivo de los riesgos de un proyecto: cada riesgo con su probabilidad, su impacto, el nivel que sale de ambos, la respuesta, el responsable y el estado. Empezar por `assets/ejemplo-registro-riesgos.json`. Diagrama: no lleva. La matriz de niveles ya es la lectura del apartado, y un esquema del mismo sistema repetiría la arquitectura de la factibilidad o el perímetro del alcance.

**Contenido:** Decidir antes de redactar; Completar cada campo; Cómo se trata un riesgo cerrado o materializado; Cómo se comprueba un registro; Personalizar; Qué no inventar; Qué se elimina cuando algo no aplica; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

Va con el informe de factibilidad ([factibilidad.md](factibilidad.md)) y sigue abierto mientras el proyecto avanza. El alcance ([alcance-proyecto.md](alcance-proyecto.md)) lo cita por su código cuando las condiciones de la aprobación son riesgos. El orden de los apartados es el del catálogo, para que se lea igual que los otros registros.

El PDF es compacto: título y contenido en la primera página, sin portada, de cinco páginas en el ejemplo (ocho riesgos). No tiene casillas. El histórico de revisiones se imprime al final con `document.show_changes: true`. El esquema del bloque `risks` está en [risks.md](../contrato/risks.md). Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Índices.** El ejemplo no los lleva: con cinco páginas, `contents` alargaría la apertura sin cambiar la lectura. Conviene `document.indexes: ["contents"]` cuando el registro pasa de siete páginas, por muchos riesgos o por un seguimiento largo. `tables` y `figures` no se recomiendan: las tablas son la matriz, el resumen, el seguimiento y las firmas, y el tipo no lleva figura.

## Decidir antes de redactar

1. **Qué se registra y para quién.** El registro lo usa quien conduce el proyecto. Cada riesgo sale de un documento citado (la factibilidad, el alcance, un acuerdo con fecha) o de un hecho ya observado. Una preocupación sin fuente no entra.
2. **Con qué base se valora.** Este tipo no tiene casillas: su regla en el motor es la de un formulario sin elecciones (`form: True`, sin `choice`). La decisión de más peso es el nivel, y no se escribe: el motor lo toma de la celda donde se cruzan la probabilidad y el impacto en la matriz que trae el propio documento. Quien responde del proyecto decide esa matriz. El motor aplica la celda tal como está escrita, sin otra fórmula.
   Si la matriz aún no está acordada, `document.status` es «Borrador» y el párrafo de la información de referencia lo dice: «Escala propuesta, por confirmar con quien conduce el proyecto.»
   - La base, de mayor a menor peso: un hecho ya observado en una prueba citada; un riesgo, un supuesto o una restricción escritos en la factibilidad o en el alcance; el juicio de quien conduce el proyecto, declarado como tal.
   - La probabilidad y el impacto se eligen de la escala del documento. Una etiqueta nueva se añade a la escala, no se cuela en un riesgo.
   - Lo que nadie ha asignado (responsable, próxima revisión, respuesta) queda «Por confirmar».
3. **Quién mantiene el registro y quién lo firma.** La responsable del registro lo actualiza en cada corte. Las firmas son de responsabilidad del documento (elaboró, revisó, aprobó). La parte solicitante no firma este registro: es interno.
4. **Qué escala usar.** Tres etiquetas por eje cuando basta con separar bajo, medio y alto, que es el caso de un solo módulo con pocos riesgos. Cinco cuando la organización ya trabaja con cinco peldaños, o cuando muchos riesgos caerían en la misma celda y el equipo necesita separar los extremos. El ejemplo usa tres por eje: con eso la matriz ya distingue bajo, medio, alto y crítico. Escribir las etiquetas de menor a mayor. El motor no interpreta el significado de la palabra: la primera etiqueta es la primera fila o la primera columna.
5. **El código.** Usar el prefijo y la numeración de la entidad (`DEMO-RIE-01` en el ejemplo). Es `document.code` y aparece en el pie. El registro cita el código de la factibilidad o del alcance, y el del requerimiento.

## Completar cada campo

La conclusión va primero dentro de cada campo. Un riesgo se redacta en tres campos, y los tres hacen la descripción: la causa (por qué puede ocurrir), el evento (qué ocurre) y la consecuencia (qué le cuesta al proyecto). Una ficha sin uno de los tres no se entiende.

1. **Información de referencia.** Un párrafo que dice si el registro está abierto y con qué documento se abrió. Después, una cuadrícula: número de registro (el código del documento), fecha de corte, proyecto, requerimiento, documento relacionado, responsable del registro, fecha de la próxima revisión y versión, que coincide con `document.version`. La fecha de corte es `document.date`. La próxima revisión, cuando consta, es posterior al corte; si nadie la fijó, queda «Por confirmar».
2. **Análisis de riesgos del proyecto.** Agrupa criterios y matriz, registro de riesgos (2.1) y resumen por nivel (2.2), con títulos que describen cada lectura. Un solo bloque `risks`. El motor imprime, desde esos mismos datos, la frase de las escalas, la matriz, la frase de respuestas y estados, el registro y el resumen. No se copia la matriz en una tabla escrita a mano: si la matriz y el cálculo se separan, dejan de ser la misma fuente.
   - **Escala y matriz.** `scale.probability` y `scale.impact` tienen de 3 a 5 etiquetas distintas, no vacías, en el orden de menor a mayor. `scale.matrix` tiene una fila por probabilidad y una columna por impacto. La celda es la etiqueta del nivel. Las etiquetas del nivel las decide quien escribe la matriz; pueden repetirse de una celda a otra.
   - **Registro de riesgos** (2.1). El motor numera este apartado debajo del análisis. Cada elemento de `items` lleva `id` (empieza por letra; se cita con `{{ref:id}}`), `cause`, `event`, `consequence`, `probability`, `impact`, `response`, `action`, `owner` y `state`. No lleva nivel: si se escribe `level` o `nivel`, el motor rechaza el documento y dice que se quite. La ficha imprime «Nivel:» con el valor calculado. La respuesta, por omisión, es Mitigar, Transferir, Aceptar o Evitar. El estado, por omisión, es Abierto, En mitigación, Materializado o Cerrado. Para usar otras palabras, reemplazar `responses` o `states` enteras. Si se reemplaza `states`, hay que indicar `open_states`: los estados que el resumen cuenta como abiertos.
   - **Mapa de calor.** La matriz sale coloreada del verde al rojo según el orden en que escribes los niveles, y cada celda lista los riesgos abiertos que le tocan; escribir la matriz de menor a mayor gravedad. La ficha pinta su nivel con el mismo color.
   - **Resumen por nivel** (2.2). El motor cuenta, por cada nivel de la matriz y en el orden en que las etiquetas aparecen, cuántos riesgos están en un estado de `open_states`. Por omisión cuenta Abierto y En mitigación. Un riesgo cerrado o materializado sigue en su ficha y queda fuera de ese recuento, salvo que se añada su estado a `open_states`.
3. **Seguimiento.** Cuándo se revisa (la fecha ya dicha en la referencia), quién y qué se hizo con los riesgos que cambiaron de estado. Una tabla con el riesgo (su `{{ref:id}}`), qué cambió, la fecha y quién lo registró. La fecha de un cambio no es posterior al corte. Si en el corte no cambió ningún riesgo, se quita la tabla y queda un párrafo que lo dice. En el ejemplo el apartado abre página, para que la tabla, las firmas y el histórico queden juntos.
4. **Firmas de responsabilidad.** Una fila por función (elaboró, revisó, aprobó) con nombre, cargo, espacio de firma y fecha. El histórico sale de `changes`, no se redacta otra tabla.

## Cómo se trata un riesgo cerrado o materializado

- **Cerrado.** La respuesta ya se aplicó y el evento no pide más acción. La ficha se queda, con su nivel calculado y el estado Cerrado. El resumen de abiertos no lo cuenta. El seguimiento dice la fecha, quién lo cerró y qué hecho lo cierra. No se borra: un corte posterior tiene que poder ver por qué salió del recuento.
- **Materializado.** El evento ya ocurrió. La ficha se queda con ese estado. Por omisión no entra en el recuento de abiertos. Si todavía hay que actuar, se pasa a En mitigación cuando la respuesta está en curso, o se añade Materializado a `open_states` si el equipo quiere verlo en el resumen. El seguimiento registra el día en que se materializó.

La matriz propone el nivel y quien conduce el proyecto decide la matriz. Cerrar un riesgo o darlo por materializado es una decisión de esa persona, anotada en el seguimiento, no un efecto automático del motor.

## Cómo se comprueba un registro

- **Origen.** Cada riesgo remite a un documento o a un hecho citado. Una probabilidad sacada de un juicio se declara como juicio de quien conduce el proyecto.
- **Descripción.** Cada ficha tiene causa, evento y consecuencia, y las tres hablan del mismo riesgo.
- **Nivel.** Coincide con la celda de la matriz para esa probabilidad y ese impacto. Si no coincide, el motor no se ha usado: el nivel no se escribe a mano.
- **Resumen.** La suma de la columna de abiertos es el total, y cada identificador de esa columna está en una ficha con un estado de `open_states` y ese nivel. Un cerrado no aparece en la columna.
- **Fechas.** Requerimiento, apertura del registro, corte (`document.date`) y próxima revisión, en ese orden. La próxima revisión, cuando consta, es posterior al corte; si nadie la fijó, queda «Por confirmar». Un cambio de estado cae entre la apertura y el corte.
- **Coherencia.** El número de registro coincide con el código del documento, la versión del campo con `document.version`, y los nombres y cargos son los mismos en las fichas, el seguimiento y las firmas.

## Personalizar

- `brand.entity`, `brand.unit` (pie de página), `brand.accent` y `brand.logo` (PNG o JPEG con ruta relativa al JSON; sin logo se imprime el nombre de la entidad). `brand.fonts` solo con licencia verificada.
- `document.code` con el prefijo propio, `document.short_title` para la cabecera y `document.paper` (`A4` o `Letter`).
- Etiquetas de `scale.probability`, `scale.impact` y las celdas de `scale.matrix`. Reemplazar `responses` y `states` cuando la entidad use otras palabras. Al cambiar `states`, indicar `open_states`.
- Títulos del bloque, si hacen falta: `matrix_title`, `register_title`, `summary_title` y `summary_table_title`. `summary_id` si se quiere un identificador propio para la tabla del resumen.
- Responsable del registro y firmantes.

## Qué no inventar

El nivel de un riesgo. Una probabilidad o un impacto que la base no sostiene. Un evento materializado que ningún documento citado registra. Firmas y fechas de firma. El nombre de un responsable que no consta. La fecha de la próxima revisión, si nadie la fijó. Que un riesgo esté cerrado porque la respuesta parece razonable, sin el hecho que lo cierra.

Las palabras para lo que falta (Pendiente, Por confirmar, Por estimar, Propuesto), quién puede firmar, el estado del documento, las fechas y el historial de un documento nuevo están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Dato | Texto |
|---|---|
| Responsable de un riesgo que nadie ha asignado | Por confirmar |
| Fecha de la próxima revisión que nadie ha fijado | Por confirmar |
| Respuesta aún no elegida | Por confirmar, y se añade esa etiqueta a `responses` |
| Estado de una condición citada que sigue sin cumplirse | Pendiente |
| Riesgo cuya probabilidad el equipo todavía no valora | Propuesto, por confirmar con quien conduce el proyecto |
| Apartado de seguimiento cuando ningún riesgo cambió de estado | Se quita la tabla y queda un párrafo |

## Qué se elimina cuando algo no aplica

- **Sin cambios de estado.** Se quita la tabla del seguimiento y la frase que anuncia esos cambios. Queda un párrafo: el corte no modificó ningún riesgo. La sección se conserva.
- **Otras respuestas o estados.** Se reemplazan las listas. Un riesgo no puede usar una etiqueta que la lista no tenga: el motor lo rechaza y nombra la etiqueta.

## ¿Necesita un diagrama?

No. La pregunta del registro es qué nivel tiene cada riesgo, y eso lo responde la matriz impresa desde los mismos datos que usa el cálculo. La arquitectura del módulo ya está en el informe de factibilidad y el perímetro en el alcance. Una figura nueva de este tipo repetiría una de esas dos lecturas. Si un registro futuro necesita un esquema de otra cosa (por ejemplo, la cadena de escalado), se añade con [diagramas.md](../diagramas.md) y se dice aquí.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** Abrir cada apartado con la conclusión: en la referencia, si el registro está abierto y con qué documento; en cada ficha, el evento y su nivel calculado ya van en la cabecera, y la acción dice qué se hace. Se conserva el orden de los apartados.
- **`unicorntext`.** Revisar el párrafo de apertura, las causas y las acciones: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las frases de trámite. Conservar los tres campos de la descripción, las etiquetas de la escala, los códigos, las fechas y los responsables.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py riesgos.json --output riesgos.pdf
python3 <skill>/scripts/check_report.py riesgos.pdf
pdftoppm -r 80 -png riesgos.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('riesgos.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que cada ficha esté entera, que el nivel de la ficha sea la celda de la matriz, que el resumen no cuente un riesgo cerrado y que las firmas queden enteras, junto al histórico, en el cierre. Entregar el PDF, su manifiesto `.manifest.json` (el comprobador lo exige junto al PDF) y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. Una ficha que cabe en una página no se parte. Los defectos habituales son:

- **Hueco al pie de una página**, porque una tabla, una ficha o una figura entera pasó a la siguiente. No se corrige recortando texto, juntando filas ni quitando datos: el contenido manda y el número de páginas no es una meta. El motor parte una tabla entre filas cuando moverla dejaría más del 35 % de la página en blanco; una ficha o una figura se queda entera. Un hueco así no se arregla: solo se reporta si estorba la lectura.
- **El seguimiento en su propia página.** En la muestra el apartado abre la página 5 (`new_page`), con la tabla de cambios, las firmas y el histórico juntos. La página 4 cierra con el resumen y deja el hueco que eso produce. Quitar el salto metería el título del seguimiento al pie de la 4 y dejaría la tabla en la 5.
- **Una página final con solo el histórico de revisiones.** Es posible: si las firmas, la remisión y el histórico no caben juntos y moverlos dejaría más del 35 % de la página en blanco, el histórico va solo en la última página. No se corrige acortando secciones anteriores ni con `new_page`.
- **Una ficha más alta que la página.** El motor la parte por filas. Se acorta la acción o la consecuencia antes de dejar una ficha cortada.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.
