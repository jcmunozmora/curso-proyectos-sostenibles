# Rúbricas de Evaluación — MF7011

**Escala institucional 0.0–5.0.** Conversión: `nota = total/100 × 5.0`
Nota aprobatoria: **[POR-VERIFICAR con Registro Académico]**

| Componente | Peso | Instrumento | Quién califica |
|---|---:|---|---|
| Artefactos de sesión | 25% | R1 · 5 entregas | Profesor |
| Auditorías cruzadas | 15% | R2 · 4 entregas | Profesor |
| Modelo financiero final | 25% | R3 | Profesor |
| Defensa · Investor Day | 20% | R4 | **Profesor 50% + Comité 50%** |
| **Calidad como evaluador** | **15%** | **R5** | Profesor |
| | **100%** | | |

**Modulador individual:** la co-evaluación de contribución intra-equipo aplica un factor de **0,85 a 1,15** sobre los componentes de equipo (R1, R2, R3, R4). Ver [co-evaluación](06-coevaluacion-comite.md) §Capa 2.

::: nota
**La co-evaluación entra por tres vías:** el 50% de R4 (el comité puntúa los proyectos), el modulador intra-equipo, y R5 —que califica **la calidad del juicio de cada estudiante como evaluador**. Esa tercera vía es la que hace honestas a las otras dos: si evaluar fuera gratis, se degradaría en cortesía mutua.

Instrumentos, salvaguardas y detección de valores atípicos: [`06-coevaluacion-comite.md`](06-coevaluacion-comite.md).
:::

---

## R1 · Artefactos de sesión — 25%

Cinco entregas, una por sesión, **producidas y subidas en el salón**. Cada una sobre 20 puntos.

| Criterio | 5 · Excelente | 3 · Suficiente | 1 · Insuficiente |
|---|---|---|---|
| **Completitud** | Todas las secciones con contenido sustantivo | Completo con vacíos menores | Secciones vacías o de relleno |
| **Trazabilidad de cifras** | Toda cifra externa con fuente verificable | Mayoría con fuente | Cifras sin fuente |
| **Corrección técnica** | Sin errores conceptuales | Errores menores no estructurales | Error estructural (doble conteo, unidades, etc.) |
| **Respuesta a la auditoría previa** | Todos los hallazgos corregidos y documentados | Mayoría corregidos | Hallazgos ignorados |

**Reglas de calificación:**

- Entregado fuera del salón: **máximo 12/20**, salvo ausencia justificada.
- Una sola cifra material sin fuente: **tope de 14/20**.
- Error de unidades (por hectárea vs. total, real vs. nominal): **tope de 10/20** hasta corregirlo.

---

## R2 · Auditorías cruzadas — 15%

Cuatro entregas. Se evalúa **la calidad de la auditoría**, no la del modelo auditado. Cada una sobre 15 puntos.

| Criterio | 5 | 3 | 1 |
|---|---|---|---|
| **Cobertura** | Recorrió los ítems de la lista con evidencia por cada uno | Recorrió la mayoría | Superficial o incompleta |
| **Precisión de los hallazgos** | Los hallazgos son reales y verificables en el modelo | Mayoría reales, alguno espurio | Hallazgos inventados o triviales |
| **Utilidad** | Cada hallazgo dice **qué corregir y cómo** | Señala el problema sin la solución | Sólo dice "está mal" |

**Bonificación por hallazgo material:** +2 puntos al equipo auditor por cada error **estructural** encontrado y confirmado por el profesor. Máximo +6 por sesión.

::: nota
**Que a un equipo le encuentren un error no resta puntos.** No corregirlo para la sesión siguiente sí: tope de 12/20 en el artefacto de R1.
:::

---

## R3 · Modelo financiero final — 25%

Sobre 100 puntos.

| Bloque | Pts | Qué se verifica |
|---|---:|---|
| **Arquitectura del modelo** | 15 | Supuestos separados de cálculos · sin números codificados en fórmulas · unidades en todos los encabezados · navegable |
| **Costos e inversiones** | 15 | CapEx completo (incluye estudios previos, resiembra, imprevistos) con cronograma · OpEx con curva de maduración · fijo vs. variable separado |
| **Capital de trabajo** | 10 | Método del déficit acumulado · **recuperación en el último año** |
| **Flujo de caja** | 20 | FCLD sin deuda · FCA con deuda descontado al Ke · impuesto cero (no negativo) en pérdida · escudo fiscal sólo con renta gravable · valor terminal con *g* defendible |
| **Criterios de decisión** | 10 | VPN con rango de WACC · TIRM además de TIR · **patrón de signos verificado y declarado** · precio de equilibrio |
| **Flujo socioeconómico** | 20 | Transferencias eliminadas · precios sombra con factor y fuente · línea base de carbono declarada · tabla sin/bajo/alto · **switching value** |
| **Escenarios NGFS** | 10 | Tres escenarios genuinamente distintos · riesgo climático contado **una sola vez** |

**Penalizaciones (se restan del total):**

