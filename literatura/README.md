# Biblioteca de literatura — MF7011

**37 PDFs · 125 MB · descargados 2026-08-19**

> `literatura/pdf/` está en `.gitignore` (peso). Se reconstruye con
> `bash ../recursos/descargar-literatura.sh`

## Obligatorias del curso

| Archivo | Referencia | Sesión |
|---|---|---|
| `Schoenmaker-Schramade2023_corporate-finance-LTV.pdf` | **Corporate Finance for Long-Term Value** · Springer OA · 652 pp | S1, S3 |
| `FOLU2023_SbN-Colombia-ES.pdf` / `-EN.pdf` | FOLU Colombia & Climate Focus · SbN | S1 |
| `Drupp-etal_discounting-disentangled.pdf` | Tasa social de descuento · WP Grantham 172 | S4 |
| `WB2024_shadow-price-carbon.pdf` | Banco Mundial · precio sombra del carbono | S4 |
| `Jayachandran-etal_cash-for-carbon-NBER.pdf` | Cash for Carbon · NBER 22378 | S4 |
| `SFC_circular-externa-015-2025.pdf` | Resumen ANDI de la circular | S5 |

## Consulta

| Archivo | Referencia |
|---|---|
| `NGFS_guide-scenario-analysis.pdf` | Escenarios climáticos de referencia |
| `DNP2023_MGA-documento-conceptual.pdf` | Metodología General Ajustada · Colombia |
| `Terrasos_bancos-de-habitat.pdf` | Bancos de hábitat · instrumento colombiano |
| `welch-cornell-clima/` | **Welch & Cornell** · libro completo, 19 capítulos |
| `WEF2025_finance-solutions-for-nature.pdf` | WEF · finanzas para la naturaleza |
| `BCA_biodiversity-credit-metrics.pdf` | Biodiversity Credit Alliance · métricas |
| `CDC-Biodiversite_biodiversity-credits.pdf` | Créditos de biodiversidad · estándares |
| `IUCN_regulating-financing-mechanisms.pdf` | IUCN · regulación de mecanismos |
| `Jayachandran_pes-tradeoff-ERL2023.pdf` | PSA · disyuntivas de diseño |
| `NBER_climate-change-long-run-discount-rates.pdf` | Descuento de largo plazo |
| `CEPAL_acb-energias-renovables.pdf` | ACB · energías renovables |
| `PwC-CFA_caso-climatico-proyectos-mitigacion.pdf` | Caso climático de proyectos |

## Lecturas curadas por sesión (`literatura/readings/`)

Extractos cortos (1 capítulo, PDF liviano) para lectura obligatoria/complementaria de una sesión puntual — distinto de `literatura/pdf/` (biblioteca completa de consulta, gitignored). **Sí se versiona en git.**

**Convención de nombres:** `SSx_Descripción.pdf` — `SS` = sesión de destino (`01`…`05`), `x` = letra de orden de llegada (`a`, `b`, …). La letra no indica obligatoria vs. complementaria; eso se declara en el syllabus.

| Archivo | Referencia | Sesión | Tipo |
|---|---|---|---|
| `01a_Schoenmaker_Schramade_Cap1.pdf` | Schoenmaker & Schramade (2023), cap. 1 [@schoenmaker2023] | S1 | Complementaria |
| `01b_Berg-etal_2022.pdf` | Berg, Kölbel & Rigobon (2022) [@berg2022] | S1 | Obligatoria |
| `01c_Schoenmaker_Schramade_Cap2.pdf` | Schoenmaker & Schramade (2023), cap. 2 [@schoenmaker2023] | S1 | Complementaria |
| `01d_FOLU2023_SbN-Colombia-ES.pdf` | FOLU Colombia (2023) [@folu2023] | S1 | Obligatoria |
| `02a_Forecasting.pdf` | Hyndman & Athanasopoulos, cap. 1 *Getting started* [@hyndman2021] | S2 | Obligatoria |
| `02b_Sapag_Cap6_Costos.pdf` | Sapag Chain, cap. 6 *Estimación de costos* [@sapag2014] | S2 | Obligatoria |
| `03a_Schoenmaker_Schramade_Cap4.pdf` | Schoenmaker & Schramade (2023), cap. 4 *Discount Rates and Scarcity of Capital* [@schoenmaker2023] | S3 | Complementaria |

⚠️ **Corregido 2026-08-23:** los tres archivos llegaron con prefijo `03a/03b/03c`. Se verificó el contenido de cada uno (`pdftotext` + inspección de secciones) y dos de los tres eran material de **S2** mal etiquetado — se renombraron a `02a`/`02b`. Sólo el capítulo de tasas de descuento (`Schoenmaker Cap. 4`) es efectivamente de S3; quedó como `03a`, coherente con la nota del syllabus de que capítulos de Schoenmaker "aparecen como lectura complementaria en S1 y S3".

⚠️ `02b_Sapag_Cap6_Costos.pdf` cubre **costos** en profundidad (12 subsecciones) pero **no** desarrolla capital de trabajo — el capítulo solo lo menciona de paso al cierre, remitiendo a un capítulo posterior del libro que no se incluyó aquí. El método de **déficit acumulado máximo** que usan los slides de S2-sábado se enseña ahí directamente, sin respaldo de lectura dedicado — es una decisión pedagógica válida, no un vacío a ocultar.

## ⚠ Pendientes de obtención manual

| Referencia | Por qué falló | Ruta |
|---|---|---|
| **Berg, Kölbel & Rigobon (2022)** | Review of Finance — acceso | EZproxy EAFIT · o SSRN 3438533 |
| **Jayachandran et al. (2017)** versión *Science* | Paywall | EZproxy · el WP NBER ya está bajado |
| **Circular Externa 015 de 2025** completa | Sitio SFC exige navegación | superfinanciera.gov.co · Normativa · CE 015 del 3-oct-2025 |
| **Carta Circular 067 de 2025** | Plan de implementación de la CE 015 | superfinanciera.gov.co |
| Papers de cacao (MDPI ×3) | Cloudflare bloquea descarga automatizada | Abrir en navegador: `mdpi.com/2071-1050/14/15/9447` |
| *Proc. R. Soc. B* créditos de biodiversidad | Bloqueo | PMC12364579 en navegador |
| **Boardman (2018)** · **Brigham (2022)** | Libros comerciales | Biblioteca EAFIT |

## Verificaciones hechas al bajar

- ✅ **Circular Externa 015 es de 2025** (3-oct-2025), no de 2024. El PDF de Camacol rotulado "015 de noviembre de 2024" resultó ser un escaneo sin capa de texto y de otro asunto — descartado.
- ✅ Schoenmaker & Schramade (2023) confirmado **acceso abierto**, 652 páginas, vía OAPEN.
- ⚠️ Los papers de cacao **no pudieron verificarse**: la cifra de VPN (1.446,45) sigue con unidad sin confirmar. No usar en clase hasta abrir el artículo.
