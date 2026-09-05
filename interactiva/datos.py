# datos.py — fuente de verdad del paquete de interactiva (Brightspace/D2L) de MF7011.
# NADA se escribe dos veces: generar.py deriva homepage, tópicos, manifest, badges,
# release conditions e intelligent agents de ESTE archivo. Nunca editar la salida
# en build/ a mano — se sobreescribe en la siguiente corrida.
from datetime import date

CURSO = {
    "nombre":      "Formulación y Evaluación de Proyectos Sostenibles",
    "codigo":      "MF7011 · Clase 6283",
    "programa":    "Maestría en Finanzas Sostenibles y Cambio Climático · Especialización en Finanzas Sostenibles",
    "institucion": "Universidad EAFIT",
    "semestre":    "2026-2",
    "sitio":       "https://jcmunozmora.github.io/curso-proyectos-sostenibles",
    "profesor":    "Juan Carlos Muñoz-Mora",
    "contacto":    "jmunozm1@eafit.edu.co",
    "gancho":      "El Corredor del Cacao — un SPV, dos flujos de caja, la brecha que paga el curso.",
    "mensaje": (
        "Formulan y evalúan un proyecto real de inversión sostenible y lo defienden "
        "ante un comité con presupuesto limitado que va a rechazar proyectos. "
        "Viernes es el Tribunal: se decide, se debate, se defiende. Sábado es el Taller: se construye."
    ),
}

# Paleta: tomada de slides/eafit.scss (Manual de Marca EAFIT v4.0). NO inventar hex.
PALETA = {
    "primario": "#000066",   # Azul Zafre · Pantone 2738 C
    "acento":   "#00A9E0",   # Azul Cielo · Pantone 306 C
    "texto":    "#333333",
    "fondo":    "#F5F5F5",
}
FUENTE = "'Inter', 'Helvetica Neue', Arial, sans-serif"

# La ÚNICA variable del mantenimiento semanal: qué módulo destaca en "Esta semana".
# Índice 1-based sobre MODULOS. Al 2026-08-21: está en curso S1 → apunta a M1.
SEMANA_ACTUAL = 4  # 1=M0 orientación · 2=M1/S1 · 3=M2/S2 · 4=M3/S3 · 5=M4/S4 · 6=M5/S5
# Al 2026-08-31: semana de S3 "El denominador" (vie 4 + sáb 5 sep) → apunta a M3.

# Formato D2L del curso (Content clásico vs New Content Experience/Lessons):
# POR-VERIFICAR — el profesor no confirmó cuál usa el tenant de EAFIT.
# El manifest es idéntico en ambos casos (ver mambrino-interactiva_assets/d2l-package.md
# §"Unidades vs Módulos"); solo cambia el rótulo. Probar primero en sandbox.
CONTENT_EXPERIENCE = "POR-VERIFICAR"

ICONOS = {
    "orientacion": "🧭",
    "tribunal":    "⚖️",
    "taller":      "🛠",
    "plantilla":   "📋",
    "comite":      "💰",
    "rol":         "🎭",
    "bibliografia": "📚",
    "asignacion":  "📝",
    "podcast":     "🎧",
}

