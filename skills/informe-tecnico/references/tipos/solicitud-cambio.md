# Solicitud de cambio

Elegir `document.kind: "solicitud-cambio"` cuando alguien pide cambiar un documento ya aprobado: un alcance, una propuesta aceptada o unos requisitos. Empezar por `assets/ejemplo-solicitud-cambio.json`. Diagrama: no lleva. El antes y el después caben en la tabla de impacto.

**Contenido:** Decidir antes de redactar; Completar cada campo; Cómo se escribe el impacto; Cómo se comprueba una solicitud; Personalizar; Qué no inventar; Texto de lo pendiente; Bloques opcionales; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

La estructura se orienta por la idea de una solicitud de cambio: lo que mueve el costo, el plazo o los entregables queda fuera del compromiso hasta que se acuerda; si cambia la viabilidad, se vuelve a la factibilidad; un defecto sobre lo ya acordado se corrige en el documento que lo contiene. No se reproduce el texto de un formulario ajeno ni el de una norma. El orden de los apartados es el del catálogo.

El PDF es compacto: título y contenido en la primera página, sin portada, de cuatro páginas en el ejemplo. El histórico de revisiones se imprime al final con `document.show_changes: true`. La decisión es una casilla de una sola marca. Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Índices.** El ejemplo no los lleva: con cuatro páginas, `contents` alargaría la apertura sin cambiar la lectura. Conviene `document.indexes: ["contents"]` cuando la solicitud pasa de siete páginas. `tables` cuenta la tabla de impacto. `figures` no se recomienda: el tipo no lleva figura.

## Decidir antes de redactar

1. **Qué se pide y sobre qué documento.** El pedido nombra el documento aprobado por código y versión. Lo que todavía no está aprobado no se modifica desde aquí: primero se aprueba.
2. **La decisión es una casilla.** Este tipo exige una elección marcada (`form: True` y `choice`). Es la decisión: una sola marca. En el ejemplo las opciones son Aprobada, Aprobada con condiciones, Diferida y Rechazada. La entidad puede cambiar las palabras en `options`. Sin esa casilla, o con la marca fuera de la lista, el motor rechaza el documento y dice qué añadir. La marca del ejemplo muestra el formulario. La fecha de firma sigue en Pendiente hasta que el acto conste.
3. **Qué entra al compromiso.** Aceptar, o aceptar con condiciones, cambia el compromiso. Diferir deja el pedido en el registro y fuera del compromiso. Rechazar cierra el pedido. Aceptar por fases pide un corte que conste; si no consta, esa opción no se marca.
4. **De dónde salen las cifras.** El antes sale del documento aprobado. El después es el compromiso que quedaría si la decisión se aplicara. Lo que nadie ha estimado se escribe `Por estimar`. La tabla puede mostrar dos lecturas y el título dice cuál es: el compromiso que se conserva con la decisión tomada (en una decisión diferida o rechazada, igual al antes) o el compromiso hipotético si el cambio se incluyera. Con una decisión diferida, el pedido va en una fila aparte, con `Por estimar`, para que no se lea como cero.

## Completar cada campo

La conclusión va primero dentro de cada campo.

1. **Información de referencia.** Número, proyecto, fecha, quién lo pide, documento aprobado que se modificaría (código y versión), prioridad y documentos relacionados por código.
2. **Cambio solicitado.** Qué se pide y por qué, en ese orden. Si el pedido repite una exclusión ya escrita, se cita esa frase.
3. **Análisis de impacto.** Alcance, plazo, esfuerzo, riesgos por código del registro, pruebas y documentos afectados. Las cifras numéricas van en el bloque `impact`. El cambio de alcance que es una frase, y no un número, se escribe en el párrafo.
4. **Opciones.** Una fila por camino, con su efecto en el compromiso. Las palabras pueden ser las del ejemplo u otras que la entidad use, alineadas con la casilla.
5. **Decisión.** La casilla, y una tabla de quién decide, quién reúne la información, a quién se consulta y a quién se informa. Esos cuatro papeles se nombran con persona y cargo de la cadena, o quedan Por confirmar si el rol no consta.
6. **Efecto en los documentos.** Cada código afectado y la versión o el estado que recibe. Un número que todavía no existe se escribe Por registrar.
7. **Firmas.** Quien pide, quien reúne y quien decide. La fecha que no ocurrió es Pendiente.

Los códigos siguen [codigos.md](../codigos.md). Este tipo usa `SCM`.

## Cómo se escribe el impacto

El bloque `impact` es la tabla de antes y después. Cada fila lleva `aspect`, `before`, `after` y `unit`. `before` y `after` son un número o exactamente `Por estimar`. La diferencia la calcula el motor: después menos antes. Si uno de los dos es `Por estimar`, la diferencia se imprime `Por estimar` y no entra en ninguna suma. El bloque no suma filas entre sí, porque las unidades pueden diferir.

