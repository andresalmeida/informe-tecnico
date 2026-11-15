# Contribuir

Este repositorio sigue gitflow. Las ramas tienen un solo propósito:

| Rama | Para qué | Sale de | Entra en |
|---|---|---|---|
| `main` | Solo versiones publicadas, cada una con su etiqueta (`v0.8.0`). | | |
| `develop` | Integración: aquí se junta el trabajo para la próxima versión. | `main` (una vez) | |
| `feature/<tema>` | Un cambio o un tipo de documento nuevo. | `develop` | `develop` |
| `release/<x.y.z>` | Cierre de una versión: número de versión, últimos ajustes y la CI. | `develop` | `main` y `develop` |
| `hotfix/<tema>` | Corrección urgente de lo publicado. | `main` | `main` y `develop` |

No se trabaja directamente en `main` ni en `develop`: todo entra por una rama y un pull request, con la CI en verde. Los commits van en español, pequeños y uno por paso.

## Publicar una versión

1. Crear `release/<x.y.z>` desde `develop`. Subir `metadata.version` en `skills/informe-tecnico/SKILL.md` y la versión del README. Correr `python tests/self_test.py`.
2. Abrir un pull request contra `main`. Cuando la CI pase, fusionarlo (merge commit, sin squash) y etiquetar `v<x.y.z>` sobre `main`.
3. Fusionar `main` en `develop` para que la versión publicada vuelva a la integración, y borrar la rama `release/<x.y.z>`.
4. Actualizar las copias instaladas con `git fetch` y `python tools/instalar.py`.

## Antes de abrir un pull request

```sh
python tests/self_test.py
python tests/comprobar_enlaces.py
python tools/regresion.py <commit-base>   # solo si cambia el motor
```

Para añadir un tipo de documento, seguir [docs/nuevo-tipo.md](docs/nuevo-tipo.md). Los ejemplos y las muestras son ficticios: ningún dato real, ningún nombre de persona o empresa reales.
