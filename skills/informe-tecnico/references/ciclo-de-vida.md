# Ciclo de vida documental

`document.lifecycle` es opcional y vale para todos los tipos. Sin ese bloque, el motor conserva exactamente la salida anterior. Describe la situación de un documento, separada del estado técnico de una decisión, un modelo, una prueba o un proyecto. No declara por sí mismo que un software esté aceptado.

Los identificadores y rótulos son fijos para que la marca de un documento fuera de uso sea inequívoca. No se admiten alias personalizados. `document.status` permanece en la fuente, en el manifiesto y en los metadatos del PDF; si hay ciclo de vida, el pie imprime únicamente el estado de `lifecycle` y evita duplicaciones o contradicciones con el estado libre. La marca del ciclo no se oculta con `show_status_in_footer: false`. Sin ciclo, esa opción conserva su comportamiento anterior.

## Estados y transiciones

| Estado | Significado y quién lo cambia | Paso permitido |
|---|---|---|
| `borrador` | Quien elabora prepara el contenido, con pendientes explícitos. | `en-revision`; `sustituido` o `retirado` si la copia circuló y se decide dejarla fuera de uso; `archivado` si se abandona y se acuerda su conservación |
| `en-revision` | Quien coordina la revisión confirma que el documento circula para revisión. | `borrador` para corregir; `vigente` cuando la autoridad acepta la versión; `sustituido` o `retirado` si se reemplaza o deja de circular sin aceptación |
| `vigente` | La autoridad competente del documento confirma su uso. La persona que custodia registra el estado con esa evidencia. | `sustituido` o `retirado` |
| `sustituido` | Quien autoriza la sustitución identifica el sucesor; quien custodia conserva el anterior. | `archivado` |
| `retirado` | Quien autoriza la baja fija la fecha efectiva; quien custodia marca la copia. | `archivado` |
| `archivado` | Quien custodia conserva la evidencia según el plazo y repositorio autorizados. | Estado final de esta copia; una reactivación necesita una decisión y una versión o documento nuevo |

Las transiciones se controlan en el expediente y en el histórico. El motor recibe un corte, valida sus datos y compone su marca; no conoce una edición anterior ni puede verificar quién autorizó el cambio. No convertir una fecha escrita por el agente en aprobación. Cuando falte autorización, mantener borrador o en revisión y registrar la acción como prevista. Una propuesta enviada que no se aceptó puede sustituirse por una revisión o retirarse de circulación por decisión de quien la emite; ese cambio no convierte la propuesta en aprobada ni exige inventar un paso por vigente.

## Congelar y conservar

Congelar una versión significa que la versión aprobada y sus activos se conservan sin editar. `frozen_on` registra la fecha documentada de esa congelación; no exige que todo documento sustituido hubiera sido aprobado. Conservar PDF, fuente, activos y manifiesto con hashes en el expediente. El motor comprueba coherencia de fechas, pero no implementa un repositorio inmutable ni una firma electrónica.

Una corrección posterior al congelado requiere una versión nueva. No cambiar silenciosamente el JSON asociado a un PDF firmado. Archivar conserva el documento y su trazabilidad; no borra la fuente, el PDF ni su antecedente. El plazo y la ubicación de conservación proceden de la política de la entidad, no de una cifra legal inventada.

## Campos y marcas

```json
"lifecycle": {
  "state": "sustituido",
  "superseded_by": "DEMO-PRO-01",
  "superseded_by_version": "0.2"
}
```

- `state` es obligatorio dentro del objeto: `borrador`, `en-revision`, `vigente`, `sustituido`, `retirado` o `archivado`.
- `frozen_on`: fecha `YYYY-MM-DD`, opcional desde vigente y no posterior a `document.date`.
- `supersedes`: lista no vacía de códigos, sin repeticiones, desde vigente. No citarse a sí mismo. Antes de la sustitución efectiva, un borrador cita su antecedente en el contenido.
- `superseded_by`: obligatorio con sustituido; también puede conservarse al archivar. No puede ser uno de los predecesores. Puede ser el código propio si se indica una versión sucesora mayor.
- `superseded_by_version`: texto opcional con partes numéricas separadas por punto, como `"0.2"` o `"1.10.3"`. Requiere `superseded_by`. Con el código propio es obligatorio y mayor que `document.version`; se comparan partes numéricas, sin tratar la versión como decimal (1.10 es mayor que 1.9). Los ceros finales no distinguen versiones: 1.0 y 1.0.0 son iguales. Con otro código se puede omitir; si se indica, también usa la forma numérica.
- `retire_on`: obligatorio con retirado, admitido con vigente y archivado. Con vigente debe ser posterior a `document.date`; con retirado o archivado no puede ser futura respecto al corte. Nunca anterior a `frozen_on`.
- `retention`: obligatorio solo con archivado, objeto con `period` y `location`, ambos textos no vacíos. Deben decir por cuánto tiempo y dónde se conserva.

