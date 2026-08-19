# Formulación y Evaluación de Proyectos Sostenibles · MF7011

Curso de la **Maestría en Finanzas Sostenibles y Cambio Climático** y la **Especialización en Finanzas Sostenibles** — Escuela de Finanzas, Economía & Gobierno, Universidad EAFIT.

**36 horas · 5 encuentros · 4 semanas · Medellín, aula 19-712 · 2026-2**

🌐 **Sitio del curso:** <https://jcmunozmora.github.io/curso-proyectos-sostenibles/>

---

## El diseño en una frase

Los estudiantes formulan y evalúan **un proyecto real de inversión sostenible** —cacao agroforestal con ingresos de naturaleza— y lo defienden ante un comité de inversión con presupuesto limitado que va a rechazar proyectos.

**Viernes = El Tribunal** (decidir, debatir, defender). **Sábado = El Taller** (construir). Ritmo **20/40/15**: ninguna exposición supera 20 minutos. Proporción 27% profesor / 73% estudiante.

## Co-evaluación

El **Comité de Inversión** de la Sesión 5 es el órgano de co-evaluación. Cada estudiante recibe un rol —banco bajo Circular 015, fondo de impacto, comprador corporativo, entidad pública, comunidad, escéptico financiero— y puntúa los proyectos ajenos **desde esa lente**, con evidencia específica obligatoria.

| Vía | Peso |
|---|---|
| El comité puntúa las defensas | 50% de R4 (= 10% del curso) |
| **Calidad del juicio como evaluador (R5)** | **15% del curso** |
| Contribución intra-equipo | modulador 0,85–1,15 |

**El giro que la hace honesta:** no se evalúa qué tan severo o generoso fue cada quien, sino **qué tan buen juicio tuvo**. Salvaguardas: presupuesto escaso por diseño, mediana en vez de promedio, evidencia obligatoria, detección de valores atípicos, ejercicio de calibración previo. Detalle en [`plantillas/06-coevaluacion-comite.md`](plantillas/06-coevaluacion-comite.md).

## ⚠ Material docente: fuera de este repo a propósito

Este repositorio es **público**. Estas rutas están en `.gitignore` porque contienen los *reveals*, las respuestas preparadas y los errores plantados — si un estudiante los lee, el diseño del curso se cae:

```
instructor/                        guías, planes de sesión, caso de calibración
datos/modelo-trampa-s1.xlsx        el detonante de la S1
datos/construir_modelo_trampa.py
datos/caso_calibracion.py          los 5 errores plantados y el ancla
datos/analisis_*.py
```

Además, el build público aplica [`filtros/sin-notas.lua`](filtros/sin-notas.lua), que **elimina las notas del presentador** de las slides publicadas. El workflow falla si alguna se filtra.

- **Render local (con notas, para clase):** `quarto render`
- **Render público (sin notas, lo que corre CI):** `quarto render --profile publico`

**Recomendación:** versionar `instructor/` en un repositorio privado aparte. Hoy sólo existe localmente y no tiene respaldo.

---

## Estructura del repositorio

```
├── index.qmd · syllabus.qmd · proyecto.qmd · materiales.qmd
├── literatura/
│   ├── revision-literatura.qmd      ← el mapa del campo, tres tradiciones en tensión
│   ├── auditoria-bibliografia.qmd   ← insumo para Comité de Programa
│   ├── referencias.bib              ← 32 entradas, [V]/[PV] etiquetadas
│   └── pdf/                         ← 40 PDFs OA (fuera de git; ver recursos/)
├── slides/
│   ├── s01/ … s05/                  ← 9 mazos RevealJS
│   └── eafit.scss                   ← Azul Zafre #000066 / Azul Cielo #00A9E0
├── instructor/                      ← EXCLUIDO del render
│   ├── 00-plan-de-registro.md       ← documento maestro
│   ├── 01-diseno-pedagogico.md      ← el método y su evidencia
│   ├── 02-guia-estudio-profesor.md  ← 10 conceptos + 8 preguntas preparadas
│   └── planes-sesion/s1..s5.md      ← minuto a minuto
├── plantillas/
│   ├── modelo-financiero-PLANTILLA.xlsx  ← 10 hojas
│   ├── 01-ficha-de-proyecto.md
│   ├── 02-nota-de-inversion.md
│   ├── 03-fichas-de-rol-investor-day.md
│   ├── 04-rubricas.md               ← R1–R5 con penalizaciones
│   └── 05-listas-auditoria-cruzada.md
├── datos/
│   ├── modelo-trampa-s1.xlsx        ← el detonante de la Sesión 1
│   ├── construir_modelo_trampa.py
│   ├── analisis_wacc_s3.py
│   └── analisis_social_s4.py
└── recursos/descargar-literatura.sh  ← reconstruye literatura/pdf/
```

## Reproducir

```bash
export PATH="/opt/homebrew/bin:$PATH"
quarto render                              # sitio completo
bash recursos/descargar-literatura.sh      # 40 PDFs de acceso abierto
python3 datos/construir_modelo_trampa.py   # modelo-trampa S1
python3 datos/analisis_wacc_s3.py          # costo de capital S3
python3 datos/analisis_social_s4.py        # flujo socioeconómico S4
```

**Todas las cifras de las slides salen de esos tres scripts.** Si se cambia un supuesto, se re-corre el script y se sincronizan las slides.

---

## Datos verificados que cargan el curso

| Dato | Valor | Fuente |
|---|---|---|
| Precio cacao — récord | USD 12.931/t (dic-2024) → ~3.000–4.000/t (2026) | ICE |
| TSD ambiental Colombia | 9,5% (0–5a) · 6,4% (6–25a) · 3,5% (26+a) real | **DNP Res. 1092/2022** |
| TSD general Colombia | 9,0% EA real | DNP Res. 1092/2022 |
| Consenso experto internacional | media 2,25% · mediana 2,0% | Drupp et al. (197 expertos) |
| Prima riesgo país Colombia | 2,85% · ERP maduro 4,23% · Baa3 | Damodaran, 5-ene-2026 |
| Precio sombra del carbono | USD 50–100/tCO₂ a 2030 | Banco Mundial / HLCCP |
| Divergencia de ratings ESG | correlación 0,38–0,71 (crediticias ~0,99) | Berg, Kölbel & Rigobon (2022) |
| Brecha de financiamiento SbN Colombia | USD 13.500 M vs. <300 M/año ≈ 50× | FOLU Colombia (2023) |
| Costo-efectividad de PSA | USD 0,46/tCO₂ | Jayachandran et al. (2017) |
| Circular ASG obligatoria | **Circular Externa 015 de 2025** (no 2024) | SFC, 3-oct-2025 |
| *Greenium* | −12,4 pb promedio | revisión empírica 2025 |

## Los tres números del proyecto ancla

A **USD 3.500/t** — el precio real de 2026:

- **VPN privado: −USD 4,04 M** → nadie invierte
- **VPN social a TSD Colombia con C=100: +USD 0,81 M** → se justifica
- ***Switching value*: USD 72/tCO₂e** → dentro de la banda 50–100 del Banco Mundial

El curso entero cabe en esa brecha, y la pregunta *"¿quién la paga?"* es la asignatura siguiente.

---

## Protección de datos

`.gitignore` bloquea `Semestres/`, `entregas/`, `notas/`, `*_calificaciones.*`. Los datos de estudiantes son datos personales bajo la **Ley 1581 de 2012**: anonimizar (E01…En) antes de cualquier procesamiento con IA. **Verificar `git status` antes de cada push.**
