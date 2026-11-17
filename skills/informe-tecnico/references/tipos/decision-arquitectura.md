# Decisión de arquitectura

Elegir `document.kind: "decision-arquitectura"` para registrar una decisión de arquitectura (ADR). Partir de `assets/ejemplo-decision-arquitectura.json`, con código ADR según [codigos.md](../codigos.md). Registra una decisión con sus razones y consecuencias. Cada opción se explica sin jerga interna, de forma que quien no estuvo en la conversación pueda entenderla.

Es una ficha corta, sin portada, con una elección de estado y el histórico al final (`show_changes: true`). No necesita índices por defecto; `document.indexes` está disponible para un registro que lo requiera. No lleva figura: comparar las opciones y explicar sus consecuencias en texto permite entender esta decisión sin repetir la arquitectura de la factibilidad. El esquema usa bloques existentes `fields`, `table` y `paragraph`, descritos en [fields.md](../contrato/fields.md) y [secciones.md](../contrato/secciones.md).

La muestra tiene dos páginas. Referencia, contexto, tabla de opciones y decisión están en la primera; consecuencias, seguimiento, firmas e histórico en la segunda. Queda espacio al pie de la segunda al mantener las firmas completas. No se fuerza un salto ni se añade texto para llenar ese espacio.

## Decidir antes de redactar

Identificar la pregunta que obliga a decidir, los documentos que la sustentan y quién tiene autoridad para tomar la decisión. Un ADR registra el resultado de una decisión; el debate previo solo aporta el contexto y las opciones necesarias para entenderla. Si todavía falta decidir, marcar Propuesta y describir explícitamente qué opción se propone y qué validación falta.

La decisión de mayor peso es el estado. Propuesta significa pendiente de decisión; Aceptada requiere una decisión técnica que conste; Rechazada registra que no se adoptó; Sustituida conserva la decisión anterior y cita la nueva. Las etiquetas pueden personalizarse sin cambiar su significado en el proyecto. La elección siempre lleva una marca, incluso en Propuesta. El estado del ADR es distinto de `document.status`: una decisión técnica aceptada puede tener firmas documentales pendientes. No deducir una aprobación institucional del uso de una opción en una prueba.

Se escribe al decidir. Después se conserva el contexto, las opciones y las razones originales; se actualiza el estado y su trazabilidad en el histórico. Si cambia la solución, crear otro ADR y vincular ambos. No reescribir una decisión antigua como si siempre se hubiera elegido la solución nueva.

## Completar cada campo

1. **Información de referencia.** Número, título de la decisión en una frase, estado, fecha, quién decide y documentos relacionados por código. Cuando corresponda, añadir «Sustituye a» y «Sustituida por». Los códigos deben identificar decisiones existentes, sin apuntar al mismo ADR. Omitir esos campos cuando no haya relación, en lugar de inventar una decisión anterior.
2. **Contexto y problema.** Fuerzas que condicionan la elección y hecho que obliga a decidir. Separar evidencia disponible y restricciones de las hipótesis por confirmar.
3. **Opciones consideradas.** Tabla de opción, ventajas, desventajas y riesgo o costo, con al menos dos opciones. La elegida debe figurar en la tabla. Describir los costos sin cifras cuando no exista una estimación sustentada; no convertir una desventaja en un presupuesto inventado.
4. **Decisión.** Abrir con «Se decide…» y después explicar por qué se elige esa opción frente a las otras. Para Propuesta, escribir «Se propone decidir…» y precisar lo pendiente. La tabla sirve como referencia interna, mientras los otros documentos se citan por código textual.
5. **Consecuencias.** Qué se facilita, qué se dificulta y qué riesgo introduce o mantiene. Citar registro e identificadores de riesgo existentes. Distinguir evitar una alternativa de haber verificado la solución final.
6. **Seguimiento.** Condición o fecha de revisión y responsable. No inventar una fecha de aprobación. Revisar cuando cambien los supuestos, las interfaces o una condición que sostuvo la elección.
7. **Firmas de responsabilidad e histórico.** Quien elabora, revisa y aprueba el documento, con firmas en blanco y fechas pendientes mientras no consten.

