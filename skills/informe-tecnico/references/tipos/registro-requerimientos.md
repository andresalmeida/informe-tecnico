# Registros de requerimientos

Elegir `document.kind: "registro-requerimientos"` para dejar constancia de un requerimiento recibido (de software, de infraestructura o de recursos) antes de evaluarlo: qué se pide, quién lo pide, cómo se clasifica y quién lo recibe y lo asigna. Empezar por `assets/ejemplo-registro-requerimientos.json`; al compilarlo se obtiene la muestra. Usa `format.profile: "institucional"`, como los demás tipos compactos: el perfil APA es solo del `informe`. Diagrama: no, porque quien decide la admisión lee un pedido y no necesita ver componentes (ver «Diagrama»).

El PDF es compacto: título y contenido en la primera página, sin portada y sin índices (la opción `document.indexes` existe, pero una ficha de dos páginas no la necesita), y dos páginas en el ejemplo. Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra). Las tres elecciones (tipo, prioridad y proceso de origen) son casillas con exactamente una marca, y una cuadrícula de dos columnas puede llevar casillas en cualquiera de sus celdas. El histórico de revisiones se imprime al final con `document.show_changes: true`. El esquema de los bloques `fields` y de `show_changes` está en [fields.md](../contrato/fields.md) y [raiz.md](../contrato/raiz.md). El registro precede a la evaluación: la viabilidad, la solución y las estimaciones pertenecen al informe de factibilidad ([factibilidad.md](factibilidad.md)).

## Decidir antes de redactar

1. **Qué se registra y para quién.** Identificar el requerimiento tal como lo plantea quien lo pide, su número de registro y quién lo recibe. Se registra la necesidad. Una tecnología o un proveedor que nadie ha evaluado no entra en la descripción.
2. **Con qué se clasifica.** Las dos elecciones que pesan son el tipo y la prioridad. Sin una regla, cada agente las decide a su criterio, y este es el que se aplica:
   - **Tipo.** Software: crear o cambiar una aplicación o una integración. Infraestructura: instalar, ampliar o cambiar servidores, redes o plataformas. Recursos: pedir personas, presupuesto o licencias sin un desarrollo ni un cambio de plataforma concretos. Si el pedido mezcla tipos, se marca el que decide quién lo evalúa primero y los demás se mencionan en la necesidad.
   - **Prioridad.** Alta: una operación está detenida o degradada, o una fecha comprometida no se cumpliría sin el requerimiento. Media: mejora una operación que hoy funciona con una alternativa y no hay fecha comprometida. Baja: mejora deseable sin fecha ni efecto en la operación. La propone quien pide y la confirma quien recibe.
   - **Prioridad que nadie ha dado.** No se infiere. Preguntar al solicitante o declarar el estado con una opción propia: `"options": ["Alta", "Media", "Baja", "Por confirmar"]` con `"selected": "Por confirmar"` (`options` admite hasta seis textos).
3. **De dónde sale cada dato.** Lo que el registro afirma sobre la necesidad remite a la solicitud original o al solicitante: un correo, un oficio, un acta o una conversación con su fecha. Una opinión de quien registra no cuenta como necesidad.
4. **Quiénes firman y quién recibe.** Los roles de la tabla de firmas y los cargos de quien recibe el requerimiento y de la persona a quien se asigna vienen de la entidad. Conservar sus nombres de cargo.
5. **El código.** El número de registro es el código del documento: va en `document.code`, en el campo «N.º de registro» y en el pie de cada página, con el prefijo y la numeración de la entidad (`DEMO-REQ-014` en el ejemplo). El informe de factibilidad que evalúe el requerimiento lo cita en «Requerimiento asociado».
6. **El diagrama.** No lleva. Ver «Diagrama».

## Completar cada campo

El orden de los apartados es el del tipo y no se reordena. La conclusión va primero dentro de cada campo.

