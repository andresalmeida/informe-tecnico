# Descripción de arquitectura

Elegir `document.kind: "descripcion-arquitectura"` para explicar la arquitectura de un sistema a quienes lo operan, revisan o extienden. Partir de `assets/ejemplo-descripcion-arquitectura.json`, con código ARQ de [codigos.md](../codigos.md). Es un formulario sin elección obligatoria: la decisión de mayor peso es qué decisiones y restricciones constan, y se escribe con sus códigos y evidencia.

Usa título y contenido desde la primera página, histórico al final con `show_changes: true` y vistas enlazadas. Se recomiendan `document.indexes: ["contents", "figures"]` cuando el documento tiene varias vistas: permiten encontrar cada apartado y figura sin recorrer las tablas. El ejemplo usa ambos. Las tablas de firmas y de componentes no necesitan índice de tablas por defecto. Los bloques existentes bastan; el contrato está en [secciones.md](../contrato/secciones.md).

La muestra tiene nueve páginas: índices en la 1; referencia y propósito en la 2; contexto, figura de contexto y componentes de la 3 a la 5; datos en la 5; operación en la 6; decisiones y calidad en la 7; riesgos en la 8; firmas e histórico en la 9. La ficha de referencia se mantiene junta después de los índices. Una figura o una tabla se mantiene entera salvo que moverla dejara más del 35 % de la página en blanco. Sin índices son ocho páginas; con papel Carta son once en las variantes probadas. No se añaden saltos ni relleno para ocupar los huecos.

