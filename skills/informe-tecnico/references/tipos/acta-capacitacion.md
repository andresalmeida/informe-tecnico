# Actas de capacitación

Elegir `document.kind: "acta-capacitacion"` para dejar constancia de una capacitación dada a quienes usarán un sistema ya construido: quién la dio, cuándo y cómo, con qué objetivos y contenidos, qué asistentes firmaron, qué materiales recibieron, cómo evaluaron la sesión y quién certifica que se realizó. Empezar por `assets/ejemplo-acta-capacitacion.json`; al compilarlo se obtiene la muestra. Diagrama: no, porque quien lee el acta comprueba asistencia, contenidos y firmas, y no necesita ver componentes (ver «¿Necesita un diagrama?»).

**Contenido:** Decidir antes de redactar; Completar cada campo; Cómo se comprueba un acta de capacitación; Personalizar; Qué no inventar; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

Va después de construir y probar el sistema, y normalmente antes del acta de entrega y recepción ([acta-entrega.md](acta-entrega.md)). No describe el sistema ni repite el alcance: dice qué parte de lo que el sistema hace se enseñó a quién. Los rótulos de las partes son los de `alcance-proyecto`: **parte solicitante** es quien recibe la capacitación y **equipo ejecutor** es quien la da, y cada entidad los reemplaza por los suyos (ver «Personalizar»).

El PDF es compacto: título y contenido en la primera página, sin portada y sin índices (la opción `document.indexes` existe, pero un acta de pocas páginas no la necesita). Son cuatro páginas en el ejemplo, con ocho filas de asistentes; de diez a veinte filas son cinco, y con treinta, seis. La modalidad es una casilla de una sola marca y los materiales entregados son una lista de casillas de varias marcas. La tabla de asistentes lleva filas en blanco para firmar y la de evaluación, celdas en blanco. El histórico de revisiones se imprime al final con `document.show_changes: true`. El esquema de los bloques `fields` (con la elección múltiple), `table` y `show_changes` está en [fields.md](../contrato/fields.md), [secciones.md](../contrato/secciones.md) y [raiz.md](../contrato/raiz.md). Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

## Decidir antes de redactar

1. **Qué se registra y para quién.** Una sesión que ya ocurrió, con quienes estuvieron. El acta registra lo que pasó, no lo previsto; antes de la sesión el documento es un borrador (ver la tabla de «Qué no inventar»). Identificar el proyecto, la parte solicitante, el alcance aprobado y su código, el instructor y el líder de proyecto.
2. **Con qué base se afirma.** Cuenta como base, de mayor a menor peso: la firma de cada asistente en su fila, la certificación de quien dictó la sesión, y el material y la agenda de la sesión. Una lista de invitados no prueba asistencia. Reglas:
   - Un contenido entra en el apartado 3 solo si se dictó. Lo previsto y no dictado se quita, porque la constancia certifica que se cubrieron los contenidos listados. Si el encargo no da lo que se dictó, el apartado 3 lleva los objetivos y la frase «Contenidos dictados: Por confirmar con (quien dictó)»; no se rellena con una agenda inventada.
   - Los objetivos salen de lo que el sistema hace según el alcance aprobado y de lo que quien lo usa debe poder hacer con él. Ninguno agrega una función que el alcance no entrega.
   - La capacitación no es un entregable por sí misma salvo que el alcance o un acuerdo citado la incluya. Si la parte solicitante la espera y no consta, se dice en las observaciones de quien elabora el acta; no se redacta como si estuviera comprometida.