MODULOS = [
    {
        "id": "m00", "titulo": "🧭 Antes de empezar — El Corredor del Cacao",
        "gancho": "Un SPV, un territorio, cuatro fuentes de ingreso de riesgo distinto.",
        "fechas": (date(2026, 8, 20), date(2026, 8, 20)),
        "topicos": [
            {"id": "m00-syllabus", "titulo": "📋 Syllabus del curso",
             "tipo": "plantilla", "link": "/syllabus.html"},
            {"id": "m00-proyecto", "titulo": "🌱 Proyecto ancla — El Corredor del Cacao",
             "tipo": "plantilla", "link": "/proyecto.html"},
            {"id": "m00-materiales", "titulo": "📚 Índice de materiales y literatura",
             "tipo": "plantilla", "link": "/materiales.html"},
        ],
    },
    {
        "id": "m01", "titulo": "⚖️ Sesión 1 — ¿Es sostenible? ¿Según quién?",
        "gancho": "Un modelo de cacao con precios de dic-2024, sin revelar la fecha.",
        "fechas": (date(2026, 8, 21), date(2026, 8, 22)),
        "topicos": [
            {"id": "s01-viernes", "titulo": "⚖️ Tribunal · Vie 21 ago",
             "tipo": "tribunal", "link": "/slides/s01/s01-viernes.html"},
            {"id": "s01-sabado", "titulo": "🛠 Taller · Sáb 22 ago — La arquitectura del proyecto",
             "tipo": "taller", "link": "/slides/s01/s01-sabado.html",
             "entrega": date(2026, 8, 22)},
            {"id": "s01-ficha", "titulo": "📋 Plantilla: Ficha de proyecto",
             "tipo": "plantilla", "link": "/plantillas/01-ficha-de-proyecto.html"},
        ],
    },
    {
        "id": "m02", "titulo": "📉 Sesión 2 — Los números que nadie te da",
        "gancho": "La serie de precios del cacao 2023–2026, revelada completa.",
        "fechas": (date(2026, 8, 28), date(2026, 8, 29)),
        "topicos": [
            {"id": "s02-viernes", "titulo": "⚖️ Tribunal · Vie 28 ago",
             "tipo": "tribunal", "link": "/slides/s02/s02-viernes.html"},
            {"id": "s02-sabado", "titulo": "🛠 Taller · Sáb 29 ago — Costos, CapEx/OpEx, capital de trabajo",
             "tipo": "taller", "link": "/slides/s02/s02-sabado.html",
             "entrega": date(2026, 8, 29)},
        ],
    },
    {
        "id": "m03", "titulo": "➗ Sesión 3 — El denominador",
        "gancho": "Dos VPN del mismo proyecto, signos opuestos. Solo cambia la tasa.",
        "fechas": (date(2026, 9, 4), date(2026, 9, 5)),
        "topicos": [
            {"id": "s03-viernes", "titulo": "⚖️ Tribunal · Vie 4 sep — ¿Por qué 14% y no 9%?",
             "tipo": "tribunal", "link": "/slides/s03/s03-viernes.html"},
            {"id": "s03-sabado", "titulo": "🛠 Taller · Sáb 5 sep — Flujo de caja, VPN, TIR, TIR Modificada",
             "tipo": "taller", "link": "/slides/s03/s03-sabado.html",
             "entrega": date(2026, 9, 5)},
        ],
    },
    {
        "id": "m04", "titulo": "🌍 Sesión 4 — El otro flujo de caja",
        "gancho": "USD 0,46/tCO₂. ¿Por qué casi ninguna política ambiental logra eso?",
        "fechas": (date(2026, 9, 11), date(2026, 9, 12)),
        "topicos": [
            {"id": "s04-viernes", "titulo": "⚖️ Tribunal · Vie 11 sep — ¿Debería hacerse igual?",
             "tipo": "tribunal", "link": "/slides/s04/s04-viernes.html"},
            {"id": "s04-sabado", "titulo": "🛠 Taller · Sáb 12 sep — VPN social, precio sombra, switching value",
             "tipo": "taller", "link": "/slides/s04/s04-sabado.html",
             "entrega": date(2026, 9, 12)},
        ],
    },
    {
        "id": "m05", "titulo": "💰 Sesión 5 — Investor Day (virtual)",
        "gancho": "Cada quien recibe un rol. El comité tiene presupuesto y va a rechazar proyectos.",
        "fechas": (date(2026, 9, 18), date(2026, 9, 18)),
        "topicos": [
            {"id": "s05-investor", "titulo": "💰 Investor Day — Defensas y Comité de Inversión",
             "tipo": "comite", "link": "/slides/s05/s05-investor-day.html",
             "entrega": date(2026, 9, 18)},
            {"id": "s05-roles", "titulo": "🎭 Fichas de rol — Comité de Inversión",
             "tipo": "rol", "link": "/plantillas/03-fichas-de-rol-investor-day.html"},
            {"id": "s05-nota", "titulo": "📋 Plantilla: Nota de inversión (entregable final)",
             "tipo": "plantilla", "link": "/plantillas/02-nota-de-inversion.html"},
        ],
    },
]

