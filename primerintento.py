import streamlit as st
from PIL import Image

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# --- Estilos generales ---
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

# --- Función para resetear el formulario ---
def resetear():
    for key in st.session_state.keys():
        # Evitar resetear el logo, pero sí inputs
        if key != 'logo':
            st.session_state[key] = None
    # Recargar app
    st.experimental_rerun()

# --- Botón Resetear ---
st.sidebar.button("🔄 Resetear formulario", on_click=resetear)

# --- Cargar y mostrar logo ---
try:
    logo = Image.open("LOGO-HRMOTOR-RGB.png")
except Exception:
    logo = None
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color:#2b344d;'>CALCULADORA DE COMISIONES VENDEDORES</h1>", unsafe_allow_html=True)
with col2:
    if logo:
        st.image(logo, width=250)

# === BLOQUE DE ENTRADA DE DATOS ===
st.markdown("<div class='input-section'>", unsafe_allow_html=True)

# === A. BLOQUE DE ENTREGAS ===
st.markdown("### A. ENTREGAS")
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    entregas = st.number_input("A.1 Entregas totales", min_value=0, step=1, key="entregas")
with col_a2:
    entregas_otra_delegacion = st.number_input("A.2 En otra delegación", min_value=0, max_value=st.session_state.entregas or 0, step=1, key="entregas_otra_delegacion")
with col_a3:
    entregas_compartidas = st.number_input("A.3 Entregas compartidas", min_value=0, max_value=st.session_state.entregas or 0, step=1, key="entregas_compartidas")
nueva_incorporacion = st.checkbox("¿Es nueva incorporación?", key="nueva_incorporacion")

# Expander con escalado entregas
with st.expander("ℹ️ Escalado de entregas y progreso hacia el siguiente nivel"):
    niveles_entregas = [
        (5, 20),
        (8, 20),
        (11, 40),
        (20, 60),
        (25, 75),
        (30, 80),
        (float('inf'), 90),
    ]
    e = st.session_state.entregas or 0
    for i, (limite, tarifa) in enumerate(niveles_entregas):
        if e <= limite:
            nivel_actual = (limite, tarifa)
            nivel_siguiente = niveles_entregas[i+1] if i+1 < len(niveles_entregas) else None
            break
    else:
        nivel_actual = niveles_entregas[-1]
        nivel_siguiente = None

    st.write(f"- Nivel actual: hasta {nivel_actual[0]} entregas → {nivel_actual[1]} € por unidad")
    if nivel_siguiente:
        faltan_unidades = nivel_siguiente[0] - e
        if faltan_unidades > 0:
            st.write(f"- Quedan **{faltan_unidades} entregas** para alcanzar el siguiente nivel: hasta {nivel_siguiente[0]} entregas → {nivel_siguiente[1]} € por unidad")
        else:
            st.write("- Has alcanzado el máximo nivel de entregas.")
    else:
        st.write("- Has alcanzado el máximo nivel de entregas.")

# === B. OTRAS OPERACIONES ===
st.markdown("### B. OTRAS OPERACIONES")
col_b1, col_b2 = st.columns(2)
with col_b1:
    compras = st.number_input("B.1 Nº de compras", min_value=0, step=1, key="compras")
with col_b2:
    vh_cambio = st.number_input("B.2 VH como cambio", min_value=0, step=1, key="vh_cambio")

# === C. GARANTÍAS Y FINANCIACIÓN ===
st.markdown("### C. GARANTÍAS Y FINANCIACIÓN")
col_c1, col_c2 = st.columns(2)
with col_c1:
    garantias_premium = st.number_input("C.1 Nº garantías premium", min_value=0, step=1, key="garantias_premium")
    facturacion_garantias = st.number_input("C.2 Facturación garantías (€)", min_value=0, step=100, key="facturacion_garantias")
with col_c2:
    beneficio_financiero = st.number_input("C.3 Beneficio financiero (€)", min_value=0, step=100, key="beneficio_financiero")
    beneficio_financiacion_total = st.number_input("C.4 Total beneficio financiación (€)", min_value=0, step=100, key="beneficio_financiacion_total")

