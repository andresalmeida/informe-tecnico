# Añadir un tipo de documento

Esta guía es para quien mantiene o amplía la skill. Quien la usa para redactar un documento lee `skills/informe-tecnico/SKILL.md` y la guía del tipo.

## Antes de empezar: ¿hace falta un tipo?

Cada tipo cuesta una guía, un ejemplo, una muestra, pruebas, una fila de ruteo y un paso de CI, y cada cambio transversal del motor obliga a regenerar todas las muestras. El catálogo tiene 22 tipos y no crece sin un uso real que alguien pueda nombrar; descongelarlo lo decide quien mantiene el repositorio, y se pide en el pull request con ese uso concreto. Un documento ocasional se pide al agente con la skill y no necesita tipo propio. Antes de crear uno, comprobar que no solapa con uno existente (por ejemplo, el cronograma del alcance y los hitos del plan de proyecto) y que registra una decisión o un traspaso que otros documentos citan.

## Qué es un tipo

Un tipo es una guía (`references/tipos/<tipo>.md`), un ejemplo (`assets/ejemplo-<tipo>.json`), una entrada en `KIND_RULES` de `scripts/build_report.py`, una muestra (`docs/muestra-<tipo>.pdf`), sus pruebas en `tests/`, una fila en la tabla de `SKILL.md` y dos pasos en el flujo de CI. Antes de crear un bloque nuevo, reutilizar los que calculan: `quote`, `risks`, `requirements`, `impact`, `wbs` y `testcase`.

## Pasos, cada uno en su propio commit

| Paso | Qué se hace |
|---|---|
| 1. Motor | Entrada en `KIND_RULES`: `form: True` si es de formulario y `choice` con su mensaje si exige una elección marcada. Una regla nueva va a la tabla, no como condición por nombre. Un cambio de comportamiento va en un commit aparte, con su documentación y su prueba. |
| 2. Ejemplo | `assets/ejemplo-<tipo>.json`, ficticio y coherente: prefijo `DEMO-`, entidad «Entidad de demostración», nombres inventados, firmas y aprobaciones en «Pendiente». Compilarlo ya, antes de escribir la guía. Si se encadena con otros ejemplos, reutilizar sus códigos, cifras y fechas. |
| 3. Guía | `references/tipos/<tipo>.md`, con el esquema de abajo. |
| 4. Contrato | Solo lo propio del tipo: un bloque o campo nuevo con sus límites y rechazos. |
| 5. Figura | Solo si el tipo la lleva, con el flujo completo de `diagram-design` (ver `references/diagramas.md`). |
| 6. Pruebas | En `tests/`, ver «Pruebas mínimas». Si el tipo es de formulario, registrar su salida en `tests/golden/heading-title.json` con `python tests/test_heading_case.py --update`. |
| 7. Muestra | `python skills/informe-tecnico/scripts/build_report.py skills/informe-tecnico/assets/ejemplo-<tipo>.json --output docs/muestra-<tipo>.pdf`. |
| 8. Ajustar la guía | Con la muestra final: páginas reales, huecos de página y descripción de la figura. |
| 9. Ruteo | Un solo commit: fila en la tabla de `SKILL.md` y la descripción si cambia, fila en la tabla por fase del README, entrada en `references/fuentes.md`, fila en `references/codigos.md`, una frase en `references/diagramas.md`, el tipo en la fase que le toca de `references/flujo-proyecto.md`, los dos pasos de CI (comprobar la muestra; compilar y comprobar el ejemplo) y los conteos de tipos (`grep` de «22», «Veintidós» y «veintiún tipos compactos» en `SKILL.md`, `README.md`, `AGENTS.md` y `references/contrato/`). |

## Si el tipo amplía o reutiliza un bloque

Ampliar un bloque (por ejemplo, que `fields` admita varias marcas) sigue cuatro reglas: un commit propio con motor, documentación y prueba; la variante simple no cambia (la regresión lo comprueba); se auditan los ayudantes de prueba y las reglas que cuentan los elementos del bloque; y cada forma incorrecta de usar la extensión tiene un rechazo con mensaje.

Reutilizar un bloque con otro vocabulario (la evaluación de impacto en datos usa `risks` para los titulares) permite cambiar títulos, escala, respuestas y estados, pero no los rótulos fijos de las fichas ni los mensajes de error. Al reemplazar `states` hay que dar `open_states`. Documentarlo junto al bloque y añadir un rechazo por cada trampa.

## Convenciones de los tipos de formulario

Un tipo con `form: True` las recibe sin pedirlas: numeración `1. Título` y `2.1. Título`; mayúscula de oración en los títulos (`format.heading_case: "sentence"` por omisión, y `"title"` para la mayúscula de cada palabra); encabezado generado «Histórico de revisiones»; e índices opcionales con `document.indexes`. Quien redacta escribe los títulos con normalidad. Los encabezados de las guías van en minúscula normal.

## Esquema de la guía

1. Cuándo elegir el tipo, el ejemplo de partida y si lleva figura.
2. Cómo es el PDF: páginas esperadas, casillas, histórico.
3. **Decidir antes de redactar:** qué se documenta y para quién, con qué evidencia, quiénes firman, qué código usar.
4. **Completar cada campo**, en el orden del tipo, con la conclusión primero.
5. **Cómo se comprueba** el contenido.
6. **Personalizar:** identidad, código, papel, firmantes y textos de las opciones.
7. **Qué no inventar:** aprobaciones, firmas, fechas, resultados y cifras sin estimación.
8. **¿Necesita un diagrama?**, con el criterio y la alternativa si falta `diagram-design`.
9. **Revisar la redacción** con los criterios de `minto-pyramid` y de `unicorntext`, que van escritos en la guía.
10. **Comprobar y entregar:** comandos exactos y qué mirar al renderizar.