# Bibliografía visible dentro de cada módulo. Los enlaces apuntan a la revisión
# pública y a su sección temática; las referencias completas viven en
# literatura/referencias.bib.
## Nota de corrección: Quarto genera los IDs de encabezado con tilde (p.ej.
## "núcleo-2-...", no "nucleo-2-..."). Verificado contra el HTML renderizado en
## _site/literatura/revision-literatura.html — usar SIEMPRE el id con tilde o el
## anchor no hace scroll a la sección (falla silenciosa, no da 404).
BIBLIOGRAFIA_POR_MODULO = {
    "m00": ("📚 Bibliografía y fuentes del curso", "/literatura/revision-literatura.html"),
    "m01": ("📚 Bibliografía S1 · sostenibilidad, ESG y valor integrado", "/literatura/revision-literatura.html#núcleo-2-finanzas-sostenibles-de-esg-como-filtro-a-valor-integrado"),
    "m02": ("📚 Bibliografía S2 · costos, commodities y pronósticos", "/literatura/revision-literatura.html#núcleo-5-finanzas-de-la-naturaleza-la-literatura-del-proyecto-ancla"),
    "m03": ("📚 Bibliografía S3 · costo de capital y evaluación", "/literatura/revision-literatura.html#núcleo-3-costo-de-capital-donde-el-curso-se-juega-la-credibilidad-técnica"),
    "m04": ("📚 Bibliografía S4 · tasa social, carbono y naturaleza", "/literatura/revision-literatura.html#núcleo-3-costo-de-capital-donde-el-curso-se-juega-la-credibilidad-técnica"),
    "m05": ("📚 Bibliografía S5 · regulación y decisión de inversión", "/literatura/revision-literatura.html#núcleo-6-estándares-regulación-y-el-terreno-colombiano"),
}

for modulo in MODULOS:
    titulo, enlace = BIBLIOGRAFIA_POR_MODULO[modulo["id"]]
    modulo["topicos"].append({
        "id": f'{modulo["id"]}-bibliografia',
        "titulo": titulo,
        "tipo": "bibliografia",
        "link": enlace,
    })

# Lecturas curadas por sesión — PDFs en literatura/readings/ (verificados; ver
# literatura/README.md). Los PDF NO van dentro del .zip del paquete de contenido
# (regla del asset d2l-package: cero material con copyright de terceros en el
# paquete; el LMS cerrado es el canal correcto). Se suben A MANO en D2L:
# Content → módulo → Upload/Create → Upload Files. generar.py deriva de ESTA
# lista la guía de subida (build/lecturas.md) — no duplicar esta info en otro lado.
# S4 y S5 aún no tienen PDF en readings/ (ver literatura/README.md §Pendientes).
LECTURAS = [
    {"modulo": "m01", "archivo": "literatura/readings/01b_Berg-etal_2022.pdf",
     "titulo": "📖 Berg, Kölbel & Rigobon (2022) — Aggregate Confusion",
     "tipo": "obligatoria",
     "nota": "Leer §1–3 y las conclusiones: por qué las calificaciones ESG de un mismo emisor divergen entre agencias."},
    {"modulo": "m01", "archivo": "literatura/readings/01d_FOLU2023_SbN-Colombia-ES.pdf",
     "titulo": "📖 FOLU Colombia (2023) — Soluciones basadas en la Naturaleza",
     "tipo": "obligatoria",
     "nota": "Leer el resumen ejecutivo: el contexto colombiano de financiamiento de SbN en el que vive el proyecto ancla."},
    {"modulo": "m01", "archivo": "literatura/readings/01a_Schoenmaker_Schramade_Cap1.pdf",
     "titulo": "⭐ Schoenmaker & Schramade (2023) — cap. 1",
     "tipo": "complementaria",
     "nota": "Opcional: el marco de valor integrado (V = FV + SV + EV) del texto base del curso."},
    {"modulo": "m01", "archivo": "literatura/readings/01c_Schoenmaker_Schramade_Cap2.pdf",
     "titulo": "⭐ Schoenmaker & Schramade (2023) — cap. 2",
     "tipo": "complementaria",
     "nota": "Opcional: profundiza el marco del cap. 1."},
    {"modulo": "m02", "archivo": "literatura/readings/02a_Forecasting.pdf",
     "titulo": "📖 Hyndman & Athanasopoulos (2021) — Getting started",
     "tipo": "obligatoria",
     "nota": "Qué hace pronosticable un fenómeno y qué decidir ANTES de pronosticar. No cubre commodities — eso lo pone la clase."},
    {"modulo": "m02", "archivo": "literatura/readings/02b_Sapag_Cap6_Costos.pdf",
     "titulo": "📖 Sapag Chain (2014) — cap. 6, Estimación de costos",
     "tipo": "obligatoria",
     "nota": "Costos diferenciales, sepultados y costo-volumen-utilidad. No desarrolla capital de trabajo — ese método lo enseña la clase."},
    {"modulo": "m03", "archivo": "literatura/readings/03b_Welch_2021.pdf",
     "titulo": "📖 Welch (2021) — If Not the CAPM, Then What?",
     "tipo": "obligatoria",
     "nota": "Completo — es corto (8 pp.). La demolición del CAPM y las diez sugerencias situacionales. Base del Tribunal del viernes."},
    {"modulo": "m03", "archivo": "literatura/readings/03c_Drupp-etal_Resultados.pdf",
     "titulo": "📖 Drupp et al. (2018) — Discounting Disentangled · resultados",
     "tipo": "obligatoria",
     "nota": "Solo la tabla de resultados y las conclusiones (el extracto ya viene recortado): 197 expertos, mediana 2%, rango 0–10%."},
    {"modulo": "m03", "archivo": "literatura/readings/03a_Schoenmaker_Schramade_Cap4.pdf",
     "titulo": "⭐ Schoenmaker & Schramade (2023) — cap. 4, Discount Rates",
     "tipo": "complementaria",
     "nota": "Opcional: el marco que reconcilia tasa financiera, tasa social y descuento integrado."},
]

