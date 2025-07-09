import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Comisiones HRMOTOR", layout="centered")

# Estilos
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
    </style>
""", unsafe_allow_html=True)

# Cargar logo
try:
    logo = Image.open("LOGO-HRMOTOR-RGB.png")
except:
    logo = None

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color:#2b344d;'>ANÁLISIS DE DATOS - PRIMER EXCEL</h1>", unsafe_allow_html=True)
with col2:
    if logo:
        st.image(logo, width=250)

# Subida de archivo Excel
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("### 📂 Sube el archivo EXCEL de oportunidades (con entregas, cambios, compras...)")

uploaded_file = st.file_uploader("Sube un archivo XLSX con los campos: Opportunity Owner, Record Type, etc.", type=["xlsx"])
st.markdown("</div>", unsafe_allow_html=True)

# Función para limpiar campos tipo "EUR85,00"
def limpiar_eur(valor):
    try:
        return float(str(valor).replace("EUR", "").replace(".", "").replace(",", ".").strip())
    except:
        return 0.0

if uploaded_file is not None:
    # Leer el archivo Excel
    df = pd.read_excel(uploaded_file)

    # Normalizar nombres de columnas
    df.columns = df.columns.str.strip()

    # Limpiar campo de beneficio
    df["Beneficio financiación comercial"] = df["Beneficio financiación comercial"].apply(limpiar_eur)

    # Agrupaciones
    entregas = df[df["Opportunity Record Type"] == "Venta"].groupby("Opportunity Owner").size()
    compras = df[df["Opportunity Record Type"] == "Tasación"].groupby("Opportunity Owner").size()
    cambios = df[df["Opportunity Record Type"] == "Cambio"].groupby("Opportunity Owner").size()
    compartidas = df[df["Coopropietario de la Oportunidad"].notna() &
                     (df["Coopropietario de la Oportunidad"].astype(str).str.strip() != "")].groupby("Opportunity Owner").size()
    beneficios = df.groupby("Opportunity Owner")["Beneficio financiación comercial"].sum()

    # Unir todos los datos en un único resumen
    resumen_df = pd.DataFrame({
        "entregas": entregas,
        "compras": compras,
        "vh_cambio": cambios,
        "entregas_compartidas": compartidas,
        "beneficio_financiero": beneficios
    }).fillna(0).reset_index().rename(columns={"Opportunity Owner": "ownername"})

    # Mostrar el resumen
    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### 📊 Resumen extraído del Excel")
    st.dataframe(resumen_df)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Por favor, sube el archivo Excel (.xlsx) para comenzar.")