## Cómo se comprueba

Contrastar fecha y evidencia con los documentos de origen. El ejemplo es del 10/11/2026, entre la factibilidad del 09/11/2026 y el alcance del 16/11/2026. Registra mantener el mecanismo ya probado en la factibilidad. R-07 del registro de riesgos dejó de ser una alternativa admitida el 09/11/2026; la comprobación de código y registros permanece bajo R-05. El ADR no convierte ese cierre de riesgo en pruebas de aceptación satisfactorias.

Comprobar que cada opción sea comprensible, que la elegida esté en la tabla, que cada razón responda a una ventaja o restricción y que las consecuencias no contradigan los riesgos. Los 50 cobros y 10 reembolsos del ejemplo son los de la prueba de concepto de DEMO-FAC-01; no se presentan como una nueva prueba.

Si el estado es Sustituida, «Sustituida por» es obligatorio en contenido y debe apuntar a un ADR existente; el sucesor cita «Sustituye a» con el código anterior. El motor valida la elección de una marca, pero no interpreta esas relaciones ni las opciones de la tabla. La revisión de contenido y las pruebas de coherencia del ejemplo cubren esas reglas.

## Personalizar

Cambiar identidad (`brand.entity`, `unit`, `accent`, `logo` relativo al JSON), código, papel A4 o Carta y responsables. Personalizar los textos del estado en `options` y actualizar `selected` al mismo texto. La fecha del documento corresponde al registro o al último cambio de estado; conservar la fecha original de la decisión en su campo. Los índices, si se usan, se calculan al compilar, sin escribir páginas manuales.

## Qué no inventar

Aplicar [pendientes-y-estado.md](../pendientes-y-estado.md) para firmas, nombres, fechas, estado documental e historial. Lo propio del ADR:

| Dato | Tratamiento |
|---|---|
| Decisión aún no tomada | Propuesta; indicar qué se debe resolver |
| Riesgo o costo sin cifra sustentada | Descripción cualitativa o Por estimar |
| Decisión sustituida sin sucesor identificado | Resolver el código antes de declarar Sustituida |
| Relación de sustitución que no existe | Se omite el campo |

No inventar aprobaciones o responsables. La marca Aceptada del ejemplo es la decisión técnica solicitada por el escenario ficticio; las firmas del documento siguen pendientes.

## ¿Necesita un diagrama?

No. La pregunta es por qué se eligió una opción. La tabla y sus consecuencias aportan esa lectura; un esquema de componentes repetiría la factibilidad. Una arquitectura que necesite vistas propias se documenta por separado.

## Revisar la redacción con las skills hermanas

Aplicar los criterios incorporados de Minto: decisión primero y razones después, sin alterar el orden de apartados. Aplicar unicorntext: quitar repeticiones y frases de trámite conservando términos, condiciones y evidencia. No se requieren instalaciones adicionales para esos criterios; si el usuario invoca una skill disponible, aplicar además sus instrucciones.

## Comprobar y entregar

Verificar `python3 -c "import reportlab, pypdf, pdfplumber, PIL"`. Si faltan dependencias, crear un entorno virtual fuera de la entrega e instalar `reportlab>=4.4,<5`, `pypdf>=6,<7`, `pdfplumber>=0.11,<1` y `Pillow>=11,<13`, como indica `SKILL.md`. Con su intérprete:

```sh
python3 <skill>/scripts/build_report.py decision.json --output decision.pdf
python3 <skill>/scripts/check_report.py decision.pdf
pdftoppm -r 80 -png decision.pdf pagina
```

Sin Poppler: `python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i,p in enumerate(pdfplumber.open('decision.pdf').pages,1)]"`.

Abrir todas las páginas y revisar una sola cruz con negrita en el estado, opciones y firmas enteras y el histórico junto al cierre. Un documento más largo de dos páginas puede contener varias decisiones: revisar si hay que separarlas, sin reducir automáticamente la letra. Entregar PDF, manifiesto `.manifest.json` y fuente JSON con sus activos.
