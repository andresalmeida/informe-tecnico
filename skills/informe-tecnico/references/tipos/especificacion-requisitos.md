# Especificación de requisitos

Elegir `document.kind: "especificacion-requisitos"` para decir, de forma verificable, qué debe hacer y cumplir un sistema. Cada requisito se traza hasta su origen y hasta la prueba que lo comprueba. Empezar por `assets/ejemplo-especificacion-requisitos.json`. Diagrama: no lleva. Los requisitos se leen en fichas y la trazabilidad en una tabla. Un esquema del sistema repetiría la arquitectura de la factibilidad o el perímetro del alcance.

**Contenido:** Decidir antes de redactar; Cómo se escribe un requisito; Qué se hace con un hueco; Completar cada campo; Cómo se comprueba una especificación; Personalizar; Qué no inventar; Qué se elimina cuando algo no aplica; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

Va después del alcance ([alcance-proyecto.md](alcance-proyecto.md)) y cita el registro de requerimiento ([registro-requerimientos.md](registro-requerimientos.md)), la factibilidad ([factibilidad.md](factibilidad.md)) y el plan de pruebas ([plan-pruebas.md](plan-pruebas.md)) por su código. El orden de los apartados es el del catálogo. La estructura se orienta por la idea de una especificación de requisitos (ISO/IEC/IEEE 29148, que sucede a IEEE 830): referencia, propósito, partes interesadas, requisitos, restricciones y trazabilidad. No se reproduce el texto de esa norma ni se afirma de ella nada que no esté en esta guía.

El PDF es compacto: título y contenido en la primera página, sin portada, de siete páginas en el ejemplo. No tiene casillas. El histórico de revisiones se imprime al final con `document.show_changes: true`. El esquema del bloque `requirements` está en [requirements.md](../contrato/requirements.md). Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Índices.** El ejemplo no los lleva: con siete páginas, `contents` alargaría la apertura sin cambiar la lectura. Conviene `document.indexes: ["contents"]` cuando la especificación pasa de siete páginas. `tables` cuenta la matriz de trazabilidad. `figures` no se recomienda: el tipo no lleva figura.

## Decidir antes de redactar

1. **Qué se especifica y para quién.** Quien construye y quien acepta leen el mismo enunciado. Cada requisito sale de un documento citado: el registro de requerimiento, un objetivo o un criterio del alcance, o una condición ya escrita. Una idea sin fuente no entra.
2. **Con qué base se cierra.** Este tipo no tiene casillas: su regla en el motor es la de un formulario sin elecciones (`form: True`, sin `choice`). La decisión de más peso es el conjunto de requisitos aprobados, y se escribe. El motor no elige la prioridad ni el método: comprueba que la etiqueta esté en la lista del bloque y arma la matriz con los mismos campos de la ficha.
3. **Funcionales y no funcionales, en dos bloques.** Van en apartados distintos, cada uno con su bloque `requirements`. Un solo bloque con un campo de tipo metería los dos grupos en el mismo sitio, y entre ellos están las restricciones. La matriz es un tercer bloque, con `matrix: true` y sin `items`, colocado después. Sale de los dos bloques anteriores. Así la tabla no puede contradecir las fichas.
4. **Quién aprueba.** Las firmas son de responsabilidad del documento. La fecha de aprobación de un documento nuevo es «Pendiente».

## Cómo se escribe un requisito

Un requisito está terminado cuando cumple estas cuatro condiciones a la vez:

- **Necesario.** Si se quita, el sistema deja de cumplir el origen citado.
- **Singular.** Una sola exigencia. El enunciado empieza por «El sistema debe» y es una sola oración. Si el origen junta dos condiciones, se escriben dos requisitos y los dos pueden citar el mismo caso.
- **Sin ambigüedad.** Un lector que no estuvo en la reunión entiende qué hay que construir. No se usan «adecuado», «rápido» ni «si procede» para tapar un número que ya consta en el origen.
- **Verificable.** Tiene método y caso, o dice «Por definir» de forma explícita porque todavía no existen.