| Falta | −pts |
|---|---:|
| FCA descontado al WACC (doble conteo de deuda) | −15 |
| Riesgo climático en flujo **y** tasa | −10 |
| Capital de trabajo sin recuperación | −8 |
| Impuesto negativo en años de pérdida | −8 |
| Cifra material sin fuente | −5 c/u |
| Celda codificada a mano que debería ser fórmula | −3 c/u |

---

## R4 · Defensa · Investor Day — 20%

Sobre 100 puntos.

$$R4 = 0{,}50 \times \text{profesor} + 0{,}50 \times \text{mediana del comité}$$

Se usa la **mediana** de las puntuaciones del comité, no el promedio: es robusta a un evaluador extremo. Las puntuaciones del comité se recogen con la **tarjeta de co-evaluación** ([`06-coevaluacion-comite.md`](06-coevaluacion-comite.md) §Capa 1), que exige evidencia específica en los cinco criterios.

**Umbral de validez:** si un proyecto recibe menos de **3 evaluaciones válidas** (con evidencia), la co-evaluación no se aplica y R4 = 100% profesor. Se informa al grupo.

| Criterio | Pts | Qué se verifica |
|---|---:|---|
| **Solidez del modelo** | 30 | Los números resisten el interrogatorio. Sin errores de doble conteo. |
| **Honestidad de los supuestos** | 25 | Declararon lo frágil **sin que se los preguntaran**. El escenario bajo es realmente bajo. |
| **Adicionalidad del impacto** | 20 | Línea base defendible. Sobreviviría a un verificador. |
| **Bancabilidad** | 15 | Alguien de la mesa podría realmente financiarlo, con el instrumento que piden. |
| **Calidad de la respuesta** | 10 | Respondieron o esquivaron. "No lo sé, y esto es lo que haría para averiguarlo" **puntúa**. |

**Reglas:**

- Presentar un VPN negativo **con su mitigación** puntúa más alto que esconderlo. Si el comité descubre un número oculto: **−20**.
- Exceder los 12 minutos: **−5** y se corta.
- Más de 8 diapositivas: **−5**.
- "No lo sé" honesto: neutro. "No lo sé" disfrazado de respuesta larga: **−5**.

---

## R5 · Calidad como evaluador — 15%

**Este componente sostiene todo el sistema de co-evaluación.** Sobre 20 puntos, acumulado a lo largo del curso: 4 auditorías cruzadas + 4 turnos de *discussant* en el Tribunal + la co-evaluación del Investor Day.

Se evalúa **la calidad del juicio, nunca la severidad o la generosidad.**

| Criterio | 5 | 3 | 1 |
|---|---|---|---|
| **Especificidad de la evidencia** | Cita celdas, cifras o frases textuales | Evidencia general pero verificable | "Buen trabajo" / sin evidencia |
| **Fidelidad al rol** | Evaluó consistentemente desde la lente de su rol | Mezcló el rol con opinión general | Ignoró el rol asignado |
| **Discriminación** | Sus puntuaciones distinguen proyectos de calidad distinta | Alguna diferenciación | Puso lo mismo a todos |
| **Detección** | Encontró al menos un problema real que otros no vieron | Encontró problemas ya conocidos | No encontró nada |
| **Coherencia** | Su asignación de presupuesto es consistente con sus puntuaciones | Inconsistencia menor | Puntuó alto y no financió, sin explicarlo |

**Bonificación:** +2 por cada error **estructural** detectado en un modelo ajeno y confirmado por el profesor. Máximo +4 en total.

**Penalizaciones:**

| Falta | Consecuencia |
|---|---|
| Puntuar 5 (o 1) a todos sin evidencia diferenciada | **máximo 8/20** |
| Tarjeta de co-evaluación sin la columna Evidencia | esa tarjeta **no se cuenta** y −3 en R5 |
| Evaluar el propio proyecto | tarjeta anulada |
| Valor atípico (>1,5 pts de la mediana) **sin** evidencia sólida | se descarta de R4 y −3 en R5 |
| Valor atípico (>1,5 pts de la mediana) **con** evidencia sólida | **se mantiene y puntúa alto en R5** |

::: nota
**Hablar mucho no puntúa.** Una pregunta que deja a un equipo sin respuesta vale más que diez comentarios de acuerdo. Y un evaluador que se aparta de la mediana **porque vio algo que nadie más vio** es exactamente el objetivo del ejercicio, no una desviación a corregir.
:::

---

## Integridad académica y uso de IA

**Se espera el uso de IA.** Dos reglas:

1. **Anexo de IA obligatorio** en el entregable final: herramienta, para qué, resumen del prompt, cómo se verificó.
2. **Toda cifra verificada contra fuente primaria.**

| Falta | Consecuencia |
|---|---|
| Cifra sin fuente verificable presentada como dato | **Anula el entregable** |
| Referencia inexistente o inventada | **Anula el entregable** |
| Anexo de IA ausente | −10 en el modelo final |

> La IA es excelente encontrando estructura y poco confiable con números específicos. Un número inventado en su modelo es responsabilidad del equipo, no de la herramienta.
