import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# Estilos visuales
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
    .result-section {
        background-color: #2b344d;
        color: white !important;
        padding: 20px;
        border-radius: 10px;
        margin-top: 25px;
        border: 1px solid #cce5ff;
    }
    </style>
""", unsafe_allow_html=True)

# Logo
try:
    logo = Image.open("LOGO-HRMOTOR-RGB.png")
except:
    logo = None

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color:#2b344d;'>CALCULADORA DE COMISIONES VENDEDORES</h1>", unsafe_allow_html=True)
with col2:
    if logo:
        st.image(logo, width=250)

# Sección carga archivo
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("### 📂 Cargar archivo Excel con oportunidades")
uploaded_file = st.file_uploader("Sube un archivo .xlsx", type=["xlsx"])
st.markdown("</div>", unsafe_allow_html=True)

# Función limpiar EUR

def limpiar_eur(valor):
    try:
        s = str(valor).strip()
        s = s.replace("EUR", "").replace("€", "").strip()
        s = s.replace(".", "")  # quitar separador miles
        s = s.replace(",", ".")  # cambiar coma decimal a punto
        return float(s)
    except:
        return 0.0

# Función comisiones beneficio según escalado
def calcular_comision_por_beneficio(b):
    if b <= 5000:
        return 0
    elif b <= 8000:
        return b * 0.03
    elif b <= 12000:
        return b * 0.04
    elif b <= 17000:
        return b * 0.05
    elif b <= 25000:
        return b * 0.06
    elif b <= 30000:
        return b * 0.07
    elif b <= 50000:
        return b * 0.08
    else:
        return b * 0.09

# Si se sube archivo
if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Convertimos columna de beneficio
    df["Beneficio financiación comercial"] = df["Beneficio financiación comercial"].apply(limpiar_eur)

    # Agrupar por comercial y delegación
    resumen = df.groupby(["Opportunity Owner", "Delegación"])["Beneficio financiación comercial"].sum().reset_index()
    resumen["comision_beneficio"] = resumen["Beneficio financiación comercial"].apply(calcular_comision_por_beneficio)

    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### Resultados por Comercial")

    for _, fila in resumen.iterrows():
        st.markdown(f"#### Delegación: {fila['Delegación']}")
        st.markdown(f"**Comercial:** {fila['Opportunity Owner']}")
        st.markdown(f"- Beneficio total: {fila['Beneficio financiación comercial']:.2f} €")
        st.markdown(f"- Comision beneficio: **{fila['comision_beneficio']:.2f} €**")
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
