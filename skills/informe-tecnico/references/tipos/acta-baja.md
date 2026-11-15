# Acta de baja

Elegir `document.kind: "acta-baja"`, código `BAJ`, para registrar que un sistema, módulo, procedimiento o conjunto documental deja de usarse. Partir de `assets/ejemplo-acta-baja.json`, con `format.profile: "institucional"`. Es formulario sin elección obligatoria. No lleva diagrama: el perímetro, las condiciones y la verificación se expresan en tablas. La estructura procede del encargo del catálogo, sin un formulario empresarial de origen.

La muestra tiene cuatro páginas, título y contenido desde la primera, firmas e histórico al cierre. Las tablas breves se mantienen completas; pueden dejar espacio al pie. Se omiten índices; son opcionales para expedientes extensos. No reducir la letra para eliminar huecos. Los bloques existentes bastan: no hay contrato nuevo ni ejecución automática de la baja.

## Decidir antes de redactar

Identificar objeto, versión, autoridad competente, alcance y evidencia de que puede retirarse. Separar una propuesta, la autorización y la ejecución. Una entrega para revisión no acredita puesta en producción. Si no hay evidencia suficiente, elaborar un borrador, registrar fechas como previstas y mantener pendientes la autorización y la fecha efectiva real.

El ejemplo enlaza con DEMO-ENT-01 del 08/01/2027 y DEMO-CIE-01 del 18/01/2027. Propone el 20/01/2027, condicionado a una producción verificada y autorización posterior a la entrega. No consta esa producción en la cadena. Por eso el acta del 19/01/2027 lleva `lifecycle.state: "borrador"` y no declara ejecutada la baja. El procedimiento telefónico consta en DEMO-REQ-014; no tiene código ni versión propios documentados.

## Completar cada campo

1. **Información de referencia.** Objeto, tipo, código o versión, fecha efectiva, motivo y quién autoriza. Si carece de código, escribir «Documento heredado sin código» y localizarlo por título, custodio y versión conocida; no crear un código retrospectivo. Distinguir fecha del acta, fecha prevista y fecha efectiva real.
2. **Alcance de la baja.** Qué sale, qué se mantiene y qué está fuera. Preservar atención de incidencias y operaciones históricas. La baja del circuito telefónico no retira automáticamente procesos excluidos del módulo de pagos.
3. **Dependencias e impacto.** Sistemas y personas afectados, condiciones de continuidad, aviso previo, responsable y evidencia. Una fecha de aviso aún no ocurrida queda pendiente.
4. **Datos.** Qué se conserva, migra o elimina, plazo, ubicación y responsable. Separar plan de resultado. No autorizar borrado por omisión; una eliminación requiere decisión y constancia propias. La política determina conservación y disposición, sin plazos legales inventados.
5. **Sustituto o alternativa.** Código del documento que lo identifica, versión y localizador cuando consten. El ejemplo cita DEMO-ALC-01, DEMO-ARQ-01, DEMO-ERS-01 y DEMO-ENT-01; no inventa un código del sistema. Si falta sustituto, identificar cómo continúa el servicio.
6. **Plan y verificación.** Pasos, fechas previstas o efectivas rotuladas, comprobación observable, resultado y responsable. Después de ejecutar, registrar evidencia de producción, autorización, avisos, conciliación y retirada de copias según corresponda. Una lista de pasos pendientes no demuestra ejecución.
7. **Documentos afectados.** Tabla con código o identificación, estado nuevo y fecha. Usar `retirado` y, después de acordar conservación, `archivado`, conforme a [ciclo-de-vida.md](../ciclo-de-vida.md). Una tabla de destinos propuestos no modifica los JSON relacionados. Quien custodia actualiza cada documento autorizado y recompila para que la banda aparezca en todas sus páginas. El acta puede seguir vigente como registro de una baja; no se marca retirada por retirar otro objeto.
8. **Firmas e histórico.** Elaboración, revisión y aprobación con espacio para firma y fechas pendientes. Confirmar además quién tiene autoridad sobre la baja; el firmante de aprobación documental no se presume competente para autorizar operaciones o eliminación de datos.

## Cómo se comprueba

La fecha efectiva sigue a la entrega y, si se sustituye un servicio, a la producción verificada. Cuando no conste la fecha real, no inventarla ni convertir el calendario propuesto en evidencia. La identificación de cada copia, su destino, su fecha y la decisión autorizada deben concordar. No archivar sin `retention.period` y `retention.location`, ni retirar sin `retire_on`. Para una copia retirada, comprobar texto y borde de la banda en cada página, también en gris.

El motor comprueba estructura y ciclo de vida; no verifica una producción ni cambia archivos externos. La prueba del ejemplo confirma fechas, borrador, códigos existentes, estados propuestos y ausencia de una baja afirmada como ejecutada.

## Personalizar y tratar lo pendiente

Cambiar entidad, unidad, color, logo relativo al JSON, código BAJ, papel A4 o Letter y firmantes. Usar [codigos.md](../codigos.md) y [pendientes-y-estado.md](../pendientes-y-estado.md). No inventar autoridad, firma, aprobación, producción, migración o destrucción. El estado «Demostración» pertenece a los ejemplos; cuando hay ciclo de vida, su estado gobierna el pie.

Los índices y el bloque `lifecycle` del acta son opcionales y tienen pruebas con y sin ellos. Sin el bloque, escribir el estado editorial fielmente; no se generan bandas de ciclo de vida. Los apartados del registro se conservan: ante falta de datos, indicar qué falta y quién lo confirma. Ajustar las filas del plan al objeto; una tabla extensa repite cabecera y leyenda al continuar.

## Redacción y diagrama

Aplicar Minto: abrir con baja ejecutada o propuesta y sus condiciones. Aplicar unicorntext: quitar trámite sin perder alcance, responsables, fechas o evidencia. Los criterios están incorporados; si el usuario invoca las skills, leer también sus instrucciones. No añadir arquitectura: la tabla de documentos afectados permite revisar cada transición y la cadena ya contiene las figuras del sistema.

## Comprobar y entregar

Verificar `python3 -c "import reportlab, pypdf, pdfplumber, PIL"`. Si faltan dependencias, usar un entorno virtual externo con `reportlab>=4.4,<5`, `pypdf>=6,<7`, `pdfplumber>=0.11,<1` y `Pillow>=11,<13`. Desde la carpeta de la skill, con ese intérprete:

```sh
python3 <skill>/scripts/build_report.py <skill>/assets/ejemplo-acta-baja.json --output baja.pdf
python3 <skill>/scripts/check_report.py baja.pdf
pdftoppm -r 80 -png baja.pdf baja
```

Abrir todas las páginas. Revisar límites de tablas, títulos acompañados, firmas completas y fechas previstas separadas de efectivas. Si falta Poppler, renderizar las páginas de `pdfplumber.open('baja.pdf')` con `page.to_image(resolution=80)`. Entregar PDF, manifiesto, JSON y activos; conservar el expediente y los documentos retirados.
