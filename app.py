import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import pandas as pd 

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def conectar_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credenciales.json", scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("clientes_finanzas").sheet1

    return sheet

def guardar_cliente(data):
    try:
        sheet = conectar_sheet()

        fila = [
            data["nombre"],
            data["email"],
            data["whatsapp"],
            data["ingresos"],
            data["gastos"],
            round(data["ahorro"] * 100, 2),
            data["score"],
            data["nivel"]
        ]

        sheet.append_row(fila)

    except Exception as e:
        print("Error guardando en Sheets:", e)    

st.set_page_config(page_title="Diagnóstico Financiero PRO", layout="centered")

# -------------------------
# INIT STATE (SaaS)
# -------------------------
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "nombre": "", "email": "", "whatsapp": "",
        "salario": 0.0, "independiente": 0.0, "empresa": 0.0,
        "alquiler": 0.0, "plazo_fijo": 0.0, "fci": 0.0,
        "acciones": 0.0, "bonos": 0.0, "on": 0.0, "otros_ing": 0.0,
        "alquiler_g": 0.0, "impuestos": 0.0, "servicios": 0.0,
        "colegio": 0.0, "salud": 0.0,
        "salidas": 0.0, "comida": 0.0, "cafe": 0.0,
        "viajes": 0.0, "otros_gastos": 0.0
    }

fd = st.session_state.form_data

# -------------------------
# LIMPIAR TODO
# -------------------------
def limpiar():
    for k in fd:
        fd[k] = 0.0 if isinstance(fd[k], (int, float)) else ""
    st.rerun()

# -------------------------
# UI
# -------------------------
st.title("📊 Diagnóstico Financiero Inteligente")

col1, col2 = st.columns([8,1])
with col2:
    if st.button("🧹"):
        limpiar()

# -------------------------
# DATOS
# -------------------------
st.header("👤 Datos personales")
fd["nombre"] = st.text_input("Nombre", value=fd["nombre"])
fd["email"] = st.text_input("Email", value=fd["email"])
fd["whatsapp"] = st.text_input("WhatsApp", value=fd["whatsapp"])

# INGRESOS
st.header("💰 Ingresos")

st.subheader("Ingresos Activos")
fd["salario"] = st.number_input("Salario", value=fd["salario"])
fd["independiente"] = st.number_input("Independiente", value=fd["independiente"])
fd["empresa"] = st.number_input("Empresa", value=fd["empresa"])

st.subheader("Ingresos Pasivos")
fd["alquiler"] = st.number_input("Alquileres", value=fd["alquiler"])
fd["plazo_fijo"] = st.number_input("Plazo fijo", value=fd["plazo_fijo"])
fd["fci"] = st.number_input("FCI", value=fd["fci"])
fd["acciones"] = st.number_input("Acciones", value=fd["acciones"])
fd["bonos"] = st.number_input("Bonos", value=fd["bonos"])
fd["on"] = st.number_input("Obligaciones Negociables", value=fd["on"])
fd["otros_ing"] = st.number_input("Otros ingresos", value=fd["otros_ing"])

# GASTOS
st.header("💸 Gastos")

st.subheader("Gastos Fijos")
fd["alquiler_g"] = st.number_input("Alquiler", value=fd["alquiler_g"])
fd["impuestos"] = st.number_input("Impuestos", value=fd["impuestos"])
fd["servicios"] = st.number_input("Servicios", value=fd["servicios"])
fd["colegio"] = st.number_input("Colegio", value=fd["colegio"])
fd["salud"] = st.number_input("Salud", value=fd["salud"])

st.subheader("Gastos Variables")
fd["salidas"] = st.number_input("Salidas", value=fd["salidas"])
fd["comida"] = st.number_input("Comida", value=fd["comida"])
fd["cafe"] = st.number_input("Café", value=fd["cafe"])
fd["viajes"] = st.number_input("Viajes", value=fd["viajes"])
fd["otros_gastos"] = st.number_input("Otros gastos", value=fd["otros_gastos"])

