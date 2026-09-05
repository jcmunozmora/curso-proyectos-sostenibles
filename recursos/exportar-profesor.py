#!/usr/bin/env python3
"""
Paquete del profesor — MF7011
================================

Genera, para la sesión N, TODO el material de clase del profesor en
    instructor/pdf/SN/
(carpeta local, ignorada por git: el repo es público y este material
contiene las notas del presentador y los reveals).

Archivos producidos
-------------------
  SN_<Deck>_slides.pdf             los slides tal como se proyectan (sin notas), 1 página por slide
  SN_<Deck>_Notas_por_slide.pdf    A4 horizontal, una página por slide: miniatura + notas + rayas
                                   para anotar a mano. Las notas salen de dos fuentes:
                                     (a) los bloques `::: {.notes}` del .qmd del deck
                                     (b) instructor/notas-slides/sN-<deck>.md  (guion extendido, opcional)
                                   Si existe instructor/notas-slides/sN-glosario.md, va al inicio.
  SN_Plan_de_sesion.pdf            instructor/planes-sesion/sN.md
  SN_<Guia>.pdf                    cada instructor/*-sN.md (p. ej. 04-guia-formulas-s3.md)

Uso
---
  python3 recursos/exportar-profesor.py 3                # sesión 3, todo
  python3 recursos/exportar-profesor.py 3 --sin-render   # reutiliza _site/ (ya renderizado con notas)
  python3 recursos/exportar-profesor.py 3 --solo notas   # slides | notas | docs (separados por coma)
  python3 recursos/exportar-profesor.py 3 --abrir        # abre la carpeta al terminar

Requisitos (todos ya presentes en el Mac Studio)
------------------------------------------------
  quarto ≥ 1.7 (trae typst)  ·  Google Chrome (o el Chromium de Playwright)
  python3 con: playwright, pymupdf        (pip install playwright pymupdf)

Nunca escribe fuera de instructor/pdf/SN/ (y un directorio temporal).
"""
from __future__ import annotations

import argparse
import datetime as dt
import html as htmlmod
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AZUL = "#000066"
CIELO = "#00A9E0"


def log(msg: str) -> None:
    print(f"  {msg}", flush=True)


def fallo(msg: str) -> None:
    print(f"\n✗ {msg}", file=sys.stderr)
    sys.exit(1)


# ───────────────────────────── utilidades ─────────────────────────────

