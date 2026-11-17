# Alcance del proyecto

Elegir `document.kind: "alcance-proyecto"` para fijar, una vez aprobada una propuesta técnica, qué se va a construir, con qué restricciones, en qué tiempo, quién responde de cada actividad y quién lo acepta. Empezar por `assets/ejemplo-alcance-proyecto.json`; al compilarlo se obtiene la muestra. Diagrama: opcional; el ejemplo incluye un esquema del perímetro y el tipo compila igual sin él (ver «¿Necesita un diagrama?»).

**Contenido:** Decidir antes de redactar; Completar cada campo; Cómo se comprueba un alcance; Personalizar; Qué no inventar; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

Va después del informe de factibilidad ([factibilidad.md](factibilidad.md)) y antes de construir. No repite la evaluación: toma sus cifras y sus condiciones y las convierte en un compromiso entre dos partes. Los rótulos de las partes son genéricos: **parte solicitante** es quien pide y acepta el resultado, y **equipo ejecutor** es quien lo construye. Sirven a un encargo interno y a uno externo; cada entidad los reemplaza por los suyos (ver «Personalizar»).

El PDF es compacto: título y contenido en la primera página, sin portada, de seis a nueve páginas (ocho en el ejemplo con figura y siete sin ella). No tiene casillas: la decisión de más peso, qué entra y qué queda fuera, se escribe y no se marca. El histórico de revisiones se imprime al final con `document.show_changes: true`. El esquema de los bloques `fields`, `table` y `figure` y de `show_changes` está en [fields.md](../contrato/fields.md), [secciones.md](../contrato/secciones.md) y [raiz.md](../contrato/raiz.md). Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Índices.** El ejemplo no los lleva: el contenido ocupa espacio adicional y `tables` listaría sobre todo tablas de firmas. Se recomienda `document.indexes: ["contents"]` solo cuando el alcance pasa de nueve páginas (varios subproyectos o muchos entregables) o se cita por apartado desde un contrato. `tables` y `figures` no se recomiendan: el tipo suele traer una sola figura y tablas de firmas.

## Decidir antes de redactar

1. **Qué se fija y para quién.** Identificar la propuesta aprobada, su código y las dos partes. El alcance describe el resultado comprometido, no la evaluación que lo precedió.
2. **Con qué base se fija.** Este tipo no tiene casillas: su regla en el motor es la de un formulario sin elecciones (`form: True`, sin `choice`), y la decisión de más peso, qué entra y qué queda fuera, la sostiene el texto. Sin una regla, cada agente la decide a su criterio, y esta es la que se aplica. La base, de mayor a menor peso: la propuesta o el informe de factibilidad aprobado; las condiciones y decisiones de la aprobación; los acuerdos escritos posteriores con la parte solicitante, citados por fecha.
   - Entra en el alcance lo que consta en esa base. Nada entra porque parezca razonable.
   - Lo que la base deja fuera se repite como exclusión, en el párrafo inicial del apartado 3 y una sola vez. Un alcance que calla una exclusión conocida es ambiguo.
   - Lo que la base no resuelve se declara «Por confirmar» con quién lo confirma; no se decide por inercia.
   - Sin propuesta aprobada no hay alcance definitivo: el documento se entrega como «Borrador» y lo que depende de la aprobación queda «Por confirmar».
3. **Quiénes aceptan y quiénes responden.** Las dos partes firman la aceptación. Una segunda tabla lleva la cadena de responsabilidad del documento (elaboró, revisó, aprobó). Los nombres y cargos vienen de la entidad.
4. **Si la aprobación fue con condiciones.** Cada condición se registra con responsable, momento y estado (apartado 4.1). Una aprobación sin condiciones elimina ese apartado.
5. **Si necesita un diagrama.** Ver «¿Necesita un diagrama?».
6. **El código.** Usar el prefijo y la numeración de la entidad (`DEMO-ALC-01` en el ejemplo). Es `document.code` y aparece en el pie. El alcance cita el código de la propuesta o del informe aprobado y el del requerimiento.

## Completar cada campo

El orden de los apartados es el del tipo y no se reordena, salvo las adiciones que se anotan. La conclusión va primero dentro de cada campo.