# Podcast recomendado — título confirmado por el profesor (2026-08-22): "Proyectos
# sostenibles". No se inventa relación temática con una sesión específica más allá
# de lo que el profesor indicó; se coloca en la sección general de lecturas (m00).
PODCAST = {
    "id": "m00-podcast",
    "titulo": "🎧 Podcast — Proyectos sostenibles",
    "descripcion": "Podcast recomendado por el profesor: Proyectos sostenibles.",
    "spotify_embed_src": "https://open.spotify.com/embed/show/2ODsXwvb3RzO6yXDcf20pd?utm_source=generator",
    "spotify_show_url": "https://open.spotify.com/show/2ODsXwvb3RzO6yXDcf20pd",
}
MODULOS_POR_ID_TMP = {m["id"]: m for m in MODULOS}
MODULOS_POR_ID_TMP["m00"]["topicos"].append({
    "id": PODCAST["id"],
    "titulo": PODCAST["titulo"],
    "tipo": "podcast",
    "link": PODCAST["spotify_show_url"],  # URL absoluta — url() en generar.py la respeta tal cual
})

# Especificación de evaluación. Los objetos nativos de Assignment/Rubric y
# Gradebook se configuran en la UI de Brightspace o mediante un export nativo
# del tenant; esta lista es la fuente única para nombres, fechas, instrucciones,
# rúbrica y peso.
ASIGNACIONES = [
    {
        "id": "a01-ficha-proyecto", "modulo": "m01", "nombre": "S1 · Ficha de proyecto",
        "fecha": "2026-08-22", "categoria": "R1 · Artefactos de sesión", "peso": 5.0,
        "rubrica": "R1", "equipo": True, "instrucciones": "Completen la ficha de proyecto con problema, actores, cadena de resultados y cinco KPI primarios. Suban un único PDF por equipo antes de salir del taller.",
        "entrega": "/plantillas/01-ficha-de-proyecto.html",
    },
    {
        "id": "a02-auditoria-s1", "modulo": "m01", "nombre": "S1 · Auditoría cruzada",
        "fecha": "2026-08-22", "categoria": "R2 · Auditorías cruzadas", "peso": 3.75,
        "rubrica": "R2", "equipo": True, "instrucciones": "Auditen el trabajo de otro equipo usando la lista de chequeo. Cada hallazgo debe citar una cifra, celda, frase o supuesto concreto; entreguen la lista diligenciada.",
        "entrega": "/plantillas/05-listas-auditoria-cruzada.html",
    },
    {
        "id": "a03-artefacto-s2", "modulo": "m02", "nombre": "S2 · Costos, CapEx y capital de trabajo",
        "fecha": "2026-08-29", "categoria": "R1 · Artefactos de sesión", "peso": 5.0,
        "rubrica": "R1", "equipo": True, "instrucciones": "Actualicen el modelo con cronograma de CapEx, costos operativos y déficit acumulado máximo de capital de trabajo. Justifiquen cada supuesto con fuente o rango.",
        "entrega": "/plantillas/modelo-financiero-PLANTILLA.xlsx",
    },
    {
        "id": "a04-auditoria-s2", "modulo": "m02", "nombre": "S2 · Auditoría cruzada",
        "fecha": "2026-08-29", "categoria": "R2 · Auditorías cruzadas", "peso": 3.75,
        "rubrica": "R2", "equipo": True, "instrucciones": "Revisen el modelo de otro equipo: cronograma, costos, capital de trabajo y trazabilidad de fuentes. Reporten al menos un hallazgo verificable.",
        "entrega": "/plantillas/05-listas-auditoria-cruzada.html",
    },
    {
        "id": "a05-artefacto-s3", "modulo": "m03", "nombre": "S3 · Flujo de caja y criterios",
        "fecha": "2026-09-05", "categoria": "R1 · Artefactos de sesión", "peso": 5.0,
        "rubrica": "R1", "equipo": True, "instrucciones": "Entreguen el flujo del proyecto y del inversionista, VPN, TIR, TIR modificada, punto de equilibrio y sensibilidad. Expliquen qué criterio guía la decisión.",
        "entrega": "/plantillas/modelo-financiero-PLANTILLA.xlsx",
    },
    {
        "id": "a06-auditoria-s3", "modulo": "m03", "nombre": "S3 · Auditoría cruzada",
        "fecha": "2026-09-05", "categoria": "R2 · Auditorías cruzadas", "peso": 3.75,
        "rubrica": "R2", "equipo": True, "instrucciones": "Auditen flujos, tasa, moneda, VPN y TIR de otro equipo. Señalen cualquier incoherencia entre la tasa usada y la pregunta que el modelo pretende responder.",
        "entrega": "/plantillas/05-listas-auditoria-cruzada.html",
    },
    {
        "id": "a07-artefacto-s4", "modulo": "m04", "nombre": "S4 · Flujo socioeconómico",
        "fecha": "2026-09-12", "categoria": "R1 · Artefactos de sesión", "peso": 5.0,
        "rubrica": "R1", "equipo": True, "instrucciones": "Construyan el flujo socioeconómico con precio sombra del carbono, tasa social de descuento, externalidades y switching value. Expongan los supuestos que cambian el signo del VPN.",
        "entrega": "/plantillas/modelo-financiero-PLANTILLA.xlsx",
    },
    {
        "id": "a08-auditoria-s4", "modulo": "m04", "nombre": "S4 · Auditoría cruzada",
        "fecha": "2026-09-12", "categoria": "R2 · Auditorías cruzadas", "peso": 3.75,
        "rubrica": "R2", "equipo": True, "instrucciones": "Auditen la separación entre flujo privado y social, la tasa aplicada y la evidencia de carbono/naturaleza. La evidencia específica es obligatoria.",
        "entrega": "/plantillas/05-listas-auditoria-cruzada.html",
    },
    {
        "id": "a09-modelo-final", "modulo": "m05", "nombre": "Modelo financiero final",
        "fecha": "2026-09-16", "categoria": "R3 · Modelo financiero final", "peso": 25.0,
        "rubrica": "R3", "equipo": True, "instrucciones": "Suban el modelo financiero completo, con supuestos trazables, flujos privado y social, VPN, criterios, sensibilidad, riesgos y control de versiones. Un número sin fuente verificable anula el entregable.",
        "entrega": "/plantillas/modelo-financiero-PLANTILLA.xlsx",
    },
    {
        # R1 exige "cinco entregas, una por sesión" (plantillas/04-rubricas.qmd
        # §R1, 25% = 5 × 5%). S1–S4 ya tienen su artefacto (a01/a03/a05/a07);
        # la Nota de inversión es el artefacto escrito de S5 — no un apoyo de
        # peso 0 bajo R4 (eso dejaba R1 en 20% y el curso en 95% en vez de 100%).
        "id": "a10-nota-inversion", "modulo": "m05", "nombre": "S5 · Nota de inversión",
        "fecha": "2026-09-16", "categoria": "R1 · Artefactos de sesión", "peso": 5.0,
        "rubrica": "R1", "equipo": True, "instrucciones": "Suban la nota de inversión de máximo cuatro páginas. Debe contener decisión, estructura, análisis financiero y socioeconómico, riesgos, fuentes y anexo de uso de IA.",
        "entrega": "/plantillas/02-nota-de-inversion.html",
    },
    {
        "id": "a11-defensa", "modulo": "m05", "nombre": "S5 · Defensa Investor Day",
        "fecha": "2026-09-18", "categoria": "R4 · Defensa · Investor Day", "peso": 20.0,
        "rubrica": "R4", "equipo": True, "instrucciones": "Defiendan el proyecto ante el comité en doce minutos y respondan el interrogatorio. El comité dispone de presupuesto limitado y debe justificar sus decisiones con evidencia.",
        "entrega": "/slides/s05/s05-investor-day.html",
    },
    {
        "id": "a12-coevaluacion", "modulo": "m05", "nombre": "S5 · Coevaluación del comité",
        "fecha": "2026-09-18", "categoria": "R5 · Calidad como evaluador", "peso": 15.0,
        "rubrica": "R5", "equipo": False, "instrucciones": "Entreguen individualmente las tarjetas de evaluación de los proyectos asignados. Distribuyan el presupuesto disponible y justifiquen cada puntuación con evidencia específica desde su rol.",
        "entrega": "/plantillas/06-coevaluacion-comite.html",
    },
]