Cada punto de esta lista es un lugar donde un agente nuevo tropezó:

- **Decisión de más peso.** La guía dice qué cuenta como base suficiente y qué se marca cuando falta; sin esa regla, cada agente decide distinto.
- **Lo pendiente.** Las palabras, quién firma, el estado, las fechas y el historial de un documento nuevo viven en `references/pendientes-y-estado.md`. La guía enlaza y solo añade filas propias.
- **Opcionalidades.** Cada bloque opcional documentado tiene un caso de prueba.
- **Coherencia.** Los ejemplos que se encadenan comparten datos, y las fechas siguen un orden cronológico que la guía enuncia.
- **Rutas.** Ninguna guía depende de archivos fuera de `skills/informe-tecnico/`: una skill instalada sola no los tiene.
- **Saltos de página.** Los defectos que el comprobador no ve (hueco al pie, histórico solo en la última página) y cómo se corrigen.

## Pruebas mínimas

Las pruebas del tipo van en `tests/`, en un módulo `test_<tipo>.py` con `run_checks` o al final de `main()` de `self_test.py`, y reutilizan sus ayudantes. Cubren: el número de páginas del ejemplo; una sola marca por elección y la opción marcada en negrita; las tablas enteras y las firmas al cierre; la personalización con y sin logo; la compilación con y sin figura si es opcional; la coherencia con los ejemplos encadenados; cada opcionalidad; y un rechazo con mensaje (`rejected_with`) por cada regla propia. Para una tabla de longitud variable, probar con muchas y con pocas filas. Las pruebas comprueban contenido y estructura; un detalle de formato se fija en un solo caso.

## Regresión y puertas

Si el cambio toca el motor, los demás tipos no deben cambiar:

```sh
python tools/regresion.py <commit-base>
```

Compila los ejemplos con el motor del commit base y con el del árbol, y compara el manifiesto, el texto de cada página y los píxeles a 50 ppp. Un cambio de convención de la familia de formularios cambia todas sus salidas de forma esperada; entonces se prueba que la opción que conserva el comportamiento anterior sale idéntica.

```sh
python tests/self_test.py
python skills/informe-tecnico/scripts/build_report.py skills/informe-tecnico/assets/ejemplo-<tipo>.json --output <carpeta-temporal>/<tipo>.pdf
python skills/informe-tecnico/scripts/check_report.py <carpeta-temporal>/<tipo>.pdf
python skills/informe-tecnico/scripts/check_report.py docs/muestra-<tipo>.pdf
```

Además: el autor del PDF es la entidad de demostración, los manifiestos no traen rutas absolutas y los ejemplos no contienen datos reales.

## Revisión visual

Renderizar todas las páginas a 80 ppp y abrirlas. Mirar: una cruz por marca, ninguna tabla partida, ningún título huérfano, la figura legible, las firmas juntas y las cifras coherentes entre secciones. La marca de una elección es gráfica: un comprobador de texto no la distingue, solo la imagen. En algunos renders la negrita se ve igual que el resto; la de la opción marcada se verifica por el nombre de la fuente en el PDF.

## Probar con un agente nuevo

Dos pruebas, ambas sin el contexto de quien escribió el tipo:

1. **Ruteo, con un modelo pequeño.** Dar al agente `SKILL.md` y una docena de peticiones de usuario, sin construir nada, y pedir el tipo y las guías que leería. Debe acertar, y decir «ninguno» cuando no corresponde un documento.
2. **Producción.** Un encargo ficticio con otra entidad y otro color: el agente usa la skill desde cero y reporta dónde la guía lo confundió. Los hallazgos se corrigen en la guía, no en su documento. Si el hallazgo aparece con dos agentes distintos, es un defecto de la skill; si solo con uno, de compatibilidad.

## Definición de terminado

1. Las puertas pasan y la revisión visual no deja hallazgos abiertos.
2. Un agente nuevo produjo un documento válido sin ayuda y lo que lo confundió está corregido.
3. La muestra publicada y el flujo de CI incluyen el tipo.
4. El ejemplo declara que sus entidad, nombres, códigos, cifras y fechas son ficticios.

## Lecciones

- La regla que pasa una sección entera a la página siguiente (`KeepSection`, hasta un 35 % de hueco) mide cada sección con `wrapOn`; un bloque nuevo debe poder medirse así y no declarar `PageBreak` dentro de una sección que quiera mantenerse entera.
- Un cambio de composición que arregla un caso suele empeorar otro: antes de adoptar una regla de página, medir las páginas y los huecos de todos los ejemplos.
- Una función de texto nueva se prueba con las aristas: siglas, dígitos, mayúsculas internas y todo en mayúsculas.
- Una regla `choice` existencial se cumple con cualquier elección: un tipo con dos casillas puede compilar sin una. La guía dice que comprobar ambas corresponde a quien redacta.
- Una etiqueta de decisión que suena a permiso («Puede continuar») es riesgosa en un documento que no es consejo legal. Las etiquetas describen el estado del análisis.
- Un agente que ajusta la redacción a mano para acomodar un salto de página suele indicar una regla de composición incompleta en el motor.
- Una receta que no se prueba se desactualiza con el primer cambio del motor.

## Limitaciones conocidas

- Un cierre (firmas, remisión e histórico) más largo que una página conserva la distribución anterior y puede dejar el histórico solo.
- El motor no comprueba referencias bibliográficas ni accesibilidad PDF/UA.
