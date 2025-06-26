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
    df = pd.read_csv(uploaded_file)
    datos = df.iloc[0].to_dict()
else:
    datos = {}

# Entradas automáticas con valores por defecto desde CSV si existe
get_val = lambda key, default=0: int(datos.get(key, default))
get_bool = lambda key: bool(datos.get(key, False))

# === A. BLOQUE DE ENTREGAS ===
st.markdown("### A. ENTREGAS")
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    entregas = st.number_input("A.1 Entregas totales", min_value=0, step=1, value=get_val("entregas"))
with col_a2:
    entregas_otra_delegacion = st.number_input("A.2 En otra delegación", min_value=0, max_value=entregas, step=1, value=get_val("entregas_otra_delegacion"))
with col_a3:
    entregas_compartidas = st.number_input("A.3 Entregas compartidas", min_value=0, max_value=entregas, step=1, value=get_val("entregas_compartidas"))
nueva_incorporacion = st.checkbox("¿Es nueva incorporación?", value=get_bool("nueva_incorporacion"))

# El resto del formulario continúa igual...

st.markdown("""</div>""", unsafe_allow_html=True)

# (Resto del código sin cambios, se mantiene lógica de cálculo y presentación)
# Solo cambia la parte de inputs para que los valores vengan pre-cargados desde el CSV




