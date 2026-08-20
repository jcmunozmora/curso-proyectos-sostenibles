#!/usr/bin/env python3
"""generar.py — emite homepage, tópicos-visor, manifest D2L y specs (badges,
release conditions, intelligent agents) desde datos.py — la única fuente de verdad.

Uso:
    python3 generar.py            # todo
    python3 generar.py homepage   # solo el widget de homepage
    python3 generar.py paquete    # solo el .zip de contenido
    python3 generar.py docs       # solo badges / release-conditions / agentes / manual

NUNCA editar la salida en build/ a mano: se sobreescribe en la siguiente corrida.
Mantenimiento semanal: tocar SEMANA_ACTUAL en datos.py y correr `python3 generar.py homepage`.

⛔ GATE: probar SIEMPRE el .zip en un sandbox antes del curso real. D2L no
reconcilia una segunda importación — la duplica.
"""
import sys
import zipfile
import html
from pathlib import Path
from xml.sax.saxutils import escape

from datos import (
    CURSO, PALETA, FUENTE, MODULOS, SEMANA_ACTUAL, ICONOS,
    CONTENT_EXPERIENCE, BADGES, RELEASE_CONDITIONS, INTELLIGENT_AGENTS,
)

OUT = Path(__file__).parent / "build"
OUT.mkdir(exist_ok=True)
SITIO = CURSO["sitio"].rstrip("/")


def url(path: str) -> str:
    return f"{SITIO}{path}"


TOPICOS_POR_ID = {t["id"]: t for m in MODULOS for t in m["topicos"]}
MODULOS_POR_ID = {m["id"]: m for m in MODULOS}


# ------------------------------------------------------------- 1. HOMEPAGE
# Widget de homepage → SOLO estilos inline (el sanitizador de Custom Widget
# y del editor HTML borra <style> y deja huérfana cualquier class="...").
def esta_semana() -> str:
    m = MODULOS[min(SEMANA_ACTUAL - 1, len(MODULOS) - 1)]
    lis = "".join(
        f'<li style="margin:.4rem 0;">{ICONOS.get(t["tipo"], "•")} '
        f'<a href="{url(t["link"])}" style="color:{PALETA["primario"]};">'
        f'{html.escape(t["titulo"])}</a>'
        + (f' — <em>entrega {t["entrega"]:%d %b}</em>' if t.get("entrega") else "")
        + "</li>"
        for t in m["topicos"]
    )
    return (
        f'<div style="border-left:5px solid {PALETA["acento"]};'
        f'background:{PALETA["fondo"]};padding:1rem 1.5rem;border-radius:8px;'
        f'font-family:{FUENTE};">'
        f'<strong style="color:{PALETA["primario"]};">Esta semana — '
        f'{html.escape(m["titulo"])}</strong>'
        f'<p style="margin:.5rem 0;color:{PALETA["texto"]};"><em>{html.escape(m["gancho"])}</em></p>'
        f'<ul style="margin:0;padding-left:1.2rem;">{lis}</ul></div>'
    )


def homepage() -> str:
    p = PALETA
    partes = [
        f'<div style="background:linear-gradient(135deg,{p["primario"]} 0%,{p["acento"]} 100%);'
        f'color:#fff;padding:3rem 2rem;border-radius:12px;margin-bottom:2rem;'
        f'font-family:{FUENTE};">',
        f'<small style="text-transform:uppercase;letter-spacing:.1em;opacity:.85;">'
        f'{html.escape(CURSO["codigo"])} · {CURSO["semestre"]}</small>',
        f'<h1 style="font-size:2.3rem;margin:.3rem 0 .5rem;font-weight:700;">'
        f'{html.escape(CURSO["nombre"])}</h1>',
        f'<p style="font-size:1.05rem;opacity:.92;margin:0 0 1.2rem;max-width:640px;">'
        f'{html.escape(CURSO["gancho"])}</p>',
        f'<p style="font-size:.95rem;line-height:1.6;max-width:640px;">'
        f'{html.escape(CURSO["mensaje"])}</p>',
        '<div style="margin-top:1.5rem;">',
        f'<a href="{url("/syllabus.html")}" style="background:#fff;color:{p["primario"]};'
        f'padding:.6rem 1.2rem;border-radius:6px;text-decoration:none;font-weight:600;'
        f'margin-right:.5rem;display:inline-block;margin-bottom:.5rem;">📋 Syllabus</a>',
        f'<a href="{url("/proyecto.html")}" style="background:rgba(255,255,255,.2);color:#fff;'
        f'padding:.6rem 1.2rem;border-radius:6px;text-decoration:none;font-weight:600;'
        f'border:1px solid #fff;margin-right:.5rem;display:inline-block;margin-bottom:.5rem;">'
        f'🌱 Proyecto ancla</a>',
        f'<a href="{SITIO}" style="background:rgba(255,255,255,.2);color:#fff;'
        f'padding:.6rem 1.2rem;border-radius:6px;text-decoration:none;font-weight:600;'
        f'border:1px solid #fff;display:inline-block;margin-bottom:.5rem;">🌐 Sitio del curso</a>',
        "</div></div>",
        esta_semana(),
    ]
    return "".join(partes)


