# Plan de proyecto

Elegir `document.kind: "plan-proyecto"` para el plan de un equipo pequeño: qué se entrega, en qué hitos, quién responde y cómo se sigue. Empezar por `assets/ejemplo-plan-proyecto.json`. Diagrama: no lleva. La EDT es la lectura del trabajo.

**Contenido:** Decidir antes de redactar; Completar cada campo; Cómo se escribe la EDT; Cómo se comprueba un plan; Personalizar; Qué no inventar; Texto de lo pendiente; Bloques opcionales; ¿Necesita un diagrama?; Revisar la redacción con las skills hermanas; Comprobar y entregar.

La estructura se orienta por la idea de un plan ligero con estructura de desglose del trabajo: el árbol de lo prometido, desglosado en paquetes, con hitos, roles y riesgos ya registrados. No se reproduce el texto de una norma ni el de un formulario ajeno. El orden de los apartados es el del catálogo.

El PDF es compacto: título y contenido en la primera página, sin portada, de cinco páginas en el ejemplo. El histórico de revisiones se imprime al final con `document.show_changes: true`. No exige casilla. Los títulos se escriben con normalidad, en mayúscula de oración: el motor los imprime con numeración «1. Título» y pone en mayúscula solo la primera palabra (con `format.heading_case: "title"`, la de cada palabra).

**Índices.** El ejemplo no los lleva: con cinco páginas, `contents` alargaría la apertura sin cambiar la lectura. Conviene `document.indexes: ["contents"]` cuando el plan pasa de siete páginas. `tables` cuenta la EDT. `figures` no se recomienda: el tipo no lleva figura.

## Decidir antes de redactar

1. **Qué plan es.** El plan de un alcance ya aceptado cita ese alcance por código y versión. Un pedido diferido, como DEMO-SCM-01, se nombra y queda fuera del árbol.
2. **La EDT es la base.** Cada rama es un entregable prometido. El esfuerzo se escribe solo en las hojas, en la unidad del plan. Por omisión, días-persona. Lo que todavía no se estima es `Por estimar`: se ve en la hoja y no entra en la suma. El motor calcula el total de cada rama y el total general. Un total escrito a mano se rechaza.
3. **Qué cifra debe cuadrar.** Si el plan ejecuta una factibilidad, el total de las hojas estimadas es el de esa factibilidad. En el ejemplo son 50 días-persona. La revisión externa de 3 días no suma: DEMO-FAC-01 y DEMO-ALC-01 ya lo dicen.
4. **Quién firma.** Quien elabora el plan, quien lo revisa y la parte solicitante, con los roles y nombres de la entidad. El ejemplo usa arquitectura e ingeniería porque así es su cadena; en un equipo pequeño dos personas cubren los tres papeles, y un rol que nadie ocupa queda «Por confirmar» sin inventar un cargo. La fecha que no ocurrió es Pendiente.

## Completar cada campo

La conclusión va primero dentro de cada campo.

1. **Información de referencia.** Número, proyecto, fecha, responsable, alcance por código y versión, y los documentos relacionados.
2. **Objetivos y alcance.** Qué se entrega y qué queda fuera, con el código del alcance. Se repiten las exclusiones ya escritas.
3. **EDT.** El bloque `wbs`. Las ramas del ejemplo son E1 a E5.
4. **Hitos y calendario.** Hito, fecha, responsable y de qué depende. Las fechas del ejemplo son el calendario propuesto, y el texto lo dice.
5. **Roles y decisiones.** Una tabla de roles y una tabla corta de tipos de decisión, con quién decide y a quién se consulta.
6. **Cadencia de seguimiento.** Revisión semanal. Flujo continuo o sprints, sin fijar la duración de un sprint y sin imponer un método.
7. **Riesgos clave.** Por código del registro, solo los que mueven este plan. El registro completo se cita, no se copia.
8. **Herramientas y comunicación.** Dónde vive el tablero y cómo se cita una tarea. El identificador tiene la forma T- y un número. No se nombra un producto. Si la herramienta no consta, queda Por confirmar.
9. **Firmas.** Las fechas en Pendiente.

Los códigos siguen [codigos.md](../codigos.md). Este tipo usa `PPR`.

## Cómo se escribe la EDT

El bloque `wbs` es un árbol. Cada paquete lleva `id` y `title`. Una rama lleva `children`. Una hoja lleva `effort`: un número de hasta 2 decimales, cero o mayor, o exactamente `Por estimar`. No se mezclan `effort` y `children`. Hasta 4 niveles y 40 paquetes. `unit` es un texto; si se omite, la unidad es días-persona.

No se escribe `total` ni `subtotal`. El motor los rechaza y dice qué quitar. También rechaza un id repetido, un esfuerzo negativo, una hoja sin esfuerzo y una rama sin hijos.

El árbol se imprime en vertical: el identificador, el paquete con sangría por nivel y el esfuerzo. La rama muestra la suma de sus hojas estimadas. La fila final es el total general. `Por estimar` se imprime en la hoja y queda fuera de esa suma. El formato de número usa coma decimal y punto de miles, y no consulta el idioma del sistema.

## Cómo se comprueba un plan