3. **Modalidad.** Una sola marca. «Presencial» si todos los asistentes estuvieron en el mismo lugar; «Virtual» si la sesión fue por videollamada. Una sesión mixta se declara añadiendo la opción «Mixta» a las opciones (`options` admite hasta seis textos) y marcándola.
4. **Quiénes firman.** Firman la lista cada asistente, la constancia quien dictó la sesión (el instructor principal; si el líder de proyecto la presenció y da fe, puede firmar él) y las firmas de responsabilidad las personas que la entidad define. Nunca firma un asistente en nombre de otro ni quien no estuvo.
5. **El código.** El número de acta es el código del documento: va en `document.code`, en el campo «N.º de acta» y en el pie de cada página, con el prefijo y la numeración de la entidad (`DEMO-CAP-01` en el ejemplo). El acta de entrega puede citarlo.
6. **El diagrama.** No lleva. Ver «¿Necesita un diagrama?».

## Completar cada campo

El orden de los apartados es el del tipo y no se reordena, salvo las adiciones que se anotan. La conclusión va primero dentro de cada campo.

1. **Información general.** Una cuadrícula de una columna: proyecto, parte solicitante, equipo ejecutor (con rótulos genéricos el ejecutor no es implícito), tema de la capacitación, modalidad (casillas), lugar o enlace, instructores y líder de proyecto. Después, una cuadrícula de dos columnas: número de acta, fecha de capacitación, duración total y alcance asociado (se añade, con el código del alcance aprobado). El tema nombra lo que se enseñó, no el sistema entero. El lugar es la sala y la sede; con modalidad virtual es la plataforma y, si se registra, el enlace de la sesión (sin contraseñas). Los instructores van uno por línea con su función.
2. **Objetivos de la capacitación.** Una frase que dice quién logra qué al terminar la sesión y una lista numerada de objetivos. Cada uno empieza por un verbo y nombra algo que se pueda observar en la práctica («Comprobar que una reserva cancelada dentro del plazo se reembolsa por completo»). De tres a seis.
3. **Contenidos abordados.** Una lista con los temas que se dictaron, en el orden de la sesión. Cada objetivo tiene al menos un contenido que lo cubre. Lo que el sistema no hace en esta fase y que se aclaró en la sesión puede ir como contenido, para que el asistente sepa dónde acaba el módulo.
4. **Lista de asistentes y firmas.** Una tabla de número, nombre y apellido, cargo o área y firma. Una fila por asistente esperado, numeradas desde 1, y al menos dos filas en blanco con solo su número, para quienes lleguen sin estar en la lista. Todas las filas llevan la línea de firma en su celda. El ejemplo lleva ocho (seis con nombre y dos en blanco). Con más asistentes, añadir filas: si no caben en la página, la tabla se parte entre páginas con su título y su encabezado repetidos. Con menos, quitar las filas sobrantes y conservar las dos en blanco. Un invitado que no asistió conserva su fila y en la celda de firma se escribe «No asistió»; no se borra ni se firma por él.
5. **Materiales entregados.** Una frase y una elección múltiple (`"multiple": true`) con los materiales de la entidad y, si hace falta, una línea «Otro: …» que nombra el material. Se marcan los que se entregaron en la sesión. Ninguno marcado se escribe con `"selected": []`. De dos a seis opciones; agrupar los materiales parecidos si son más. Se declara que se entregó un acceso, nunca las credenciales ni un enlace con clave.
6. **Evaluación y retroalimentación.** La frase de la escala (de 1 a 5, con el sentido de cada extremo), una tabla de aspectos por nota con las celdas en blanco y una tabla con espacio para comentarios y sugerencias. Los aspectos son los de la entidad. Las celdas se llenan a mano cuando los asistentes califican. Si el acta se entrega con resultados, cada celda lleva cuántos asistentes dieron esa nota, la suma de cada fila es el número de quienes respondieron (que no supera el de firmas) y no se escribe ningún promedio.
7. **Constancia de ejecución y cierre.** Una frase de certificación y una fila con quien certifica, su cargo, su firma y la fecha. Quien firma certifica que la sesión se realizó en la fecha y con los asistentes registrados, y que se cubrieron los contenidos del apartado 3. Es una constancia de la entidad, no una acreditación ni un certificado de competencia.
8. **Firmas de responsabilidad.** Una fila por función (elaboró, revisó, aprobó) con nombre, cargo, espacio de firma y fecha.

