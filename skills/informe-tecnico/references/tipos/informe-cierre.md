# Informe de cierre y lecciones aprendidas

Elegir `document.kind: "informe-cierre"`, código `CIE`, para consolidar el balance interno de un proyecto. Partir de `assets/ejemplo-informe-cierre.json` con `format.profile: "institucional"`. La parte solicitante recibe el acta de entrega; este informe registra resultados, desviaciones y aprendizaje. Es un formulario sin elección obligatoria: la conclusión se escribe con su evidencia. No lleva diagrama porque las comparaciones y el traspaso de pendientes se leen en tablas.

El PDF es compacto, empieza directamente con contenido y termina con firmas de responsabilidad e histórico (`show_changes: true`). Los índices son opcionales y se omiten en el ejemplo. La muestra ocupa cuatro páginas; las tablas se mantienen enteras cuando caben en una página. Eso puede dejar espacio al pie. No reducir la letra ni agregar relleno para ocuparlo.

## Decidir antes de redactar

Identificar destinatario interno, período informado, responsable y documentos de respaldo. Elegir «Entregado», «Entregado con pendientes» o «No entregado» según el inventario y la evidencia. Declarar aparte el estado de la conformidad: recibir para revisión no acredita aceptación. Si faltan pruebas ejecutadas, certificado o decisión de quien acepta, mantener pendientes la conformidad y el cierre definitivo. Las firmas de este informe tampoco sustituyen la aceptación del software.

## Completar cada campo

1. **Información de referencia.** Proyecto, período, responsable y códigos relacionados. Diferenciar fecha del documento, período de medición y fecha de entrega.
2. **Resumen.** Conclusión primero, estado de conformidad, evidencia y decisión pendiente con responsable. El ejemplo entrega con pendientes; DEMO-ENT-01 recibe para revisión y DEMO-ATP-01 sigue sin ejecutar.
3. **Objetivos y resultados.** Tabla de objetivo, resultado observado y evidencia por código. Un criterio previsto se identifica como pendiente de comprobar, sin presentarlo como resultado satisfactorio.
4. **Entregables.** Reutilizar identificadores y nombres del alcance. Citar el acta que respalda cada entrega y su condición. E5 mantiene la constancia pendiente de DEMO-CAP-01.
5. **Plazo y esfuerzo.** Tabla estimado, real, variación absoluta y relativa. Declarar unidades: semanas calendario y días-persona son magnitudes diferentes. Fórmulas: real menos estimado; 100 × (real menos estimado) / estimado. Si el estimado es cero, la variación relativa es «No aplica» y se explica. Precisar período, origen y redondeo; no convertir desviaciones en cambios aprobados. El motor imprime estas celdas y no las calcula; la prueba del ejemplo verifica ambas fórmulas con Decimal.
6. **Cambios aprobados.** Código de solicitud y alcance de cada decisión autorizada. Si no constan, decirlo expresamente; no inventar un código. El ejemplo no trae solicitudes aprobadas.
7. **Riesgos materializados y abiertos.** Citar registro, identificador, último corte y responsable. Separar materialización observada de riesgo abierto. El ejemplo conserva el corte de DEMO-RIE-01 del 16/11/2026, con R-07 cerrado y los demás pendientes de seguimiento; no afirma que se materializaron.
8. **Lecciones aprendidas.** Qué funcionó, qué sigue sin resolverse y qué se hará distinto, cada hallazgo con base, acción y responsable. No escribir evaluaciones generales sin un hecho que las sostenga.
9. **Pendientes y soporte.** Qué falta, quién lo recibe y plazo. Si falta canal, plazo o localizador, usar «Por confirmar» con responsable. No inventar un acuerdo de soporte.
10. **Firmas e histórico.** Elaboración, revisión y aprobación, espacios de firma y fechas pendientes. El histórico de una primera versión contiene un solo registro.

## Cómo se comprueba

Comparar objetivos y entregables con el alcance, responsables con entrega y riesgos, y aceptación con el ATP. El ejemplo conserva siete semanas y 50 días-persona estimados. Sus ocho semanas reales y 54 días-persona son cifras de demostración: +1 semana (+14,29 %) y +4 días-persona (+8,00 %). El intervalo del 23/11/2026 al 17/01/2027 cuenta ambos extremos y suma 56 días; incluye el período de balance posterior a la entrega del 08/01/2027. No modifica el cronograma comprometido ni afirma una puesta en producción.

Para datos reales, conservar partes de esfuerzo y fechas observadas como evidencia. Una prueba de coherencia del ejemplo no valida cifras de otro proyecto. La estructura usa bloques existentes (`fields`, `paragraph`, `table`); no añade campos al contrato ni una calculadora general para dos variaciones.

## Personalizar y tratar lo pendiente

Cambiar entidad, unidad, color y logo relativo al JSON, código, papel A4 o Letter, firmantes y textos. Mantener identificadores acordados entre documentos. Aplicar [pendientes-y-estado.md](../pendientes-y-estado.md), [codigos.md](../codigos.md) y [ciclo-de-vida.md](../ciclo-de-vida.md). Un informe de cierre puede estar en borrador mientras espera aprobación; su título no lo hace vigente. Omitir `lifecycle` conserva la salida anterior; declararlo exige cumplir sus reglas.

No inventar aprobaciones, firma, materialización de riesgos, ejecución de pruebas, cifras reales ni conformidad. No eliminar los apartados de cambios o riesgos por falta de evidencia: escribir qué consta y qué falta. Solo los índices son opcionales; el ejemplo ya prueba su inclusión y omisión.

## Redacción y diagrama

Aplicar Minto: conclusión y decisión primero, después la evidencia. Aplicar unicorntext: quitar trámite y repeticiones conservando responsables, condiciones y medidas. Estos criterios están incorporados; las skills hermanas se leen además si el usuario las invoca. Sin diagrama: el balance necesita comparación de cifras y registros; no repite las figuras de arquitectura.

## Comprobar y entregar

Verificar dependencias: `python3 -c "import reportlab, pypdf, pdfplumber, PIL"`. Si faltan, usar un entorno virtual externo con `reportlab>=4.4,<5`, `pypdf>=6,<7`, `pdfplumber>=0.11,<1` y `Pillow>=11,<13`. Desde la carpeta instalada de la skill, con ese intérprete:

```sh
python3 <skill>/scripts/build_report.py <skill>/assets/ejemplo-informe-cierre.json --output cierre.pdf
python3 <skill>/scripts/check_report.py cierre.pdf
pdftoppm -r 80 -png cierre.pdf cierre
```

Abrir todas las páginas. Revisar tablas completas, títulos acompañados, firmas juntas al cierre y que el histórico no ocupe solo una página. Si falta Poppler, renderizar con `pdfplumber.open('cierre.pdf').pages` y `page.to_image(resolution=80)`. Entregar PDF, manifiesto obligatorio para el comprobador, JSON y activos utilizados.
