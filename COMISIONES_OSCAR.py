import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

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

# Subida de Excel
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("### 📂 Cargar archivo Excel con oportunidades")
uploaded_file = st.file_uploader("Sube un archivo .xlsx", type=["xlsx"])
st.markdown("</div>", unsafe_allow_html=True)

# Función limpieza
def limpiar_eur(valor):
    try:
        return float(str(valor).replace("EUR", "").replace(".", "").replace(",", ".").strip())
    except:
        return 0.0

# FUNCIONES DE CÁLCULO (idénticas a las tuyas)
# [...] Aquí irían tus funciones calcular_tarifa_entrega, calcular_comision_entregas, etc.
# Las omito para brevedad en este mensaje (me confirmas si las pego de nuevo o las tienes)

# ⬇️ Nos centramos en rellenar los campos necesarios automáticamente desde el Excel

if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()  # limpiar espacios

    # Limpiar el campo beneficio
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    # Crear resumen por Opportunity Owner
    resumen = pd.DataFrame()
    resumen["ownername"] = df_raw["Opportunity Owner"].dropna().unique()
    resumen = resumen.set_index("ownername")

    # Entregas = tipo Venta
    entregas = df_raw[df_raw["Opportunity Record Type"] == "Venta"].groupby("Opportunity Owner").size()
    resumen["entregas"] = entregas

    # Entregas compartidas = hay copropietario
    compartidas = df_raw[df_raw["Coopropietario de la Oportunidad"].notna() & (df_raw["Coopropietario de la Oportunidad"] != "")].groupby("Opportunity Owner").size()
    resumen["entregas_compartidas"] = compartidas

    # Compras = tipo Tasación
    compras = df_raw[df_raw["Opportunity Record Type"] == "Tasación"].groupby("Opportunity Owner").size()
    resumen["compras"] = compras

    # VH como cambio = tipo Cambio
    cambios = df_raw[df_raw["Opportunity Record Type"] == "Cambio"].groupby("Opportunity Owner").size()
    resumen["vh_cambio"] = cambios

    # Con descuento = descuento marcado como algo distinto a vacío o nulo
    con_descuento = df_raw[df_raw["Descuento"].notna() & (df_raw["Descuento"].astype(str).str.strip() != "")].groupby("Opportunity Owner").size()
    resumen["entregas_con_descuento"] = con_descuento

    # Beneficio financiero
    beneficio = df_raw.groupby("Opportunity Owner")["Beneficio financiación comercial"].sum()
    resumen["beneficio_financiero"] = beneficio

    # Rellenar columnas faltantes con ceros
    for col in [
        "entregas", "entregas_compartidas", "compras", "vh_cambio", "beneficio_financiero", "entregas_con_descuento"
    ]:
        if col not in resumen:
            resumen[col] = 0
    resumen.fillna(0, inplace=True)

    # Agregar columnas que aún no tenemos pero necesita la función
    resumen["nueva_incorporacion"] = False
    resumen["facturacion_garantias"] = 0
    resumen["beneficio_financiacion_total"] = resumen["beneficio_financiero"]
    resumen["entregas_con_financiacion"] = 0
    resumen["entregas_rapidas"] = 0
    resumen["entregas_stock_largo"] = 0
    resumen["resenas"] = 0
    resumen["garantias_premium"] = 0
    resumen["n_casos_venta_superior"] = 0

    # Convertimos a DataFrame plano
    resumen = resumen.reset_index()

    # Aplicamos tu lógica
    resultados = []
    for _, fila in resumen.iterrows():
        resultado = calcular_comision_fila(fila)
        resultados.append({
            'ownername': fila['ownername'],
            'prima_final': resultado['prima_final'],
            'prima_total': resultado['prima_total'],
            'penalizaciones_detalle': resultado['penalizaciones_detalle'],
            'desglose': resultado['desglose']
        })

    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### Resultados por Comercial")

    for r in resultados:
        st.markdown(f"## Comercial: **{r['ownername']}**")
        st.markdown(f"### Prima total antes de penalizaciones: {r['prima_total']:.2f} €")
        st.markdown(f"### Prima final a cobrar: **{r['prima_final']:.2f} €**")
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")

