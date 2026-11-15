# Informe técnico institucional

Una skill para agentes (Claude Code, Codex, Cursor y otros) que redacta y compila en PDF documentos técnicos y de gestión de proyectos con la identidad de tu entidad: nombre, logo, colores y esquema de códigos. El agente lee `SKILL.md`, elige el tipo de documento, escribe una fuente JSON y un motor en Python la convierte en un PDF con cabecera, paginación, historial de cambios, índices y un comprobador.

**Versión 0.8.0** · licencia MIT · Python 3.10 o posterior

[![CI](https://github.com/andresalmeida/informe-tecnico/actions/workflows/validate.yml/badge.svg)](https://github.com/andresalmeida/informe-tecnico/actions/workflows/validate.yml)

![Primera página de los seis documentos del núcleo: acta de reunión, factibilidad, propuesta, alcance, plan de pruebas y acta de entrega](docs/muestras-collage.png)

<sub>Muestras con una entidad ficticia. Cada PDF completo está en [`docs/`](docs/).</sub>

## Qué produce

Veintidós tipos de documento y un dossier, pensados para seguir un proyecto del primer encuentro al cierre. Casi ningún proyecto los usa todos. Estos seis cubren la mayoría:

| Documento | Para qué |
|---|---|
| [Acta de reunión](docs/muestra-acta-reunion.pdf) | Dejar constancia de lo tratado y de los compromisos |
| [Informe de factibilidad](docs/muestra-informe-factibilidad.pdf) | Decidir si una propuesta técnica se puede asumir |
| [Propuesta de servicio](docs/muestra-propuesta-servicio.pdf) | Ofrecer qué se hace, en qué plazo y por cuánto |
| [Alcance del proyecto](docs/muestra-alcance-proyecto.pdf) | Fijar qué se construye y quién lo acepta |
| [Plan de pruebas de aceptación](docs/muestra-plan-pruebas.pdf) | Acordar casos, registrar resultados y cerrar con un certificado |
| [Acta de entrega y recepción](docs/muestra-acta-entrega.pdf) | Registrar qué se entregó y con qué conformidad |

<details>
<summary>Los otros dieciséis tipos</summary>

Informe, manual o catálogo; registro de requerimientos; registro de riesgos; evaluación de impacto en datos; especificación de requisitos; decisión de arquitectura; descripción de arquitectura; plan de proyecto; solicitud de cambio; acta de capacitación; traspaso a operación; notas de versión; informe de cierre; acta de baja; ficha de modelo; ficha de proceso. El dossier de sistema es un flujo aparte que no usa el motor JSON.

Cada uno tiene su guía en [`skills/informe-tecnico/references/`](skills/informe-tecnico/references/), un JSON de partida en `assets/` y un PDF de muestra en [`docs/`](docs/).
</details>

Qué documento va en cada fase y cuáles son indispensables: [mapa de uso](skills/informe-tecnico/references/flujo-proyecto.md).

## Cómo se usa

Instala la skill y pide el documento con tus palabras:

```text
Usa $informe-tecnico para preparar la propuesta de servicio del módulo de pagos
a partir de la factibilidad ya cerrada. Da el plazo, los entregables y la
cotización con mis precios, y deja la aceptación pendiente.
```

El agente elige el tipo con la tabla de `SKILL.md`, lee solo la guía de ese tipo, escribe el JSON, compila, comprueba y revisa cada página. Lo que no consta queda en «Pendiente», «Por confirmar» o «Por estimar»: no inventa firmas, aprobaciones ni cifras.

La identidad se configura en el JSON:

```json
"brand": { "entity": "Estudio de Software Ejemplo", "unit": "Equipo de Proyectos",
           "accent": "#2F4B7C", "logo": "logo.png" }
```

Cada guía incorpora dos criterios de escritura: la pirámide de Minto (la conclusión primero) y la revisión de estilo de unicorntext (sin relleno). Para los esquemas, la skill colaboradora `diagram-design` los dibuja con los colores y la tipografía del documento.

Los documentos de un proyecto forman una cadena: cada uno cita a los anteriores por su código (`SRO-ALC-01, versión 0.2`) y las versiones nuevas conservan el código.

## Instalar y actualizar

La versión instalada está en `metadata.version` de `SKILL.md` y debe coincidir con la de este README. Una copia antigua enruta un proyecto a un informe genérico. Para actualizar, guarda tus JSON fuera de la carpeta de la skill, bórrala y vuelve a instalar.

- **Claude Code.** Copia `skills/informe-tecnico` a `~/.claude/skills/informe-tecnico` (para todos tus proyectos) o a `.claude/skills/informe-tecnico` (para uno).
- **Codex.** Pide al agente: «Instala la skill informe-tecnico desde https://github.com/andresalmeida/informe-tecnico, ruta skills/informe-tecnico».
- **Esquemas nuevos (opcional).** La skill colaboradora [diagram-design](https://github.com/cathrynlavery/diagram-design) se instala por separado.

## Ejecutar el motor sin el agente

```sh
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt

python skills/informe-tecnico/scripts/build_report.py \
  skills/informe-tecnico/assets/ejemplo-acta-reunion.json --output output/acta.pdf
python skills/informe-tecnico/scripts/check_report.py output/acta.pdf
```

Copia el JSON de partida del tipo que necesites, cambia los datos de demostración y conserva los activos junto a la fuente. El acta de reunión también se exporta a Word. Si falta una dependencia, el script termina con un mensaje que dice qué instalar.

Para modificar el motor o añadir un tipo: `python tests/self_test.py` ejecuta las pruebas, [docs/nuevo-tipo.md](docs/nuevo-tipo.md) explica los pasos y [CONTRIBUTING.md](CONTRIBUTING.md) describe las ramas.

## Qué hay en el repositorio

```text
skills/informe-tecnico/   la skill que se instala
  SKILL.md                lo que lee el agente: elige el tipo y enruta
  references/             guías por tipo (tipos/), del informe (informe/) y comunes
  assets/                 JSON de partida de cada tipo
  scripts/                el motor: compila el PDF y lo comprueba
tests/                    pruebas del motor
tools/                    regresión entre versiones
docs/                     muestras en PDF y guía para añadir un tipo
```

Este README es para quien llega al repositorio. El agente lee `SKILL.md` y las guías; quien mantiene la skill lee [CONTRIBUTING.md](CONTRIBUTING.md).

## Lo que esta skill no hace

- **No da asesoría legal ni contable.** Los campos normativos de la evaluación de impacto en datos quedan «Por confirmar con asesoría legal», y las condiciones de pago, garantía y validez de una propuesta las escribe la entidad.
- **No firma.** Las firmas del PDF son espacios para firmar; el motor no implementa firma electrónica. Una aceptación comunicada no es una firma.
- **No acredita.** El certificado del plan de pruebas registra una decisión entre las partes, no la certificación de un tercero.
- **No garantiza la composición.** El comprobador revisa lo que puede medir; abrir todas las páginas renderizadas sigue siendo parte del trabajo.

## Licencia y atribuciones

[MIT](LICENSE). Las referencias de diseño y las decisiones de adaptación están en [fuentes.md](skills/informe-tecnico/references/fuentes.md). El ejemplo de diagrama conserva la [licencia de diagram-design](skills/informe-tecnico/assets/diagrams/LICENSE-diagram-design.txt). El dossier se apoya en el skill `nasa-handbook` de R44VC0RP, que no se copia aquí, y cita el decálogo de Prodigioso Volcán (`unicorntext`) y el Pyramid Principle de Barbara Minto.