def norm(s: str) -> str:
    """Clave de comparación: sin acentos, sin puntuación, minúsculas."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def esc(s: str) -> str:
    """Texto markdown-ish → markup Typst. Conserva **negrita** (→ *negrita*) y `código`."""
    s = s.replace("\\", "\\\\")
    for ch in "#$_@<>~*[]":
        s = s.replace(ch, "\\" + ch)
    s = s.replace("//", "\\/\\/")
    s = re.sub(r"\\\*\\\*(.+?)\\\*\\\*", r"*\1*", s)
    return s


def esc_lineas(texto: str) -> str:
    """Bloque de texto (párrafos y viñetas '- ') → markup Typst."""
    out = []
    for ln in texto.strip("\n").split("\n"):
        ln = ln.rstrip()
        if ln.startswith("- "):
            out.append("- " + esc(ln[2:]))
        elif ln.startswith(("* ", "• ")):
            out.append("- " + esc(ln[2:]))
        elif ln == "":
            out.append("")
        else:
            t = esc(ln)
            if t.startswith(("= ", "+ ", "/ ")):
                t = "\\" + t
            out.append(t)
    return "\n".join(out)


def quarto(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k != "QUARTO_PROFILE"}
    env["PATH"] = "/opt/homebrew/bin:/Applications/quarto/bin:" + env.get("PATH", "")
    return subprocess.run(["quarto", *args], cwd=cwd, env=env, capture_output=True, text=True)


# ───────────────────────────── 1. slides ─────────────────────────────

class _Parser(HTMLParser):
    """Extrae del HTML RevealJS renderizado: slides de primer nivel, su título,
    su primera línea de texto (clave para slides sin título) y sus notas."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.slides: list[dict] = []
        self.doc_title = ""
        self.doc_subtitle = ""
        self._depth = 0          # anidamiento de <section>
        self._cur: dict | None = None
        self._in_h2 = False
        self._in_notes = False
        self._notes_stack: list[str] = []
        self._notes_parts: list[str] = []
        self._li_prefix: list[str] = []
        self._grab: str | None = None   # "title" | "subtitle"
        self._skip = 0                  # dentro de <script>/<style>

    # helpers
    def _attr(self, attrs, name):
        for k, v in attrs:
            if k == name:
                return v or ""
        return ""

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
            return
        if tag == "section":
            self._depth += 1
            if self._depth == 1:
                self._cur = {"id": self._attr(attrs, "id"), "h2": "", "first": "",
                             "notes": "", "title_slide": self._attr(attrs, "id") == "title-slide"}
                self.slides.append(self._cur)
            return
        if self._cur is None:
            return
        cls = self._attr(attrs, "class")
        if tag == "h2" and not self._in_notes:
            self._in_h2 = True
        elif tag == "h1" and "title" in cls.split():
            self._grab = "title"
        elif tag == "p" and "subtitle" in cls.split():
            self._grab = "subtitle"
        elif tag == "aside" and "notes" in cls.split():
            self._in_notes = True
            self._notes_parts = []
        elif self._in_notes:
            if tag == "p":
                self._notes_parts.append("\n\n")
            elif tag in ("ul", "ol"):
                self._li_prefix.append("- " if tag == "ul" else "1. ")
                self._notes_parts.append("\n")
            elif tag == "li":
                self._notes_parts.append("\n" + (self._li_prefix[-1] if self._li_prefix else "- "))
            elif tag == "br":
                self._notes_parts.append("\n")
            elif tag in ("strong", "b"):
                self._notes_parts.append("**")
            elif tag in ("em", "i"):
                self._notes_parts.append("*")
            elif tag == "code":
                self._notes_parts.append("`")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
            return
        if tag == "section":
            if self._depth == 1:
                self._cur = None
            self._depth -= 1
            return
        if self._cur is None:
            return
        if tag == "h2":
            self._in_h2 = False
        elif tag in ("h1", "p") and self._grab:
            self._grab = None
        elif tag == "aside" and self._in_notes:
            self._in_notes = False
            txt = "".join(self._notes_parts)
            txt = re.sub(r"[ \t]+\n", "\n", txt)
            txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
            self._cur["notes"] = (self._cur["notes"] + "\n\n" + txt).strip()
        elif self._in_notes:
            if tag in ("ul", "ol") and self._li_prefix:
                self._li_prefix.pop()
                self._notes_parts.append("\n")
            elif tag in ("strong", "b"):
                self._notes_parts.append("**")
            elif tag in ("em", "i"):
                self._notes_parts.append("*")
            elif tag == "code":
                self._notes_parts.append("`")

    def handle_data(self, data):
        if self._skip or self._cur is None:
            return
        if self._grab == "title":
            self.doc_title += data
        elif self._grab == "subtitle":
            self.doc_subtitle += data
        if self._in_notes:
            self._notes_parts.append(re.sub(r"\s+", " ", data))
            return
        if self._in_h2:
            self._cur["h2"] += data
        elif not self._cur["first"] and data.strip():
            self._cur["first"] = data.strip()