1. **Información de referencia y antecedentes.** Una cuadrícula de una columna con el nombre del proyecto, la parte solicitante, el equipo ejecutor (con rótulos genéricos el ejecutor no es implícito), el patrocinador (el responsable del lado de la parte solicitante), el líder de proyecto, el líder técnico, los miembros del equipo con su función y la versión del documento, que coincide con `document.version`. Un miembro que nadie ha confirmado se escribe «Por confirmar». Después, una cuadrícula de dos columnas: número de alcance (el código del documento), fecha de elaboración, propuesta técnica aprobada y requerimiento asociado. Los antecedentes abren con lo que decidió la aprobación, siguen con el requerimiento que originó el proyecto, citan las condiciones si las hubo y cierran con lo que fija el documento. La fecha de elaboración es posterior a la de la aprobación y a la del requerimiento.
2. **Objetivo del proyecto.** Una frase con el resultado y una lista numerada de los objetivos de desarrollo y de implementación. Cada uno empieza por un verbo y nombra algo que se pueda comprobar. Ninguno agrega lo que la base aprobada no contiene.
3. **Definición del alcance técnico.** Un párrafo que dice lo que entra y lo que queda fuera.
   - **Arquitectura propuesta** (3.1). Qué se añade, qué componente existente cambia y cómo, y con qué tecnologías y dependencias. Si lleva figura, se llama desde aquí con `{{ref:id}}`.
   - **Entregables incluidos** (3.2). Una tabla con código (E1, E2…), entregable y qué incluye. Los códigos se usan en la matriz de responsabilidades; la figura muestra los que corresponden a componentes. En el ejemplo, E1 a E4 son componentes y E5 es la capacitación del equipo de operaciones, incluida en la implementación y en las mismas siete semanas y 50 días-persona. E5 se verifica con el acta de capacitación y sus materiales, sin añadir un componente a la figura.
   - **Criterios de aceptación** (3.3). La frase inicial dice quién acepta y dónde se comprueba. Cada criterio lleva umbral, método y entorno. Un umbral que nadie ha acordado se declara «Propuesto, por confirmar con (área)» en la frase inicial.
4. **Restricciones.** Los requisitos de instalación en una cuadrícula: hardware mínimo, sistema operativo, software adicional y consideraciones especiales (aquí van los límites que no son de instalación, como los medios de pago admitidos o los periodos en que no se despliega). Un requisito que no aplica se escribe «No aplica».
   - **Condiciones de la aprobación** (4.1). Es opcional. Una tabla con la condición, su responsable, cuándo se cumple y su estado. Cada condición de la aprobación aparece una vez.
5. **Cronograma de trabajo.** Una fila por fase, con duración estimada y observaciones, y el total en una cuadrícula. Son dos magnitudes, como en la factibilidad: la duración está en tiempo de calendario (semanas) y su total es la suma de las fases que no se solapan; el esfuerzo está en días-persona. Las dos cifras del alcance coinciden con las del informe de factibilidad aprobado. Si cambian, la observación dice por qué y el histórico registra el cambio. El calendario propuesto del ejemplo va del 23/11/2026 al 10/01/2027; la última semana, del 04/01/2027 al 10/01/2027, incluye la capacitación. Las fechas propuestas no afirman ejecución ni aprobación.
6. **Matriz de responsabilidades.** Una tabla de actividades por recursos y, debajo, la leyenda en un párrafo. Las columnas son funciones, no personas. Cada actividad lleva al menos una R y una sola A; cuando quien hace aprueba, la celda dice «R/A». Las actividades salen del cronograma y de los entregables, y cada condición que crea una actividad tiene su fila.
7. **Firmas de aceptación.** Una tabla de dos columnas, una por parte, con nombre y cargo, firma y fecha. Firmar acredita que las partes aceptan el alcance, los criterios y el cronograma; no acredita el producto, que lo decide la comprobación de los criterios.
8. **Firmas de responsabilidad.** Una fila por función (elaboró, revisó, aprobó) con nombre, cargo, espacio de firma y fecha.

Las fechas siguen este orden: requerimiento, informe o propuesta aprobada, fecha de elaboración y fecha del documento (`document.date`), que coinciden. Los campos impresos van en `dd/mm/aaaa` y el del documento en ISO.

## Cómo se comprueba un alcance