La prioridad sale de la lista del bloque. Por omisión: Alta, Media y Baja. Alta cuando el origen es el pedido o un criterio de aceptación. Media cuando el requisito puede esperar a una versión posterior sin impedir la aceptación. Baja cuando es conveniente y el origen no lo exige para aceptar. Una etiqueta nueva se añade a `priorities`, no se cuela en un requisito. Si quien pide no confirmó la prioridad (por ejemplo, el registro de requerimiento la dejó «Por confirmar»), se añade «Por confirmar» a `priorities` y se usa en esos requisitos: no se marca «Alta» por costumbre.

El método sale de la lista. Por omisión: Prueba, Inspección, Análisis, Demostración y Por definir. La prueba ejecuta el sistema. La inspección mira código, registros o un documento. El análisis examina un resultado ya medido. La demostración recorre el flujo delante de quien acepta.

El estado sale de la lista. Por omisión: Propuesto, Aprobado y Rechazado. `verified_states` dice cuáles exigen método, caso y entregable distintos de «Por definir». Por omisión solo Aprobado. Un requisito en ese estado sin método, sin caso o con el entregable en «Por definir» hace que el motor rechace el documento.

## Qué se hace con un hueco

«Por definir» es un hueco escrito a propósito. Va en el método, en los casos o en el entregable cuando ese dato todavía no existe. En los casos se escribe exactamente `["Por definir"]`, no mezclado con un identificador. La ficha lo muestra y la matriz repite la misma celda. Quien lee un hueco no da el requisito por terminado: pide el caso, el método o el entregable, o deja el estado fuera de `verified_states`. Un requisito Aprobado no admite ese hueco.

## Completar cada campo

La conclusión va primero dentro de cada campo.

1. **Información de referencia.** Número, sistema, versión del producto y los documentos relacionados por código. La versión del producto que nadie ha asignado es «Por confirmar». La versión del documento va en `document.version`.
2. **Propósito, alcance y definiciones.** Qué cubre y qué queda fuera, en una frase cada cosa. El glosario solo entra si una palabra del documento no se entiende sin él. Si todas se entienden, se quita la tabla.
3. **Partes interesadas y usuarios.** Una fila por parte, con su necesidad principal. El nombre que no consta es «Por confirmar».
4. **Requisitos funcionales.** Un bloque `requirements` con `items`. Cada elemento lleva `id`, `statement`, `priority`, `source`, `method`, `tests`, `deliverable` y `state`. El `id` es estable (`RF-01`) y se puede citar con `{{ref:id}}`.
5. **Requisitos no funcionales.** Otro bloque, con sus propios `id` (`RNF-01`). Rendimiento, seguridad, fiabilidad, compatibilidad y conciliación viven aquí cuando el origen los trae como criterios medibles.
6. **Restricciones, supuestos y dependencias.** Lo que limita la solución y no es un requisito de comportamiento: moneda, ventana de despliegue, plazo aún no acordado, versión de una API, una capacitación citada por su código.
7. **Trazabilidad.** Un bloque `requirements` con `matrix: true`, `id` y `title`, sin `items` y sin filas. El motor imprime una fila por requisito, en el orden de los bloques anteriores: identificador, fuente, entregable, casos, método y estado. Esos valores son los de la ficha. Una matriz escrita a mano (`rows`, `headers`, `matrix_rows` o `trazabilidad`) se rechaza.
8. **Aprobación.** Tabla de firmas de responsabilidad e histórico. La fecha que no ocurrió es «Pendiente».

Los códigos de documento siguen [codigos.md](../codigos.md). Este tipo usa `ERS`.

## Cómo se comprueba una especificación

- **Una sola fuente.** La celda de la matriz coincide con la ficha del mismo id. Si no coincide, sobra un texto escrito a mano: se borra y se deja el bloque.
- **Casos y entregables.** Cada caso citado, distinto de «Por definir», existe en el plan de pruebas. Cada entregable citado, distinto de «Por definir», existe en el alcance.
- **Aprobado.** Método, caso y entregable están cubiertos. «Por definir» en un estado de `verified_states` no compila.
- **Ids.** No se repiten entre fichas ni con el id de un bloque o de una sección.
- **Fechas.** El alcance, luego esta especificación. El plan de pruebas puede ser del mismo día o del día anterior si los casos ya estaban escritos: la especificación los cita, no los adelanta.
- **Coherencia.** Nombres, cargos, cifras y condiciones coinciden con los documentos citados. El plazo que sigue en «Por confirmar» no se convierte aquí en un número.