def parse_deck(html_path: Path) -> dict:
    p = _Parser()
    p.feed(html_path.read_text(encoding="utf-8"))
    slides = []
    for i, s in enumerate(p.slides, 1):
        if s["title_slide"]:
            title, key = p.doc_title.strip() or "Portada", "Portada"
        else:
            h2 = re.sub(r"\s+", " ", s["h2"]).strip()
            key = h2 or re.sub(r"\s+", " ", s["first"])[:60].strip() or f"Slide {i}"
            title = key
        notes = s["notes"]
        m = re.match(r"^MIN\s+([0-9][0-9:–\-\s]*[0-9])\.?\s*", notes)
        minuto = f"MIN {m.group(1)}" if m else ""
        slides.append({"n": i, "title": title, "key": key, "notes": notes, "minuto": minuto})
    return {"title": p.doc_title.strip(), "subtitle": re.sub(r"\s+", " ", p.doc_subtitle).strip(),
            "slides": slides}


JS_DESBORDE = """() => Array.from(document.querySelectorAll('.reveal .slides .pdf-page')).map((p, i) => {
  const pr = p.getBoundingClientRect();
  const sec = p.querySelector('section');
  let bottom = 0;
  if (sec) for (const e of sec.querySelectorAll('*')) { const r = e.getBoundingClientRect(); if (r.height > 0) bottom = Math.max(bottom, r.bottom); }
  return [i + 1, Math.round(bottom - pr.bottom), ((p.querySelector('h2') || {}).textContent || '').trim().slice(0, 60)];
}).filter(r => r[1] > 6)"""