Como orientación de estructura, se organizan partes interesadas, preocupaciones y vistas. La ficha pública de [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) describe su alcance sobre descripciones de arquitectura y puntos de vista; el [avance publicado por ANSI](https://webstore.ansi.org/preview-pages/iso/preview_iso%2Biec%2Bieee%2B42010-2022.pdf) identifica esos conceptos en sus apartados. Consultados el 14/11/2026. Se toma esa orientación, sin reproducir cláusulas ni declarar conformidad; el orden de esta guía es una decisión editorial del catálogo.

## Decidir antes de redactar

Identificar sistema, versión y fecha de corte. Separar el diseño previsto de lo implementado y lo desplegado: un diagrama de una propuesta no acredita una instalación real. Si solo hay propuesta y alcance, declarar diseño de referencia y dejar versión y despliegue pendientes. El ejemplo tiene corte del 18/11/2026, posterior al alcance del 16/11/2026 y anterior a la entrega del 08/01/2027; describe un diseño y conserva el ATP sin ejecutar.

Identificar quién necesita la descripción y qué pregunta debe resolver cada vista. Usar como base documentos del proyecto, decisiones registradas, código o evidencia de despliegue que conste. No añadir componentes, tecnologías, puertos ni responsables para completar una figura. Cada dato que la base no resuelve queda por confirmar. No editar un ejemplo anterior para fabricar el antecedente que falta.

## Completar cada campo

1. **Información de referencia.** Número, módulo, versión del sistema, corte y responsable. Mantener separadas versión del documento y versión del sistema. Declarar si el corte es diseño o arquitectura implementada, con el origen de la información.
2. **Propósito y partes interesadas.** Explicar para qué se usa la descripción y registrar cada parte con su preocupación principal. Las preocupaciones orientan las vistas y las comprobaciones posteriores.
3. **Contexto del sistema.** Actores y vecinos, con la pregunta que resuelve la figura de contexto. Dibujar el módulo como una unidad; los componentes internos pertenecen a la vista siguiente.
4. **Vista de componentes.** Figura y tabla por componente: responsabilidad, tecnología, interfaces y responsable. Distinguir componentes propios y sistemas vecinos, y mostrar la frontera de los datos cuando sea relevante. En el ejemplo, la tarjeta se captura en campos de la pasarela y no cruza a los servidores propios.
5. **Vista de datos.** Qué se guarda, dónde, sensibilidad y conservación. Indicar también lo que no se almacena y su razón. Sin clasificación o plazo acordado, escribir Por confirmar con el área responsable; no inferir una retención legal ni una certificación de seguridad.
6. **Despliegue y operación.** Entornos, capacidad que consta, quién despliega y vigilancia. Si el monitoreo es una propuesta, rotularlo así. Dos instancias, una de pruebas y otra de producción, no son dos réplicas en producción. No inventar alta disponibilidad ni una plataforma de nube.
7. **Decisiones y restricciones.** Tabla de códigos ADR existentes, decisión y estado. Las restricciones sin ADR conservan su documento de origen; no se les fabrica un código de decisión. Una aceptación técnica de un ADR no equivale a una firma documental ni a la aceptación del software.
8. **Atributos de calidad.** Atributo, criterio medible, mecanismo de diseño y caso del plan de pruebas con código de documento e ID. Conservar los umbrales del alcance y distinguir mecanismo previsto de cumplimiento medido. En el ejemplo, CP-01 a CP-05 pertenecen a DEMO-ATP-01 y siguen pendientes.
9. **Riesgos y pendientes.** Citar registro, ID y corte. Conservar estado y responsable del origen, incluido un riesgo cerrado que explique una frontera del diseño. Añadir las decisiones o datos todavía sin resolver y quién los confirma.
10. **Firmas de responsabilidad e histórico.** Mantener firmas y fechas pendientes mientras no consten. El histórico registra las revisiones reales de la descripción, sin convertirlas en aprobaciones.

## Cómo se comprueba

Verificar cada código contra su documento y cada ID contra la lista correspondiente. Un código citado fuera del mismo JSON va como texto; `{{ref:id}}` solo enlaza objetos de la fuente actual. Cada componente de una figura tiene una responsabilidad identificable, y cada criterio de calidad conserva unidad, umbral y método del alcance. La tabla de calidad no convierte las pruebas de concepto de la factibilidad en aceptación del producto.

Comprobar que los riesgos y decisiones reflejen sus cortes, que los datos de tarjeta no aparezcan almacenados en la vista de datos y que la figura no envíe una tarjeta al servidor propio mientras el texto dice que no pasa. El ejemplo conserva los estados del registro del 16/11/2026 y cita DEMO-ADR-01 del 10/11/2026. Las versiones, tecnología de servidor, retención y reparto de operación que no constan permanecen pendientes.

## Personalizar

Cambiar `brand.entity`, `unit`, `accent`, `logo` relativo al JSON, código, papel y firmantes. Al cambiar colores, regenerar también los diagramas desde su HTML editable con esos tokens; modificar el JSON no recolorea una imagen. Ajustar partes interesadas, componentes, datos y vistas a la evidencia del sistema. Los índices son opcionales; quitar `document.indexes` si la descripción breve no los necesita.

## Qué no inventar

Aplicar [pendientes-y-estado.md](../pendientes-y-estado.md) para estados documentales, firmas, responsables, fechas e historial. Lo propio de este tipo:

| Dato | Tratamiento |
|---|---|
| Versión desplegada sin evidencia | Por confirmar; declarar diseño de referencia |
| Tecnología, interfaz o responsable no asignado | Por confirmar con el equipo correspondiente |
| Sensibilidad o retención sin criterio acordado | Por confirmar con el área responsable |
| Vigilancia sin implementación verificada | Propuesta; herramientas y responsables por confirmar |
| Criterio sin ejecución del ATP | Pendiente de comprobación |

No omitir una vista necesaria porque falte el dato: conservar el pendiente y su responsable. No inventar ADR adicionales, una revisión externa completada, resultados de prueba ni certificaciones.

## ¿Necesita un diagrama?

Sí. El contexto añade actores y sistemas vecinos; la vista de componentes añade la frontera de los datos de tarjeta. Son lecturas distintas de la arquitectura propuesta de factibilidad y del perímetro del alcance. La figura de contexto no descompone el módulo; la de componentes identifica cliente, servidores y pasarela. Dibujar una arquitectura nueva con el flujo de [diagramas.md](../diagramas.md), en «Integración» y «Comandos y medidas»; no copiar una figura anterior para repetir sus relaciones.

Aplicar `diagram-design` con tipo arquitectura y salida estática. En el ejemplo se sigue el flujo mínimo documentado: instrucciones y referencia del tipo, sistema visual adaptado a los tokens de la entidad, HTML con SVG en línea, comprobación sin red y exportaciones mediante los helpers. Se conservan fuentes HTML/SVG y PNG a 3x. El verificador de geometría puede faltar en la instalación: decirlo y revisar a mano los conectores. Mantener las etiquetas legibles en una columna de 168 mm, sin comprimir un preset ancho para pantalla.

Si falta `diagram-design`, resolver su disponibilidad dentro del alcance autorizado o informar la limitación; no afirmar que se siguió su flujo. Una alternativa SVG propia debe declararse como tal y conservar los mismos datos, accesibilidad, fuentes editables y revisión a escala de impresión. Las figuras son parte de este tipo y del ejemplo; una fuente sin figuras puede compilar por el motor genérico, pero queda incompleta como descripción de este catálogo.

## Revisar la redacción con las skills hermanas

Aplicar Minto: abrir cada apartado con lo que la vista permite entender y después su evidencia. Aplicar unicorntext: eliminar relleno y duplicación del diagrama en la prosa, conservando límites, condiciones y nombres técnicos. Son criterios incorporados; no requieren instalaciones adicionales. Si el usuario invoca una skill disponible, aplicar además sus instrucciones.

## Comprobar y entregar

Comprobar `python3 -c "import reportlab, pypdf, pdfplumber, PIL"`. Resolver el entorno según `SKILL.md` con `reportlab>=4.4,<5`, `pypdf>=6,<7`, `pdfplumber>=0.11,<1` y `Pillow>=11,<13`. SVG integrado directamente requiere además `svglib`; el ejemplo usa PNG para conservar las dependencias habituales del motor.

```sh
python3 <skill>/scripts/build_report.py arquitectura.json --output arquitectura.pdf
python3 <skill>/scripts/check_report.py arquitectura.pdf
pdftoppm -r 80 -png arquitectura.pdf pagina
```

Sin Poppler: `python3 -c "import pdfplumber; [p.to_image(resolution=80).save(f'pagina-{i}.png') for i,p in enumerate(pdfplumber.open('arquitectura.pdf').pages,1)]"`.

Abrir todas las páginas, revisar cada figura a tamaño impreso y ampliar un recorte a 150 ppp. Comprobar destinos de índices, fronteras, sentido de las flechas, tablas y firmas enteras e histórico al cierre. No recortar evidencia para forzar una página ni reducir la letra silenciosamente. Entregar PDF, manifiesto, JSON y activos HTML, SVG y PNG. El comprobador valida estructura, sin acreditar la arquitectura real ni la conformidad normativa.
