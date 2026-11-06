# Dossier de sistema (`informe-dossier`)

Un dossier presenta en 6 a 8 páginas A4 cómo funciona un sistema y qué tan confiable es. Lleva la conclusión primero y figuras de ingeniería con el aspecto de un manual de operaciones del Apolo. No usa el motor JSON de este skill ni `document.kind`, y tampoco trae scripts propios: el agente decide el contenido con esta guía y los skills de apoyo, y luego arma las páginas con el skill `nasa-handbook`.

Se activa cuando el usuario dice «informe-dossier», «modo nasa dossier» o «flow NASA». Ver una muestra en [muestra-dossier.pdf](../../../docs/muestra-dossier.pdf).

## Orden de trabajo

1. Leer `minto-pyramid`, `unicorntext` y `diagram-design`, y las reglas de esta guía. Si `diagram-design` no está instalado, elegir las figuras con la sección «Choosing the figures» (§5) de `style-guide.md` y las piezas de `svg-parts.md`, ambos de `nasa-handbook`, y seguir.
2. Decidir el contenido: la pirámide, el texto de cada página, el tipo de figura de cada argumento y los códigos del documento.
3. Ir al skill `nasa-handbook`, leer su `style-guide.md` completo (sobre todo §2, presupuesto de espacio, y §4, redacción) y reproducir el dossier con él, aplicando lo decidido en el paso 2.
4. Revisar cada página renderizada y corregir hasta que cumpla.

## Requisito: `nasa-handbook` congelado

