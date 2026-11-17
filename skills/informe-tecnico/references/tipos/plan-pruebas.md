# Plan y registro de pruebas de aceptación

Elegir `document.kind: "plan-pruebas"` para acordar cómo se aceptará un software, ejecutar los casos y registrar la decisión final de las partes. Partir de `assets/ejemplo-plan-pruebas.json`. Diagrama: no; los pasos y sus resultados bastan para decidir sobre cada criterio. El plan toma sus criterios del alcance acordado ([alcance-proyecto.md](alcance-proyecto.md)).

Es un formulario compacto, sin portada, con las casillas de resultado junto a cada caso. El histórico se imprime al final con `document.show_changes: true`. Los índices son opcionales: para planes extensos conviene `document.indexes: ["contents"]`; las fichas `testcase` tienen marcadores y referencias, pero no un índice impreso propio ni entradas en `tables`. Ver el esquema en [testcase.md](../contrato/testcase.md).

La muestra tiene nueve páginas: preparación en las tres primeras, CP-01 a CP-05 en las páginas 4 a 8, certificado pendiente en la 8 y firmas e histórico en la 9. Los casos completos dejan huecos al pie, especialmente en las páginas 4 a 7: el caso siguiente no cabe en el espacio restante y pasa entero. Es el compromiso elegido para consultar y firmar cada ficha sin cortes. No forzar saltos ni rellenar con texto; si se necesita reducir páginas, revisar la extensión de las fichas manteniendo sus criterios y evidencia. Un caso largo admite continuidad entre filas con su cabecera repetida.

## Decidir antes de redactar

Identificar proyecto, versión del software, partes, alcance y criterios acordados. Cada criterio da al menos un caso; para cada uno hacen falta precondiciones reproducibles, actividades y un resultado observable. Si el criterio carece de umbral o método, escribir «Propuesto, por confirmar con (área)» y resolverlo con la parte solicitante antes de ejecutar. La aprobación del diseño, el resultado de un caso y la aceptación final son decisiones separadas.

La decisión de mayor peso es la aceptación final. Requiere evidencia de todos los criterios y una decisión expresa de la parte solicitante. Un caso sin ejecutar deja el certificado «Pendiente». Un incumplimiento bloquea la aceptación; un reparo requiere observación, responsable, tratamiento y decisión documentada. El motor valida el formato de cada elección; la cobertura, la suficiencia de la evidencia y la decisión final las revisa quien prepara el documento.

Usar el código de la entidad (`DEMO-ATP-01` en el ejemplo), identificar quién ejecuta y quién acepta y conservar nombres y cargos de los documentos anteriores. La fecha del documento es la elaboración o la última revisión; la fecha de ejecución y la aprobación del diseño quedan «Pendiente» mientras no ocurran. La elaboración del plan sigue al alcance; la aprobación del diseño precede a la ejecución y la aceptación sigue a la revisión de resultados. Las fechas futuras del ejemplo pertenecen exclusivamente al escenario ficticio.

## Completar cada campo

1. **Información de referencia.** Proyecto, parte solicitante, equipo ejecutor, líder y fecha de ejecución. Añadir código y fecha del alcance y los antecedentes para seguir la cadena documental.
2. **Definición de aceptación.** Explicar el acuerdo sobre cobertura y método. Registrar responsable de aprobar el diseño y fecha de aprobación. Los responsables de ejecutar y aceptar se indican por parte, sin suponer que son la misma persona. Describir los tres resultados y qué implica cada uno.
3. **Prerrequisitos.** Identificar entorno, versión del módulo, comunicaciones y accesos. Indicar usos y cuentas de prueba, sin credenciales, y los datos necesarios para reproducir las pruebas. Lo que falte lleva el texto de [pendientes-y-estado.md](../pendientes-y-estado.md).
4. **Aplicación y módulo.** Una sección por aplicación y una subsección por módulo. Añadir tantos bloques `testcase` como casos hagan falta, con IDs únicos en todo el documento. Una nueva ejecución puede usar otro ID y citar el caso anterior, para conservar la evidencia de ambos intentos. Registrar los resultados y la repetición de un caso es una versión nueva del mismo plan, con el caso repetido como caso nuevo que cita el original.
5. **Certificado de aceptación de pruebas (ATR).** Identificar el proyecto, registrar estado y fecha y escribir la decisión sustentada. Antes de ejecutar, conservar una frase explícita de aceptación pendiente. No reutilizar una declaración de aceptación consumada de una plantilla. El certificado es el registro de la decisión de las partes sobre los criterios del alcance: no es la certificación de un tercero ni acredita el cumplimiento de una norma, y «Conforme» se refiere al criterio de aceptación acordado.
6. **Firmas de aceptación.** Las dos partes, con nombre, cargo, espacio de firma y fecha.
7. **Firmas de responsabilidad.** Elaboración, revisión y aprobación del documento. Cada tabla de firmas queda entera; la de responsabilidad cierra el cuerpo, antes del histórico.

### Completar un caso `testcase`