1. **Datos Generales del Requerimiento.** Una cuadrícula de dos columnas: número de registro, fecha de recepción, tipo, prioridad, solicitante y proceso de origen. La fecha de recepción es el día en que el requerimiento llegó a la entidad. El solicitante lleva nombre y cargo o área, o el nombre del cliente. El proceso de origen es el proceso de la entidad del que nace el pedido y sus opciones son propias de cada entidad.
2. **Descripción del Requerimiento.** Tres campos. El asunto es una línea que nombra lo que se pide, sin la solución. La necesidad abre con lo que hace falta y sigue con la situación actual y su efecto. El resultado esperado abre con el cambio que se busca y, si el solicitante propone cómo medirlo, lo cita como propuesta suya y deja la meta para la evaluación.
3. **Información Adicional.** Proyecto o cliente relacionado y documentos adjuntos, uno por línea y citados por título o código y fecha. Es una sección opcional: si ninguno de los dos datos existe, se elimina entera. Si existe uno solo, el otro campo lleva «No aplica».
4. **Recepción y Asignación.** Quién recibió el requerimiento y a quién se asignó, cada uno con su fecha. La fecha de registro es la del día en que se asentó la ficha y puede ser posterior a la de recepción. A continuación, el párrafo «Observaciones iniciales», que abre con lo que ocurre con el requerimiento (por ejemplo, que pasa a evaluación) y sigue con lo que quien evalúa debe saber al recibirlo. Es opcional: sin observaciones se elimina el párrafo y no se escribe «Sin observaciones».
5. **Firmas de Responsabilidad.** Una fila por función con nombre, cargo, espacio de firma y fecha. Los firmantes los confirma la entidad. Firmar el registro acredita que los datos son los recibidos. La aprobación del requerimiento la decide la evaluación.

Las fechas del registro cumplen este orden: recepción, registro, asignación y fecha del documento (`document.date`). El campo del documento va en formato ISO (`2026-10-29`) y los campos impresos en `dd/mm/aaaa`. El registro no lleva esfuerzo ni plazo del equipo. Las cantidades que da quien solicita (usuarios, volumen de datos, plazo deseado) se anotan tal como las dio, atribuidas a quien las dio, y no se presentan como compromiso ni como estimación: la estimación es de la factibilidad.

## Comprobar el contenido

- **Clasificación.** El tipo y la prioridad responden a los criterios de «Decidir antes de redactar» y la solicitud los respalda.
- **Necesidad sin solución.** Ninguna oración propone una tecnología, una arquitectura ni un plazo de entrega que quien pide no haya planteado.
- **Resultado observable.** El resultado esperado se puede reconocer cuando ocurra: un cambio en una operación o una cifra que quien pide acepta medir. «Mejorar el servicio» no basta.
- **Coherencia.** El número de registro coincide en el código del documento y en el campo; las fechas están en orden; el nombre y el cargo de quien recibe y de quien firma son los mismos en todas las apariciones; la elección de prioridad, las observaciones y los plazos que pide el solicitante dicen lo mismo.

## Personalizar

- `brand.entity`, `brand.unit` (pie de página), `brand.accent` y `brand.logo` (PNG o JPEG con ruta relativa al JSON; sin logo se imprime el nombre de la entidad). `brand.fonts` solo con licencia verificada.
- `document.code` con el prefijo propio, `document.short_title` para la cabecera y `document.paper` (`A4` o `Letter`).
- **Opciones de las elecciones.** Los tipos del ejemplo (Software, Infraestructura, Recursos), los procesos de origen (Operación, Proyectos, Atención a clientes) y la escala de prioridad son genéricos y cada entidad los reemplaza por los suyos: de 2 a 6 textos por elección, siempre con exactamente una marcada. Cambiar las opciones del tipo obliga a ajustar sus definiciones en «Decidir antes de redactar» al pasar la guía a la entidad.
- Cargos de quien recibe el requerimiento y de la persona asignada, y firmantes: cambiar los roles, nombres y cargos de la cuadrícula de recepción y de la tabla de firmas.

## Qué no inventar

Aprobaciones, firmas y fechas de firma. Responsables y nombres que no consten. La prioridad que quien pide no ha dado. Plazos y estimaciones que nadie ha acordado. Una solución o una tecnología que no figure en la solicitud. La existencia de documentos adjuntos.