El skill **`nasa-handbook`** de R44VC0RP ([github.com/R44VC0RP/skills](https://github.com/R44VC0RP/skills), carpeta `skills/nasa-handbook`) debe estar instalado. Si no lo está, decirlo y detenerse. De ahí salen la plantilla, las fuentes, `render.sh` y `check.py`, y sus referencias de estilo y de figuras; nada de eso se copia a este repositorio.

Versión congelada: commit `e6f8682d1` (26 de octubre de 2026), probada con dos dossiers reales y con un agente que no conocía el proyecto. No actualizar sin revisar la diferencia y comprobar que la plantilla siga funcionando con esta guía. Para saber si cambió:

```sh
gh api "repos/R44VC0RP/skills/commits?path=skills/nasa-handbook&per_page=1" --jq '.[0].sha'
```

Si el resultado no empieza con `e6f8682d1`, hay cambios que revisar.

## Contenido y redacción

- **Pirámide (`minto-pyramid`).** Una conclusión, de tres a cinco argumentos y la evidencia de cada uno. La conclusión va en la portada. Un argumento puede compartir subsección con otro, y cada frase cita la subsección donde está su evidencia. Si el usuario todavía no tiene una conclusión, pedirla antes de seguir.
- **Redacción (`unicorntext`).** Frases directas, sin tríadas, sin «no es X sino Y», sin rayas largas y sin dos puntos dramáticos. Una enumeración real de tres elementos del sistema se admite, pero conviene reescribirla en dos y uno si se puede. El texto va en español, con coma decimal y punto de millar, y «7 %» con espacio.
- **Figuras (`diagram-design`).** Elegir el tipo de diagrama según lo que debe mostrar, con un máximo de nueve nodos, y borrar antes que agregar. Cada subsección lleva dos figuras: un diagrama funcional o de flujo y una figura de datos con barras.
- **Cifras.** Cada cifra se escribe con su fuente. No se inventan datos para llenar una figura. En cada figura de datos va una línea `FUENTE: …` abajo a la izquierda del dibujo, y el README del dossier repite la fuente de cada cifra.

## Códigos propios, no los del Apolo

El estilo es el del Apolo, pero los códigos y los nombres son del proyecto. No dejar identificadores del manual original (como «SM2A», «Block II» o los nombres de sus sistemas). Usar este esquema:

| Elemento | Forma | Ejemplo | Qué significa |
| --- | --- | --- | --- |
| Número del documento | `SISTEMA-MÓDULO-SECCIÓN-REV letra-(volumen)` | `SIGC-CDA-04-REV A-(1)` | Sistema, módulo, sección del manual, revisión (la siguiente será B) y volumen. |
| Informe de la portada | `SISTEMA MÓDULO-AAMM`, con un espacio entre el sistema y el módulo | `SIGC CDA-2611` | Sistema, módulo y año y mes de emisión. |
| Pestaña lateral | tres letras por subsección, sin repetirlas | `ACT`, `OPE` | Las primeras letras del verbo o sustantivo que resume la subsección. |
| Código de figura | `PESTAÑA-NNL` | `OPE-03A` | Pestaña de la subsección, número de la figura (dos dígitos, corre a lo largo de todo el dossier) y letra de revisión del dibujo (`A` en la primera). |
| Numeración | final desde el inicio | `4.1`, `4.1-1`, `4.1.2.1` | Las páginas se escriben con su numeración definitiva, sin renumerar después. |

Cabecera de cada página: el número del documento, el nombre del programa («SISTEMA · Módulo · Manual de operaciones», con el nombre corto del sistema al inicio) y la parte («Datos de sistemas»). Pie: se quita «Mission», «Fecha base» y «Fecha de cambio» llevan la fecha de emisión en una revisión A (y se ensanchan los huecos a unos 40 mm para que quepa «5 de noviembre de 2026»), y el número de página es el de la subsección. Sin barra de cambio en la revisión A. Los títulos de los apartados van en español: INTRODUCCIÓN, DESCRIPCIÓN FUNCIONAL, DATOS DE DISEÑO Y RENDIMIENTO, y los avisos NOTA y PRECAUCIÓN.

## Portada

`nasa-handbook` trae páginas de contenido, no una portada. La del dossier es propia: título corto, código y mes, título completo, subtítulo en cursiva, autoría, y cuatro bloques con su encabezado subrayado (CONCLUSIÓN, POR QUÉ, EVIDENCIA y TÉRMINOS). Cabe en una página y en blanco y negro. Su CSS está en [dossier-portada.css](dossier-portada.css) y su resultado se ve en la muestra.

Esqueleto del HTML. Se parte de la plantilla de `nasa-handbook`: se conserva su `<head>` (con `lang="es"`) y su script final de ajuste. El contenido de `dossier-portada.css` se pega dentro de un segundo bloque `<style>…</style>` justo antes de `</head>`, y el contenido de la página se reemplaza por este:

```html
<div class="page cover">
  <div class="top">TÍTULO CORTO DEL SISTEMA</div>
  <div class="nro">SIS MÓD-AAMM &nbsp;·&nbsp; MES DE AAAA</div>
  <div class="linea"></div>
  <div class="titulo">TÍTULO COMPLETO EN MAYÚSCULAS</div>
  <div class="sub">Subtítulo en cursiva</div>
  <div class="aut">AUTORÍA</div>
  <h4>CONCLUSIÓN</h4>
  <p>Un párrafo.</p>
  <h4>POR QUÉ</h4>
  <ol class="why"><li><span>1.</span><span>Frase con su sección.</span></li></ol>
  <h4>EVIDENCIA</h4>
  <ol class="idx"><li><span>4.1&nbsp;&nbsp;&nbsp;Título de la subsección</span><span class="d"></span><span>4.1-1</span></li></ol>
  <h4>TÉRMINOS</h4>
  <dl class="term"><dt>Término</dt><dd>Definición corta.</dd></dl>
  <div class="foot pie"><div class="r"></div>ENTIDAD<br>PAÍS &nbsp;·&nbsp; MES DE AAAA</div>
</div>
```

El pie debe conservar las dos clases (`foot pie`): el chequeo de ajuste de la plantilla depende de `foot`.

- **Conclusión:** un párrafo.
- **Por qué:** una lista numerada de tres frases, cada una con la subsección donde está la evidencia.
- **Evidencia:** el índice de subsecciones, con línea de puntos y el número de su primera figura (por ejemplo `4.1-1`), no su código de figura.
- **Términos:** de tres a seis términos. Las definiciones pueden ser de conocimiento general y nunca llevan cifras.
- **Autoría:** la entidad dueña del sistema, salvo que el usuario indique otra.

## Páginas

De cuatro a cinco subsecciones de una página A4 (dos o tres si es un dossier corto). Cada una lleva introducción (3 líneas), descripción funcional (4), un apartado con una regla (2), dos figuras, una tabla de dos columnas, un aviso (NOTA o PRECAUCIÓN) de tres líneas como máximo y una tarjeta de procedimiento. El orden de las subsecciones sigue a la pirámide: diseño, el detalle de cada parte, la evidencia de calidad y, al final, la operación y los límites.

- **Tabla:** de seis a ocho filas, con valores de 30 caracteres o menos.
- **Tarjeta:** líneas de 34 caracteres o menos, sin contar el número del paso, de seis a siete líneas. Si la subsección no tiene un procedimiento propio, la tarjeta puede ser un control de la función o una verificación. No inventar controles ni nombres de botones que el usuario no haya descrito.
- **Presupuesto de espacio:** el de `style-guide.md` §2. El chequeo de ajuste debe dejar de 4 a 10 mm libres.

## Ciclo de revisión

Renderizar cada página con `render.sh` (el chequeo de ajuste no debe decir OVERFLOW), mirar la página, corregir, pasar `check.py` y unir las páginas en un solo PDF (por ejemplo con `pypdf` o `pymupdf`). El PDF es la referencia: si el PNG que escribe `render.sh` sale con una franja gris abajo o sin pie, rasterizar el PDF con `pymupdf` (`page.get_pixmap(dpi=130)`) y mirar esa imagen. Esperar de dos a cuatro pasadas por página: los solapes de etiquetas y de títulos de eje, las puntas de flecha pegadas al panel y los desbordes casi siempre aparecen en la primera. Entregar el PDF y un README que diga de dónde sale cada cifra y cómo regenerar el documento.

## Lecciones

- Una tabla con valores largos aprieta la primera columna y desborda la página. Acortar las filas.
- No poner etiquetas encima de los cables de un diagrama. Alinearlas a la derecha o quitarlas.
- Envolver cada referencia como «figura 4.3-1» en `<span class="nowrap">` para que no se parta en el guion, y comprobar que no quede sola en la última línea del párrafo. Si pasa, recortar la frase.
- Las etiquetas de estratos deben decir qué son («PLAN PND1», no «PND1»).
- Un cable de bus debe llegar a todos sus destinos.
- No entregar sin mirar cada página a buena resolución.
- `render.sh` a veces termina con «Killed: 9» en el paso del PNG, o su chequeo de ajuste sale «unknown». Repetirlo.

## Créditos

- `nasa-handbook`, de R44VC0RP: plantilla, fuentes (Routed Gothic, SIL OFL 1.1; Letter Gothic Code, Aladdin Free Public License), `render.sh`, `check.py` y referencias de estilo.
- El decálogo de Prodigioso Volcán, en el que se basa `unicorntext`.
- El Pyramid Principle de Barbara Minto, en el que se basa `minto-pyramid`.