Ejemplo de conservación: `"retention": {"period": "Plazo acordado en la política de la entidad", "location": "Archivo documental del proyecto"}`. En una entrega real reemplazar la descripción del plazo por el plazo que conste. No declarar archivado mientras esos datos estén por confirmar.

Los códigos de relaciones usan el esquema de [codigos.md](codigos.md): prefijo de 2 a 5 letras mayúsculas, tipo de tres letras y número de al menos dos cifras. Se valida su formato y que no creen autorreferencia; la existencia del documento se comprueba en el expediente. El ejemplo de sustitución puede citar el sucesor previsto por el escenario sin un archivo completo de ese sucesor.

`document.date` es la fecha del cambio que declara este corte: se usa como fecha efectiva en la banda de sustituido y archivado. `retire_on` es la fecha efectiva de retirado. No se usa la fecha del equipo para decidir estados ni recalcular una banda al recompilar un documento antiguo.

Sustituido, retirado y archivado llevan en cada página una banda de texto y borde negros con estado, fecha y sucesor cuando corresponde, y «No usar para decidir». Se coloca entre la cabecera y el cuerpo, sin cambiar los márgenes anteriores. Vigente con retiro programado lleva allí una nota discreta con la fecha. Borrador, en revisión y vigente sin anuncio se reconocen en el pie y no añaden otra banda. Una banda demasiado larga falla con una indicación de corregir el código; la letra no se reduce automáticamente.

El manifiesto conserva el bloque tanto en `document.lifecycle` como en `lifecycle`. El comprobador exige que coincidan y comprueba la banda, su texto y su borde en cada página. Una mención en el cuerpo no reemplaza la banda. No es una comprobación de la autoridad o de la veracidad de la declaración.

## Versiones, sustituciones y cambios de proyecto

Una versión nueva del mismo documento conserva código y aumenta `document.version`. Un documento distinto que lo sustituye recibe el siguiente número y cita al anterior; marcar la copia vieja sin borrarla. Los documentos de un proyecto no cambian de versión todos juntos: cada uno registra sus cambios reales.

Antes de que la parte solicitante acepte una propuesta, modificarla produce otra versión de esa propuesta. Después de aceptada, un cambio de lo acordado se tramita como solicitud de cambio, con evaluación y autorización; no se sustituye el acuerdo en silencio. Una prueba fallida respecto de lo ya acordado exige corregir el software y volver a comprobarlo. No equivale por sí sola a una ampliación de alcance ni a una cotización nueva.

La muestra conserva DEMO-PRO-01, versión 0.1, como sustituida por DEMO-PRO-01, versión 0.2. Es una revisión ordinaria del mismo documento, sin renumerarlo. La banda y el pie identifican código y versión sucesora. Un documento distinto con otro código también sigue siendo un sucesor válido, con versión opcional. Las situaciones de las muestras son simulaciones explícitas y no crean aceptación comercial en la cadena de ejemplos.

El histórico de la copia sustituida conserva una única fila por versión editorial. La fila 0.1 mantiene su fecha de edición y explica en el resumen la fecha de sustitución y el sucesor; el corte del ciclo usa `document.date`. No se añade una segunda fila 0.1 por cambiar la marca de la copia, ni se inventa una versión de contenido que no se editó. Conservar la fuente original y el registro de custodia para documentar esa acción sobre la copia.

## Ejemplos, comprobación y entrega

`assets/ejemplo-propuesta-sustituida.json` deriva de la propuesta sin modificar su fuente original. Conserva el contenido y añade el cambio de estado; su muestra tiene cuatro páginas con banda en todas. `assets/ejemplo-propuesta-retiro-programado.json` es una simulación breve de una página, con una nota de retiro futuro. La segunda no acredita una aceptación de la propuesta de la cadena.

Con el entorno de `SKILL.md` (reportlab, pypdf, pdfplumber y Pillow), compilar con `python3 <skill>/scripts/build_report.py fuente.json --output documento.pdf`, comprobar con `python3 <skill>/scripts/check_report.py documento.pdf` y renderizar todas las páginas a 80 ppp. Abrirlas y revisar texto, borde y legibilidad de la banda también en escala de grises. Entregar PDF, manifiesto, JSON y activos. El ciclo no autoriza a borrar ni a sobrescribir documentos anteriores.
