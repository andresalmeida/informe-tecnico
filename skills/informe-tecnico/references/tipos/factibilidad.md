# Informes de factibilidad

Elegir `document.kind: "informe-factibilidad"` para evaluar si una propuesta técnica se puede realizar con la arquitectura, los recursos y el tiempo disponibles, antes de comprometer su desarrollo. Empezar por `assets/ejemplo-informe-factibilidad.json`; al compilarlo se obtiene la muestra. Diagrama: opcional; el ejemplo incluye uno y el tipo compila igual sin él.

**Contenido:** Decidir antes de redactar; Completar cada campo; Variante completa; Cómo se comprueba una factibilidad; Personalizar; Qué no inventar; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

El PDF es compacto: título y contenido en la primera página, sin portada, de cuatro a seis páginas. Los índices y la introducción son opcionales (ver «Variante completa»). Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra). Las elecciones (viabilidad, recursos externos, decisión final) son casillas con exactamente una marca. El histórico de revisiones se imprime al final con `document.show_changes: true`. El esquema de los bloques `fields` y de `show_changes` está en [fields.md](../contrato/fields.md) y [raiz.md](../contrato/raiz.md).

## Decidir antes de redactar

1. **Qué se evalúa y para quién.** Identificar el requerimiento o la propuesta, su código y el órgano que decide. La evaluación es técnica y operativa: si cabe en la arquitectura actual y si el equipo puede construirla y operarla.
2. **Con qué evidencia se concluye.** Cuenta como evidencia, de mayor a menor peso: una prueba hecha en el entorno de la entidad, una medición, la documentación pública del proveedor o de la plataforma con su versión y su fecha de consulta, y la respuesta de un responsable del proceso. Una opinión sin fuente no cuenta. Regla de suficiencia:
   - Con una prueba o una medición se puede marcar «Factible».
   - Con solo documentación se marca como máximo «Factible con observaciones», y una de las observaciones es validar el resultado en el entorno real.
   - Sin ninguna de las anteriores no se marca una viabilidad: pedir lo que falta, o declarar el estado con una opción propia. Ejemplo: `"options": ["Factible", "Factible con observaciones", "No factible", "Pendiente de evidencia"]` con `"selected": "Pendiente de evidencia"` (`options` admite hasta seis textos).

   La justificación dice qué evidencia se usó. Una capacidad de plataforma se cita por el nombre de su documentación pública y la fecha de consulta; no se escriben versiones ni compatibilidades que no se hayan comprobado.
3. **Quiénes firman y a quién se remite.** Los roles del bloque de firmas y el área destinataria vienen de la entidad. Conservar sus nombres de cargo.
4. **Si necesita un diagrama.** Ver «¿Necesita un diagrama?» más abajo.
5. **El código.** Usar el prefijo y la numeración de la entidad (`DEMO-FAC-01` en el ejemplo). Es `document.code` y aparece en el pie de cada página.
6. **Si el proyecto trata datos personales.** Al evaluar la factibilidad se anota si el proyecto trata datos personales: Sí, No o Por confirmar. Con Sí o Por confirmar se abre una evaluación de impacto en datos ([evaluacion-impacto-datos.md](evaluacion-impacto-datos.md), código `EID`) y se cita por su código cuando ya existe. Si todavía no se emitió, el código se deja «Por confirmar» y no se inventa; la evaluación, al emitirse, cita este informe, y el informe ya fechado no se reedita para añadirle el código. Se registra en el impacto en procesos y sistemas existentes (apartado 2.1) y, si cambia el plan, como observación o condición. El análisis de los datos y de sus riesgos pertenece a esa evaluación, no a este informe.

## Completar cada campo

El orden de los apartados es el del tipo y no se reordena. La conclusión va primero dentro de cada campo.

1. **Información de referencia.** N.º de informe, fecha de elaboración, requerimiento asociado y autor con su rol. La fecha es la de elaboración, no la de aprobación.
2. **Evaluación de factibilidad técnica.** Marcar una sola viabilidad: Factible, Factible con observaciones o No factible. En la justificación, la primera oración da el veredicto y su razón principal; después van la evidencia con cifras, las tecnologías involucradas, las dependencias técnicas y, si hay observaciones, cada una como condición verificable. Un «No factible» indica la causa técnica y el cambio que lo haría viable.
   - **Impacto en procesos y sistemas existentes** (2.1). Efecto en operaciones, integraciones, arquitectura actual y riesgos técnicos, uno por línea.
   - **Supuestos y restricciones técnicas** (2.2). Separar lo que debe mantenerse para que la conclusión valga (supuesto) de lo que ya limita la solución (restricción).