# Expander con escalado beneficio financiero
with st.expander("ℹ️ Escalado de beneficio financiero y progreso hacia el siguiente nivel"):
    niveles_beneficio = [
        (5000, 0.02),
        (8000, 0.03),
        (12000, 0.04),
        (17000, 0.05),
        (25000, 0.06),
        (30000, 0.07),
        (50000, 0.08),
        (float('inf'), 0.09),
    ]
    b = st.session_state.beneficio_financiero or 0
    for i, (limite, porcentaje) in enumerate(niveles_beneficio):
        if b <= limite:
            nivel_actual_b = (limite, porcentaje)
            nivel_siguiente_b = niveles_beneficio[i+1] if i+1 < len(niveles_beneficio) else None
            break
    else:
        nivel_actual_b = niveles_beneficio[-1]
        nivel_siguiente_b = None

    st.write(f"- Nivel actual: hasta {nivel_actual_b[0]} € → {nivel_actual_b[1]*100:.1f}% de comisión")
    if nivel_siguiente_b:
        faltan_euros = nivel_siguiente_b[0] - b
        if faltan_euros > 0:
            st.write(f"- Faltan **{faltan_euros:.2f} €** para alcanzar el siguiente nivel: hasta {nivel_siguiente_b[0]} € → {nivel_siguiente_b[1]*100:.1f}% de comisión")
        else:
            st.write("- Has alcanzado el máximo nivel de beneficio financiero.")
    else:
        st.write("- Has alcanzado el máximo nivel de beneficio financiero.")

# === D. BONIFICACIONES POR ENTREGA ===
st.markdown("### D. BONIFICACIONES POR ENTREGA")
col_d1, col_d2, col_d3, col_d4 = st.columns(4)
with col_d1:
    entregas_con_financiacion = st.number_input("D.1 Con financiación", min_value=0, max_value=st.session_state.entregas or 0, step=1, key="entregas_con_financiacion")
with col_d2:
    entregas_rapidas = st.number_input("D.2 Entregas rápidas", min_value=0, max_value=st.session_state.entregas or 0, step=1, key="entregas_rapidas")
with col_d3:
    entregas_stock_largo = st.number_input("D.3 Stock >150 días", min_value=0, max_value=st.session_state.entregas or 0, step=1, key="entregas_stock_largo")
with col_d4:
    entregas_con_descuento = st.number_input("D.4 Con descuento", min_value=0, max_value=st.session_state.entregas or 0, step=1, key="entregas_con_descuento")
resenas = st.number_input("D.5 Nº de reseñas conseguidas", min_value=0, step=1, key="resenas")

# Bonificación por ventas sobre PVP
st.subheader("🚗 Bonificación por venta sobre precio de tarifa")
n_casos_venta_superior = st.number_input("¿Cuántas ventas han sido por encima del PVP?", min_value=0, step=1, key="n_casos_venta_superior")
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

# === BLOQUE DE RESULTADOS ===
st.markdown("<div class='result-section'>", unsafe_allow_html=True)
st.markdown("### RESUMEN Y RESULTADO DE LA COMISIÓN")

# Funciones de cálculo

def calcular_tarifa_entrega(n):
    if n <= 5:
        return 20
    elif 6 <= n <= 8:
        return 20
    elif 9 <= n <= 11:
        return 40
    elif 12 <= n <= 20:
        return 60
    elif 21 <= n <= 25:
        return 75
    elif 26 <= n <= 30:
        return 80
    else:
        return 90

def calcular_comision_entregas(total, otras, nueva):
    normales = total - otras
    tarifa = calcular_tarifa_entrega(total)
    if nueva and total <= 5:
        return normales * 20 + otras * 10
    elif not nueva and total <= 5:
        return 0
    else:
        return normales * tarifa + otras * (tarifa * 0.5)

def calcular_comision_por_beneficio(b):
    if b <= 5000:
        return b * 0.02
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

