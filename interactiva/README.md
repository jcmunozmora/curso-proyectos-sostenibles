# Paquete de interactiva — MF7011 (Brightspace/D2L)

Paquete completo de personalización del curso en Brightspace/D2L, generado desde
una única fuente de verdad (`datos.py`). Nunca editar los archivos de `build/` a
mano: se sobreescriben en cada corrida de `generar.py`.

## Decisiones tomadas en el diagnóstico (2026-08-20)

- **Nivel de control asumido:** Import/Export + widgets HTML (el profesor confirmó
  tener este nivel). Si resulta ser menor, los templates de tópico siguen sirviendo
  como HTML embebible; el `.zip` de importación requiere este nivel.
- **Alcance:** paquete completo — homepage, 6 módulos (orientación + S1–S5), 34
  tópicos (tribunal/taller, plantillas, bibliografía por módulo, un podcast
  recomendado, 12 asignaciones), badges, release conditions, intelligent
  agents, especificación de asignaciones/rúbricas/libreta y el `.zip` de contenido.
- **Content clásico vs. New Content Experience (Lessons):** **POR-VERIFICAR** — el
  profesor no confirmó cuál usa el tenant de EAFIT. El manifest es idéntico en
  ambos casos (ver `mambrino-interactiva_assets/d2l-package.md` §"Unidades vs
  Módulos"); solo cambia si los módulos de primer nivel se leen "Módulos" o
  "Unidades". **Probar en sandbox antes de asumir uno u otro.**
- **Tópicos = visor con iframe, no redirect puro.** El profesor pidió embeber los
  slides directamente desde GitHub Pages en vez de solo rebotar a una pestaña
  nueva. Cada tópico es un `.html` que se **sube como archivo** a Course Files
  (Add Existing → Upload) — por eso puede llevar `<style>` completo, a diferencia
  del widget de homepage — con un iframe al sitio vivo y un enlace de respaldo
  ("Pantalla completa") para el caso de que el framing falle o el estudiante
  prefiera navegar el deck sin el chrome de D2L.
- **Sección de lecturas + podcast.** Cada módulo lleva un tópico de bibliografía
  que enlaza a `literatura/revision-literatura.html` (con anchor a su núcleo
  temático) y el módulo de orientación (`m00`) lleva además el podcast
  **"Proyectos sostenibles"** embebido en Spotify, con el iframe exacto que
  entregó el profesor (mismos atributos `allow`, para no perder
  autoplay/fullscreen/picture-in-picture). Título confirmado por el profesor
  (2026-08-22) en `datos.py` (`PODCAST`).

## Calificaciones y asignaciones nativas — verificadas contra un export real (2026-08-22)

Hasta la versión anterior, `assignments.md`/`rubrics.md`/`gradebook.md` eran solo
**especificación en texto** para transcribir a mano — no había evidencia empírica
del esquema exacto de `d2lgrades`/`d2ldropbox` para arriesgarse a fabricar el XML.

Esa evidencia ya existe: el profesor entregó un **export nativo real de su propio
tenant EAFIT** (curso "Semin. de Invest. Aplicada", ago-2026). De ahí se verificó:

- El esquema institucional **"Escala 0 a 5" tiene `identifier="347"`** — se usa
  literalmente ese valor en `grades_d2l.xml`, no un placeholder.
- La estructura real de `<grades>` (schemes/configuration/categories/items) y de
  `<dropbox>` (folder con instructions/date_due/grade_item).
- **El mecanismo de enlace real**: `item.category_id` ↔ `category.identifier`
  (dentro de `grades_d2l.xml`); `dropbox.folder.grade_item` ↔ `item.resource_code`
  (entre `dropbox_d2l.xml` y `grades_d2l.xml`). Sin este hallazgo, un buzón de
  entrega quedaría sin conectar a su casilla del libro de notas.
- `d2ldropbox` y `d2lgrades` **sí son `material_type` reales** que este tenant
  acepta — confirmado por el propio `imsmanifest.xml` del export.

Con esa base, `generar.py` ahora emite **`build/{semestre}_evaluacion.zip`**:
12 buzones de entrega (Dropbox) nativos + el libro de notas completo (5
categorías R1–R5, 12 ítems, pesos derivados de `ASIGNACIONES` — cero datos de
estudiantes) — ya no solo el `.md`. Va en un **zip separado** del contenido
("separar por riesgo"): si falla al importar, no afecta los módulos ya
importados. Grades y Dropbox sí van **juntos** entre sí, porque el cruce
`grade_item`/`resource_code` se resuelve en una sola pasada de importación,
igual que en el export real.

**Lo que sigue sin verificar empíricamente** (aun con el export real de referencia):
- El comportamiento exacto de `category_id`/`identifier` en una importación a un
  curso **nuevo** (el export que se revisó es de un curso ya existente, no una
  importación fresca) — de ahí que el gate de sandbox sea aún más estricto aquí.
- El significado exacto de `max_item_points` en el modo de distribución manual
  (`WeightDistributionType=0`) — se replicó el valor observado sin poder
  confirmar si el importador lo usa.
- La hora exacta de corte (`04:59:59` UTC = 23:59:59 Bogotá) — replicada del
  export real; verificar que el tenant no cambió de convención.

**Paso manual que el paquete no puede evitar:** Groups/Equipos no es
empaquetable (ninguna evidencia de un `material_type` para ello). Después de
importar, crear los equipos reales en Brightspace y asociar cada buzón marcado
"entrega grupal" (11 de 12) a su grupo — si no, cada estudiante entrega solo.

**Asignaciones — el visor ya no rompe con archivos binarios.** El tópico de
cada asignación en el zip de *contenido* dejó de ser un iframe genérico (que
mostraba en blanco o forzaba una descarga rota cuando el material de apoyo era
`modelo-financiero-PLANTILLA.xlsx`). Ahora es una ficha con fecha, categoría,
peso, rúbrica e instrucciones — con un botón "Abrir" (páginas del sitio) o
"Descargar" (binarios) según corresponda.

## Correcciones aplicadas sobre el estado heredado (2026-08-22)

Dos errores encontrados al verificar `datos.py`/`generar.py` antes de entregar:

- **Anchors de bibliografía rotos.** Apuntaban a `#nucleo-N-...`, pero Quarto
  genera los IDs con tilde (`#núcleo-N-...`) — verificado contra
  `_site/literatura/revision-literatura.html`. El enlace cargaba la página
  pero no hacía scroll a la sección (falla silenciosa). Corregido en las 6
  entradas de `BIBLIOGRAFIA_POR_MODULO`.
- **R1 sumaba 20% en vez de 25%.** `plantillas/04-rubricas.qmd` exige "cinco
  entregas, una por sesión" para R1, pero `ASIGNACIONES` solo tenía 4
  (S1–S4) — el total del curso daba 95%, no 100%. Se reclasificó
  `a10-nota-inversion` (S5) de "R4, peso 0%" a "R1, peso 5%": es el artefacto
  escrito de S5, igual que la ficha/modelo/flujo de las otras sesiones. `R4`
  sigue en 20% con solo `a11-defensa`. `validar()` ahora suma pesos por
  categoría y el total del curso, para que este error no pueda reaparecer
  en silencio.

## Cómo correr

```bash
cd interactiva
python3 generar.py            # todo: homepage + paquete + docs
python3 generar.py homepage   # solo build/homepage_widget.html
python3 generar.py paquete    # solo build/2026-2_contenido.zip
python3 generar.py evaluacion # solo build/2026-2_evaluacion.zip (buzones + libro de notas nativos)
python3 generar.py docs       # solo badges.md / release-conditions.md / intelligent-agents.md / assignments.md / rubrics.md / gradebook.md / manual-mantenimiento.md
```

`validar()` corre siempre primero (ids únicos, sitio https, fechas coherentes,
release conditions bien referenciadas, pesos de asignaciones cuadrando con cada
categoría y con el 100% del curso). Si falla, no se genera nada.

## ⛔ Orden obligatorio antes de tocar el curso real

1. **Publicar el sitio Quarto** (`quarto render` desde la raíz del repo + push).
   Los visores embeben el sitio vivo — si no está publicado, el iframe queda en
   blanco y da la impresión de que el paquete está roto.
2. **Importar el `.zip` en un SANDBOX**, nunca directo en el curso real — el
   esquema de D2L es propietario y no está documentado oficialmente.
3. Verificar visualmente: nomenclatura de módulos, que cada visor cargue el
   iframe correcto, que las fechas de "Esta semana" coincidan con el calendario
   corregido de `instructor/00-plan-de-registro.md`.
4. Recién ahí, importar al curso real. **Si algo salió mal y hay que
   reimportar: borrar lo anterior primero** — D2L no reconcilia, duplica.

## Qué incluye este paquete

| Pieza | Archivo | Estado |
|---|---|---|
| Homepage (hero + "Esta semana") | `build/homepage_widget.html` | Listo — pegar como Custom Widget |
| 6 módulos / 34 tópicos-visor (incl. bibliografía y podcast) | `build/2026-2_contenido.zip` | Listo — probar en sandbox |
| **12 buzones de entrega (Dropbox) nativos** | `build/2026-2_evaluacion.zip` | Listo — probar en sandbox (aparte del contenido) |
| **Libro de notas nativo** (5 categorías, 12 ítems, 0 datos de estudiantes) | `build/2026-2_evaluacion.zip` | Listo — mismo zip que los buzones |
| Badges (3, anclados a artefactos reales) | `build/badges.md` | Spec para configurar en Awards |
| Release conditions (cadena Tribunal→Taller) | `build/release-conditions.md` | Spec para configurar en Release Conditions |
| Intelligent agents (2, ligados a hitos reales) | `build/intelligent-agents.md` | Spec para configurar en Intelligent Agents |
| Manual de mantenimiento | `build/manual-mantenimiento.md` | Listo |
| Asignaciones — referencia legible de lo que trae el zip | `build/assignments.md` | Listo — ya no hay que transcribirlo a mano |
| Rúbricas R1–R5 (contenido de las celdas) | `build/rubrics.md` | Spec — crear en Rubrics y asociar a cada buzón |

## Qué NO incluye (y por qué)

- **Objetos nativos de rúbricas** (`d2lrubrics`) — sí hay evidencia real del
  esquema (ver export de referencia), pero escribir las 5 rúbricas completas
  (criterios, niveles, texto de cada celda) es un trabajo aparte; por ahora
  sigue como especificación en `build/rubrics.md`. Candidato claro para la
  próxima iteración, ya con el esquema verificado.
- **Cover del curso** (`d2lcourseimage`) — falta el PNG (~2400×960).
- **Homepage/navbar/tema del curso** — D2L no los expone en el `.zip` de
  importación de un curso (son nivel admin/plantilla). Este repo entrega el HTML
  del widget para pegarlo a mano en Course Admin → Homepages.
- **Badges / Release Conditions / Intelligent Agents como artefacto importable**
  — no existe un `material_type` empírico verificado para ninguno de los tres
  (ver `mambrino-interactiva_assets/d2l-package.md` §tabla ✅/❌). Se entregan
  como especificación exacta para configurar en la UI, generada desde la misma
  fuente de verdad para que nunca se desincronicen del plan del curso.

## Paleta y datos institucionales

Azul Zafre `#000066` / Azul Cielo `#00A9E0` — tomados de `slides/eafit.scss`
(Manual de Marca EAFIT v4.0), nunca inventados. Hechos institucionales (LMS,
Ley 1581/2012, calendario) en `mambrino_assets/eafit-contexto.md`. Cualquier
dato marcado POR-VERIFICAR en `datos.py` se declara así hasta que el profesor
lo confirme.
