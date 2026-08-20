# Paquete de interactiva — MF7011 (Brightspace/D2L)

Paquete completo de personalización del curso en Brightspace/D2L, generado desde
una única fuente de verdad (`datos.py`). Nunca editar los archivos de `build/` a
mano: se sobreescriben en cada corrida de `generar.py`.

## Decisiones tomadas en el diagnóstico (2026-08-20)

- **Nivel de control asumido:** Import/Export + widgets HTML (el profesor confirmó
  tener este nivel). Si resulta ser menor, los templates de tópico siguen sirviendo
  como HTML embebible; el `.zip` de importación requiere este nivel.
- **Alcance:** paquete completo — homepage, 6 módulos (orientación + S1–S5), 15
  tópicos, badges, release conditions, intelligent agents y el `.zip` de contenido.
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

## Cómo correr

```bash
cd interactiva
python3 generar.py            # todo: homepage + paquete + docs
python3 generar.py homepage   # solo build/homepage_widget.html
python3 generar.py paquete    # solo build/2026-2_contenido.zip
python3 generar.py docs       # solo badges.md / release-conditions.md / intelligent-agents.md / manual-mantenimiento.md
```

`validar()` corre siempre primero (ids únicos, sitio https, fechas coherentes,
release conditions bien referenciadas). Si falla, no se genera nada.

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
| 6 módulos / 15 tópicos-visor | `build/2026-2_contenido.zip` | Listo — probar en sandbox |
| Badges (3, anclados a artefactos reales) | `build/badges.md` | Spec para configurar en Awards |
| Release conditions (cadena Tribunal→Taller) | `build/release-conditions.md` | Spec para configurar en Release Conditions |
| Intelligent agents (2, ligados a hitos reales) | `build/intelligent-agents.md` | Spec para configurar en Intelligent Agents |
| Manual de mantenimiento | `build/manual-mantenimiento.md` | Listo |

## Qué NO incluye (y por qué)

- **Rúbricas** (`d2lrubrics`) — `plantillas/04-rubricas.qmd` existe pero no se
  confirmó como cerrado con `/mambrino-assessment`. Empaquetar rúbricas sin esa
  confirmación arriesga transcribir umbrales que luego cambian.
- **Libro de notas** (`d2lgrades`) — se entrega en un **zip separado** cuando el
  esquema de categorías/pesos esté confirmado (separar por riesgo: si ese zip
  falla al importar, no se lleva el contenido).
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