- **Alcance.** Los identificadores de las ramas existen como entregables del alcance citado.
- **Total.** La suma de las hojas con número es el total impreso, y coincide con la factibilidad cuando el plan es de esa estimación.
- **Hueco al pie de una página**, porque una tabla, una ficha o una figura entera pasó a la siguiente. No se corrige recortando texto, juntando filas ni quitando datos: el contenido manda y el número de páginas no es una meta. El motor parte una tabla entre filas cuando moverla dejaría más del 35 % de la página en blanco; una ficha o una figura se queda entera. Un hueco así no se arregla: solo se reporta si estorba la lectura.
- **Fechas.** El calendario cabe entre el inicio y el fin propuestos del alcance. La capacitación y la entrega de la cadena caen en la semana de implementación.
- **Riesgos.** Cada código citado existe en el registro, con el estado que ese registro trae.
- **Pedido diferido.** Si una solicitud de cambio está diferida, sus entregables no aparecen en el árbol.

## Personalizar

Se cambian `brand.entity`, `brand.unit`, `brand.accent` y, si hace falta, `brand.logo`. El código sigue el prefijo de la entidad. `paper` admite `A4` y `Letter`. `unit` puede ser horas u otra unidad de la entidad. Los identificadores de paquete los elige el proyecto; no tienen que ser E1.

## Qué no inventar

- Una fecha de firma o una aprobación que no conste.
- Un responsable de pruebas o de despliegue que la cadena deja por confirmar.
- Días de un pedido que quedó diferido.
- Los 3 días de la revisión externa dentro de los 50.
- El nombre de un producto de tablero.

## Texto de lo pendiente

Pendiente, Por confirmar, Por estimar y Propuesto están en [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio de este tipo:

| Situación | Qué escribir |
|---|---|
| Hoja cuyo esfuerzo no está estimado | Por estimar, en effort |
| Rol que el alcance no nombra | Por confirmar |
| Herramienta del tablero | Por confirmar, sin nombrar un producto |
| Firma | Pendiente |

## Bloques opcionales

- **Sin hueco de estimación.** Se quita la hoja en `Por estimar` cuando todo el trabajo está estimado. El total sigue siendo la suma de las hojas que quedan.
- **Sin índice.** El ejemplo no lleva `document.indexes`. Se añade `tables` cuando se quiere listar la EDT.

## ¿Necesita un diagrama?

No. La EDT ya es el árbol, con sangría y totales. Un esquema repetiría los mismos paquetes, y la arquitectura del sistema ya está en la factibilidad y en el alcance.

## Revisar la redacción con las skills hermanas

- **`minto-pyramid`.** La apertura dice qué alcance se ejecuta, cuál es el total y qué pedido queda fuera. El árbol y los hitos sostienen esa frase.
- **`unicorntext`.** Revisar objetivos y cadencia: quitar el contraste «no es X sino Y», las enumeraciones de tres elementos por costumbre, la raya larga y las frases de trámite. Conservar cifras, fechas, códigos y las palabras Por estimar y Por confirmar.

Estos criterios se aplican siempre, por escrito, y no dependen de que esas skills estén instaladas. Si el usuario nombra una de ellas y está disponible, se usa además, respetando su modo de activación (el nombre exacto puede llevar un prefijo de la instalación, como `anthropic-skills:`). En la entrega, decir cuál de los dos caminos se siguió.

## Comprobar y entregar

Antes de compilar, comprobar el entorno con `python3 -c "import reportlab, pypdf, pdfplumber"`. Si falla con `ModuleNotFoundError`, seguir la instrucción de instalación de `SKILL.md` y usar ese intérprete en los comandos siguientes.

```sh
python3 <skill>/scripts/build_report.py plan.json --output plan.pdf
python3 <skill>/scripts/check_report.py plan.pdf
pdftoppm -r 80 -png plan.pdf pagina
```

Sin Poppler, las mismas imágenes salen con las dependencias del motor:
`python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i, p in enumerate(pdfplumber.open('plan.pdf').pages, 1)]"`.

Renderizar todas las páginas y abrirlas. Revisar que el total de la EDT coincida con la suma de las hojas, que `Por estimar` se vea y que el histórico comparta página con las firmas. Entregar el PDF, su manifiesto `.manifest.json` y el JSON.

El comprobador no detecta los saltos de página mal repartidos; solo se ven en las imágenes. Una tabla que cabe en una página no se parte, salvo que moverla dejara más del 35 % de la página en blanco: entonces se parte entre filas, con su título y encabezado repetidos y al menos tres filas en cada página. Los defectos habituales son un hueco al pie porque la tabla siguiente no cabe, y una página final con solo el histórico.

Después de cada ajuste, volver a compilar y renderizar todo: un cambio en una página mueve las siguientes.

Los saltos medidos de la muestra:

- La página 1 cierra con los objetivos y deja un hueco al pie, porque la EDT no cabe debajo y se mantiene entera en la página 2, con el total 50 y la hoja en Por estimar.
- La página 2 cierra con el título de hitos y su párrafo. La tabla de hitos abre la página 3. El hueco queda por debajo de un tercio.
- La página 4 cierra con las herramientas y deja un hueco mayor que un tercio. Las firmas van con `new_page` para quedar con el histórico.
- La página 5 reúne firmas e histórico. Debajo queda espacio libre: es el final del documento. El espacio de firma queda cerca del nombre.