La fecha de la sesión sigue al alcance y se ubica en el cronograma del proyecto. `document.date` corresponde a la última acción que registra el acta (la sesión o una posterior). Los campos impresos van en `dd/mm/aaaa` y el del documento en ISO. En el ejemplo, la sesión del 07/01/2027 cae dentro de la semana de implementación propuesta del 04/01/2027 al 10/01/2027, que incluye E5. La capacitación no acredita por sí sola pruebas satisfactorias ni aceptación del producto; DEMO-ATP-01 mantiene sus resultados y su certificado pendientes.

## Cómo se comprueba un acta de capacitación

- **Asistencia.** Los números de las filas son consecutivos, hay al menos dos filas en blanco y ninguna fila con nombre tiene una firma de otra persona. El número de asistentes del acta es el de filas con firma.
- **Contenidos y objetivos.** Cada objetivo tiene un contenido que lo cubre, y ningún contenido ni objetivo agrega una función que el alcance no entrega.
- **Materiales.** Las casillas marcadas son las de lo que se entregó. Una cruz en «Acceso» sin que conste el acceso es un dato inventado.
- **Evaluación.** Con resultados, cada fila suma el número de respuestas y todas las filas suman lo mismo.
- **Coherencia.** El número de acta coincide con el código del documento; la fecha de capacitación no es posterior a la del documento; el instructor, el líder de proyecto y los firmantes tienen el mismo nombre y cargo en todas las apariciones, y coinciden con los del alcance y los demás documentos del proyecto.

## Personalizar

- `brand.entity`, `brand.unit` (pie de página), `brand.accent` y `brand.logo` (PNG o JPEG con ruta relativa al JSON; sin logo se imprime el nombre de la entidad). `brand.fonts` solo con licencia verificada.
- `document.code` con el prefijo propio, `document.short_title` para la cabecera y `document.paper` (`A4` o `Letter`).
- **Rótulos de las partes.** «Parte solicitante» y «equipo ejecutor» son genéricos. Para un encargo externo pueden ser «Cliente» y «Proveedor»; para uno interno, el área usuaria y la unidad de desarrollo. Se reemplazan buscando «solicitante» y «ejecutor» en el JSON.
- **Textos de las opciones.** Los materiales del ejemplo (manual de usuario, ficha técnica, presentación, acceso al entorno de pruebas y una línea «Otro») son genéricos y cada entidad pone los suyos. Las opciones de modalidad también (por ejemplo, la opción «Mixta»). Una elección o una lista de materiales cambia sin tocar nada más.
- **Aspectos y escala de la evaluación.** Los cinco aspectos del ejemplo son genéricos. Si la entidad usa otra escala, cambiar los encabezados de las columnas y la frase que la explica.
- Número de filas de la tabla de asistentes, firmantes de la constancia y de las firmas de responsabilidad.

## Qué no inventar

Asistentes y sus cargos que el encargo no da. Firmas y fechas de firma. Contenidos que no se dictaron. Materiales que no se entregaron. Notas de evaluación, promedios y comentarios. Duración, lugar y modalidad que no constan. La certificación de quien dictó la sesión.

Las palabras para lo que falta (Pendiente, Por confirmar, Por estimar, Propuesto), quién puede firmar, el estado del documento, las fechas y el historial de un documento nuevo están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Dato | Texto |
|---|---|
| Fecha de firma o de certificación que aún no ocurrió | Pendiente |
| Fecha de una capacitación aún no realizada | La prevista, con «(prevista)», y el documento en Borrador |
| Asistentes que nadie ha confirmado | Solo filas en blanco numeradas |
| Invitado que no asistió | «No asistió» en la celda de firma |
| Cargo o nombre del instructor que nadie ha confirmado | Por confirmar |
| Duración que nadie ha registrado | Por confirmar |
| Ningún material entregado | `"selected": []` |
| Evaluación sin respuestas | Celdas en blanco |
| Línea «Otro: …» sin material | Se elimina de las opciones |