# -------------------------
# ANALISIS
# -------------------------
if st.button("🚀 Analizar"):

    ingresos_activos = fd["salario"] + fd["independiente"] + fd["empresa"]
    ingresos_pasivos = fd["alquiler"] + fd["plazo_fijo"] + fd["fci"] + fd["acciones"] + fd["bonos"] + fd["on"] + fd["otros_ing"]

    total_ingresos = ingresos_activos + ingresos_pasivos
    
    ingresos = {
    "Salario": fd["salario"],
    "Independiente": fd["independiente"],
    "Empresa": fd["empresa"],
    "Alquiler": fd["alquiler"],
    "Plazo fijo": fd["plazo_fijo"],
    "FCI": fd["fci"],
    "Acciones": fd["acciones"],
    "Bonos": fd["bonos"],
    "ON": fd["on"],
    "Otros": fd["otros_ing"]
}
    total_ingresos = sum(ingresos.values())
    ingresos_pasivos = fd["alquiler"] + fd["plazo_fijo"] + fd["fci"] + fd["acciones"] + fd["bonos"] + fd["on"] + fd["otros_ing"]

    if total_ingresos > 0:
        porcentaje_pasivo = (ingresos_pasivos / total_ingresos) * 100
    else:
        porcentaje_pasivo = 0

    gastos_dict = {
        "Alquiler": fd["alquiler_g"],
        "Impuestos": fd["impuestos"],
        "Servicios": fd["servicios"],
        "Colegio": fd["colegio"],
        "Salud": fd["salud"],
        "Salidas": fd["salidas"],
        "Comida": fd["comida"],
        "Café": fd["cafe"],
        "Viajes": fd["viajes"],
        "Otros": fd["otros_gastos"]
    }

    total_gastos = sum(gastos_dict.values())
    tasa_ahorro = (total_ingresos - total_gastos) / total_ingresos if total_ingresos > 0 else 0 
    if total_ingresos > 0:
        tasa_ahorro = (total_ingresos - total_gastos) / total_ingresos
    else:
        tasa_ahorro = 0
    
    # SCORE
    if tasa_ahorro >= 0.3:
        score = 90
        nivel = "Excelente"
        color_score = "#00c46a"
    elif tasa_ahorro >= 0.15:
        score = 70
        nivel = "Bueno"
        color_score = "#f1c40f"
    else:
        score = 40
        nivel = "Bajo"
        color_score = "#ff4b4b"
        
    # 👇 DESPUÉS de calcular ingresos, gastos, tasa, score

    data_cliente = {
        "nombre": fd["nombre"],
        "email": fd["email"],
        "whatsapp": fd["whatsapp"],
        "ingresos": total_ingresos,
        "gastos": total_gastos,
        "ahorro": tasa_ahorro,
        "score": score,
        "nivel": nivel
    }

    guardar_cliente(data_cliente)

    st.success("✅ Datos guardados en la nube")


    # RESULTADOS
    st.header("📊 Resultados")

    st.subheader("Distribución de Ingresos (%)")
    for k, v in ingresos.items():
        if total_ingresos > 0:
            st.write(f"{k}: {v/total_ingresos*100:.1f}%")

    st.subheader("Distribución de Gastos (%)")
    for k, v in gastos_dict.items():
        if total_gastos > 0:
            st.write(f"{k}: {v/total_gastos*100:.1f}%")
            
    st.subheader("💰 Resumen General")
    # SEGURIDAD ANTI ERRORES
    total_ingresos = total_ingresos if total_ingresos else 0
    total_gastos = total_gastos if total_gastos else 0
    tasa_ahorro = tasa_ahorro if tasa_ahorro else 0
    score = score if 'score' in locals() else 0
    nivel = nivel if 'nivel' in locals() else ""
    color_score = color_score if 'color_score' in locals() else "#00c46a"

    components.html(f"""
    <style>
    body {{
        background-color: #0e1117;
        color: white;
        font-family: Arial;
    }}
    .container {{
        display: flex;
        gap: 20px;
        justify-content: center;
        margin-top: 30px;
    }}
    .card {{
        background: #1a1f2b;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        width: 200px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.5);
    }}
    .title {{
        font-size: 14px;
        color: #aaa;
    }}
    .value {{
        font-size: 28px;
        font-weight: bold;
        margin-top: 10px;
    }}
    .score {{
        font-size: 80px;
        margin-top: 40px;
        color: {color_score};
    }}
    </style>

    <h2 style="text-align:center;">📊 Dashboard Financiero</h2>

    <div class="container">
        <div class="card">
            <div class="title">Ingresos</div>
            <div class="value">💰 {total_ingresos:,.0f}</div>
        </div>

        <div class="card">
            <div class="title">Gastos</div>
            <div class="value">💸 {total_gastos:,.0f}</div>
        </div>

        <div class="card">
            <div class="title">Ahorro</div>
            <div class="value">📈 {tasa_ahorro*100:.1f}%</div>
        </div>
    </div>

    <div style="text-align:center;">
        <div class="score">{score}</div>
        <div>{nivel}</div>
    </div>

    """, height=500)
        
    if tasa_ahorro > 0.3:
        st.success("🚀 Excelente nivel de ahorro")
    elif tasa_ahorro > 0.1:
        st.warning("⚠️ Podés mejorar tu ahorro")
    else:
        st.error("❌ Bajo nivel de ahorro")    

    # -------------------------
    # GRAFICO 1
    # -------------------------
    st.subheader("📊 Distribución de Ingresos")
    fig1, ax1 = plt.subplots()
    ax1.pie(
        [ingresos_activos, ingresos_pasivos],
        labels=["Activos", "Pasivos"],
        autopct='%1.1f%%',
        startangle=90
    )
    ax1.set_title("Ingresos Activos vs Pasivos")
    st.pyplot(fig1)

    # -------------------------
    # GRAFICO 2
    # -------------------------
    st.subheader("📊 Comparación Ingresos vs Gastos")
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(
        ["Ingresos", "Gastos"],
        [total_ingresos, total_gastos],
        color=["green", "red"]
    )

    for bar in bars:
        ax2.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height(),
            f"${bar.get_height():,.0f}",
            ha='center'
        )

    ax2.set_title("Ingresos vs Gastos")
    st.pyplot(fig2)

    # -------------------------
    # GRAFICO 3 (FIX PRO)
    # -------------------------
    st.subheader("📊 Distribución de Gastos")

    valores = list(gastos_dict.values())
    labels = list(gastos_dict.keys())

    # FILTRAR CEROS → mejora visual PRO
    valores_filtrados = [v for v in valores if v > 0]
    labels_filtrados = [labels[i] for i, v in enumerate(valores) if v > 0]

    fig3, ax3 = plt.subplots(figsize=(6,6))
    ax3.pie(
        valores_filtrados,
        labels=labels_filtrados,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.8,
        labeldistance=1.1
    )
    ax3.set_title("Composición de Gastos")
    ax3.axis('equal')
    st.pyplot(fig3)

    # -------------------------
    # RECOMENDACIONES PRO
    # -------------------------
    st.markdown("## 🧠 Recomendaciones Inteligentes")

    # MENSAJE PRINCIPAL SEGÚN SCORE
    if score >= 80:
        st.success("🚀 Excelente manejo financiero. Estás en una posición sólida para crecer patrimonialmente.")
    elif score >= 60:
        st.info("👍 Buen manejo general, pero hay oportunidades claras de mejora.")
    else:
        st.error("⚠️ Tu situación financiera requiere atención inmediata.")

    # RECOMENDACIONES DETALLADAS
    recomendaciones = []

    # 1. AHORRO
    if tasa_ahorro < 0:
        recomendaciones.append("❌ Estás gastando más de lo que ganás. Prioridad absoluta: reducir gastos inmediatamente.")
    elif tasa_ahorro < 0.1:
        recomendaciones.append("⚠️ Tu tasa de ahorro es muy baja. Intentá llevarla al menos al 10% de tus ingresos.")
    elif tasa_ahorro < 0.3:
        recomendaciones.append("👍 Buen nivel de ahorro. Podés optimizarlo automatizando inversiones.")
    else:
        recomendaciones.append("🚀 Excelente tasa de ahorro. Considerá diversificar inversiones para maximizar rendimiento.")

    # 2. DEPENDENCIA DE INGRESOS ACTIVOS
    if ingresos_activos > ingresos_pasivos:
        porcentaje_pasivo = (ingresos_pasivos / total_ingresos * 100) if total_ingresos > 0 else 0
    
    if porcentaje_pasivo < 10:
        recomendaciones.append("💼 Dependés casi totalmente de ingresos activos. Construí fuentes de ingresos pasivos.")
    elif porcentaje_pasivo < 30:
        recomendaciones.append("📈 Tenés algunos ingresos pasivos, pero aún podés potenciarlos.")
    else:
        recomendaciones.append("💸 Excelente balance: tus ingresos pasivos son relevantes.")

    # 3. ANALISIS DE GASTOS
    if total_gastos > total_ingresos * 0.8:
        recomendaciones.append("⚠️ Tus gastos representan más del 80% de tus ingresos. Hay poco margen financiero.")
    elif total_gastos < total_ingresos * 0.5:
        recomendaciones.append("💰 Buen control de gastos. Tenés capacidad de inversión.")

    # 4. DETECCION DE GASTOS ALTOS
    for categoria, valor in gastos_dict.items():
        if total_gastos > 0:
            porcentaje = valor / total_gastos
            if porcentaje > 0.3:
                recomendaciones.append(f"🔎 Alto gasto en {categoria} ({porcentaje*100:.1f}%). Revisar optimización.")

    # 5. RECOMENDACIONES DE INVERSIÓN
    if tasa_ahorro > 0.2:
        recomendaciones.append("📊 Podés destinar parte del ahorro a inversiones como FCI, acciones o bonos.")
    else:
        recomendaciones.append("📉 Antes de invertir, consolidá un fondo de emergencia.")

    # 6. FONDO DE EMERGENCIA
    recomendaciones.append("🛟 Construí un fondo de emergencia equivalente a 3-6 meses de gastos.")

    # -------------------------
    # MOSTRAR RECOMENDACIONES
    # -------------------------
    for r in recomendaciones:
        st.write(r)

    # -------------------------
    # WHATSAPP
    # -------------------------
    import urllib.parse

    numero = "5493513371388"

    mensaje = f"""Hola! Soy {fd["nombre"]}

    Acabo de analizar mis finanzas:

    💰 Ingresos: ${total_ingresos:,.0f}
    💸 Gastos: ${total_gastos:,.0f}
    📈 Ahorro: {tasa_ahorro*100:.1f}%
    🎯 Score: {score} ({nivel})

    Me gustaría recibir asesoramiento 👇
    """

    mensaje_encoded = urllib.parse.quote(mensaje)

    link = f"https://wa.me/{numero}?text={mensaje_encoded}"

    st.markdown(f"""
    <a href="{link}" target="_blank">
        <button style="
            background-color:#25D366;
            color:white;
            padding:12px 20px;
            border:none;
            border-radius:10px;
            font-size:16px;
            cursor:pointer;">
            💬 Contactar por WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)