# --------------------------------------------------- 2. TÓPICOS (visor iframe)
# Cada tópico se SUBE como archivo a Course Files (Add Existing → Upload), no se
# pega en un widget/editor → sobrevive <style> completo (regla de oro del
# sanitizador). Embebe el sitio vivo en un iframe; el enlace de respaldo cubre
# el caso de que el framing falle o el estudiante quiera pantalla completa.
VISOR = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{titulo_plano}</title>
<style>
  html, body {{ margin:0; padding:0; height:100%; font-family:{fuente}; }}
  .barra {{
    background:{primario}; color:#fff; padding:.7rem 1.2rem;
    display:flex; justify-content:space-between; align-items:center;
    font-size:.95rem; box-sizing:border-box;
  }}
  .barra a {{ color:#fff; text-decoration:none; border:1px solid rgba(255,255,255,.6);
    padding:.3rem .7rem; border-radius:6px; white-space:nowrap; margin-left:.5rem; }}
  .barra a:hover {{ background:rgba(255,255,255,.15); }}
  .titulo {{ font-weight:600; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
  iframe {{ width:100%; height:calc(100vh - 48px); border:0; display:block; }}
  .respaldo {{ padding:1rem 1.2rem; font-size:.9rem; color:{texto}; }}
</style>
</head>
<body>
  <div class="barra">
    <span class="titulo">{titulo}</span>
    <span>
      <a href="{destino}" target="_blank" rel="noopener">🔗 Pantalla completa</a>
    </span>
  </div>
  <iframe src="{destino}" title="{titulo_plano}" allowfullscreen loading="lazy"></iframe>
  <p class="respaldo">¿No carga? <a href="{destino}" target="_blank" rel="noopener">Abre {titulo_plano} directamente en el sitio del curso</a>.</p>
</body>
</html>"""


def escribir_visores(base: Path) -> dict:
    (base / "topicos").mkdir(parents=True, exist_ok=True)
    rutas = {}
    for m in MODULOS:
        for t in m["topicos"]:
            rel = f"topicos/{t['id']}.html"
            (base / rel).write_text(
                VISOR.format(
                    titulo=html.escape(t["titulo"]),
                    titulo_plano=html.escape(t["titulo"], quote=True),
                    destino=url(t["link"]),
                    primario=PALETA["primario"],
                    texto=PALETA["texto"],
                    fuente=FUENTE,
                ),
                encoding="utf-8",
            )
            rutas[t["id"]] = rel
    return rutas


# ------------------------------------------------------------- 3. MANIFEST
# Reglas duras (verificadas contra exports nativos, ver
# mambrino-interactiva_assets/d2l-package.md): sin <schema>; organizations
# default="d2l_orgs"; organization identifier="d2l_org" sin structure ni title;
# cada <item> con identifierref + d2l_2p0:id (entero global único, orden DFS) +
# completion_type="2"; módulo → resource contentmodule con href=""; tópico →
# resource content con href al .html bundleado; imsmanifest.xml en la RAÍZ del zip.
def manifest(rutas: dict, ou: str = "000000") -> str:
    items, resources = [], []
    d2l_id = 0
    for m in MODULOS:
        d2l_id += 1
        mid = d2l_id
        rm = f"RM_{m['id']}"
        hijos = []
        for t in m["topicos"]:
            d2l_id += 1
            rt = f"RT_{t['id']}"
            hijos.append(
                f'        <item identifier="I_{t["id"]}" identifierref="{rt}" '
                f'd2l_2p0:id="{d2l_id}" description="" completion_type="2">\n'
                f'          <title>{escape(t["titulo"])}</title>\n'
                f"        </item>"
            )
            resources.append(
                f'    <resource identifier="{rt}" type="webcontent" '
                f'd2l_2p0:material_type="content" d2l_2p0:link_target="" '
                f'href="{rutas[t["id"]]}" title="">\n'
                f'      <file href="{rutas[t["id"]]}" />\n    </resource>'
            )
        items.append(
            f'      <item identifier="I_{m["id"]}" identifierref="{rm}" '
            f'd2l_2p0:id="{mid}" description="" completion_type="2">\n'
            f'        <title>{escape(m["titulo"])}</title>\n'
            + "\n".join(hijos)
            + "\n      </item>"
        )
        resources.append(
            f'    <resource identifier="{rm}" type="webcontent" '
            f'd2l_2p0:material_type="contentmodule" d2l_2p0:link_target="" '
            f'href="" title="" />'
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="D2L_{ou}"
  xmlns:d2l_2p0="http://desire2learn.com/xsd/d2lcp_v2p0"
  xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_rootv1p2p1"
  xmlns="http://www.imsglobal.org/xsd/imscp_v1p1">
  <metadata>
    <imsmd:lom><imsmd:general>
      <imsmd:title><imsmd:langstring xml:lang="es-mx">{escape(CURSO["nombre"])}</imsmd:langstring></imsmd:title>
      <imsmd:language>es-mx</imsmd:language>
    </imsmd:general></imsmd:lom>
  </metadata>
  <organizations default="d2l_orgs">
    <organization identifier="d2l_org">
{chr(10).join(items)}
    </organization>
  </organizations>
  <resources>
{chr(10).join(resources)}
  </resources>
</manifest>
"""


# ------------------------------------------------------------- 4. EMPAQUETAR
def paquete():
    stage = OUT / "pkg"
    stage.mkdir(parents=True, exist_ok=True)
    rutas = escribir_visores(stage)
    (stage / "imsmanifest.xml").write_text(manifest(rutas), encoding="utf-8")
    zpath = OUT / f"{CURSO['semestre']}_contenido.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(stage.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(stage))  # manifest en la RAÍZ
    print(f"✅ {zpath}")
    print(f"   Formato Content/Lessons del tenant: {CONTENT_EXPERIENCE} — el manifest es el mismo; solo cambia el rótulo (Módulos vs Unidades).")
    print("⛔ GATE: importar primero en un SANDBOX. Importar dos veces DUPLICA todo.")
    print("⚠️  Publicar el sitio ANTES de importar, o los visores quedan en blanco (404 en el iframe).")
    print("   Rúbricas, libro de notas y cover NO están en este zip — ver interactiva/README.md.")


# --------------------------------------------------- 5. DOCS (specs de UI)
# Badges, Release Conditions e Intelligent Agents se configuran en la UI de D2L —
# no hay un material_type empírico para empaquetarlos (ver tabla ✅/❌ del asset).
# Estos documentos son la especificación exacta a transcribir a mano, generada
# desde la misma fuente de verdad para que nunca se desincronicen del curso real.
def doc_badges() -> str:
    filas = "\n".join(
        f"| **{b['nombre']}** | {b['gana_cuando']} | `{b['fuente']}` |" for b in BADGES
    )
    return (
        "# Badges — MF7011\n\n"
        "Configurar en Awards. Diseño visual: usar Azul Zafre "
        f"({PALETA['primario']}) como color base del ícono, coherente con `/eafit-style`.\n\n"
        "| Badge | Se gana cuando... | Fuente del criterio |\n|---|---|---|\n" + filas + "\n"
    )


def doc_release_conditions() -> str:
    filas = []
    for mod_id, req_topico_id, texto in RELEASE_CONDITIONS:
        mod = MODULOS_POR_ID[mod_id]
        filas.append(f"### {html.escape(mod['titulo'])}\n{texto}\n")
    return (
        "# Release Conditions — MF7011\n\n"
        "Configurar en Course Admin → Release Conditions, encadenando cada módulo "
        "al tópico Taller de la sesión anterior. No hay track opcional/bonus: el "
        "diseño del curso (ver `instructor/00-plan-de-registro.md`) no contempla uno; "
        "si se decide añadir, se declara aquí antes de configurarlo en D2L.\n\n"
        + "\n".join(filas)
    )


def doc_intelligent_agents() -> str:
    partes = ["# Intelligent Agents — MF7011\n"]
    for a in INTELLIGENT_AGENTS:
        partes.append(
            f"## {a['nombre']}\n\n"
            f"**Disparador:** {a['disparador']}\n\n"
            f"**Asunto:** {a['asunto']}\n\n"
            "**Cuerpo:**\n```\n" + a["cuerpo"] + "\n```\n"
        )
    partes.append(
        "> Los agentes solo tocan el merge field `{FirstName}` que ofrece D2L — "
        "ningún dato de estudiante pasa por este repo ni por un modelo de IA "
        "(Ley 1581/2012, ver `mambrino_assets/eafit-contexto.md` §6)."
    )
    return "\n".join(partes)


def doc_manual_mantenimiento() -> str:
    return f"""# Manual de mantenimiento — paquete de interactiva MF7011

## Actualizar "Esta semana" (1 minuto)
1. Abrir `datos.py`.
2. Cambiar `SEMANA_ACTUAL` al índice del módulo vigente (1 = orientación, 2 = S1, …).
3. Correr `python3 generar.py homepage`.
4. Pegar `build/homepage_widget.html` en el Custom Widget de la homepage
   (reemplaza el contenido completo — es un widget, solo estilos inline).

## Añadir o corregir un módulo/tópico
1. Editar la lista `MODULOS` en `datos.py` (nunca el HTML generado).
2. Correr `python3 generar.py` (regenera homepage + visores + manifest + docs).
3. Probar el `.zip` de `build/` en el **sandbox** antes de tocar el curso real.
4. Si el módulo ya estaba importado: borrarlo en D2L antes de reimportar
   (D2L no reconcilia — importar dos veces duplica).

## Checklist semanal (15 min)
- [ ] `SEMANA_ACTUAL` refleja la sesión que viene
- [ ] El sitio Quarto está publicado (`quarto render` + push) — los visores
      embeben el sitio vivo; si no está publicado, el iframe queda en blanco
- [ ] Ningún enlace nuevo aparece en `datos.py` sin su página real en el sitio

## Lo que este paquete NO incluye todavía
- **Rúbricas** (`d2lrubrics`) — cuando `plantillas/04-rubricas.qmd` esté cerrado
  y verificado con `/mambrino-assessment`.
- **Libro de notas** (`d2lgrades`, cero datos de estudiantes) — zip separado,
  por riesgo, cuando el esquema de categorías esté confirmado.
- **Cover del curso** (`d2lcourseimage`) — falta el PNG ~2400×960.
- **Homepage/navbar/tema** — no son empaquetables vía `.zip` de curso; se
  configuran a nivel de plantilla/admin. Este repo solo entrega el HTML del
  widget para pegar a mano.
- Badges, Release Conditions e Intelligent Agents — no tienen `material_type`
  empírico; se configuran en la UI siguiendo `build/badges.md`,
  `build/release-conditions.md` y `build/intelligent-agents.md`.

Color primario: `{PALETA['primario']}` (Azul Zafre) · secundario: `{PALETA['acento']}` (Azul Cielo).
Fuente única de verdad: `/eafit-style`. Nunca inventar un hex distinto aquí.
"""


def docs():
    (OUT / "badges.md").write_text(doc_badges(), encoding="utf-8")
    (OUT / "release-conditions.md").write_text(doc_release_conditions(), encoding="utf-8")
    (OUT / "intelligent-agents.md").write_text(doc_intelligent_agents(), encoding="utf-8")
    (OUT / "manual-mantenimiento.md").write_text(doc_manual_mantenimiento(), encoding="utf-8")
    print(f"✅ {OUT}/badges.md, release-conditions.md, intelligent-agents.md, manual-mantenimiento.md")


# --------------------------------------------------------------- VALIDAR
def validar():
    ids = [m["id"] for m in MODULOS] + [t["id"] for m in MODULOS for t in m["topicos"]]
    assert len(ids) == len(set(ids)), "ids duplicados en datos.py"
    assert SITIO.startswith("https://"), "el sitio debe ser https"
    for m in MODULOS:
        assert m["fechas"][0] <= m["fechas"][1], f"fechas invertidas en {m['id']}"
        assert m["topicos"], f"módulo sin tópicos: {m['id']}"
    for mod_id, req_id, _ in RELEASE_CONDITIONS:
        assert mod_id in MODULOS_POR_ID, f"release condition apunta a módulo inexistente: {mod_id}"
        if req_id:
            assert req_id in TOPICOS_POR_ID, f"release condition apunta a tópico inexistente: {req_id}"


if __name__ == "__main__":
    validar()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if cmd in ("todo", "homepage"):
        (OUT / "homepage_widget.html").write_text(homepage(), encoding="utf-8")
        print(f"✅ {OUT/'homepage_widget.html'} — pegar como Custom Widget (solo estilos inline)")
    if cmd in ("todo", "paquete"):
        paquete()
    if cmd in ("todo", "docs"):
        docs()