def calcular_incentivo_garantias(f):
    if f <= 4500:
        return f * 0.03
    elif f <= 8000:
        return f * 0.05
    elif f <= 12000:
        return f * 0.06
    elif f <= 17000:
        return f * 0.08
    else:
        return f * 0.10

# Cálculos
comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, nueva_incorporacion)
comision_compras = compras * 60
comision_vh_cambio = vh_cambio * 30
bono_financiacion = entregas_con_financiacion * 10
bono_rapida = entregas_rapidas * 5
bono_stock = entregas_stock_largo * 5
penalizacion_descuento = entregas_con_descuento * -15
comision_beneficio = calcular_comision_por


ChatGPT Plus
_beneficio(beneficio_financiacion_total)
bono_garantias = calcular_incentivo_garantias(facturacion_garantias)
bono_resenas = resenas * 5 if entregas > 0 and resenas / entregas >= 0.5 else 0
comision_entregas_compartidas = entregas_compartidas * 30

prima_total = sum([
comision_entregas, comision_entregas_compartidas, comision_compras, comision_vh_cambio,
bono_financiacion, bono_rapida, bono_stock, penalizacion_descuento,
comision_beneficio, bono_garantias, bono_resenas, bono_ventas_sobre_pvp
])

Penalizaciones
penalizacion_total = 0
penalizaciones_detalle = []
if entregas > 0 and garantias_premium / entregas < 0.4:
p = prima_total * 0.10
penalizacion_total += p
penalizaciones_detalle.append(("Garantías premium < 40%", p))
if entregas > 0 and resenas / entregas <= 0.5:
p = prima_total * 0.10
penalizacion_total += p
penalizaciones_detalle.append(("Reseñas ≤ 50%", p))
if beneficio_financiero < 4000:
p = prima_total * 0.10
penalizacion_total += p
penalizaciones_detalle.append(("Beneficio financiero < 4000 €", p))

prima_final = prima_total - penalizacion_total

Mostrar desglose
st.subheader("🧾 Desglose de la Prima Total")
st.markdown(f"Comisión por entregas: {comision_entregas:.2f} €")
st.markdown(f"Comisión por entregas compartidas: {comision_entregas_compartidas:.2f} €")
st.markdown(f"Comisión por compras: {comision_compras:.2f} €")
st.markdown(f"Comisión por VH cambio: {comision_vh_cambio:.2f} €")
st.markdown(f"Comisión sobre beneficio financiero: {comision_beneficio:.2f} €")
st.markdown(f"Bonificación por financiación: {bono_financiacion:.2f} €")
st.markdown(f"Bonificación por entrega rápida: {bono_rapida:.2f} €")
st.markdown(f"Bonificación por stock >150 días: {bono_stock:.2f} €")
st.markdown(f"Bonificación por garantías premium: {bono_garantias:.2f} €")
st.markdown(f"Bonificación por reseñas: {bono_resenas:.2f} €")
st.markdown(f"Bonificación por ventas sobre PVP: {bono_ventas_sobre_pvp:.2f} €")
st.markdown(f"Penalización por entregas con descuento: {penalizacion_descuento:.2f} €")

st.markdown(f"### ✔ Prima total antes de penalizaciones = {prima_total:.2f} €")

if penalizaciones_detalle:
st.markdown("""
<div style='background-color: #ffcccc; padding: 15px; border: 2px solid red; border-radius: 10px;'>
<h4 style='color: red;'>⚠️ Penalizaciones aplicadas</h4>
""", unsafe_allow_html=True)
for motivo, valor in penalizaciones_detalle:
st.markdown(f"<p>🔸 <strong>{motivo}</strong>: -{valor:.2f} €</p>", unsafe_allow_html=True)
st.markdown(f"<p><strong>Total penalizaciones: -{penalizacion_total:.2f} €</strong></p></div>", unsafe_allow_html=True)
else:
st.info("No se aplican penalizaciones.")

st.markdown(f"## ✅ Prima final a cobrar = {prima_final:.2f} €")
st.markdown("</div>", unsafe_allow_html=True)