CATEGORIAS_CALIFICACIONES = [
    ("R1 · Artefactos de sesión", 25.0),
    ("R2 · Auditorías cruzadas", 15.0),
    ("R3 · Modelo financiero final", 25.0),
    ("R4 · Defensa · Investor Day", 20.0),
    ("R5 · Calidad como evaluador", 15.0),
]

for asignacion in ASIGNACIONES:
    modulo = next(m for m in MODULOS if m["id"] == asignacion["modulo"])
    modulo["topicos"].append({
        "id": asignacion["id"],
        "titulo": f'📝 Asignación · {asignacion["nombre"]}',
        "tipo": "asignacion",
        "link": asignacion["entrega"],
        "entrega": date.fromisoformat(asignacion["fecha"]),
    })

# Badges — anclados a artefactos REALES del plan de registro (nunca inventados).
BADGES = [
    {
        "nombre": "Arquitecto del Corredor",
        "gana_cuando": "Entrega la Ficha de proyecto + árbol de decisiones + 5 KPI primarios (S1, Taller).",
        "fuente": "instructor/00-plan-de-registro.md · Arco S1 · Artefacto del Taller",
    },
    {
        "nombre": "Domina el denominador",
        "gana_cuando": "Entrega el flujo de caja completo con VPN, TIR y TIR Modificada (S3, Taller).",
        "fuente": "instructor/00-plan-de-registro.md · Arco S3 · Artefacto del Taller",
    },
    {
        "nombre": "Juicio en el Comité",
        "gana_cuando": "Actúa como evaluador en el Investor Day con evidencia específica obligatoria (R5, 15% del curso).",
        "fuente": "README.md · Co-evaluación · Comité de Inversión",
    },
]

