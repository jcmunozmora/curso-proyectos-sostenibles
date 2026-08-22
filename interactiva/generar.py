#!/usr/bin/env python3
"""generar.py — emite homepage, tópicos-visor, manifest D2L y specs (badges,
release conditions, intelligent agents) desde datos.py — la única fuente de verdad.

Uso:
    python3 generar.py            # todo
    python3 generar.py homepage   # solo el widget de homepage
    python3 generar.py paquete    # solo el .zip de contenido
    python3 generar.py evaluacion # solo el .zip de calificaciones (d2lgrades + d2ldropbox nativos)
    python3 generar.py docs       # solo badges / release-conditions / agentes / manual

NUNCA editar la salida en build/ a mano: se sobreescribe en la siguiente corrida.
Mantenimiento semanal: tocar SEMANA_ACTUAL en datos.py y correr `python3 generar.py homepage`.

⛔ GATE: probar SIEMPRE el .zip en un sandbox antes del curso real. D2L no
reconcilia una segunda importación — la duplica.
"""
import sys
import zipfile
import html
import shutil
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

from datos import (
    CURSO, PALETA, FUENTE, MODULOS, SEMANA_ACTUAL, ICONOS,
    CONTENT_EXPERIENCE, BADGES, RELEASE_CONDITIONS, INTELLIGENT_AGENTS,
    ASIGNACIONES, CATEGORIAS_CALIFICACIONES, PODCAST,
)

OUT = Path(__file__).parent / "build"
OUT.mkdir(exist_ok=True)
SITIO = CURSO["sitio"].rstrip("/")


def url(path: str) -> str:
    # Recursos externos (p.ej. Spotify) ya son URL absoluta — no anteponer el sitio.
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{SITIO}{path}"


TOPICOS_POR_ID = {t["id"]: t for m in MODULOS for t in m["topicos"]}
MODULOS_POR_ID = {m["id"]: m for m in MODULOS}
ASIGNACIONES_POR_ID = {a["id"]: a for a in ASIGNACIONES}


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