def imprimir_slides(html_path: Path, pdf_out: Path) -> tuple[int, list]:
    """Imprime el deck RevealJS (modo ?print-pdf) con Chrome: una página por slide,
    recortando lo que no cabe en pantalla (igual que al proyectar).
    Devuelve (nº de páginas, [(nº slide, px que desbordan, título), …])."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        fallo("falta playwright:  pip install playwright && playwright install chromium")
    url = html_path.resolve().as_uri() + "?print-pdf"
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome")
        except Exception:
            browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(url, wait_until="load")
        page.wait_for_selector(".reveal.ready", timeout=60000)
        page.wait_for_timeout(2500)          # MathJax / fuentes
        desbordes = page.evaluate(JS_DESBORDE)
        # sin esto Chrome parte en dos páginas cualquier slide con contenido más alto que la pantalla
        page.add_style_tag(content=".reveal .slides .pdf-page{overflow:hidden !important}")
        page.wait_for_timeout(300)
        page.pdf(path=str(pdf_out), prefer_css_page_size=True, print_background=True)
        page.close()
        browser.close()
    import fitz  # pymupdf
    with fitz.open(pdf_out) as doc:
        return doc.page_count, desbordes


def miniaturas(pdf: Path, destino: Path, prefijo: str, dpi: int = 96) -> list[Path]:
    import fitz
    out = []
    with fitz.open(pdf) as doc:
        for i, pg in enumerate(doc, 1):
            f = destino / f"{prefijo}-{i:02d}.png"
            pg.get_pixmap(dpi=dpi).save(str(f))
            out.append(f)
    return out


# ───────────────────────────── 2. notas extendidas ─────────────────────────────

def cargar_notas_ext(path: Path) -> list[dict]:
    """instructor/notas-slides/sN-<deck>.md →
       [{key, num, minuto, bloques:[(etiqueta, texto)]}] en orden de aparición."""
    secs: list[dict] = []
    cur = None
    blk = None
    texto = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    for ln in texto.splitlines():
        if ln.startswith("## "):
            h = ln[3:].strip()
            attrs = ""
            m = re.search(r"\{([^}]*)\}\s*$", h)
            if m:
                attrs, h = m.group(1), h[: m.start()].strip()
            num = None
            mm = re.match(r"^(\d+)\s*·\s*(.*)$", h)
            if mm:
                num, h = int(mm.group(1)), mm.group(2).strip()
            mn = re.search(r'min="([^"]*)"', attrs)
            cur = {"key": h, "num": num, "minuto": mn.group(1) if mn else "", "bloques": [], "match": None}
            secs.append(cur)
            blk = None
        elif ln.startswith("### ") and cur is not None:
            blk = [ln[4:].strip(), []]
            cur["bloques"].append(blk)
        elif cur is not None:
            if blk is None:
                if not ln.strip():
                    continue
                blk = ["Notas", []]
                cur["bloques"].append(blk)
            blk[1].append(ln)
    for s in secs:
        s["bloques"] = [(e, "\n".join(t).strip("\n")) for e, t in s["bloques"] if "".join(t).strip()]
    return secs


def casar_notas(slides: list[dict], ext: list[dict]) -> list[str]:
    """Asigna cada sección del .md a un slide: por título (normalizado) y, si no, por número."""
    avisos = []
    libres = {s["n"] for s in slides}
    for sec in ext:
        k = norm(sec["key"])
        hit = next((s for s in slides if s["n"] in libres and norm(s["key"]) == k), None)
        if hit is None and sec["num"] and sec["num"] in libres:
            hit = slides[sec["num"] - 1]
            avisos.append(f"'{sec['key']}' no coincide con ningún título; usado el nº {sec['num']} "
                          f"(«{hit['title']}»)")
        if hit is None:
            avisos.append(f"HUÉRFANA: '{sec['key']}' no coincide con ningún slide (¿se renombró?)")
            continue
        libres.discard(hit["n"])
        hit["ext"] = sec
        sec["match"] = hit["n"]
    return avisos


def cargar_glosario(path: Path) -> list[tuple]:
    """Tabla markdown de 4 columnas. Fila con solo la 1ª celda = encabezado de grupo."""
    filas = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        if not ln.strip().startswith("|"):
            continue
        celdas = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c or "--") for c in celdas):
            continue                                   # separador |---|---|
        celdas = [re.sub(r"^\*\*(.*)\*\*$", r"\1", c) for c in celdas]
        if not filas and norm(celdas[0]) in ("termino", "concepto"):
            continue                                   # encabezado de columnas
        if len(celdas) >= 2 and not any(celdas[1:]):
            filas.append((celdas[0],))
        else:
            filas.append(tuple((celdas + ["", "", ""])[:4]))
    return filas


# ───────────────────────────── 3. Typst: notas por slide ─────────────────────────────

TYP_HEAD = '''#set page(paper: "a4", flipped: true, margin: (x: 11mm, top: 9mm, bottom: 8mm),
  footer: context [#set text(size: 7pt, fill: luma(120)); {pie} #h(1fr) #counter(page).display()])
#set text(size: 8.4pt, lang: "es", font: ("Inter", "Helvetica Neue", "Libertinus Serif"))
#set par(leading: 0.55em)
#set list(indent: 0.6em, body-indent: 0.4em, spacing: 0.45em)
#let rayas(n) = for i in range(n) {{ v(6.2mm); line(length: 100%, stroke: 0.4pt + luma(175)) }}
#let etiqueta(t) = text(fill: rgb("{azul}"), weight: "bold", size: 8.3pt, upper(t))
#let pagina(num, total, titulo, minuto, img, notas) = [
  #block(width: 100%, inset: (bottom: 1.5mm), stroke: (bottom: 0.9pt + rgb("{azul}")))[
    #text(size: 11pt, weight: "bold", fill: rgb("{azul}"))[#titulo]
    #h(1fr)
    #text(size: 9pt, weight: "bold", fill: rgb("{cielo}"))[#minuto]
    #h(8pt)
    #text(size: 8pt, fill: luma(120))[slide #num / #total]
  ]
  #v(2mm)
  #grid(columns: (55%, 45%), column-gutter: 5mm,
    [
      #box(stroke: 0.5pt + luma(140), image(img, width: 100%))
      #v(1.5mm)
      #text(size: 7pt, fill: luma(120))[Notas a mano]
      #rayas(8)
    ],
    [#notas]
  )
]
'''


def typ_glosario(filas: list[tuple]) -> str:
    rows = []
    for e in filas:
        if len(e) == 1:
            rows.append(f'table.cell(colspan: 4, fill: rgb("{CIELO}"))[#text(fill: white, weight: "bold")[{esc(e[0])}]]')
        else:
            rows.append(f"[*{esc(e[0])}*], [{esc(e[1])}], [{esc(e[2])}], [{esc(e[3])}]")
    body = ",\n  ".join(rows)
    return f'''#block(width: 100%, inset: (bottom: 1.5mm), stroke: (bottom: 0.9pt + rgb("{AZUL}")))[
  #text(size: 11pt, weight: "bold", fill: rgb("{AZUL}"))[Glosario · definición, fórmula y valor en el proyecto]
  #h(1fr) #text(size: 8pt, fill: luma(120))[consúltalo desde cualquier slide]
]
#v(2mm)
#set text(size: 7.6pt)
#table(columns: (17%, 36%, 22%, 25%), stroke: 0.3pt + luma(170), inset: 3pt, align: left,
  fill: (x, y) => if y == 0 {{ rgb("{AZUL}") }} else if calc.odd(y) {{ luma(247) }} else {{ white }},
  table.header([#text(fill: white, weight: "bold")[Término]], [#text(fill: white, weight: "bold")[Qué es]],
               [#text(fill: white, weight: "bold")[Fórmula]], [#text(fill: white, weight: "bold")[En este proyecto]]),
  {body}
)
#set text(size: 8.4pt)
#pagebreak()
'''


def typ_notas_slide(s: dict) -> str:
    partes = []
    ext = s.get("ext")
    if ext:
        for etiqueta, texto in ext["bloques"]:
            partes.append(f"#etiqueta[{esc(etiqueta)}]\n\n{esc_lineas(texto)}\n")
    if s["notes"]:
        partes.append(f"#etiqueta[Notas en el deck]\n\n{esc_lineas(s['notes'])}\n")
    if not partes:
        return "#text(fill: luma(140))[Sin notas para este slide.]"
    return "\n".join(partes)


def construir_notas(deck: dict, pngs: list[Path], pie: str, glosario: list[tuple] | None,
                    typ_path: Path) -> None:
    doc = TYP_HEAD.format(pie=esc(pie), azul=AZUL, cielo=CIELO)
    if glosario:
        doc += typ_glosario(glosario)
    total = len(deck["slides"])
    for s, png in zip(deck["slides"], pngs):
        minuto = (s.get("ext") or {}).get("minuto") or s["minuto"]
        doc += (f'#pagina({s["n"]}, {total}, [{esc(s["title"])}], [{esc(minuto)}], '
                f'"{png.name}", [\n{typ_notas_slide(s)}\n])\n')
        if s["n"] < total:
            doc += "#pagebreak()\n"
    typ_path.write_text(doc, encoding="utf-8")


def compilar_typst(typ_path: Path, pdf_out: Path) -> None:
    r = quarto("typst", "compile", typ_path.name, pdf_out.name, cwd=typ_path.parent)
    if r.returncode != 0:
        fallo(f"typst falló en {typ_path.name}:\n{r.stderr[-3000:]}")
    shutil.move(str(typ_path.parent / pdf_out.name), str(pdf_out))


# ───────────────────────────── 4. documentos (.md → PDF) ─────────────────────────────

CALLOUTS = {
    "aviso": '::: {.callout-warning}',
    "importante": '::: {.callout-important}',
    "error-fatal": '::: {.callout-important title="Error fatal"}',
    "guion": '::: {.callout-tip title="Guion"}',
    "nota": '::: {.callout-note}',
}


def md_a_pdf(md: Path, pdf_out: Path, subtitulo: str, tmp: Path) -> None:
    texto = md.read_text(encoding="utf-8")
    m = re.match(r"^# (.+)\n", texto)
    titulo = m.group(1).strip() if m else md.stem
    if m:
        texto = texto[m.end():]
    for nombre, repl in CALLOUTS.items():
        texto = re.sub(rf"^::: *{nombre} *$", repl, texto, flags=re.M)
    hdr = (f'---\ntitle: "{titulo.replace(chr(34), chr(39))}"\nsubtitle: "{subtitulo}"\nlang: es\n'
           "format:\n  typst:\n    papersize: a4\n    margin: {x: 2cm, y: 2cm}\n    fontsize: 10pt\n"
           "    toc: true\n    toc-depth: 2\n    number-sections: false\n---\n\n")
    qmd = tmp / (md.stem + ".qmd")
    qmd.write_text(hdr + texto, encoding="utf-8")
    r = quarto("render", qmd.name, "--to", "typst", cwd=tmp)
    pdf = tmp / (md.stem + ".pdf")
    if r.returncode != 0 or not pdf.exists():
        fallo(f"quarto render falló en {md.name}:\n{(r.stderr or r.stdout)[-3000:]}")
    shutil.move(str(pdf), str(pdf_out))


# ───────────────────────────── main ─────────────────────────────

def nombre_deck(stem: str, n: int) -> str:
    """s03-viernes → Viernes · s05-investor-day → Investor_day"""
    base = re.sub(rf"^s0?{n}[-_]", "", stem)
    return base.replace("-", "_").capitalize()


def nombre_doc(stem: str, n: int) -> str:
    """04-guia-formulas-s3 → Guia_formulas"""
    base = re.sub(r"^\d+[-_]", "", stem)
    base = re.sub(rf"[-_]s0?{n}$", "", base)
    return base.replace("-", "_").capitalize()


def main() -> None:
    ap = argparse.ArgumentParser(description="Paquete del profesor MF7011 → instructor/pdf/SN/")
    ap.add_argument("sesion", type=int, help="número de sesión (1–5)")
    ap.add_argument("--sin-render", action="store_true", help="no re-renderizar los decks (usa _site/)")
    ap.add_argument("--solo", default="slides,notas,docs", help="slides,notas,docs (coma)")
    ap.add_argument("--abrir", action="store_true", help="abrir la carpeta al terminar (macOS)")
    a = ap.parse_args()
    n = a.sesion
    partes = {p.strip() for p in a.solo.split(",")}
    hoy = dt.date.today().strftime("%-d-%b-%Y").lower()

    sdir = RAIZ / "slides" / f"s{n:02d}"
    if not sdir.is_dir():
        fallo(f"no existe {sdir}")
    out = RAIZ / "instructor" / "pdf" / f"S{n}"
    out.mkdir(parents=True, exist_ok=True)
    notas_dir = RAIZ / "instructor" / "notas-slides"
    tmp = Path(tempfile.mkdtemp(prefix=f"mf7011-S{n}-"))
    print(f"\nPaquete del profesor · Sesión {n} → {out.relative_to(RAIZ)}/   (temp: {tmp})")

    glos = notas_dir / f"s{n}-glosario.md"
    glosario = cargar_glosario(glos) if glos.exists() else None
    if glosario:
        log(f"glosario: {glos.relative_to(RAIZ)} ({sum(1 for f in glosario if len(f) > 1)} términos)")

    # ── slides + notas, deck por deck ──
    if partes & {"slides", "notas"}:
        for qmd in sorted(sdir.glob("*.qmd")):
            etiqueta = nombre_deck(qmd.stem, n)
            html = RAIZ / "_site" / "slides" / qmd.parent.name / (qmd.stem + ".html")
            print(f"\n▸ {qmd.stem}  ({etiqueta})")
            if not a.sin_render:
                log("quarto render (con notas)…")
                r = quarto("render", str(qmd.relative_to(RAIZ)), cwd=RAIZ)
                if r.returncode != 0:
                    fallo(f"quarto render falló:\n{(r.stderr or r.stdout)[-3000:]}")
            if not html.exists():
                fallo(f"no existe {html} — corre sin --sin-render")
            n_notes_qmd = len(re.findall(r"^::: *\{\.notes\}", qmd.read_text(encoding="utf-8"), re.M))
            n_notes_html = html.read_text(encoding="utf-8").count('<aside class="notes">')
            if n_notes_qmd and not n_notes_html:
                fallo(f"{html.name} no tiene notas del presentador: fue renderizado con "
                      "--profile publico. Vuelve a correr sin --sin-render.")
            deck = parse_deck(html)
            log(f"{len(deck['slides'])} slides · {n_notes_html} con notas en el deck")

            pdf_slides = out / f"S{n}_{etiqueta}_slides.pdf"
            slides_existia = pdf_slides.exists()
            log("imprimiendo con Chrome…")
            paginas, desbordes = imprimir_slides(html, pdf_slides)
            for i, px, t in desbordes:
                log(f"⚠ slide {i} «{t or deck['slides'][i-1]['title']}» no cabe en pantalla "
                    f"(sobran ~{px} px): recortado en el PDF, revisar en el deck")
            if paginas != len(deck["slides"]):
                log(f"⚠ el PDF tiene {paginas} páginas y el HTML {len(deck['slides'])} slides; "
                    "las notas se emparejan por posición hasta donde alcance")
            log(f"✓ {pdf_slides.name} ({paginas} págs.)")

            if "notas" in partes:
                pngs = miniaturas(pdf_slides, tmp, qmd.stem)
                ext_path = notas_dir / f"s{n}-{re.sub(rf'^s0?{n}[-_]', '', qmd.stem)}.md"
                if ext_path.exists():
                    ext = cargar_notas_ext(ext_path)
                    for av in casar_notas(deck["slides"], ext):
                        log(f"⚠ {av}")
                    con = sum(1 for s in deck["slides"] if s.get("ext"))
                    log(f"guion extendido: {ext_path.relative_to(RAIZ)} → {con}/{len(deck['slides'])} slides")
                else:
                    log(f"sin guion extendido (opcional): {ext_path.relative_to(RAIZ)}")
                sin = [s["title"] for s in deck["slides"] if not s.get("ext") and not s["notes"]]
                if sin:
                    log(f"slides sin ninguna nota ({len(sin)}): " + " · ".join(sin)[:300])
                sub = deck["subtitle"] or etiqueta
                sub = sub if sub.lower().startswith("sesión") else f"Sesión {n} · {sub}"
                pie = f"MF7011 · {sub} · notas del profesor ({hoy})"
                typ = tmp / f"notas-{qmd.stem}.typ"
                construir_notas(deck, pngs[: len(deck["slides"])], pie, glosario, typ)
                pdf_notas = out / f"S{n}_{etiqueta}_Notas_por_slide.pdf"
                compilar_typst(typ, pdf_notas)
                log(f"✓ {pdf_notas.name}")
            if "slides" not in partes and not slides_existia:
                pdf_slides.unlink(missing_ok=True)   # subproducto de --solo notas; no borrar un PDF previo

    # ── documentos del instructor ──
    if "docs" in partes:
        print("\n▸ documentos del instructor")
        docs: list[tuple[Path, str]] = []
        plan = RAIZ / "instructor" / "planes-sesion" / f"s{n}.md"
        if plan.exists():
            docs.append((plan, "Plan_de_sesion"))
        for md in sorted((RAIZ / "instructor").glob("*.md")):
            if re.search(rf"(^|[-_])s0?{n}([-_.]|$)", md.stem) and md.name.lower() != "readme.md":
                docs.append((md, nombre_doc(md.stem, n)))
        if not docs:
            log("no hay planes-sesion/sN.md ni guías *-sN.md")
        for md, nombre in docs:
            pdf = out / f"S{n}_{nombre}.pdf"
            md_a_pdf(md, pdf, f"MF7011 · Sesión {n} · material del profesor · {hoy}", tmp)
            log(f"✓ {pdf.name}  ← {md.relative_to(RAIZ)}")

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n✓ Listo: {out}")
    for f in sorted(out.glob("*.pdf")):
        print(f"    {f.name:<40} {f.stat().st_size/1e6:5.1f} MB")
    if a.abrir:
        subprocess.run(["open", str(out)])


if __name__ == "__main__":
    main()