Las palabras para lo que falta (Pendiente, Por confirmar, Por estimar, Propuesto), quién puede firmar, el estado del documento, las fechas y el historial de un documento nuevo están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Dato | Texto |
|---|---|
| Prioridad que nadie ha dado | Opción «Por confirmar» marcada |
| Proceso de origen que la solicitud no indica | Opción «Por confirmar» marcada (se añade a las opciones) |
| Un campo de «Información Adicional» sin dato cuando el otro sí lo tiene | No aplica |
| Sección «Información Adicional» sin ningún dato, o «Observaciones iniciales» sin contenido | Se elimina |
| Plazo o estimación | No se escribe: queda para la evaluación |

Si el solicitante propone cómo medir el resultado esperado, se cita como propuesta suya. Si nadie propone una medida, se cita como base la situación actual que dio el solicitante, atribuida a él, y la meta queda para la evaluación. La necesidad se apoya en la solicitud original, citada por quien la hizo y su fecha («según la solicitud de la jefa de atención al socio del 02/11/2026»); no se inventa un documento adjunto.

## Diagrama

El registro no lleva diagrama. Una ficha de registro recoge un pedido antes de evaluarlo: quien decide si lo admite lee la necesidad, el tipo y la prioridad y no necesita ver qué componentes se hablan entre sí. Un esquema propondría una solución que nadie ha evaluado, lo contrario de lo que el registro asienta. Si el requerimiento exige un esquema, va en el informe de factibilidad que lo evalúa, con el criterio de [factibilidad.md](factibilidad.md#necesita-un-diagrama). El motor no rechaza una figura en este tipo; el ejemplo y esta guía no la prevén.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** Abrir cada campo con la conclusión: en la necesidad, lo que hace falta; en el resultado esperado, el cambio que se busca; en las observaciones, lo que ocurre con el requerimiento. Después van las razones y los datos. Se conserva el orden de los campos del tipo.
- **`unicorntext`.** Revisar la necesidad, el resultado esperado y las observaciones: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las palabras o frases de trámite que no aportan. Conservar términos técnicos, fechas, responsables y las palabras del solicitante que fijan el pedido.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` (crear un entorno virtual fuera de la carpeta de entrega e instalar `reportlab`, `pypdf`, `pdfplumber` y `Pillow`) y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py registro.json --output registro.pdf
python3 <skill>/scripts/check_report.py registro.pdf
pdftoppm -r 80 -png registro.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('registro.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que cada elección tenga una sola cruz y que esté en la opción elegida, que ninguna tabla ni cuadrícula quede partida, que el párrafo de observaciones siga a su cuadrícula y que las firmas queden en una sola página. Entregar el PDF, su manifiesto `.manifest.json` (el comprobador lo exige junto al PDF), el JSON y, si hay figura, sus activos (HTML, SVG y PNG).

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. El motor mantiene enteras las tablas y las cuadrículas que caben en una página, junto con el bloque siguiente cuando es una tabla, una lista o un párrafo. En el ejemplo, la primera página reúne los cuatro primeros apartados y la segunda las firmas y el histórico. Los defectos habituales son:

- **Hueco grande al pie de la primera página**, porque la cuadrícula de recepción pasó entera con su párrafo a la segunda. Se corrige acortando la necesidad o el resultado esperado, o quitando una línea de los adjuntos. Un hueco de hasta un tercio de página es un compromiso del diseño y se acepta cuando la tabla siguiente no cabe en el resto; se corrige cuando una frase de más lo causa.
- **Una página final con solo el histórico de revisiones.** El motor agrupa las firmas, la remisión y el histórico cuando caben juntos en una página, así que el caso ya no debería darse. Si aparece (el cierre no cabe en una página o hay un `new_page` escrito antes del histórico), se corrige acortando una sección anterior. Poner `new_page: true` en una sección suele empeorarlo.
- **Subtítulo que salta de línea y deja una palabra sola.** Mantenerlo en una línea.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

La estructura se orientó con un formato genérico de gestión de proyectos de software facilitado como referencia. Redacción, diseño y ejemplo son propios y ficticios.
