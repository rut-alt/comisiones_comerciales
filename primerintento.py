import streamlit as st
from PIL import Image

# === FUNCIONES PARA RESETEAR EL FORMULARIO ===
if 'reset' not in st.session_state:
    st.session_state.reset = False

def reset_form():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# === FUNCIONES AUXILIARES DE ESCALADO ===
def siguiente_tramo_entregas(n):
    tramos = [5, 8, 11, 20, 25, 30]
    for limite in tramos:
        if n <= limite:
            return limite - n
    return 0

def siguiente_tramo_beneficio(b):
    tramos = [5000, 8000, 12000, 17000, 25000, 30000, 50000]
    for limite in tramos:
        if b <= limite:
            return limite - b
    return 0

# === CONFIGURACIÓN DE PÁGINA ===
st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# === ESTILO ===
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

# === CABECERA ===
logo = Image.open("LOGO-HRMOTOR-RGB.png")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color:#2b344d;'>CALCULADORA DE COMISIONES VENDEDORES</h1>", unsafe_allow_html=True)
with col2:
    st.image(logo, width=250)

# === BLOQUE DE ENTRADA ===
st.markdown("""<div class='input-section'>""", unsafe_allow_html=True)

# === A. ENTREGAS ===
st.markdown("### A. ENTREGAS")
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    entregas = st.number_input("A.1 Entregas totales", min_value=0, step=1)
with col_a2:
    entregas_otra_delegacion = st.number_input("A.2 En otra delegación", min_value=0, max_value=entregas, step=1)
with col_a3:
    entregas_compartidas = st.number_input("A.3 Entregas compartidas", min_value=0, max_value=entregas, step=1)

# Escalado de entregas
faltan = siguiente_tramo_entregas(entregas)
if faltan > 0:
    st.info(f"📊 Te faltan **{faltan} entregas** para subir al siguiente escalado de comisión.")
else:
    st.success("✅ ¡Ya estás en el escalado máximo!")

with st.expander("📊 Ver escalado de comisiones por entregas"):
    st.markdown("""
    - 1-5 entregas → 20 €/entrega  
    - 6-8 entregas → 20 €/entrega  
    - 9-11 entregas → 40 €/entrega  
    - 12-20 entregas → 60 €/entrega  
    - 21-25 entregas → 75 €/entrega  
    - 26-30 entregas → 80 €/entrega  
    - +30 entregas → 90 €/entrega  
    """)

nueva_incorporacion = st.checkbox("¿Es nueva incorporación?")

# === B. OTRAS OPERACIONES ===
st.markdown("### B. OTRAS OPERACIONES")
col_b1, col_b2 = st.columns(2)
with col_b1:
    compras = st.number_input("B.1 Nº de compras", min_value=0, step=1)
with col_b2:
    vh_cambio = st.number_input("B.2 VH como cambio", min_value=0, step=1)

# === C. GARANTÍAS Y FINANCIACIÓN ===
st.markdown("### C. GARANTÍAS Y FINANCIACIÓN")
col_c1, col_c2 = st.columns(2)
with col_c1:
    garantias_premium = st.number_input("C.1 Nº garantías premium", min_value=0, step=1)
    facturacion_garantias = st.number_input("C.2 Facturación garantías (€)", min_value=0, step=100)
with col_c2:
    beneficio_financiero = st.number_input("C.3 Beneficio financiero (€)", min_value=0, step=100)
    beneficio_financiacion_total = st.number_input("C.4 Total beneficio financiación (€)", min_value=0, step=100)

faltan_beneficio = siguiente_tramo_beneficio(beneficio_financiacion_total)
if faltan_beneficio > 0:
    st.info(f"📈 Te faltan **{faltan_beneficio:.2f} €** para alcanzar el siguiente tramo de comisión sobre beneficio financiero.")
else:
    st.success("✅ ¡Estás en el tramo máximo de beneficio!")

with st.expander("📈 Ver escalado de comisión sobre beneficio financiero"):
    st.markdown("""
    - Hasta 5.000 € → 2%  
    - Hasta 8.000 € → 3%  
    - Hasta 12.000 € → 4%  
    - Hasta 17.000 € → 5%  
    - Hasta 25.000 € → 6%  
    - Hasta 30.000 € → 7%  
    - Hasta 50.000 € → 8%  
    - Más de 50.000 € → 9%  
    """)

# === D. BONIFICACIONES POR ENTREGA ===
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

# === E. BONUS POR PVP ===
st.subheader("🚗 Bonificación por venta sobre precio de tarifa")
n_casos_venta_superior = st.number_input("¿Cuántas ventas han sido por encima del PVP?", min_value=0, step=1)
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

st.markdown("""</div>""", unsafe_allow_html=True)

# === FUNCIONES DE CÁLCULO ===
def calcular_tarifa_entrega(n):
    if n <= 5:
        return 20
    elif 6 <= n <= 8:
        return 20
    elif 9 <= n <= 11:
        return 40
    elif 12 <= n <= 20:
        return 

