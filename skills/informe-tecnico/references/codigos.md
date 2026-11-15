# Códigos documentales

`document.code` identifica el documento. Se imprime en el pie de cada página y sirve para citar un documento desde otro. La skill no impone el código de nadie: propone un esquema general que el proyecto o la entidad reemplaza.

## Qué código se usa

En este orden:

1. **El esquema de la entidad, si lo tiene.** Un formato institucional con su propio código se usa tal cual. Es parte de la identidad de la entidad: la skill no lo cambia, no lo copia a otros proyectos y no lo escribe en documentos de otra entidad.
2. **El del proyecto, si hay un proyecto con nombre.** El código sale del proyecto con el esquema de abajo. Un agente que abre la carpeta de un proyecto toma el prefijo de su nombre.
3. **El de la entidad o unidad emisora, si no hay proyecto.** El prefijo sale de quien emite el documento.

## Esquema general

`<PREFIJO>-<TIPO>-<NN>`, por ejemplo `ATL-FAC-01`.

- **Prefijo.** De 2 a 5 letras mayúsculas derivadas del nombre del proyecto: de «Proyecto Atlas», `ATL`. Con un nombre de dos o más palabras se usan las iniciales o las primeras letras que lo hagan reconocible. Si hay duda, se pregunta al usuario. No se adivina un prefijo que otro proyecto ya use.
- **Tipo.** Tres letras, según la tabla.
- **Número.** Dos cifras, consecutivo por proyecto y por tipo. Antes de asignarlo se miran los documentos del mismo tipo que ya existen en el proyecto y se continúa la serie.
- **Versión fuera del código.** La versión va en `document.version`. Una nueva versión del mismo documento conserva su código y sube la versión. Un documento que sustituye a otro recibe el siguiente número y cita al anterior.

| Tipo de documento | Código |
|---|---|
| `informe` | INF |
| `acta-entrega` | ENT |
| `acta-reunion` | REU |
| `informe-factibilidad` | FAC |
| `registro-requerimientos` | REQ |
| `alcance-proyecto` | ALC |
| `acta-capacitacion` | CAP |
| `plan-pruebas` | ATP |
| `registro-riesgos` | RIE |
| `propuesta-servicio` | PRO |
| `decision-arquitectura` | ADR |
| `descripcion-arquitectura` | ARQ |
| `especificacion-requisitos` | ERS |
| `ficha-modelo` | MOD |
| `evaluacion-impacto-datos` | EID |
| `informe-cierre` | CIE |
| `acta-baja` | BAJ |
| `ficha-proceso` | FPR |
| `solicitud-cambio` | SCM |
| `plan-proyecto` | PPR |
| `traspaso-operacion` | TRA |
| `notas-version` | NOV |

Cada tipo nuevo del catálogo añade aquí su código al incorporarse. Los ejemplos de riesgos, de propuesta, de especificación, de ficha, de evaluación de impacto, de solicitud, de plan, de traspaso y de notas ya usan `DEMO-RIE-01`, `DEMO-PRO-01`, `DEMO-ERS-01`, `DEMO-MOD-01`, `DEMO-EID-01`, `DEMO-SCM-01`, `DEMO-PPR-01`, `DEMO-TRA-01` y `DEMO-NOV-01`.

## Entre documentos

Los documentos de un mismo proyecto se citan por su código: el registro de requerimiento `ATL-REQ-01` es el «requerimiento asociado» de la factibilidad `ATL-FAC-01`, que antecede al alcance `ATL-ALC-01`. Un código citado debe existir en el proyecto: si el documento citado todavía no tiene número, se escribe «Por confirmar» como indica [pendientes-y-estado.md](pendientes-y-estado.md). Un documento cita a los de fecha anterior y no a uno que se emitirá después. Manda la fecha del documento y no el orden en que se redactó: uno fechado antes puede citarse aunque se escribiera más tarde. Cuando dos documentos comparten día y cada uno necesita al otro, el que se emite primero cita al segundo solo en una versión posterior. Para citar una versión concreta se escribe «SRO-ALC-01, versión 0.2» (con el código del proyecto): el posterior, al emitirse, cita al anterior, y un documento ya fechado no se reedita para añadirle el código de otro más reciente.

## En los ejemplos de la skill

Los ejemplos usan el prefijo `DEMO` (`DEMO-FAC-01`). Son ficticios y no se reutilizan en un documento real.

## Versiones y ciclo de vida

Aplicar [ciclo-de-vida.md](ciclo-de-vida.md): una revisión conserva código y aumenta versión; un documento distinto que sustituye a otro recibe el siguiente número y lo cita. Cada documento del proyecto registra sus propios cambios, sin subir todas las versiones juntas. Conservar las copias anteriores con su marca y evidencia.

Antes de aceptar una propuesta, un cambio produce una nueva versión de esa propuesta. Después de aceptarla, tramitar lo que cambie el acuerdo como solicitud de cambio. Si una prueba falla sobre lo acordado, corregir el software y repetir la comprobación; el fallo no crea una nueva cotización. La muestra de sustitución marca DEMO-PRO-01 versión 0.1 como sustituida por DEMO-PRO-01 versión 0.2 (`superseded_by_version`), que es el caso ordinario: una revisión conserva el código. Un documento distinto que sustituye a otro recibe su propio código.

Las relaciones de `lifecycle` validan el esquema general de esta guía, con números de al menos dos cifras. Si la entidad usa un esquema distinto, conservarlo en el documento y adaptar esa validación antes de declarar relaciones; el motor actual no ofrece un patrón configurable. Un documento heredado sin código se identifica por título y custodia, sin inventar su numeración retrospectiva.
