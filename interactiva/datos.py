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
# Índice 1-based sobre MODULOS. Hoy (2026-08-20): S1 empieza mañana → apunta a M1.
SEMANA_ACTUAL = 2  # 1=M0 orientación · 2=M1/S1 · 3=M2/S2 · 4=M3/S3 · 5=M4/S4 · 6=M5/S5

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