## ¿Necesita un diagrama?

No. Un acta de capacitación registra quién asistió, qué se enseñó y qué se firmó. Quien la lee decide si la sesión consta y no necesita ver componentes ni flujos: el sistema ya está dibujado en el informe de factibilidad y en el alcance, y repetirlo no responde a ninguna pregunta del acta. Si una capacitación exige un esquema (por ejemplo, un procedimiento de operación que se enseñó), va en el manual de operación y el acta lo cita. El motor no rechaza una figura en este tipo; el ejemplo y esta guía no la prevén.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** Abrir cada campo con la conclusión: en los objetivos, lo que cada asistente logra; en los contenidos, el tema central de la sesión; en la constancia, lo que se certifica. Después van las razones y los datos. Se conserva el orden de los campos del tipo.
- **`unicorntext`.** Revisar los objetivos, los contenidos y la constancia: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las palabras o frases de trámite que no aportan. Conservar términos técnicos, fechas, cifras y nombres.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` (crear un entorno virtual fuera de la carpeta de entrega e instalar `reportlab`, `pypdf`, `pdfplumber` y `Pillow`) y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py acta.json --output acta.pdf
python3 <skill>/scripts/check_report.py acta.pdf
pdftoppm -r 80 -png acta.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('acta.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que la modalidad tenga una sola cruz y esté en la opción elegida, que los materiales tengan una cruz en cada opción marcada y ninguna en las demás, que la tabla de asistentes quede entera con sus filas en blanco y su línea de firma, que la hoja de evaluación no se parta, y que la constancia y las firmas de responsabilidad queden cada una enteras, con la de responsabilidad antes del histórico. Entregar el PDF, su manifiesto `.manifest.json` (el comprobador lo exige junto al PDF) y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. La marca de una casilla es gráfica: el texto extraído del PDF no distingue la opción elegida. El motor mantiene enteras las tablas y las cuadrículas que caben en una página, junto con el bloque siguiente cuando es una tabla, una lista o un párrafo. En el ejemplo, la primera página termina con los objetivos y la segunda con la lista de asistentes; los contenidos y los materiales pasan enteros a la página siguiente y dejan un hueco de menos de un octavo de página al pie de cada una. Los defectos habituales son:

- **Hueco grande al pie de una página**, porque una tabla, una cuadrícula o una lista entera pasó a la siguiente. Se corrige acortando el texto de antes o juntando dos contenidos. Un hueco de hasta un tercio de página es un compromiso del diseño y se acepta cuando el bloque siguiente no cabe en el resto; se corrige cuando una frase de más lo causa. La tabla de asistentes es el caso más visible: con diez o más filas ya no cabe en el resto de la página de los contenidos y pasa entera a la siguiente, y el hueco es del tamaño de la tabla. Se acepta; no se recortan los contenidos ni las filas para evitarlo.
- **Una página final con solo el histórico de revisiones.** El motor agrupa las firmas, la remisión y el histórico cuando caben juntos en una página, así que el caso ya no debería darse. Si aparece (el cierre no cabe en una página o hay un `new_page` escrito antes del histórico), se corrige acortando una sección anterior. Poner `new_page: true` en una sección suele empeorarlo.
- **Subtítulo que salta de línea y deja una palabra sola.** Mantenerlo en una línea.
- **Celdas en blanco sin bordes.** La hoja de evaluación y los espacios de los asistentes no llevan rayas verticales: la nota se marca bajo el número del encabezado y la firma sobre la línea de su celda. No es un defecto del acta ni se corrige con texto de relleno.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

La estructura se orientó con un formato genérico de gestión de proyectos de software facilitado como referencia. Redacción, diseño y ejemplo son propios y ficticios.