No se escribe `difference`, `diferencia` ni `delta`. El motor los rechaza y dice qué quitar. Hasta 2 decimales. De 1 a 12 filas. El formato de número usa coma decimal y punto de miles, y no consulta el idioma del sistema.

En el ejemplo, el esfuerzo de esta fase sigue en 50 días-persona y la duración en 7 semanas, porque la decisión es Diferida. El esfuerzo del pedido queda `Por estimar`. Esas cifras son de demostración y salen de DEMO-FAC-01 y de DEMO-ALC-01.

## Cómo se comprueba una solicitud

- **Documento aprobado.** El código y la versión citados existen en la cadena, o el campo dice que todavía no.
- **Cifras.** El antes coincide con el documento aprobado. La diferencia impresa es después menos antes. Una fila en `Por estimar` se lee como hueco, no como cero.
- **Decisión y efecto.** La tabla de documentos dice lo mismo que la casilla. Una decisión diferida no cambia la versión del alcance.
- **Riesgos y pruebas.** Cada código de riesgo citado existe en el registro. Cada caso citado existe en el plan de pruebas. Un caso que habría que crear no se inventa: se dice que no hay caso.
- **Firmas.** Las fechas que no constan son Pendiente.

## Personalizar

Se cambian `brand.entity`, `brand.unit`, `brand.accent` y, si hace falta, `brand.logo`. El código sigue el prefijo de la entidad. `paper` admite `A4` y `Letter`. Las opciones de la decisión se reescriben en `options` y `selected` marca una de ellas. La unidad de cada fila de impacto es la de la entidad.

## Qué no inventar

- Una fecha de firma, un nombre de firmante o una aprobación que no conste. La marca del ejemplo es la decisión de demostración; la firma sigue en Pendiente.
- Un número de requerimiento nuevo. Mientras no exista la ficha, el efecto dice Por registrar.
- Una cifra de esfuerzo del pedido que nadie estimó. Va `Por estimar`.
- Un riesgo o un caso de prueba que el registro y el plan no tienen.
- Una viabilidad nueva. Si el pedido, al aceptarse, cambiara la viabilidad, el efecto remite a la factibilidad y no la reescribe aquí.

## Texto de lo pendiente

Pendiente, Por confirmar, Por estimar y Propuesto, quién puede firmar y el estado del documento están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Situación | Qué escribir |
|---|---|
| Esfuerzo, plazo o costo del pedido sin estimar | Por estimar, en el antes o en el después |
| Ficha de requerimiento que todavía no tiene número | Por registrar |
| Firma de la decisión | Pendiente |

## Bloques opcionales

- **Sin cifras todavía.** Se quita el bloque `impact` y el párrafo dice que el impacto numérico está por estimar. El resto de la solicitud se queda.
- **Sin índice.** El ejemplo no lleva `document.indexes`. Se añade `tables` cuando se quiere listar la tabla de impacto.

## ¿Necesita un diagrama?

No. La solicitud responde qué se pide, cuánto se mueve el compromiso y quién decide. Eso cabe en la tabla de impacto y en la casilla. Un esquema del sistema repetiría la factibilidad y el alcance.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** La apertura dice el pedido, el documento que se tocaría y la decisión. El análisis sostiene esa frase.
- **`unicorntext`.** Revisar el pedido y el efecto: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las frases de trámite. Conservar cifras, códigos, versiones y las palabras Pendiente y Por estimar.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py solicitud.json --output solicitud.pdf
python3 <skill>/scripts/check_report.py solicitud.pdf
pdftoppm -r 80 -png solicitud.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('solicitud.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que la casilla marcada sea la decisión, que la diferencia coincida con el después menos el antes y que el histórico comparta página con las firmas. Entregar el PDF, su manifiesto `.manifest.json` y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. Una tabla que cabe en una página no se parte. Los defectos habituales son un hueco al pie porque la tabla siguiente no cabe, y una página final con solo el histórico. El apartado de firmas se deja en esa página, con el histórico.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

Los saltos medidos de la muestra:

- La página 1 cierra con la frase de la diferencia. La tabla de impacto abre la página 2. El hueco queda por debajo de un tercio.
- La página 2 cierra con el párrafo de la decisión. La casilla abre la página 3. La marca es Diferida.
- La página 3 cierra con la tabla de documentos. El hueco queda por debajo de un tercio, porque las firmas no caben debajo y pasan enteras a la página 4.
- La página 4 reúne firmas e histórico. Debajo queda espacio libre: es el final del documento. El espacio de firma queda cerca del nombre.
