# Ficha de modelo

Elegir `document.kind: "ficha-modelo"` para acompañar un modelo estadístico o de aprendizaje automático: para qué sirve, con qué datos se hizo, cómo rinde, para quién, y qué no debe hacerse con él. Empezar por `assets/ejemplo-ficha-modelo.json`. Usa `format.profile: "institucional"`, como los demás tipos compactos: el perfil APA es solo del `informe`. Diagrama: no lleva. Quién decide y qué marca el modelo cabe en dos frases. La arquitectura del sistema ya está en la factibilidad.

**Contenido:** Decidir antes de redactar; Completar cada campo; Qué no afirma la ficha; Cómo se comprueba una ficha; Personalizar; Qué no inventar; Qué se elimina cuando algo no aplica; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

La estructura se orienta por la idea de una ficha de modelo: uso previsto, datos, modelo, evaluación y limitaciones. No se reproduce el texto de una publicación ni se afirma de ella nada que no esté en esta guía. El orden de los apartados es el del catálogo.

El PDF es compacto: título y contenido en la primera página, sin portada, de cuatro páginas en el ejemplo. El histórico de revisiones se imprime al final con `document.show_changes: true`. No hay bloque nuevo: las tablas y las fichas de campos bastan. Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Índices.** El ejemplo no los lleva: con cuatro páginas, `contents` alargaría la apertura sin cambiar la lectura. Conviene `document.indexes: ["contents"]` cuando la ficha pasa de siete páginas. `tables` y `figures` no se recomiendan en una ficha corta.

## Decidir antes de redactar

1. **Qué hace el modelo y quién responde.** El modelo recomienda o marca. Una persona decide. Esa frase va en el uso previsto, con el nombre del rol que decide.
2. **El estado es una casilla.** Este tipo exige una elección marcada (`form: True` y `choice`). Es el estado del modelo: una sola marca entre las opciones del documento. Por omisión del ejemplo: En desarrollo, En validación, En uso y Retirado. La entidad puede cambiar las palabras. Sin esa casilla, o con la marca fuera de la lista, el motor rechaza el documento y dice qué añadir.
3. **De dónde salen las cifras.** Toda cifra de rendimiento lleva al lado la procedencia de los datos: el conjunto, la fecha de corte y si los datos son reales o sintéticos. Esa declaración no se omite.
4. **Datos sintéticos.** Una cifra sobre datos sintéticos mide el generador de los datos, no el negocio. El ejemplo lo dice en la apertura y otra vez junto a las métricas. No se presentan como resultado de producción.

## Completar cada campo

La conclusión va primero dentro de cada campo.

1. **Información de referencia.** Nombre, versión, fecha, responsable, estado (la casilla) y documentos relacionados por código. La evaluación de impacto en datos se cita por su código, o queda «Por confirmar» si no existe.
2. **Uso previsto.** Qué marca o qué recomienda, quién lo usa, quién decide al final y para qué no debe usarse. Lo que no debe hacerse incluye los canales que el sistema ya dejó fuera.
3. **Datos.** Origen, periodo, fecha de corte, tamaño, variable objetivo y su definición, sesgos de selección conocidos y el tratamiento de datos personales. La frase que declara si los datos son reales o sintéticos va en este apartado, visible, no en una nota al pie.
4. **Modelo.** Tipo de algoritmo, variables principales, versión de las librerías y cómo reproducir el entrenamiento. La versión que nadie ha fijado, y el script que el ejemplo no trae, quedan «Por confirmar». No se inventa un comando.
5. **Evaluación.** Una tabla de métricas (métrica, valor, conjunto, intervalo, procedencia) y una tabla por grupos (grupo, tamaño, métrica, diferencia respecto del total, procedencia). El umbral de aceptación y la decisión van después. La diferencia es el valor del grupo menos el total del mismo conjunto. Si no cuadra, se corrige la tabla: el motor no la calcula.
6. **Limitaciones y riesgos.** Lo que el modelo no hace bien, con el registro de riesgos citado por su código. Solo los riesgos que cambian el uso de la ficha.
7. **Monitoreo y mantenimiento.** Qué se vigila, con qué umbrales de alerta, cuándo se reentrena y quién decide retirarlo. El umbral que la entidad no ha fijado es «Por confirmar».
8. **Aprobaciones.** Responsable del modelo y revisión independiente. La fecha que no ocurrió es «Pendiente».