- **Origen.** Cada entregable, restricción y cifra remite a la propuesta aprobada o a un acuerdo citado. Una cifra sin origen se declara «Por estimar».
- **Trazabilidad.** Cada objetivo tiene al menos un entregable y cada entregable al menos un criterio de aceptación. Un entregable sin criterio no se puede aceptar.
- **Criterios medibles.** Un número, un método y un entorno: «el 95 % de los pagos de prueba se confirma en menos de 5 segundos». Si falta alguno, reformular o declararlo pendiente.
- **Exclusiones.** Las de la propuesta están todas, y ni los entregables ni la figura las contradicen.
- **Cifras.** Las fases suman el total de semanas; el esfuerzo coincide con el de la factibilidad; lo que hace un tercero, como una revisión externa, se rotula aparte y no suma al esfuerzo interno.
- **Responsabilidades.** Una sola A por actividad, al menos una R, y cada función con firma (la parte solicitante, el equipo ejecutor) con el mismo nombre en la matriz y en la tabla de firmas; una forma abreviada («Solicitante» por «Parte solicitante») es aceptable cuando la columna es estrecha.
- **Condiciones.** Cada una tiene responsable, momento y estado.
- **Coherencia.** El número de alcance coincide con el código del documento, la versión del campo con `document.version`, y los nombres y cargos son los mismos en todas las apariciones.

## Personalizar

- `brand.entity`, `brand.unit` (pie de página), `brand.accent` y `brand.logo` (PNG o JPEG con ruta relativa al JSON; sin logo se imprime el nombre de la entidad). `brand.fonts` solo con licencia verificada.
- `document.code` con el prefijo propio, `document.short_title` para la cabecera y `document.paper` (`A4` o `Letter`).
- **Rótulos de las partes.** «Parte solicitante» y «equipo ejecutor» son genéricos. Para un encargo externo pueden ser «Cliente» y «Proveedor»; para uno interno, el área usuaria y la unidad de desarrollo. Se reemplazan buscando «solicitante» y «ejecutor» en el JSON: aparecen en la cuadrícula de referencia, en la frase de los criterios, en la matriz y en la tabla de aceptación.
- **Requisitos de instalación.** Hardware, sistema operativo y software adicional son los de un proyecto de software. Para otro tipo de proyecto, reemplazar las etiquetas por las que correspondan (de una a dieciséis filas).
- Códigos de los entregables, columnas de la matriz, firmantes y miembros del equipo.

## Qué no inventar

La aprobación de la propuesta y su fecha. Firmas y fechas de firma. Miembros del equipo y firmantes que no consten. Cifras de esfuerzo o de plazo que no vengan de la base. Umbrales que nadie ha acordado. Exclusiones o condiciones que la aprobación no trae. El cumplimiento de una condición.

Las palabras para lo que falta (Pendiente, Por confirmar, Por estimar, Propuesto), quién puede firmar, el estado del documento, las fechas y el historial de un documento nuevo están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Dato | Texto |
|---|---|
| Estado de una condición de la aprobación aún no cumplida | Pendiente |
| Responsable o momento de una condición que la aprobación no asignó | Por confirmar |
| Valor que una condición debe fijar y nadie ha fijado | Por confirmar |
| Código de la propuesta aprobada que no consta | «Código: Por confirmar» |
| Patrocinador que el encargo no da | Por confirmar (no se supone que sea el solicitante) |
| Dato de instalación que depende de otro equipo | Por confirmar con (área) |
| Requisito de instalación que no aplica | No aplica |
| Duración o esfuerzo sin estimar | Por estimar |
| Apartado 4.1 cuando la aprobación no tuvo condiciones | Se elimina |

Este tipo no desglosa el esfuerzo por rol: el total en días-persona va en el cronograma y el desglose pertenece al informe de factibilidad. Si el encargo pide cifras por rol, remitir a ese informe.

**Qué se elimina cuando algo no aplica.**

- **Sin figura:** se quita el bloque `figure` y la oración que lo llama con `{{ref:id}}`. El tipo compila igual.
- **Sin condiciones:** se quita el apartado de condiciones y, en los antecedentes, la frase que las cita con su `{{ref:id}}`; no debe quedar ninguna referencia a él. La numeración se cierra sola. Una actividad de la matriz o una observación del cronograma que existía solo por una condición se quita también.

## ¿Necesita un diagrama?

Opcional. El alcance gana con una figura cuando el proyecto añade o cambia componentes que se hablan entre sí, porque quien firma debe ver qué se construye, qué se ajusta y qué queda fuera, y la lista de entregables no deja ver los puntos de contacto. Si el alcance trata de un documento, una compra, una configuración, un solo componente o un sistema entero nuevo que no toca ninguno existente, bastan el párrafo del apartado 3 y la tabla de entregables. Prueba práctica: si, leída la tabla, alguien puede preguntarse si un componente forma parte de la entrega, dibujar el perímetro.