## Personalizar

- `brand.entity`, `brand.unit`, `brand.accent` y `brand.logo` (ruta relativa al JSON; sin logo se imprime el nombre). `brand.fonts` solo con licencia verificada.
- `document.code`, `document.short_title` y `document.paper` (`A4` o `Letter`).
- `priorities`, `methods`, `states` y `verified_states`. Si se cambia `states`, hay que indicar también `verified_states`.
- Rótulos de las partes y firmantes.

## Qué no inventar

Un requisito cuyo origen no está en los documentos citados. Un caso de prueba que el plan no tiene. Un entregable que el alcance no tiene. Una prioridad o un método fuera de la lista, para «cerrar» la ficha. Una firma o una fecha de aprobación. El texto de una norma. La versión del producto, si nadie la dio: va en «Por confirmar».

Pendiente, Por confirmar y Propuesto, quién puede firmar y el estado del documento están en [pendientes-y-estado.md](../pendientes-y-estado.md). «Por definir» es el hueco de este tipo: va en el método, en los casos o en el entregable, y la tabla siguiente dice cuándo se usa. Lo propio de este tipo:

| Dato | Texto |
|---|---|
| Fecha de aprobación aún no ocurrida | Pendiente |
| Versión del producto sin asignar | Por confirmar |
| Caso, método o entregable que todavía no existe | Por definir, y el estado fuera de verified_states |
| Requisito aún no aceptado | Propuesto |

## Qué se elimina cuando algo no aplica

- **Sin glosario.** Se quita la tabla. El apartado de propósito conserva el párrafo.
- **Sin requisitos de un grupo.** Se quita ese bloque y, si el apartado queda vacío, el apartado entero. La matriz sigue saliendo de los bloques que queden. Hace falta al menos un bloque con `items` antes de la matriz.
- **Sin huecos.** No se escribe «Por definir» para rellenar. Si el caso ya existe, se cita su id.

## ¿Necesita un diagrama?

No. Quien lee tiene que ver el enunciado, la fuente y el caso. Eso lo dan la ficha y la matriz. La arquitectura está en la factibilidad y el perímetro en el alcance. Una figura de esta especificación repetiría una de esas lecturas.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** El propósito abre con lo que el sistema debe lograr y lo que queda fuera. Cada requisito sostiene una parte de esa frase. Se conserva el orden de los apartados.
- **`unicorntext`.** Revisar el propósito y los enunciados: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las frases de trámite. Conservar umbrales, códigos, nombres y la palabra Por definir.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py especificacion.json --output especificacion.pdf
python3 <skill>/scripts/check_report.py especificacion.pdf
pdftoppm -r 80 -png especificacion.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('especificacion.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que ninguna ficha quede partida, que la matriz repita los mismos casos y entregables que las fichas, y que el histórico no ocupe una página solo. Entregar el PDF, su manifiesto `.manifest.json` y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. Una ficha que cabe en una página no se parte. Los defectos habituales son:

- **Hueco al pie de una página**, porque una tabla, una ficha o una figura entera pasó a la siguiente. No se corrige recortando texto, juntando filas ni quitando datos: el contenido manda y el número de páginas no es una meta. El motor parte una tabla entre filas cuando moverla dejaría más del 35 % de la página en blanco; una ficha o una figura se queda entera. Un hueco así no se arregla: solo se reporta si estorba la lectura.
- **El título de un apartado al pie y su tabla en la página siguiente.** Se abre el apartado en la página de la tabla.
- **Una página final con solo el histórico de revisiones.** Es posible: si las firmas, la remisión y el histórico no caben juntos y moverlos dejaría más del 35 % de la página en blanco, el histórico va solo en la última página. No se corrige acortando secciones anteriores ni con `new_page`.

En la muestra medida:

- La página 3 cierra con el título de los requisitos no funcionales, su párrafo y la frase de etiquetas. La primera ficha de ese apartado abre la página 4. El título no queda solo.
- La página 5 cierra con las restricciones y deja un hueco mayor que un tercio, porque la matriz no cabe debajo y se mantiene entera en la página 6, con la fila de RF-07 en Por definir.
- La página 7 reúne la aprobación, las firmas y el histórico. Debajo queda espacio libre: es el final del documento.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.
