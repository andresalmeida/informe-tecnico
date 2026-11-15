# Guía para agentes que mantienen este repositorio

Este archivo es para quien **modifica** el repositorio (una persona o un agente). Quien solo **usa** la skill para redactar un documento lee `skills/informe-tecnico/SKILL.md`; quien llega a conocer el proyecto lee el `README.md`.

## Qué es

`informe-tecnico` es una skill para agentes: redacta y compila en PDF documentos técnicos y de gestión de proyectos con la identidad de una entidad. Un agente lee `SKILL.md`, elige el tipo de documento (hay 22 y un dossier), escribe un JSON y el motor en Python (`reportlab`) lo convierte en PDF y lo comprueba. **Solo `skills/informe-tecnico/` se instala**; el resto del repositorio es para mantenerla.

```text
skills/informe-tecnico/
  SKILL.md        enrutador: una tabla de tipos, qué leer y reglas comunes (menos de 100 líneas)
  references/     tipos/ (una guía por tipo), informe/ (solo el informe y el manual), contrato/ (esquema del motor), comunes
  assets/         ejemplo-<tipo>.json, el JSON de partida de cada tipo (ficticios)
  scripts/        el motor: build_report.py, check_report.py y sus módulos
tests/            self_test.py y sus módulos; comprobar_enlaces.py; golden/
tools/            regresion.py (compara versiones del motor) e instalar.py (instala la skill en Claude Code y Codex)
docs/             muestra-<tipo>.pdf y su manifiesto; nuevo-tipo.md
```

## Antes de tocar nada

1. Leer [CONTRIBUTING.md](CONTRIBUTING.md): el flujo de ramas es gitflow.
2. Si el cambio es un tipo de documento nuevo o cambia el esquema de uno, leer [docs/nuevo-tipo.md](docs/nuevo-tipo.md). El catálogo está congelado en 22 tipos: no se añaden sin un uso real que alguien pueda nombrar.
3. Preparar un entorno de Python fuera del repositorio:

```sh
python3 -m venv ~/.cache/informe-venv && ~/.cache/informe-venv/bin/python -m pip install -r requirements.txt
```

## Flujo de ramas

- `main` y `develop` están **protegidas**: un `git push` directo se rechaza. Todo entra por pull request con la CI `validate` en verde.
- Cada cambio va en `feature/<tema>` creada desde `develop`, con un pull request a `develop` y merge commit (sin squash). Una versión nueva sale de `release/<x.y.z>` hacia `main`, con etiqueta, y vuelve a `develop`.
- Los commits van en español, pequeños y uno por paso. Terminan con las líneas de coautoría que correspondan a tu agente.
- No subas nada que no esté verificado. Un agente no fusiona un pull request sin que la CI haya pasado.

## Qué hacer según el cambio

| Cambio | Qué se hace |
|---|---|
| Corregir el texto de una guía | Editar `references/`, correr `python tests/comprobar_enlaces.py`. No cambian las muestras. |
| Cambiar `SKILL.md` | Mantenerlo corto y su tabla de tipos al día. Después de un cambio de enrutamiento, probar con un agente nuevo y un modelo pequeño que elija el tipo para unas doce peticiones, sin construir nada. |
| Cambiar el motor | Correr `python tests/self_test.py` y `python tools/regresion.py <commit-base>`. Solo deben cambiar los ejemplos que el cambio busca cambiar. Una prueba nueva debe fallar con el motor anterior. Regenerar las muestras afectadas. |
| Regenerar una muestra | `python skills/informe-tecnico/scripts/build_report.py skills/informe-tecnico/assets/ejemplo-<tipo>.json --output docs/muestra-<tipo>.pdf`, y comprobarla con `check_report.py`. Una muestra nunca se edita a mano. |
| Añadir o cambiar un tipo | Seguir `docs/nuevo-tipo.md` paso a paso. |
| Cambiar los títulos de un tipo de formulario | Pasa por `format.heading_case`; actualizar `tests/golden/heading-title.json` con `python tests/test_heading_case.py --update`. |

Antes de abrir el pull request: `python tests/self_test.py` termina con `ok: true`, los enlaces están bien, y has **abierto las páginas renderizadas** de lo que cambió (un comando exitoso no demuestra buena composición).

## Reglas de contenido

- **Español sobrio.** Sin raya larga, sin el contraste «no es X sino Y», sin enumeraciones de tres elementos por costumbre y sin emojis.
- **Datos ficticios.** Entidad «Entidad de demostración», códigos con prefijo `DEMO-`, nombres, cifras y fechas inventados. Nunca datos, nombres ni logotipos reales, ni copia del texto de un formato ajeno.
- **Lo que falta se escribe con palabras fijas** (`references/pendientes-y-estado.md`): «Pendiente», «Por confirmar», «Por estimar». Los ejemplos no inventan firmas, aprobaciones ni resultados.
- **Títulos en mayúscula de oración** («Información de referencia»). La mayúscula de cada palabra es la opción `format.heading_case: "title"`.
- Los encabezados de las guías van en minúscula normal.

## Lo que no se hace

- No se suben pruebas ni herramientas a `skills/informe-tecnico/`: lo que se instala es solo el motor.
- No se cambia el comportamiento del motor sin la regresión que demuestre qué cambió y qué no.
- No se reintroduce la mayúscula de título como valor por defecto, ni se copian o se citan formatos de otras entidades.
- No se versiona nada fuera del árbol que describe este archivo: las referencias locales (`/*.pdf`, `output/`, `tmp/`) están en `.gitignore` y no se distribuyen.

## Instalar la versión publicada

`git fetch` y `python tools/instalar.py` instalan la versión de `main` en Claude Code y en Codex, con respaldo y verificación (`--simular` no escribe).