La figura de este tipo no repite la arquitectura del informe de factibilidad. Marca el perímetro: lo que el equipo construye, lo que ajusta en un componente existente, lo que queda sin cambios, lo externo y lo excluido, con los códigos de los entregables que son componentes. La capacitación E5 es un servicio durante la implementación y se documenta en la tabla y la matriz, sin dibujarla como componente. Si el informe de factibilidad ya trae la arquitectura, el alcance solo añade esa lectura. Tipo: arquitectura con una zona de límite, según [diagramas.md](../diagramas.md).

Lo ejecuta el agente que lee esta skill y `diagram-design`, no el script. Si `diagram-design` está disponible, seguir la «Integración» y los «Comandos y medidas» de [diagramas.md](../diagramas.md#comandos-y-medidas). En este tipo: tipo arquitectura con una zona de límite, fuente en `assets/diagrams/alcance-pagos.html`, bloque `figure` llamado desde el apartado 3.1 con `{{ref:id}}`, y lo que no describa un sistema real se declara demostrativo en la imagen y en el pie.


Si falta, aplicar el mismo criterio sin la skill: pocos nodos, un foco de atención, rótulos legibles y conectores que no crucen texto. Usar un SVG propio o el flujo lineal de 2 a 5 nodos del motor, e informar de que no se usó `diagram-design`.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** Abrir cada campo con la conclusión: en los antecedentes, lo que decidió la aprobación; en el apartado 3, lo que entra y lo que queda fuera; en cada criterio, el umbral. Después van las razones y los datos. Se conserva el orden de los campos del tipo.
- **`unicorntext`.** Revisar los antecedentes, el párrafo del alcance, la arquitectura y los criterios: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las palabras o frases de trámite que no aportan. Conservar términos técnicos, cifras, responsables, plazos y condiciones.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py alcance.json --output alcance.pdf
python3 <skill>/scripts/check_report.py alcance.pdf
pdftoppm -r 80 -png alcance.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('alcance.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que ninguna tabla ni cuadrícula quede partida ni con título huérfano, que la leyenda de la matriz siga a su tabla, que la figura se lea y que cada tabla de firmas quede entera, con la de responsabilidad al cierre y antes del histórico. Entregar el PDF, su manifiesto `.manifest.json` (el comprobador lo exige junto al PDF), el JSON y, si hay figura, sus activos (HTML, SVG y PNG).

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. El motor mantiene enteras las tablas y las cuadrículas que caben en una página, y una lista larga puede partirse siempre que no deje un solo elemento a cada lado. Los defectos habituales son:

- **Hueco grande al pie de una página**, porque una tabla, una cuadrícula o la figura entera pasó a la siguiente. En el ejemplo, la figura llena la página 2, las restricciones y las fases están en la 4 y el total con el calendario propuesto pasa entero a la 5, junto a la matriz. Las dos tablas de firmas y el histórico quedan en la 6. Se corrige acortando el texto de antes o juntando dos filas con el mismo dato. Un hueco de hasta un tercio de página es un compromiso del diseño y se acepta cuando la tabla siguiente no cabe en el resto; se corrige cuando una frase de más lo causa.
- **La leyenda de la matriz sola al inicio de una página.** El motor mantiene la tabla con el párrafo o la lista que la sigue. Revisar en el render que ambas sigan juntas; la matriz del ejemplo y su leyenda comparten la página 5.
- **Las firmas de aceptación y las de responsabilidad en páginas distintas.** Es aceptable si cada tabla está entera. Forzar una página nueva suele dejar un hueco mayor.
- **Una página final con solo el histórico de revisiones.** El motor agrupa las firmas, la remisión y el histórico cuando caben juntos en una página, así que el caso ya no debería darse. Si aparece (el cierre no cabe en una página o hay un `new_page` escrito antes del histórico), se corrige acortando una sección anterior. Poner `new_page: true` en una sección suele empeorarlo.
- **Subtítulo que salta de línea y deja una palabra sola.** Mantenerlo en una línea.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

La estructura se orientó con un formato genérico de gestión de proyectos de software facilitado como referencia. Redacción, diseño y ejemplo son propios y ficticios.
