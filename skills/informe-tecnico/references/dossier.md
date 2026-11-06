# Dossier de sistema (`informe-dossier`)

Un dossier presenta en 6 a 8 páginas A4 cómo funciona un sistema y qué tan confiable es. Lleva la conclusión primero y figuras de ingeniería con el aspecto de un manual de operaciones del Apolo. No usa el motor JSON de este skill ni `document.kind`, y tampoco trae scripts propios: el agente decide el contenido con esta guía y los skills de apoyo, y luego arma las páginas con el skill `nasa-handbook`.

Se activa cuando el usuario dice «informe-dossier», «modo nasa dossier» o «flow NASA». Ver una muestra en [muestra-dossier.pdf](../../../docs/muestra-dossier.pdf).

## Orden de trabajo

1. Leer `minto-pyramid`, `unicorntext` y `diagram-design`, y las reglas de esta guía (códigos propios, portada, páginas y lecciones).
2. Decidir el contenido: la pirámide, el texto de cada página, el tipo de figura de cada argumento y los códigos del documento.
3. Ir al skill `nasa-handbook` y reproducir el dossier con él, aplicando lo decidido en el paso 2.
4. Revisar cada página renderizada y corregir hasta que cumpla.

## Requisito: `nasa-handbook` congelado

El skill **`nasa-handbook`** de R44VC0RP ([github.com/R44VC0RP/skills](https://github.com/R44VC0RP/skills), carpeta `skills/nasa-handbook`) debe estar instalado. Si no lo está, decirlo y detenerse. De ahí salen la plantilla, las fuentes, `render.sh` y `check.py`, y sus referencias de estilo y de figuras; nada de eso se copia a este repositorio.

Versión congelada: commit `e6f8682d1` (26 de octubre de 2026), probada con dos dossiers reales. No actualizar sin revisar la diferencia y comprobar que la plantilla siga funcionando con esta guía. Para saber si cambió:

```sh
gh api "repos/R44VC0RP/skills/commits?path=skills/nasa-handbook&per_page=1" --jq '.[0].sha'
```

Si el resultado no empieza con `e6f8682d1`, hay cambios que revisar.

## Contenido y redacción

- **Pirámide (`minto-pyramid`).** Una conclusión, de tres a cinco argumentos y la evidencia de cada uno. La conclusión va en la portada. Si el usuario todavía no tiene una conclusión, pedirla antes de seguir.
- **Redacción (`unicorntext`).** Frases directas, sin tríadas, sin «no es X sino Y», sin rayas largas y sin dos puntos dramáticos. El texto va en español, con coma decimal y punto de millar.
- **Figuras (`diagram-design`).** Elegir el tipo de diagrama según lo que debe mostrar, con un máximo de nueve nodos, y borrar antes que agregar. Cada subsección lleva dos figuras: un diagrama funcional o de flujo y una figura de datos con barras.
- **Cifras.** Cada cifra se escribe con su fuente. No se inventan datos para llenar una figura.

## Códigos propios, no los del Apolo

El estilo es el del Apolo, pero los códigos y los nombres son del proyecto. No dejar identificadores del manual original (como «SM2A», «Block II» o los nombres de sus sistemas). Usar este esquema:

| Elemento | Forma | Ejemplo | Qué significa |
| --- | --- | --- | --- |
| Número del documento | `SISTEMA-MÓDULO-SECCIÓN-REV letra-(volumen)` | `SIGC-CDA-04-REV A-(1)` | Sistema, módulo, sección del manual, revisión (la siguiente será B) y volumen. |
| Informe de la portada | `SISTEMA MÓDULO-AAMM` | `SIGC CDA-2611` | Módulo y año y mes de emisión. |
| Pestaña lateral | tres letras por subsección | `CDA`, `MAT`, `CLA`, `CAL`, `OPE` | Una abreviatura del tema de la subsección. |
| Código de figura | `PESTAÑA-número y letra` | `MAT-03A` | Pestaña de la subsección, número de la figura en el dossier y letra de revisión del dibujo. |
| Numeración | final desde el inicio | `4.1`, `4.1-1`, `4.1.2.1` | Las páginas se escriben con su numeración definitiva, sin renumerar después. |

Cabecera de cada página: el número del documento, el nombre del programa («Sistema · Módulo · Manual de operaciones») y la parte («Datos de sistemas»). Pie: «Fecha base», «Fecha de cambio» y el número de página de la subsección. Los títulos de los apartados van en español: INTRODUCCIÓN, DESCRIPCIÓN FUNCIONAL, DATOS DE DISEÑO Y RENDIMIENTO, y los avisos NOTA y PRECAUCIÓN.

## Portada

`nasa-handbook` trae páginas de contenido, no una portada. La del dossier es propia: título corto, código y mes, título completo, subtítulo en cursiva, autoría, y cuatro bloques con su encabezado subrayado (CONCLUSIÓN, POR QUÉ, EVIDENCIA y TÉRMINOS). Cabe en una página y en blanco y negro. Su CSS está en [dossier-portada.css](dossier-portada.css) y su estructura se ve en la muestra.

Esqueleto del HTML. Se parte de la plantilla de `nasa-handbook`: se conserva su `<head>` (con `lang="es"`) y su script final de ajuste, se agrega el CSS de la portada antes de `</head>` y se reemplaza el contenido de la página por este:

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

- **Conclusión:** un párrafo.
- **Por qué:** una lista numerada de tres frases, cada una con la sección donde está la evidencia.
- **Evidencia:** el índice de subsecciones, con línea de puntos y el código de su primera figura.
- **Términos:** un glosario corto de los términos que el lector necesita.

## Páginas

De cuatro a cinco subsecciones de una página A4. Cada una lleva introducción, descripción funcional, un apartado con una regla, dos figuras, una tabla de dos columnas con filas cortas, un aviso (NOTA o PRECAUCIÓN) y una tarjeta de procedimiento con líneas de 34 caracteres o menos. El orden de las subsecciones sigue a la pirámide: diseño, el detalle de cada parte, la evidencia de calidad y, al final, la operación y los límites.

## Ciclo de revisión

Renderizar cada página con `render.sh` (el chequeo de ajuste no debe decir OVERFLOW), mirar el PNG, corregir, pasar `check.py` y unir las páginas en un solo PDF (por ejemplo con `pypdf` o `pymupdf`). Esperar de dos a cuatro pasadas por página: los solapes de etiquetas y los desbordes de tablas casi siempre aparecen en la primera. Entregar el PDF y un README que diga de dónde sale cada cifra y cómo regenerar el documento.

## Lecciones

- Una tabla con valores largos aprieta la primera columna y desborda la página. Acortar las filas.
- No poner etiquetas encima de los cables de un diagrama. Alinearlas a la derecha o quitarlas.
- Reescribir las frases donde una referencia como «figura 4.3-1» cae partida en el guion.
- Las etiquetas de estratos deben decir qué son («PLAN PND1», no «PND1»).
- Un cable de bus debe llegar a todos sus destinos.
- La primera revisión suele encontrar solapes y desbordes: no entregar sin mirar cada página.
- `render.sh` a veces termina con «Killed: 9» en el paso del PNG. Repetirlo.

## Créditos

- `nasa-handbook`, de R44VC0RP: plantilla, fuentes (Routed Gothic, SIL OFL 1.1; Letter Gothic Code, Aladdin Free Public License), `render.sh`, `check.py` y referencias de estilo.
- El decálogo de Prodigioso Volcán, en el que se basa `unicorntext`.
- El Pyramid Principle de Barbara Minto, en el que se basa `minto-pyramid`.