- `id` y `title`: identificador estable y nombre reconocible del criterio. `{{ref:CP-01}}` crea un enlace con el rótulo del caso.
- `description`: criterio de origen y qué verifica; ahí también van los requisitos que cubre el caso («Criterio E3 del alcance y RF-05 de la especificación»). La fecha de cada ejecución va en el resultado observado y la duración de los pasos no se estima por caso. `preconditions`: estado inicial, entorno y recursos. `expected`: umbral o condición de éxito del caso.
- `steps`: lista no vacía; cada paso lleva `task` (tarea breve), `activity` (acción reproducible), `expected` (resultado esperado) y `actual` (resultado observado con localizador de evidencia; si nadie dio el localizador, «Localizador de evidencia: Por confirmar»). Los números de paso se generan.
- `options`: exactamente tres textos distintos, personalizables. Antes de ejecutar, `executed: false` (también es el valor por omisión), `selected` ausente o `null`, resultados reales «Pendiente» y las tres casillas vacías. Al ejecutar, usar `executed: true` y `selected` con exactamente uno de esos textos. Una lista de resultados o una marca con `executed: false` se rechaza.
- `responsible`: quien acepta ese caso; «Por confirmar» si no consta. `observations`: «Pendiente de ejecución» antes de ejecutar; después, evidencia, incidencias y tratamiento de reparos. Usar «Sin observaciones» solo cuando esa conclusión conste.

No escribir el resultado esperado como resultado real sin evidencia. Si una ejecución se interrumpe, describir hasta dónde llegó y aplicar la clasificación acordada; no dejar una marca que dé por terminado lo que quedó pendiente. Un caso marcado no autoriza por sí solo la puesta en producción.

## Cómo se comprueba

Comparar los casos con todos los criterios del alcance. Mantener umbrales, unidades, nombres, cargos y códigos. Revisar que cada paso tenga un resultado real verificable cuando se declare ejecutado y que los reparos indiquen responsable y tratamiento. En el ejemplo, los cinco criterios de DEMO-ALC-01 dan los casos CP-01 a CP-05; el lote de 100 pagos para medir rendimiento es una propuesta demostrativa, y las 100 confirmaciones duplicadas y el ancho de 360 píxeles provienen del alcance.

El motor exige una marca en cada caso ejecutado y permite ninguna antes de ejecutar. No comprueba que los registros externos existan, que la matriz de navegadores esté completa ni que el certificado concuerde con las pruebas. Esa revisión es de contenido.

## Personalizar

Cambiar `brand.entity`, `brand.unit`, `brand.accent` y `brand.logo` (PNG/JPEG relativo al JSON), `document.code`, `paper` y firmantes. Reemplazar los rótulos «parte solicitante» y «equipo ejecutor» donde aparezcan. Los textos de las opciones se pueden cambiar por caso; si hay `selected`, actualizarlo al mismo texto. Las etiquetas fijas de la ficha y de los pasos están en español en el motor.

Eliminar una sección opcional sin datos y sus referencias. `selected` es opcional; el certificado, las firmas y las precondiciones se conservan con sus pendientes. Sin índices basta omitir `document.indexes`. Una skill instalada sola incluye el ejemplo y esta guía; no necesita archivos de la carpeta `docs`.

## Qué no inventar

No inventar ejecución, evidencia, aprobaciones, firmas, fechas efectivas ni responsables. Para estado, historial de un documento nuevo y palabras de lo pendiente, aplicar [pendientes-y-estado.md](../pendientes-y-estado.md). Lo propio del plan:

| Dato | Texto o estado |
|---|---|
| Caso aún no ejecutado | `executed: false`, sin `selected`; resultado real «Pendiente» |
| Certificado antes de decidir | Pendiente |
| Fecha de ejecución sin ejecución | Pendiente |
| Versión o acceso no confirmado | Por confirmar con (área) |

## ¿Necesita un diagrama?

No. La trazabilidad al alcance y las fichas expresan qué se prueba y cómo se decide. El plan puede citar la arquitectura o el perímetro del alcance sin repetirlos. No necesita `diagram-design` para compilar ni revisar este ejemplo.

## Revisar la redacción con las skills hermanas

Aplicar los criterios incorporados de Minto: en la decisión final, respuesta sustentada primero y después razones y evidencia; conservar el orden operativo en los pasos. Aplicar el criterio de unicorntext: quitar relleno y duplicaciones, conservando términos y repeticiones necesarias para consultar cada caso por separado. No requieren instalar esas skills; si el usuario las invoca, aplicar además sus instrucciones disponibles.

## Comprobar y entregar

Comprobar el entorno: `python3 -c "import reportlab, pypdf, pdfplumber, PIL"`. Si faltan paquetes, crear un entorno virtual fuera de la entrega e instalar `reportlab>=4.4,<5`, `pypdf>=6,<7`, `pdfplumber>=0.11,<1` y `Pillow>=11,<13`, según `SKILL.md`. Usar su intérprete en todos los comandos:

```sh
python3 <skill>/scripts/build_report.py plan.json --output plan.pdf
python3 <skill>/scripts/check_report.py plan.pdf
pdftoppm -r 80 -png plan.pdf pagina
```

Sin Poppler: `python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i,p in enumerate(pdfplumber.open('plan.pdf').pages,1)]"`.

Abrir todas las imágenes. Comprobar casillas vacías o una única cruz con texto en negrita por caso ejecutado; las marcas son vectoriales y el texto extraído no las distingue. Una ficha que cabe en una página pasa entera a la siguiente si falta espacio. Una ficha larga se divide solo entre filas de pasos, repite la cabecera con descripción, precondiciones y resultado esperado y conserva el resultado, responsable y observaciones junto al último paso. Si una ficha repetida y un paso no caben, el motor pide acortar o dividir la actividad; no reduce la letra.

Entregar PDF, manifiesto `.manifest.json` y JSON editable con sus activos. El comprobador exige el manifiesto y no verifica la verdad de los resultados ni de la aceptación.