3. **Definición del alcance técnico.** Un párrafo que fija lo que entra y lo que queda fuera. Los objetivos técnicos (3.1) empiezan por un verbo y nombran un resultado que se pueda comprobar. Los criterios de aceptación mínimos (3.2) llevan umbral, método y entorno de comprobación. Un umbral que propone quien redacta, sin acuerdo previo con el área, se declara «propuesto» en la introducción de la lista («Umbrales propuestos, por confirmar con el área de …»); uno ya acordado cita quién lo acordó.
4. **Evaluación y asignación de recursos.** Tres tablas: humanos (rol, cantidad, esfuerzo con su unidad), técnicos (tipo, cantidad, detalle) y externos, con la elección No o Sí y, si es Sí, el perfil y su justificación. Una fila sin recurso se elimina; un dato sin estimar se escribe «Por estimar», nunca cero. Con la elección «No», se elimina también la tabla de perfiles externos (el motor la admite ausente) y no queda ningún texto que la nombre.
5. **Estimación preliminar de tiempo.** Una fila por fase con duración y observaciones, y el total. Son dos magnitudes. La duración está en tiempo de calendario (semanas) y su total es la suma de las fases que no se solapan. El esfuerzo está en días-persona y su total es la suma de la tabla de recursos humanos. Las dos pueden diferir si las personas trabajan a tiempo parcial o en paralelo: cuando difieran, la columna de observaciones dice la dedicación (por ejemplo, «dos personas en paralelo» o «media dedicación»). La coherencia se revisa a mano; el motor no la valida.
6. **Conclusiones y recomendaciones.** La decisión final (continuar, continuar con condiciones, no continuar) y después las recomendaciones. Una viabilidad con observaciones lleva una decisión con condiciones y cada observación aparece como condición. La decisión es una propuesta del informe; su aprobación consta en las firmas.
7. **Aprobaciones y firmas.** Una fila por función con nombre, cargo, espacio de firma y fecha. Los firmantes los confirma la entidad. A continuación, el área a la que se remite el informe, la fecha de remisión y quién lo remite.

## Variante completa

Para un informe que va a un comité o que pasa de seis páginas, se activan tres extras. Son opcionales y se pueden combinar:

- **Índices.** `document.indexes: ["contents", "tables", "figures"]` imprime bajo el título el contenido y los índices de tablas y de figuras, con sus páginas. Pedir solo los que tengan entradas: el motor rechaza `tables` o `figures` si el documento no tiene tablas o figuras.
- **Histórico de revisiones.** `document.show_changes: true`, con una entrada por versión y los localizadores de las secciones que cambian.
- **Introducción y objetivos.** Una sección «Introducción y objetivos» después de la información de referencia. El primer párrafo da la conclusión: el veredicto, el esfuerzo y el plazo, y la decisión propuesta. Después van los objetivos del informe en una lista numerada. No repite la justificación de la evaluación ni la adelanta con otras palabras. La numeración se corre una posición; citar las secciones con `{{ref:id}}`, nunca por su número.

El ejemplo `assets/ejemplo-informe-factibilidad-completo.json` reúne los tres. Un informe de dos a cuatro páginas no lleva índices: ocuparían más de media página. Si el informe lleva introducción, sus cifras y su decisión coinciden con las de las conclusiones.

## Cómo se comprueba una factibilidad

- **Evidencia.** Cada afirmación de viabilidad remite a algo verificable: el resultado de una prueba, la versión de una API, una medición, una respuesta de un responsable. Citar por nombre o código documental, sin rutas del equipo.
- **Supuestos.** Escribir la condición y qué cambia si deja de cumplirse. Un supuesto sin consecuencia no informa.
- **Restricciones.** Son límites conocidos del entorno, del presupuesto o del proveedor. No se superan con una redacción optimista.
- **Criterios medibles.** Un número, un método y un entorno: «el 95 % de los pagos de prueba se confirma en menos de 5 segundos». Si falta el número o el método, reformular el criterio o declararlo pendiente.
- **Coherencia.** Viabilidad, observaciones y decisión final dicen lo mismo; las fases suman el total; los recursos nombrados en el tiempo existen en la tabla de recursos.

## Personalizar

- `brand.entity`, `brand.unit` (pie de página), `brand.accent` y `brand.logo` (PNG o JPEG con ruta relativa al JSON; sin logo se imprime el nombre de la entidad). `brand.fonts` solo con licencia verificada.
- `document.code` con el prefijo propio, `document.short_title` para la cabecera y `document.paper` (`A4` o `Letter`).
- Firmantes: cambiar los roles, nombres y cargos de la tabla de firmas y el área del campo «Remitido a».
- Textos de las opciones: pueden reescribirse (por ejemplo, «Continuar a cotización»), siempre con exactamente una marcada.

## Qué no inventar

