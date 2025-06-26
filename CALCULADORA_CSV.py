import streamlit as st
import pandas as pd
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

# Cargar archivo CSV y extraer datos
st.markdown("""<div class='input-section'>""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Sube un archivo CSV con los datos del vendedor", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, thousands=',')
    datos = df.iloc[0].to_dict()
else:
    datos = {}

# Funciones de extracción con tipos adecuados
get_int = lambda key, default=0: int(datos.get(key, default))
get_float = lambda key, default=0.0: float(str(datos.get(key, default)).replace(',', '.'))
get_bool = lambda key: bool(int(datos.get(key, 0)))

# === A. BLOQUE DE ENTREGAS ===
st.markdown("### A. ENTREGAS")
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    entregas = st.number_input("A.1 Entregas totales", min_value=0, step=1, value=get_int("entregas"))
with col_a2:
    entregas_otra_delegacion = st.number_input("A.2 En otra delegación", min_value=0, max_value=entregas, step=1, value=get_int("entregas_otra_delegacion"))
with col_a3:
    entregas_compartidas = st.number_input("A.3 Entregas compartidas", min_value=0, max_value=entregas, step=1, value=get_int("entregas_compartidas"))
nueva_incorporacion = st.checkbox("¿Es nueva incorporación?", value=get_bool("nueva_incorporacion"))

# === B. OTRAS OPERACIONES ===
st.markdown("### B. OTRAS OPERACIONES")
col_b1, col_b2 = st.columns(2)
with col_b1:
    compras = st.number_input("B.1 Nº de compras", min_value=0, step=1, value=get_int("compras"))
with col_b2:
    vh_cambio = st.number_input("B.2 VH como cambio", min_value=0, step=1, value=get_int("vh_cambio"))

# === C. GARANTÍAS Y FINANCIACIÓN ===
st.markdown("### C. GARANTÍAS Y FINANCIACIÓN")
col_c1, col_c2 = st.columns(2)
with col_c1:
    garantias_premium = st.number_input("C.1 Nº garantías premium", min_value=0, step=1, value=get_int("garantias_premium"))
    facturacion_garantias = st.number_input("C.2 Facturación garantías (€)", min_value=0.0, step=100.0, value=get_float("facturacion_garantias"))
with col_c2:
    beneficio_financiero = st.number_input("C.3 Beneficio financiero (€)", min_value=0.0, step=100.0, value=get_float("beneficio_financiero"))
    beneficio_financiacion_total = st.number_input("C.4 Total beneficio financiación (€)", min_value=0.0, step=100.0, value=get_float("beneficio_financiacion_total"))

st.markdown("""</div>""", unsafe_allow_html=True)

# (Resto del código sin cambios, se mantiene lógica de cálculo y presentación)
