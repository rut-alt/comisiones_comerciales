import streamlit as st
from PIL import Image

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# Estilos generales y fondo
st.markdown("""
    <style>
    .main {
        background-color: white !important;
        color: black !important;
    }
    .input-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    .result-section {
        background-color: #eaf6ff;
        padding: 20px;
        border-radius: 10px;
        margin-top: 25px;
        border: 1px solid #cce5ff;
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

# === A. BLOQUE DE ENTREGAS ===
st.markdown("""<div class='input-section'>""", unsafe_allow_html=True)
st.markdown("### A. ENTREGAS")
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    entregas = st.number_input("A.1 Entregas totales", min_value=0, step=1)
with col_a2:
    entregas_otra_delegacion = st.number_input("A.2 En otra delegación", min_value=0, max_value=entregas, step=1)
with col_a3:
    entregas_compartidas = st.number_input("A.3 Entregas compartidas", min_value=0, max_value=entregas, step=1)
nueva_incorporacion = st.checkbox("¿Es nueva incorporación?")
st.markdown("""</div>""", unsafe_allow_html=True)

# === B. OTRAS OPERACIONES ===
st.markdown("""<div class='input-section'>""", unsafe_allow_html=True)
st.markdown("### B. OTRAS OPERACIONES")
col_b1, col_b2 = st.columns(2)
with col_b1:
    compras = st.number_input("B.1 Nº de compras", min_value=0, step=1)
with col_b2:
    vh_cambio = st.number_input("B.2 VH como cambio", min_value=0, step=1)
st.markdown("""</div>""", unsafe_allow_html=True)

# === C. GARANTÍAS Y FINANCIACIÓN ===
st.markdown("""<div class='input-section'>""", unsafe_allow_html=True)
st.markdown("### C. GARANTÍAS Y FINANCIACIÓN")
col_c1, col_c2 = st.columns(2)
with col_c1:
    garantias_premium = st.number_input("C.1 Nº garantías premium", min_value=0, step=1)
    facturacion_garantias = st.number_input("C.2 Facturación garantías (€)", min_value=0, step=100)
with col_c2:
    beneficio_financiero = st.number_input("C.3 Beneficio financiero (€)", min_value=0, step=100)
    beneficio_financiacion_total = st.number_input("C.4 Total beneficio financiación (€)", min_value=0, step=100)
st.markdown("""</div>""", unsafe_allow_html=True)

# === D. BONIFICACIONES POR ENTREGA ===
st.markdown("""<div class='input-section'>""", unsafe_allow_html=True)
st.markdown("### D. BONIFICACIONES POR ENTREGA")
col_d1, col_d2, col_d3, col_d4 = st.columns(4)
with col_d1:
    entregas_con_financiacion = st.number_input("D.1 Con financiación", min_value=0, max_value=entregas, step=1)
with col_d2:
    entregas_rapidas = st.number_input("D.2 Entregas rápidas", min_value=0, max_value=entregas, step=1)
with col_d3:
    entregas_stock_largo = st.number_input("D.3 Stock >150 días", min_value=0, max_value=entregas, step=1)
with col_d4:
    entregas_con_descuento = st.number_input("D.4 Con descuento", min_value=0, max_value=entregas, step=1)
resenas = st.number_input("D.5 Nº de reseñas conseguidas", min_value=0, step=1)
st.markdown("""</div>""", unsafe_allow_html=True)

# Zona de resultados
st.markdown("""<div class='result-section'>""", unsafe_allow_html=True)
st.markdown("### RESULTADOS Y RESUMEN")
# Aquí irían los cálculos y el resumen
st.markdown("""</div>""", unsafe_allow_html=True)

