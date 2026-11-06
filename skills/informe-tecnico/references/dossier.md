# Dossier de sistema (`informe-dossier`)

Un dossier presenta en 6 a 8 páginas A4 cómo funciona un sistema y qué tan confiable es. Lleva la conclusión primero y figuras de ingeniería con el aspecto de un manual de operaciones del Apolo. No usa el motor JSON de este skill ni `document.kind`: es un flujo que se apoya en otros skills.

Se activa cuando el usuario dice «informe-dossier», «modo nasa dossier» o «flow NASA».

## Requisito

El skill **`nasa-handbook`** de R44VC0RP ([github.com/R44VC0RP/skills](https://github.com/R44VC0RP/skills), carpeta `skills/nasa-handbook`) debe estar instalado. Si no lo está, decirlo y detenerse. El dossier toma de ahí la plantilla, las fuentes, `render.sh` y `check.py`; no se copian a este repositorio.

Versión congelada: commit `e6f8682d1` (26 de octubre de 2026), probada con dos dossiers reales. No actualizar sin revisar la diferencia y comprobar que sigan funcionando los nombres de clase CSS de la plantilla. Para saber si cambió:

```sh
gh api "repos/R44VC0RP/skills/commits?path=skills/nasa-handbook&per_page=1" --jq '.[0].sha'
```

Si el resultado no empieza con `e6f8682d1`, hay cambios que revisar.

## Método

1. **Estructura con `minto-pyramid`.** Una conclusión, de tres a cinco argumentos y la evidencia de cada uno. La conclusión va en la portada. Si el usuario todavía no tiene una conclusión, pedirla antes de seguir.
2. **Redacción con `unicorntext`.** Frases directas, sin tríadas, sin «no es X sino Y», sin rayas largas y sin dos puntos dramáticos.
3. **Figuras con `diagram-design`.** Elegir el tipo de diagrama según lo que debe mostrar, con un máximo de nueve nodos, y borrar antes que agregar.
4. **Páginas.** Una portada con la pirámide, el índice y los términos, y de cuatro a cinco subsecciones de una página A4. Cada subsección lleva introducción, descripción funcional, un apartado con una regla, dos figuras, una tabla de dos columnas, un aviso (NOTA o PRECAUCIÓN) y una tarjeta de procedimiento con líneas de 34 caracteres o menos.
5. **Ciclo de revisión.** Armar las páginas, renderizar cada una, mirar el PNG, corregir, pasar `check.py` y unir en un solo PDF. El chequeo de ajuste no debe decir OVERFLOW.
6. **Entrega.** El PDF y un README que diga de dónde sale cada cifra y cómo regenerar el documento.

Las cifras se escriben con su fuente. No se inventan datos para llenar una figura.

## Lecciones

- Una tabla con valores largos aprieta la primera columna y desborda la página. Acortar las filas.
- No poner etiquetas encima de los cables de un diagrama. Alinearlas a la derecha o quitarlas.
- Reescribir las frases donde una referencia como «figura 4.3-1» cae partida en el guion.
- Las etiquetas de estratos deben decir qué son («PLAN PND1», no «PND1»).
- Un cable de bus debe llegar a todos sus destinos.
- `render.sh` a veces termina con «Killed: 9» en el paso del PNG. Repetirlo.

## Estado

Esta guía describe el método. Los scripts de armado (portada, páginas, unión del PDF) todavía no están en este repositorio y se añadirán, junto con un PDF de muestra sin datos reales.

## Créditos

- `nasa-handbook`, de R44VC0RP: plantilla, fuentes (Routed Gothic, SIL OFL 1.1; Letter Gothic Code, Aladdin Free Public License), `render.sh` y `check.py`.
- El decálogo de Prodigioso Volcán, en el que se basa `unicorntext`.
- El Pyramid Principle de Barbara Minto, en el que se basa `minto-pyramid`.
