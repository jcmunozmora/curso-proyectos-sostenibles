"""Genera la plantilla de modelo financiero del curso (9 hojas, con fórmulas vivas)."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as col

wb = openpyxl.Workbook()
Z  = PatternFill("solid", fgColor="000066")     # Azul Zafre EAFIT
C  = PatternFill("solid", fgColor="00A9E0")     # Azul Cielo EAFIT
AM = PatternFill("solid", fgColor="FFF3CD")     # celda de INPUT
GR = PatternFill("solid", fgColor="EAEAEA")
WB_ = Font(color="FFFFFF", bold=True)
B   = Font(bold=True)
thin = Side(style="thin", color="BBBBBB")
BOX  = Border(left=thin, right=thin, top=thin, bottom=thin)
HOR = 15   # horizonte

def titulo(ws, t, sub=""):
    ws["A1"] = t; ws["A1"].font = Font(size=14, bold=True, color="000066")
    if sub: ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="666666", size=10)

def cab_anios(ws, fila, c0=3, etiqueta="Año"):
    ws.cell(fila, c0-1, etiqueta).font = WB_; ws.cell(fila, c0-1).fill = Z
    for a in range(HOR+1):
        c = ws.cell(fila, c0+a, a); c.fill = Z; c.font = WB_
        c.alignment = Alignment(horizontal="center")
    for j in range(1, c0+HOR+1):
        ws.cell(fila, j).border = BOX

def encabezados(ws, fila, heads, c0=1):
    for j,h in enumerate(heads, c0):
        c = ws.cell(fila, j, h); c.fill = Z; c.font = WB_
        c.alignment = Alignment(horizontal="center", wrap_text=True); c.border = BOX

# ══════════════ 1. LÉEME ══════════════
ws = wb.active; ws.title = "LÉEME"
titulo(ws, "MODELO FINANCIERO — Formulación y Evaluación de Proyectos Sostenibles",
       "MF7011 · EAFIT · plantilla del curso")
reglas = [
 ("", ""),
 ("CÓDIGO DE COLORES", ""),
 ("  Celda AMARILLA", "INPUT — ustedes escriben aquí. Todo supuesto va en una celda amarilla."),
 ("  Celda BLANCA", "FÓRMULA — no escribir números a mano."),
 ("  Celda GRIS", "Calculada automáticamente. No tocar."),
 ("", ""),
 ("LAS SEIS REGLAS DEL MODELO", ""),
 ("  1", "Ningún número codificado dentro de una fórmula. Todo supuesto vive en 'Supuestos'."),
 ("  2", "Toda celda numérica lleva su UNIDAD en el encabezado. 'USD/ha', no 'Costo'."),
 ("  3", "Toda cifra externa lleva su FUENTE en la columna correspondiente."),
 ("  4", "Nominal con nominal, real con real. Nunca mezclar en el mismo cálculo."),
 ("  5", "La deuda aparece UNA vez: o en el numerador (FCA) o en el denominador (WACC)."),
 ("  6", "El riesgo específico va al flujo. El sistemático, a la tasa. Nunca a los dos."),
 ("", ""),
 ("ORDEN DE LLENADO", ""),
 ("  Sesión 1", "Ficha de proyecto (documento aparte)"),
 ("  Sesión 2", "Supuestos → CapEx → OpEx → KTrabajo"),
 ("  Sesión 3", "WACC → FCLD → FCA → Criterios"),
 ("  Sesión 4", "FlujoSocial → Escenarios"),
 ("  Sesión 5", "Nota de inversión (documento aparte)"),
]
for i,(a,b_) in enumerate(reglas, 4):
    ws.cell(i,1,a).font = B if a.strip() and not a.startswith("  ") else Font()
    if a.strip() and not a.startswith("  "): ws.cell(i,1).fill = C
    ws.cell(i,2,b_)
ws.column_dimensions["A"].width = 22; ws.column_dimensions["B"].width = 92

# ══════════════ 2. SUPUESTOS ══════════════
ws = wb.create_sheet("Supuestos")
titulo(ws, "SUPUESTOS", "Toda celda amarilla es una decisión suya. Cada una necesita fuente.")
encabezados(ws, 4, ["Parámetro","Valor","Unidad","Fuente","Notas / justificación"])
sup = [
 ("— PROYECTO —",None,"","",""),
 ("Escala", 500, "ha", "", "¿Por qué esta escala y no otra?"),
 ("Horizonte de evaluación", 15, "años", "", ""),
 ("— MERCADO —",None,"","",""),
 ("Precio del producto · escenario BAJO", 3500, "USD/t", "", "Mundo en que el proyecto pierde"),
 ("Precio del producto · escenario CENTRAL", 5000, "USD/t", "", ""),
 ("Precio del producto · escenario ALTO", 8000, "USD/t", "", ""),
 ("Prima de certificación", 0.12, "fracción", "", "¿Desde qué año?"),
 ("Rendimiento en madurez", 0.80, "t/ha", "", ""),
 ("Año de inicio de producción", 4, "año", "", ""),
 ("— COSTOS —",None,"","",""),
 ("CapEx total", 4200000, "USD", "", "Ver hoja CapEx"),
 ("OpEx en madurez", 1900, "USD/ha/año", "", "Ver hoja OpEx"),
 ("Fracción de OpEx que es mano de obra", 0.60, "fracción", "", "Se usa en FlujoSocial"),
 ("— FINANCIACIÓN —",None,"","",""),
 ("Deuda / (Deuda + Patrimonio)", 0.60, "fracción", "", "Estructura OBJETIVO, no la de hoy"),
 ("Kd — costo de la deuda", 0.14, "EA nominal COP", "", "Tasa cotizada, no esperada"),
 ("Tasa impositiva", 0.35, "fracción", "", ""),
 ("— COSTO DE CAPITAL —",None,"","",""),
 ("Rf — tasa libre de riesgo", 0.042, "EA nominal USD", "", "Tesoro USA 10 años"),
 ("ERP de mercado maduro", 0.0423, "fracción", "Damodaran ene-2026", "DESCARGAR el día de uso"),
 ("Prima de riesgo país Colombia", 0.0285, "fracción", "Damodaran ene-2026", "DESCARGAR el día de uso"),
 ("Beta", 0.85, "—", "", "JUSTIFICAR. ¿Qué comparables?"),
 ("Beta — límite inferior IC 95%", 0.35, "—", "", ""),
 ("Beta — límite superior IC 95%", 1.35, "—", "", ""),
 ("Inflación Colombia", 0.050, "EA", "", ""),
 ("Inflación Estados Unidos", 0.025, "EA", "", ""),
 ("— EVALUACIÓN SOCIAL —",None,"","",""),
 ("TSD ambiental · años 0-5", 0.095, "EA real", "DNP Res. 1092/2022", "Obligatoria en Colombia"),
 ("TSD ambiental · años 6-25", 0.064, "EA real", "DNP Res. 1092/2022", ""),
 ("TSD ambiental · años 26+", 0.035, "EA real", "DNP Res. 1092/2022", ""),
 ("Factor de salario sombra rural", 0.70, "fracción", "", "JUSTIFICAR"),
 ("Stock de C — con proyecto", 35, "Mg C/ha", "", ""),
 ("Stock de C — línea base", 8, "Mg C/ha", "", "LA DECISIÓN MÁS CONTESTADA"),
 ("Precio sombra del carbono · BAJO", 50, "USD/tCO2e", "Banco Mundial 2024", ""),
 ("Precio sombra del carbono · ALTO", 100, "USD/tCO2e", "Banco Mundial 2024", ""),
]
r = 5
for nom,val,uni,fte,nota in sup:
    if val is None:
        c = ws.cell(r,1,nom); c.fill = C; c.font = B
        for j in range(2,6): ws.cell(r,j).fill = C
    else:
        ws.cell(r,1,nom)
        cv = ws.cell(r,2,val); cv.fill = AM; cv.border = BOX
        if isinstance(val,float) and val < 1: cv.number_format = '0.00%' if 'fracción' in uni or 'EA' in uni else '0.00'
        ws.cell(r,3,uni); ws.cell(r,4,fte).fill = AM; ws.cell(r,5,nota)
    r += 1
# Derivados
ws.cell(r+1,1,"— DERIVADOS (no tocar) —").fill = C; ws.cell(r+1,1).font = B
der = [("Ke en USD","=B24+B27*B25+B26"),
       ("Ke en COP","=(1+B{})*(1+B29)/(1+B30)-1".format(r+2)),
       ("WACC en COP","=(1-B17)*B{}+B17*B18*(1-B19)".format(r+3)),
       ("Adicionalidad de carbono","=(B37-B38)*44/12*B6"),]
for k,(nom,f) in enumerate(der, r+2):
    ws.cell(k,1,nom).font = B
    c = ws.cell(k,2,f); c.fill = GR; c.font = Font(bold=True,color="000066"); c.number_format='0.00%'
ws.cell(r+5,3,"tCO2e totales")
for j,w in enumerate([42,14,18,26,48],1): ws.column_dimensions[col(j)].width = w

# ══════════════ 3-4. CapEx / OpEx ══════════════
for nombre, heads, hint in [
  ("CapEx", ["Rubro","Unidad","Cantidad","Costo unitario","Año 0","Año 1","Año 2","Año 3","TOTAL","Fuente"],
   "Mínimo 12 rubros. No olviden: estudios previos, vivero, beneficiadero, vías, riego, RESIEMBRA, imprevistos."),
  ("OpEx",  ["Rubro","Unidad","Costo unitario","Tipo (fijo/variable)","Fuente"],
   "Separen fijo de variable — lo necesitan para el punto de equilibrio en S3.")]:
    ws = wb.create_sheet(nombre)
    titulo(ws, nombre.upper(), hint)
    encabezados(ws, 4, heads)
    for rr in range(5, 25):
        for j in range(1, len(heads)+1):
            ws.cell(rr,j).border = BOX
            if j in (1,2,3,4) or heads[j-1]=="Fuente": ws.cell(rr,j).fill = AM
    ws.cell(26,1,"TOTAL").font = B
    for j,w in enumerate([34,14,12,16,14,14,14,14,14,30][:len(heads)],1):
        ws.column_dimensions[col(j)].width = w
    if nombre=="OpEx":
        ws.cell(28,1,"OpEx por año (USD/ha) — curva de maduración").font = B
        cab_anios(ws, 29, c0=2)
        ws.cell(30,1,"OpEx USD/ha").font = B
        for a in range(HOR+1): ws.cell(30,2+a).fill = AM

# ══════════════ 5. Capital de trabajo ══════════════
ws = wb.create_sheet("KTrabajo")
titulo(ws,"CAPITAL DE TRABAJO","Método del déficit acumulado máximo. ⚠ NO OLVIDAR LA RECUPERACIÓN EN EL ÚLTIMO AÑO.")
cab_anios(ws, 4, c0=3, etiqueta="")
filas = ["Ingresos operativos","Costos operativos","Flujo operativo","ACUMULADO"]
for i,f in enumerate(filas,5):
    ws.cell(i,2,f).font = B
    for a in range(HOR+1):
        c = ws.cell(i,3+a); c.border = BOX; c.number_format='#,##0'
        if i<7: c.fill = AM
        if i==8: c.fill = GR
ws.cell(10,2,"DÉFICIT ACUMULADO MÁXIMO =").font = B
ws.cell(10,4).fill = GR; ws.cell(10,4).font = Font(bold=True,color="000066")
ws.cell(11,2,"→ Se invierte en año 0 y SE RECUPERA en año {}".format(HOR)).font = Font(italic=True,color="C00000")
ws.column_dimensions["B"].width = 26

# ══════════════ 6-7. FCLD / FCA ══════════════
ws = wb.create_sheet("FCLD")
titulo(ws,"FLUJO DE CAJA DEL PROYECTO (FCLD)","¿Es buena la IDEA? — NO incluye deuda. Se descuenta al WACC.")
cab_anios(ws, 4, c0=3, etiqueta="")
for i,f in enumerate(["Ingresos","(−) Costos operativos","(−) Depreciación","(=) EBIT",
                      "(−) Impuestos  ⚠ CERO si EBIT<0","(+) Depreciación","(−) CapEx",
                      "(−) Δ Capital de trabajo","(+) Valor terminal","(=) FCLD"],5):
    ws.cell(i,2,f).font = B if f.startswith("(=") else Font()
    for a in range(HOR+1):
        c = ws.cell(i,3+a); c.border=BOX; c.number_format='#,##0'
        if f.startswith("(="): c.fill = GR; c.font = Font(bold=True)
ws.column_dimensions["B"].width = 34

ws = wb.create_sheet("FCA")
titulo(ws,"FLUJO DE CAJA DEL INVERSIONISTA (FCA)","¿Le sirve al ACCIONISTA? — SÍ incluye deuda. Se descuenta al Ke, NO al WACC.")
cab_anios(ws, 4, c0=3, etiqueta="")
for i,f in enumerate(["FCLD","(+) Desembolso de deuda","(−) Intereses × (1−t)",
                      "(−) Amortización de capital","(=) FCA"],5):
    ws.cell(i,2,f).font = B if f.startswith("(=") else Font()
    for a in range(HOR+1):
        c = ws.cell(i,3+a); c.border=BOX; c.number_format='#,##0'
        if f.startswith("(="): c.fill = GR; c.font = Font(bold=True)
ws.cell(11,2,"TABLA DE AMORTIZACIÓN").font = B; ws.cell(11,2).fill = C
cab_anios(ws, 12, c0=3, etiqueta="")
for i,f in enumerate(["Saldo inicial","Intereses","Amortización","Saldo final"],13):
    ws.cell(i,2,f)
    for a in range(HOR+1): ws.cell(i,3+a).border=BOX; ws.cell(i,3+a).number_format='#,##0'
ws.column_dimensions["B"].width = 34

# ══════════════ 8. Criterios ══════════════
ws = wb.create_sheet("Criterios")
titulo(ws,"CRITERIOS DE DECISIÓN","⚠ Verifiquen el patrón de SIGNOS del flujo antes de reportar la TIR.")
encabezados(ws, 4, ["Criterio","Valor","Fórmula Excel","¿Qué decide?","Observación"])
crit = [("VPN del proyecto @ WACC","","=VNA(WACC; F1:F15)+F0","Crea o destruye valor",""),
        ("VPN @ WACC límite inferior","","","Robustez",""),
        ("VPN @ WACC límite superior","","","Robustez",""),
        ("VPN del accionista @ Ke","","=VNA(Ke; ...)+F0","Retorno al patrimonio","≠ VPN del proyecto"),
        ("TIR","","=TIR(rango)","Eficiencia","⚠ verificar signos"),
        ("TIR Modificada","","=TIRM(rango; Kd; WACC)","Eficiencia honesta","Siempre única"),
        ("Payback descontado","","","Exposición temporal",""),
        ("Costo Anual Equivalente","","=PAGO(WACC; n; -VPN)","Comparar vidas distintas",""),
        ("Índice de rentabilidad","","=VPN/Inversión","Racionamiento de capital",""),
        ("Precio de equilibrio","","Buscar objetivo","¿A qué precio VPN=0?","LA cifra comunicable"),
        ("Punto de equilibrio (t)","","=CF/(p−cv)","Volumen mínimo",""),
        ("GAO","","","Sensibilidad operativa",""),
        ("GAF","","","Sensibilidad financiera",""),
        ("Cambios de signo del flujo","","","¿TIR confiable?","⚠ si >1, declararlo")]
for i,(a,b_,c_,d_,e_) in enumerate(crit,5):
    ws.cell(i,1,a).font=B; ws.cell(i,2).fill=GR; ws.cell(i,3,c_); ws.cell(i,4,d_); ws.cell(i,5,e_)
    for j in range(1,6): ws.cell(i,j).border=BOX
for j,w in enumerate([34,18,30,30,26],1): ws.column_dimensions[col(j)].width=w

# ══════════════ 9. Flujo social ══════════════
ws = wb.create_sheet("FlujoSocial")
titulo(ws,"FLUJO SOCIOECONÓMICO","Transferencias fuera · precios sombra · externalidades dentro · descontar a la TSD")
cab_anios(ws, 4, c0=3, etiqueta="")
for i,f in enumerate(["FCLD privado","(−) Eliminar impuestos  [transferencia]",
                      "(−) Eliminar prima de certificación  [transferencia]",
                      "(±) Ajuste por salario sombra","(+) Carbono removido × precio sombra",
                      "(+) Otra externalidad (agua / biodiversidad)","(=) FLUJO SOCIAL"],5):
    ws.cell(i,2,f).font = B if f.startswith("(=") else Font()
    for a in range(HOR+1):
        c=ws.cell(i,3+a); c.border=BOX; c.number_format='#,##0'
        if f.startswith("(="): c.fill=GR; c.font=Font(bold=True)
ws.cell(14,2,"PROTOCOLO BANCO MUNDIAL").font=B; ws.cell(14,2).fill=C
encabezados(ws, 15, ["Tasa de descuento","VPN sin carbono","VPN carbono BAJO","VPN carbono ALTO"], c0=2)
for i,t in enumerate(["TSD ambiental Colombia (Res. 1092/2022)","TSD general 9,0%",
                      "Consenso experto internacional 2,0%","WACC privado (referencia)"],16):
    ws.cell(i,2,t)
    for j in range(3,6): ws.cell(i,j).fill=GR; ws.cell(i,j).border=BOX; ws.cell(i,j).number_format='#,##0'
ws.cell(21,2,"SWITCHING VALUE (USD/tCO2e)").font=B
ws.cell(21,3).fill=AM; ws.cell(21,3).border=BOX
ws.cell(22,2,'→ "Este proyecto se justifica socialmente si el carbono supera USD ___/tCO2e"').font=Font(italic=True,color="000066")
ws.column_dimensions["B"].width=44

# ══════════════ 10. Escenarios ══════════════
ws = wb.create_sheet("Escenarios")
titulo(ws,"ESCENARIOS CLIMÁTICOS NGFS","Si su proyecto gana en los tres, no construyó escenarios.")
encabezados(ws, 4, ["Variable","Current Policies","Net Zero 2050","Delayed Transition"])
for i,v in enumerate(["Precio del producto (USD/t)","Rendimiento físico (t/ha)",
                      "Precio del carbono (USD/t)","CapEx de adaptación (USD)",
                      "VPN privado","VPN social","¿Se financia?"],5):
    ws.cell(i,1,v).font=B
    for j in range(2,5):
        ws.cell(i,j).border=BOX
        ws.cell(i,j).fill = GR if v.startswith("VPN") else AM
for j,w in enumerate([32,24,24,24],1): ws.column_dimensions[col(j)].width=w

wb.save("modelo-financiero-PLANTILLA.xlsx")
print("✓ plantillas/modelo-financiero-PLANTILLA.xlsx")
print("  Hojas:", ", ".join(wb.sheetnames))