Los códigos siguen [codigos.md](../codigos.md). Este tipo usa `MOD`.

## Qué no afirma la ficha

La ficha no afirma equidad. Dice qué grupos se midieron, el tamaño, la métrica y la diferencia respecto del total. Dice también qué grupos no se pudieron medir y por qué. Un grupo sin datos no se rellena con cero: el tamaño queda «Por confirmar» y la métrica no se inventa.

No se inventan métricas presentadas como reales. Las del ejemplo son de demostración y lo dicen en el título de la tabla y en la procedencia. No se reutilizan como umbral de un sistema real.

## Cómo se comprueba una ficha

- **Procedencia.** Cada cifra de la evaluación tiene al lado el conjunto y si los datos son reales o sintéticos.
- **Sintéticos.** Si los datos son sintéticos, el texto dice que la cifra mide el generador. No aparece como resultado del negocio.
- **Grupos.** La suma de los tamaños medidos es el tamaño del conjunto. La diferencia de cada fila es la métrica del grupo menos la del total. El grupo no medido está nombrado, con el motivo.
- **Estado.** Hay una sola marca, y es una de las opciones.
- **Fechas.** Los datos son posteriores al plan de pruebas que les dio forma y anteriores a la entrega. La fecha del documento no adelanta una aprobación.
- **Coherencia.** Nombres, cargos y códigos coinciden con la cadena. El registro de riesgos citado es el del proyecto.

## Personalizar

- `brand.entity`, `brand.unit`, `brand.accent` y `brand.logo`. `brand.fonts` solo con licencia verificada.
- `document.code`, `document.short_title` y `document.paper` (`A4` o `Letter`).
- Las palabras del estado. Siguen siendo una sola marca.
- Responsable, revisión independiente y umbrales, con lo que la entidad haya fijado.

## Qué no inventar

Métricas, intervalos y tamaños que no salgan de un conjunto citado. Una librería o un script que nadie entregó. Una evaluación de impacto en datos que no existe: «Por confirmar». Una aprobación o una fecha de firma. Un grupo medido para que la tabla se vea completa. El texto de una publicación sobre fichas de modelo.

Las palabras para lo que falta están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Dato | Texto |
|---|---|
| Fecha de aprobación o de retirada aún no ocurrida | Pendiente |
| Evaluación de impacto, umbral o script que no consta | Por confirmar |
| Grupo que no se pudo medir | Se nombra y se dice por qué. El tamaño, si no hay registros, es Por confirmar |
| Cifras del ejemplo | De demostración, con la procedencia en la misma tabla |

## Qué se elimina cuando algo no aplica

- **Sin intervalo.** La celda dice «Por confirmar». No se pone un rango inventado.
- **Sin un grupo medido.** Se quita esa fila. El párrafo de los grupos no medidos se queda.
- **Sin alerta acordada.** El campo de umbral queda en «Por confirmar». No se copia el umbral del ejemplo.

## ¿Necesita un diagrama?

No. La ficha responde quién decide y qué cifra, con qué datos. Eso cabe en el texto y en las dos tablas. Un esquema del modelo repetiría variables que ya están en una fila, y un esquema del sistema repetiría la factibilidad.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** La apertura dice qué marca el modelo, que los datos son sintéticos o reales, y que una persona decide. El resto sostiene esa frase.
- **`unicorntext`.** Revisar el uso previsto y la decisión: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las frases de trámite. Conservar cifras, procedencia, códigos y la palabra Pendiente.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py ficha.json --output ficha.pdf
python3 <skill>/scripts/check_report.py ficha.pdf
pdftoppm -r 80 -png ficha.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('ficha.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que la casilla marcada sea la del estado, que cada cifra lleve su procedencia y que el histórico comparta página con las firmas. Entregar el PDF, su manifiesto `.manifest.json` y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. Una tabla que cabe en una página no se parte. Los defectos habituales son un hueco al pie porque la tabla siguiente no cabe, y una página final con solo el histórico. El apartado de aprobaciones se deja en esa página, con las firmas.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

En la muestra medida:

- La página 1 cierra con el párrafo de datos. Las fichas de ese apartado abren la página 2. El hueco queda por debajo de un tercio.
- La página 2 cierra con la tabla de una sola métrica y deja un hueco, porque la tabla por canal no cabe debajo y se mantiene entera en la página 3.
- La página 4 reúne aprobaciones, firmas e histórico. Debajo queda espacio libre: es el final del documento. La casilla marcada es En validación.
