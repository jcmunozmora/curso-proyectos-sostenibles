# Prompts para NotebookLM — podcast por sesión

Un prompt por **sesión de la semana** (S1, S2...), no por lectura individual. Cada sesión tiene varias lecturas — se suben todas al mismo notebook de NotebookLM y el prompt le pide al podcast que las teja entre sí, no que las resuma una por una.

## Cómo usarlos

1. Crea un notebook nuevo en NotebookLM por sesión.
2. Sube **todos** los PDF de `literatura/readings/` con el prefijo de esa sesión (p. ej. todos los `01*` para S1).
3. En "Personalizar" → "Audio Overview", pega el bloque de prompt del archivo `SX.md` correspondiente.
4. Genera. Escucha antes de compartirlo con el grupo — NotebookLM puede seguir alucinando cifras aunque las fuentes estén bien acotadas.

## Regla de emisión

Un prompt semanal solo se escribe cuando **todas** las lecturas obligatorias de esa sesión están en `literatura/readings/` y pasaron el gate de verificación de `/mambrino-lit` (contenido confirmado, no solo nombre de archivo). Si falta una, el prompt se marca **parcial** y dice explícitamente qué falta — nunca se rellena el hueco inventando qué diría la lectura ausente.

## Inventario

| Prompt | Sesión | Lecturas que cubre | Estado |
|---|---|---|---|
| [S1](S1.md) | "¿Qué es un proyecto sostenible y quién decide que lo es?" | Schoenmaker cap. 1 y 2 · Berg et al. (2022) · FOLU Colombia (2023) | ✅ Completo |
| [S2](S2.md) | "Los números que nadie te da" | Hyndman & Athanasopoulos cap. 1 · Sapag Chain cap. 6 | ✅ Completo |
| [S3](S3.md) | "El denominador" | Schoenmaker cap. 4 | ⚠️ Parcial — faltan Welch (2021) y Drupp et al. en `readings/` |
| S4 | "El otro flujo de caja" | WB (2024) shadow price · Jayachandran et al. (2017) | ⏳ Sin PDFs en `readings/` todavía |
| S5 | Investor Day | Circular Externa 015 · Schoenmaker cap. Decisiones de inversión | ⏳ Sin PDFs en `readings/` todavía |

Cuando lleguen los PDF de S3 (completar), S4 y S5, primero pasan por `/mambrino-lit` (verificación de contenido + nombre correcto en `literatura/readings/`) y solo después se escribe o completa el prompt aquí.
