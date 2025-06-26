import streamlit as st
import pandas as pd
from PIL import Image

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

# Logo
logo = Image.open("LOGO-HRMOTOR-RGB.png")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color:#2b344d;'>CALCULADORA DE COMISIONES VENDEDORES</h1>", unsafe_allow_html=True)
with col2:
    st.image(logo, width=250)

# === BLOQUE DE ENTRADA DE DATOS ===
st.markdown("""<div class='input-section'>""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📎 Sube un archivo CSV con los datos del vendedor", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    datos = df.iloc[0].to_dict()
else:
    datos = {}

# Helpers
get_val = lambda key, default=0: int(datos.get(key, default))
get_float = lambda key, default=0: float(datos.get(key, default))
get_bool = lambda key: bool(int(datos.get(key))) if key in datos else False

# === A. ENTREGAS ===
st.markdown("### A. ENTREGAS")
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    entregas = st.number_input("A.1 Entregas totales", min_value=0, step=1, value=get_val("entregas"))
with col_a2:
    entregas_otra_delegacion = st.number_input("A.2 En otra delegación", min_value=0, max_value=entregas, step=1, value=get_val("entregas_otra_delegacion"))
with col_a3:
    entregas_compartidas = st.number_input("A.3 Entregas compartidas", min_value=0, max_value=entregas, step=1, value=get_val("entregas_compartidas"))
nueva_incorporacion = st.checkbox("¿Es nueva incorporación?", value=get_bool("nueva_incorporacion"))

# === B. OTRAS OPERACIONES ===
st.markdown("### B. OTRAS OPERACIONES")
col_b1, col_b2 = st.columns(2)
with col_b1:
    compras = st.number_input("B.1 Nº de compras", min_value=0, step=1, value=get_val("compras"))
with col_b2:
    vh_cambio = st.number_input("B.2 VH como cambio", min_value=0, step=1, value=get_val("vh_cambio"))

# === C. GARANTÍAS Y FINANCIACIÓN ===
st.markdown("### C. GARANTÍAS Y FINANCIACIÓN")
col_c1, col_c2 = st.columns(2)
with col_c1:
    garantias_premium = st.number_input("C.1 Nº garantías premium", min_value=0, step=1, value=get_val("garantias_premium"))
    facturacion_garantias = st.number_input("C.2 Facturación garantías (€)", min_value=0, step=100, value=get_float("facturacion_garantias"))
with col_c2:
    beneficio_financiero = st.number_input("C.3 Beneficio financiero (€)", min_value=0, step=100, value=get_float("beneficio_financiero"))
    beneficio_financiacion_total = st.number_input("C.4 Total beneficio financiación (€)", min_value=0, step=100, value=get_float("beneficio_financiacion_total"))

# === D. BONIFICACIONES POR ENTREGA ===
st.markdown("### D. BONIFICACIONES POR ENTREGA")
col_d1, col_d2, col_d3, col_d4 = st.columns(4)
with col_d1:
    entregas_con_financiacion = st.number_input("D.1 Con financiación", min_value=0, max_value=entregas, step=1, value=get_val("entregas_con_financiacion"))
with col_d2:
    entregas_rapidas = st.number_input("D.2 Entregas rápidas", min_value=0, max_value=entregas, step=1, value=get_val("entregas_rapidas"))
with col_d3:
    entregas_stock_largo = st.number_input("D.3 Stock >150 días", min_value=0, max_value=entregas, step=1, value=get_val("entregas_stock_largo"))
with col_d4:
    entregas_con_descuento = st.number_input("D.4 Con descuento", min_value=0, max_value=entregas, step=1, value=get_val("entregas_con_descuento"))
resenas = st.number_input("D.5 Nº de reseñas conseguidas", min_value=0, step=1, value=get_val("resenas"))

# === E. VENTAS SOBRE PVP ===
st.subheader("🚗 Bonificación por venta sobre precio de tarifa")
n_casos_venta_superior = st.number_input("¿Cuántas ventas han sido por encima del PVP?", min_value=0, step=1, value=get_val("ventas_sobre_pvp"))
bono_ventas_sobre_pvp = 0

for i in range(n_casos_venta_superior):
    st.markdown(f"**Coche {i+1}**")
    pvp = st.number_input(f"→ PVP recomendado coche {i+1} (€)", min_value=0, step=100, key=f"pvp_{i}")
    precio_final = st.number_input(f"→ Precio final de venta coche {i+1} (€)", min_value=0, step=100, key=f"venta_{i}")

    if precio_final > pvp:
        diferencia = precio_final - pvp
        bono = diferencia * 0.05
        bono_ventas_sobre_pvp += bono
        st.success(f"✅ Bonificación por este coche: {bono:.2f} €")
    else:
        st.warning("❌ No hay bonificación: no supera el PVP.")

st.markdown("</div>", unsafe_allow_html=True)

# === RESULTADOS (idéntico al tuyo, sigue abajo) ===
# Puedes copiar el bloque final de resultados desde tu código actual sin modificar nada