# Tópico "podcast" — reproduce el iframe de Spotify tal como lo entregó el
# profesor (mismos atributos `allow`, sin los cuales el reproductor pierde
# autoplay/fullscreen/picture-in-picture). Se sube como archivo, igual que los
# demás visores, así que el <style> sobrevive el sanitizador.
PODCAST_VISOR = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{titulo_plano}</title>
<style>
  html, body {{ margin:0; padding:0; font-family:{fuente}; background:{fondo}; }}
  .barra {{ background:{primario}; color:#fff; padding:.7rem 1.2rem; font-weight:600; }}
  .contenedor {{ max-width:660px; margin:0 auto; padding:1.5rem 1.2rem; box-sizing:border-box; }}
  .nota {{ font-size:.9rem; color:{texto}; }}
  .nota a {{ color:{primario}; }}
</style>
</head>
<body>
  <div class="barra">{titulo}</div>
  <div class="contenedor">
    <p class="nota">{descripcion}</p>
    <iframe data-testid="embed-iframe" style="border-radius:12px" src="{embed_src}"
      width="100%" height="352" frameborder="0" allowfullscreen
      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
      loading="lazy"></iframe>
    <p class="nota">¿No carga? <a href="{show_url}" target="_blank" rel="noopener">Abre el podcast directamente en Spotify</a>.</p>
  </div>
</body>
</html>"""


# Tópico "asignación" — el "material de apoyo" de una ASIGNACIONES a veces es
# un .xlsx (modelo-financiero-PLANTILLA.xlsx): un iframe sobre un binario no
# renderiza nada útil (algunos navegadores lo descargan, otros lo dejan en
# blanco). En vez de un visor, esta plantilla muestra fecha/categoría/peso/
# rúbrica/instrucciones (ya en ASIGNACIONES, fuente única) y un enlace directo
# — "Abrir" si el material es una página del sitio, "Descargar" si es binario.
ASIGNACION_VISOR = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{titulo_plano}</title>
<style>
  body {{ margin:0; padding:0; font-family:{fuente}; background:{fondo}; color:{texto}; }}
  .barra {{ background:{primario}; color:#fff; padding:.9rem 1.2rem; font-weight:600; }}
  .contenedor {{ max-width:720px; margin:0 auto; padding:1.5rem 1.2rem; box-sizing:border-box; }}
  .ficha {{ display:grid; grid-template-columns:auto 1fr; gap:.3rem 1rem; font-size:.92rem; margin-bottom:1.2rem; }}
  .ficha dt {{ font-weight:600; color:{primario}; }}
  .ficha dd {{ margin:0; }}
  .instrucciones {{ background:#fff; border-left:5px solid {acento}; padding:1rem 1.2rem; border-radius:8px; line-height:1.6; white-space:pre-wrap; }}
  .boton {{ display:inline-block; margin-top:1.2rem; background:{primario}; color:#fff; text-decoration:none; padding:.6rem 1.2rem; border-radius:6px; font-weight:600; }}
</style>
</head>
<body>
  <div class="barra">{titulo}</div>
  <div class="contenedor">
    <dl class="ficha">
      <dt>Fecha de entrega</dt><dd>{fecha}</dd>
      <dt>Categoría</dt><dd>{categoria}</dd>
      <dt>Peso en el curso</dt><dd>{peso}%</dd>
      <dt>Modalidad</dt><dd>{modalidad}</dd>
      <dt>Rúbrica</dt><dd>{rubrica}</dd>
    </dl>
    <div class="instrucciones">{instrucciones}</div>
    <a class="boton" href="{destino}" target="_blank" rel="noopener">{etiqueta_boton}</a>
  </div>
</body>
</html>"""


def escribir_visores(base: Path) -> dict:
    (base / "topicos").mkdir(parents=True, exist_ok=True)
    rutas = {}
    for m in MODULOS:
        for t in m["topicos"]:
            rel = f"topicos/{t['id']}.html"
            if t["tipo"] == "podcast":
                contenido = PODCAST_VISOR.format(
                    titulo=html.escape(t["titulo"]),
                    titulo_plano=html.escape(t["titulo"], quote=True),
                    descripcion=html.escape(PODCAST["descripcion"]),
                    embed_src=PODCAST["spotify_embed_src"],
                    show_url=PODCAST["spotify_show_url"],
                    primario=PALETA["primario"],
                    texto=PALETA["texto"],
                    fondo=PALETA["fondo"],
                    fuente=FUENTE,
                )
            elif t["tipo"] == "asignacion":
                a = ASIGNACIONES_POR_ID[t["id"]]
                destino = url(a["entrega"])
                es_pagina = a["entrega"].endswith(".html")
                contenido = ASIGNACION_VISOR.format(
                    titulo=html.escape(t["titulo"]),
                    titulo_plano=html.escape(t["titulo"], quote=True),
                    fecha=a["fecha"],
                    categoria=html.escape(a["categoria"]),
                    peso=f'{a["peso"]:.2f}',
                    modalidad="Entrega grupal" if a["equipo"] else "Entrega individual",
                    rubrica=html.escape(a["rubrica"]),
                    instrucciones=html.escape(a["instrucciones"]),
                    destino=destino,
                    etiqueta_boton="📄 Abrir plantilla" if es_pagina else "⬇️ Descargar plantilla",
                    primario=PALETA["primario"],
                    acento=PALETA["acento"],
                    texto=PALETA["texto"],
                    fondo=PALETA["fondo"],
                    fuente=FUENTE,
                )
            else:
                contenido = VISOR.format(
                    titulo=html.escape(t["titulo"]),
                    titulo_plano=html.escape(t["titulo"], quote=True),
                    destino=url(t["link"]),
                    primario=PALETA["primario"],
                    texto=PALETA["texto"],
                    fuente=FUENTE,
                )
            (base / rel).write_text(contenido, encoding="utf-8")
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
    # El staging es completamente regenerable. Limpiarlo evita que un módulo
    # o tópico eliminado de datos.py sobreviva accidentalmente en el ZIP.
    if stage.exists():
        shutil.rmtree(stage)
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
    print("   Calificaciones y asignaciones nativas van en un zip aparte (ver paquete_evaluacion()). Rúbricas y cover siguen como spec en build/*.md.")


# --------------------------------------------- 4b. EVALUACIÓN (d2lgrades + d2ldropbox)
# Verificado contra un export NATIVO real del tenant de EAFIT (2026-08-22, curso
# "Semin. de Invest. Aplicada") — no contra documentación oficial de D2L (no la
# publica). De ese export: el esquema institucional "Escala 0 a 5" tiene
# identifier="347"; item.category_id enlaza con category.identifier (no con
# category.id); item.resource_code enlaza con dropbox.folder.grade_item — así
# es como un buzón de entrega queda ligado a su casilla del libro de notas.
ESCALA_0_A_5_IDENTIFIER = "347"


def _id_categoria(nombre_categoria: str) -> int:
    idx = [c for c, _ in CATEGORIAS_CALIFICACIONES].index(nombre_categoria)
    return 100_001 + idx


def _id_item(asignacion_id: str) -> int:
    return 200_001 + [a["id"] for a in ASIGNACIONES].index(asignacion_id)


def _resource_code(asignacion_id: str) -> str:
    return f"mf7011-{asignacion_id}"


def _fin_de_dia_utc(fecha_iso: str) -> str:
    # El export real de EAFIT guarda "23:59:59 hora Bogotá" como
    # "04:59:59 del día siguiente" en UTC (Bogotá = UTC-5). Se replica ese
    # mismo corrimiento para que la fecha mostrada en Brightspace sea la
    # correcta. Verificar en sandbox si el tenant cambia de convención.
    siguiente = date.fromisoformat(fecha_iso) + timedelta(days=1)
    return f"{siguiente.isoformat()}T04:59:59"


def grades_xml() -> str:
    categorias_xml = []
    for nombre, peso in CATEGORIAS_CALIFICACIONES:
        cid = _id_categoria(nombre)
        codigo_corto = nombre.split(" · ")[0].lower()
        categorias_xml.append(
            f'<category id="{cid}" identifier="{cid}" resource_code="{_resource_code("cat-" + codigo_corto)}">'
            f"<name>{escape(nombre)}</name><short_name>{escape(nombre.split(' · ')[0])}</short_name>"
            f"<sort_order>{cid}</sort_order><show_average>false</show_average>"
            f'<show_distribution>false</show_distribution><description text_type="text/html"><text/></description>'
            f"<is_active>true</is_active><scoring><weight>{peso:g}</weight>"
            f"<can_exceed_weight>false</can_exceed_weight><WeightDistributionType>0</WeightDistributionType>"
            f"<is_auto_pointed>false</is_auto_pointed><high_non_bonus_drop>0</high_non_bonus_drop>"
            f"<low_non_bonus_drop>0</low_non_bonus_drop><max_item_points>100</max_item_points>"
            f"<exclude_from_final_grade_calc>false</exclude_from_final_grade_calc></scoring></category>"
        )
    items_xml = []
    for a in ASIGNACIONES:
        cat_peso = dict(CATEGORIAS_CALIFICACIONES)[a["categoria"]]
        max_grade = round(100 * a["peso"] / cat_peso)
        items_xml.append(
            f'<item id="{_id_item(a["id"])}" identifier="{_id_item(a["id"])}" dates_in_calendar="false" '
            f'resource_code="{_resource_code(a["id"])}"><category_id>{_id_categoria(a["categoria"])}</category_id>'
            f"<name>{escape(a['nombre'])}</name><short_name/><sort_order>{_id_item(a['id'])}</sort_order>"
            f'<show_average>false</show_average><show_distribution>false</show_distribution>'
            f'<description text_type="text/html"><text/></description><type_id>1</type_id><is_active>true</is_active>'
            f"<scoring><can_exceed_weight>false</can_exceed_weight><out_of>5</out_of><is_bonus>false</is_bonus>"
            f"<max_grade>{max_grade}</max_grade><exclude_from_final_grade_calc>false</exclude_from_final_grade_calc>"
            f"<is_milestone_grade>false</is_milestone_grade></scoring></item>"
        )
    return (
        '<grades xmlns:d2l_2p0="http://desire2learn.com/xsd/d2lcp_v2p0">'
        f'<schemes default_scheme_identifier="{ESCALA_0_A_5_IDENTIFIER}">'
        f'<scheme identifier="{ESCALA_0_A_5_IDENTIFIER}" name="Escala 0 a 5" short_name="Escala 0 a 5" '
        'is_valid="true" is_org_scheme="true" /></schemes>'
        '<configuration><calculation_options auto_update_final_grade="1" grading_system="1" '
        'include_empty_grades_in_final="0" release_adjusted_grade="0" auto_release_final_grade="1" />'
        '<org_unit_display_options decimals_displayed="1" show_points="1" show_colour="1" show_symbol="1" '
        'show_weighted="0" decimals_displayed_my_grades="1" max_characters="50" show_final_grade_calc="1" />'
        "</configuration>"
        f"<categories>{''.join(categorias_xml)}</categories>"
        f"<items>{''.join(items_xml)}</items></grades>"
    )


def dropbox_xml() -> str:
    folders = []
    for i, a in enumerate(ASIGNACIONES, start=1):
        instrucciones_html = f"<p>{html.escape(a['instrucciones'])}</p>"
        folders.append(
            f'<folder name="{escape(a["nombre"])}" id="{300_000 + i}" submission_type="0" '
            f'completion_type="0" allowable_file_type="0" folder_type="2" sort_order="{i}" '
            f'out_of="5.000000000" grade_item="{_resource_code(a["id"])}" folder_is_retricted="false" '
            f'files_per_submission="0" submissions="2" ai_human_origin="0" '
            f'resource_code="{_resource_code("db-" + a["id"])}" is_hidden="false" is_anonymous="false">'
            f'<instructions text_type="text/html"><text>{instrucciones_html}</text></instructions>'
            f"<date_due>{_fin_de_dia_utc(a['fecha'])}</date_due>"
            f"</folder>"
        )
    return (
        '<dropbox xmlns:d2l_2p0="http://desire2learn.com/xsd/d2lcp_v2p0">'
        f"{''.join(folders)}</dropbox>"
    )


def manifest_evaluacion() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="D2L_000000_evaluacion"
  xmlns:d2l_2p0="http://desire2learn.com/xsd/d2lcp_v2p0"
  xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_rootv1p2p1"
  xmlns="http://www.imsglobal.org/xsd/imscp_v1p1">
  <metadata>
    <imsmd:lom><imsmd:general>
      <imsmd:title><imsmd:langstring xml:lang="es-mx">{escape(CURSO["nombre"])} — Evaluación</imsmd:langstring></imsmd:title>
      <imsmd:language>es-mx</imsmd:language>
    </imsmd:general></imsmd:lom>
  </metadata>
  <organizations default="d2l_orgs">
    <organization identifier="d2l_org">
    </organization>
  </organizations>
  <resources>
    <resource identifier="res_grades" type="webcontent" d2l_2p0:material_type="d2lgrades" d2l_2p0:link_target="" href="grades_d2l.xml" title="">
      <file href="grades_d2l.xml" />
    </resource>
    <resource identifier="res_dropbox" type="webcontent" d2l_2p0:material_type="d2ldropbox" d2l_2p0:link_target="" href="dropbox_d2l.xml" title="">
      <file href="dropbox_d2l.xml" />
    </resource>
  </resources>
</manifest>
"""


def paquete_evaluacion():
    # Separado del zip de contenido a propósito ("separar por riesgo"): si
    # este falla al importar, el contenido ya importado no se ve afectado.
    # Grades y Dropbox SÍ van juntos entre sí — el cruce grade_item↔resource_code
    # se resuelve en una sola pasada de importación, como en el export real.
    stage = OUT / "pkg_evaluacion"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)
    (stage / "grades_d2l.xml").write_text(grades_xml(), encoding="utf-8")
    (stage / "dropbox_d2l.xml").write_text(dropbox_xml(), encoding="utf-8")
    (stage / "imsmanifest.xml").write_text(manifest_evaluacion(), encoding="utf-8")
    zpath = OUT / f"{CURSO['semestre']}_evaluacion.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(stage.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(stage))
    print(f"✅ {zpath} — {len(ASIGNACIONES)} buzones de entrega + libro de notas (5 categorías, cero datos de estudiantes)")
    print("⛔ GATE: importar primero en un SANDBOX — el cruce grade_item/resource_code no se verificó contra un D2L en vivo, solo contra un export real.")
    print("   Después de importar: crear los Equipos (no empaquetable) y asociar cada buzón marcado 'equipo' a su grupo — ver build/assignments.md.")


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


def doc_asignaciones() -> str:
    partes = [
        "# Asignaciones — MF7011\n",
        "> Los 12 buzones (Dropbox) y el libro de notas (5 categorías, 12 ítems) ya "
        "vienen como objetos NATIVOS en `build/{semestre}_evaluacion.zip` — no hay "
        "que crearlos a mano. Esta tabla es la referencia de lo que ese zip trae, "
        "más lo que el zip NO puede traer.\n".format(semestre=CURSO["semestre"]),
        "\n**Paso manual obligatorio después de importar:** Groups/Equipos no es "
        "empaquetable (ver `mambrino-interactiva_assets/d2l-package.md`). Crear los "
        "equipos reales del curso en Brightspace y luego, en cada buzón marcado "
        "'entrega grupal' abajo, asociarlo al grupo correspondiente — si no, "
        "cada estudiante entrega por separado.\n",
        "\n**Reglas generales:** las entregas de equipo deben tener una sola entrega por grupo; la coevaluación es individual; toda cifra debe tener fuente verificable.\n",
    ]
    for a in ASIGNACIONES:
        partes.append(
            f"## {a['nombre']}\n\n"
            f"- **ID:** `{a['id']}`\n"
            f"- **Fecha de entrega:** {a['fecha']}\n"
            f"- **Categoría:** {a['categoria']}\n"
            f"- **Peso:** {a['peso']:.2f}% del curso\n"
            f"- **Rúbrica:** `{a['rubrica']}` · {'entrega grupal' if a['equipo'] else 'entrega individual'}\n"
            f"- **Material de apoyo:** `{a['entrega']}`\n\n"
            f"**Instrucciones para pegar en Brightspace**\n\n{a['instrucciones']}\n"
        )
    return "\n".join(partes)


def doc_rubricas() -> str:
    return """# Rúbricas — configuración en Brightspace

La fuente académica completa es `plantillas/04-rubricas.qmd`. En Brightspace crear cinco rúbricas con escala de 0 a 5 y asociarlas a las asignaciones indicadas en `assignments.md`.

| Rúbrica | Asignaciones | Escala | Nota clave |
|---|---|---:|---|
| R1 · Artefactos de sesión | a01, a03, a05, a07, a10 | 0–5 | Cinco entregas (una por sesión, S1–S5), 25% total; máximo 12/20 si se entrega fuera del salón salvo ausencia justificada. |
| R2 · Auditorías cruzadas | a02, a04, a06, a08 | 0–5 | Evalúa la calidad del hallazgo y su evidencia, no la calidad del modelo auditado. |
| R3 · Modelo financiero final | a09 | 0–5 | Supuestos, flujos, criterios, sensibilidad, riesgos y trazabilidad. |
| R4 · Defensa · Investor Day | a11 | 0–5 | La defensa combina 50% profesor y 50% mediana de evaluaciones válidas del comité. |
| R5 · Calidad como evaluador | a12 | 0–5 | Evidencia específica, discriminación entre proyectos, coherencia con el presupuesto y rol asignado. |

**Importante:** R4 y R5 incorporan cálculos externos al motor estándar de rúbricas: mediana del comité, umbral de tres evaluaciones válidas y modulador individual 0,85–1,15. Esos resultados deben cargarse como nota final por el profesor.
"""


def doc_gradebook() -> str:
    filas = [
        "# Libreta de calificaciones — MF7011\n",
        "Configurar la libreta en modo **ponderado**. Las categorías suman 100% y cada asignación usa su peso directamente sobre el curso. La escala de entrada recomendada es 0–5; Brightspace debe mostrar también el porcentaje.\n",
        "| Categoría | Peso | Ítems |\n|---|---:|---|",
    ]
    for categoria, peso in CATEGORIAS_CALIFICACIONES:
        items = ", ".join(a["nombre"] for a in ASIGNACIONES if a["categoria"] == categoria)
        filas.append(f"| {categoria} | {peso:.2f}% | {items} |")
    filas.extend([
        "\n## Ítems y pesos\n",
        "| ID | Ítem | Categoría | Peso curso | Entrega | Tipo |\n|---|---|---|---:|---|---|",
    ])
    for a in ASIGNACIONES:
        filas.append(
            f"| `{a['id']}` | {a['nombre']} | {a['categoria']} | {a['peso']:.2f}% | {a['fecha']} | {'Grupo' if a['equipo'] else 'Individual'} |"
        )
    filas.extend([
        "\n## Fórmula final",
        "",
        "`Nota final = Σ (nota del ítem en escala 0–5 × peso del ítem) / 5`.",
        "",
        "La nota de `a10-nota-inversion` es un artefacto de apoyo y tiene peso 0%; la calificación de R4 entra en `a11-defensa`. La nota de comité se registra en R4/R5 después de aplicar las salvaguardas descritas en `plantillas/06-coevaluacion-comite.qmd`.",
        "",
        "> No importar calificaciones de estudiantes desde este repositorio. Crear los ítems vacíos primero y cargar resultados únicamente desde Brightspace, respetando la Ley 1581/2012.",
    ])
    return "\n".join(filas) + "\n"


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
    (OUT / "assignments.md").write_text(doc_asignaciones(), encoding="utf-8")
    (OUT / "rubrics.md").write_text(doc_rubricas(), encoding="utf-8")
    (OUT / "gradebook.md").write_text(doc_gradebook(), encoding="utf-8")
    (OUT / "manual-mantenimiento.md").write_text(doc_manual_mantenimiento(), encoding="utf-8")
    print(f"✅ {OUT}/badges.md, release-conditions.md, intelligent-agents.md, assignments.md, rubrics.md, gradebook.md, manual-mantenimiento.md")


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
    # Los pesos de ASIGNACIONES deben sumar exactamente el peso de su categoría,
    # y las categorías deben sumar 100% del curso. Detecta en segundos lo que
    # a mano se descubre semanas después (ver a10-nota-inversion, jul-2026).
    from collections import defaultdict
    sumas = defaultdict(float)
    for a in ASIGNACIONES:
        sumas[a["categoria"]] += a["peso"]
    for categoria, peso in CATEGORIAS_CALIFICACIONES:
        assert abs(sumas[categoria] - peso) < 1e-6, (
            f"{categoria}: las asignaciones suman {sumas[categoria]}%, "
            f"la categoría declara {peso}%"
        )
    total = sum(peso for _, peso in CATEGORIAS_CALIFICACIONES)
    assert abs(total - 100.0) < 1e-6, f"las categorías suman {total}%, no 100%"


if __name__ == "__main__":
    validar()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if cmd in ("todo", "homepage"):
        (OUT / "homepage_widget.html").write_text(homepage(), encoding="utf-8")
        print(f"✅ {OUT/'homepage_widget.html'} — pegar como Custom Widget (solo estilos inline)")
    if cmd in ("todo", "paquete"):
        paquete()
    if cmd in ("todo", "evaluacion"):
        paquete_evaluacion()
    if cmd in ("todo", "docs"):
        docs()