# Release conditions — declaradas como texto (Awards/Release Conditions se configuran
# en la UI de D2L; no hay material_type empírico para empaquetarlas). Encadenan el
# arco Tribunal→Taller ya definido en el plan de registro; no se fabrica contenido bonus
# porque el diseño del curso no contempla ninguno.
RELEASE_CONDITIONS = [
    ("m01", None, "Abierto desde el inicio del curso."),
    ("m02", "s01-sabado", "Se desbloquea al completar el Taller de S1 (Ficha de proyecto)."),
    ("m03", "s02-sabado", "Se desbloquea al completar el Taller de S2 (modelo de costos)."),
    ("m04", "s03-sabado", "Se desbloquea al completar el Taller de S3 (flujo de caja + criterios)."),
    ("m05", "s04-sabado", "Se desbloquea al completar el Taller de S4 (VPN social + switching value)."),
]

# Intelligent Agents — plantillas de texto (D2L no expone un formato de import
# empírico para agentes; se configuran en la UI). Ligadas a hitos reales del curso.
INTELLIGENT_AGENTS = [
    {
        "nombre": "No has entrado en 7 días",
        "disparador": "Sin acceso al curso en los últimos 7 días.",
        "asunto": f"{CURSO['nombre']} — Te eché de menos esta semana",
        "cuerpo": (
            "Hola {FirstName},\n\n"
            "Vi que no has entrado al curso en los últimos 7 días. No es regaño — "
            "sé que el semestre se pone pesado.\n\n"
            "Si necesitas ayuda con el Corredor del Cacao, escríbeme directamente. "
            f"Estoy en {CURSO['contacto']}.\n\n"
            f"— {CURSO['profesor']}"
        ),
    },
    {
        "nombre": "48h antes del Investor Day",
        "disparador": "No ha accedido al tópico 'Plantilla: Nota de inversión' 48h antes de S5 (18 sep).",
        "asunto": "Investor Day el viernes — ¿cómo va tu nota de inversión?",
        "cuerpo": (
            "Hola {FirstName},\n\n"
            "El Investor Day es el viernes 18 de septiembre. El comité tiene presupuesto "
            "limitado y va a rechazar proyectos con evidencia débil.\n\n"
            "Si tu modelo financiero o tu memoria de decisión de 4 páginas todavía no están "
            f"listos, escríbeme hoy: {CURSO['contacto']}.\n\n"
            f"— {CURSO['profesor']}"
        ),
    },
]