Aprobaciones, firmas y fechas de aprobación o remisión. Responsables y nombres de firmantes que no consten. Resultados de pruebas, versiones de proveedores y cifras de esfuerzo o de tiempo que no provengan de una estimación. La aceptación de la entidad.

Las palabras para lo que falta (Pendiente, Por confirmar, Por estimar, Propuesto), quién puede firmar, el estado del documento, las fechas y el historial de un documento nuevo están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Dato | Texto |
|---|---|
| Destinatario del campo «Remitido a» que no consta | Por confirmar |
| Fecha de remisión | Pendiente |
| Cifra de esfuerzo, plazo o recurso sin estimar | Por estimar |
| Viabilidad que ninguna evidencia sostiene | Opción «Pendiente de evidencia» marcada |

## ¿Necesita un diagrama?

Agregar un esquema cuando el informe describe relaciones entre componentes o un flujo que el texto no deja ver de una lectura: un servicio nuevo que se conecta con varios sistemas, o un cobro que atraviesa varias etapas. Si la factibilidad se refiere a una herramienta aislada, a un cambio de configuración o a una cifra, bastan un párrafo o una tabla. Una prueba práctica: si quien decide necesita ver qué componentes se hablan entre sí para juzgar la viabilidad, el esquema ayuda; si la viabilidad se entiende leyendo la justificación y las observaciones, el esquema repite lo ya dicho. Una función que se ejecuta dentro de una aplicación existente, sin servicio ni integración nuevos, rara vez lo necesita.

Elegir el tipo por la pregunta, según [diagramas.md](../diagramas.md): límites y componentes, arquitectura o contexto; secuencia de pasos con decisiones, flujo; intercambio en el tiempo entre servicios, secuencia; entidades y cardinalidad, ER; estados de un objeto, estados; responsables y entregas, carriles.

Lo ejecuta el agente que lee esta skill y `diagram-design`, no el script. Si `diagram-design` está disponible, seguir la «Integración» y los «Comandos y medidas» de [diagramas.md](../diagramas.md#comandos-y-medidas). En este tipo: fuente en `assets/diagrams/<nombre>.html`, bloque `figure` con `path`, `id`, `title`, `description` y `source`, llamado desde el texto con `{{ref:id}}`, y lo que no describa un sistema real se declara demostrativo en la imagen y en el pie.


Si falta, aplicar el mismo criterio sin la skill: tipo según la pregunta, pocos nodos, un foco de atención, rótulos legibles y conectores que no crucen texto. Usar un SVG propio o el flujo lineal de 2 a 5 nodos del motor, e informar de que no se usó `diagram-design`. La figura es opcional en la fuente: al quitarla se elimina también la llamada `{{ref:id}}`.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** Abrir cada campo con la conclusión y seguir con las razones y la evidencia. Agrupar las razones por un mismo criterio. Se conserva el orden de los campos del tipo.
- **`unicorntext`.** Revisar la justificación, el impacto, los supuestos y las recomendaciones: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las palabras o frases de trámite que no aportan. Conservar términos técnicos, cifras, responsables, plazos y condiciones.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py informe.json --output informe.pdf
python3 <skill>/scripts/check_report.py informe.pdf
pdftoppm -r 80 -png informe.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('informe.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que cada elección tenga una sola cruz, que ninguna tabla quede partida ni con título huérfano, que la figura se lea y que las firmas queden en la misma página. Entregar el PDF, su manifiesto `.manifest.json` (el comprobador lo exige junto al PDF), el JSON y, si hay figura, sus activos (HTML, SVG y PNG).

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. El motor mantiene enteras las tablas y las cuadrículas que caben en una página, junto con el bloque siguiente cuando es una tabla, una lista o un párrafo, y una lista larga puede partirse siempre que no deje un solo elemento a cada lado. Con ese diseño, los defectos habituales son:

- **Hueco al pie de una página**, porque una tabla, una ficha o una figura entera pasó a la siguiente. No se corrige recortando texto, juntando filas ni quitando datos: el contenido manda y el número de páginas no es una meta. El motor parte una tabla entre filas cuando moverla dejaría más del 35 % de la página en blanco; una ficha o una figura se queda entera. Un hueco así no se arregla: solo se reporta si estorba la lectura.
- **Una página final con solo el histórico de revisiones.** Es posible: si las firmas, la remisión y el histórico no caben juntos y moverlos dejaría más del 35 % de la página en blanco, el histórico va solo en la última página. No se corrige acortando secciones anteriores ni con `new_page`.
- **Subtítulo que salta de línea y deja una palabra sola.** Mantenerlo en una línea.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

La estructura se orientó con un formato genérico de gestión de proyectos de software facilitado como referencia. Redacción, diseño y ejemplo son propios y ficticios.
