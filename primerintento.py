import streamlit as st
from PIL import Image

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# Estilos generales con bloques diferenciados
st.markdown("""
    <style>
    .main {
        background-color: white !important;
        color: black !important;
    }
    .input-section {
        background-color: #2b344d;
        color: white !important;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 1px solid #ccc;
    }
    .input-section label,
    .input-section input,
    .input-section div[data-baseweb="input"] input {
        color: white !important;
    }
    .result-section {
        background-color: #2b344d;
        color: white !important;
        padding: 20px;
        border-radius: 10px;
        margin-top: 25px;
        border: 1px solid #cce5ff;
    }
    .resumen-item {
        font-weight: bold;
    }
    .resumen-item span.comision {
        color: #1a3e5f;
    }
    .resumen-item span.bonificacion {
        color: #1c5f1a;
    }
    .resumen-item span.penalizacion {
        color: #8b0000;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar y mostrar logo
logo = Image.open("LOGO-HRMOTOR-RGB.png")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color:#2b344d;'>CALCULADORA DE COMISIONES VENDEDORES</h1>", unsafe_allow_html=True)
with col2:
    st.image(logo, width=250)

# === BLOQUE DE ENTRADA DE DATOS ===
st.markdown("""<div class='input-section'>""", unsafe_allow_html=True)

# (Entrada de datos se mantiene igual...)
# (Código omitido por brevedad...)

st.markdown("""</div>""", unsafe_allow_html=True)

# === BLOQUE DE RESULTADOS ===
st.markdown("""<div class='result-section'>""", unsafe_allow_html=True)
st.markdown("### 📊 RESUMEN Y RESULTADO DE LA COMISIÓN")

# (Funciones y cálculos se mantienen igual...)
# (Código omitido por brevedad...)

# Mostrar desglose de la prima total
st.subheader("🧾 Desglose de la Prima Total")
st.markdown(f"<p class='resumen-item'><span class='comision'>Comisión</span> por entregas: {comision_entregas:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='comision'>Comisión</span> por compras: {comision_compras:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='comision'>Comisión</span> por VH cambio: {comision_vh_cambio:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='bonificacion'>Bonificación</span> por financiación: {bono_financiacion:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='bonificacion'>Bonificación</span> por entrega rápida: {bono_rapida:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='bonificacion'>Bonificación</span> por stock largo: {bono_stock:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='penalizacion'>Penalización</span> por entregas con descuento: {penalizacion_descuento:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='comision'>Comisión</span> sobre beneficio financiero: {comision_beneficio:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='bonificacion'>Bonificación</span> por garantías premium: {bono_garantias:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='bonificacion'>Bonificación</span> por reseñas: {bono_resenas:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p class='resumen-item'><span class='bonificacion'>Bonificación</span> por ventas sobre PVP: {bono_ventas_sobre_pvp:.2f} €</p>", unsafe_allow_html=True)

st.markdown(f"### ✔ Prima total antes de penalizaciones= {prima_total:.2f} €")

if penalizaciones_detalle:
    st.markdown("""
        <div style='background-color: #ffcccc; padding: 15px; border: 2px solid red; border-radius: 10px;'>
        <h4 style='color: red;'>⚠️ Penalizaciones aplicadas</h4>
    """, unsafe_allow_html=True)
    for motivo, valor in penalizaciones_detalle:
        st.markdown(f"<p>🔸 {motivo}: <strong>-{valor:.2f} €</strong></p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Total penalizaciones: -{penalizacion_total:.2f} €</strong></p></div>", unsafe_allow_html=True)

st.markdown(f"## ✅ Prima final a cobrar= **{prima_final:.2f} €**")

st.markdown("""</div>""", unsafe_allow_html=True)


