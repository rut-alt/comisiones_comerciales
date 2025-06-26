import streamlit as st
from PIL import Image

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# Fondo blanco y texto negro
st.markdown("""
    <style>
    .main {
        background-color: white !important;
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# Logo y título con estilo
logo = Image.open("LOGO-HRMOTOR-RGB.png")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color:#2b344d;'>CALCULADORA DE COMISIONES VENDEDORES</h1>", unsafe_allow_html=True)
with col2:
    st.image(logo, width=150)
nueva_incorporacion = st.checkbox("¿Es nueva incorporación?")
# BLOQUE A - ENTREGAS
st.markdown("### A. ENTREGAS")
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    entregas = st.number_input("A.1 Entregas totales", min_value=0, step=1)
with col_a2:
    entregas_otra_delegacion = st.number_input("A.2 Entregas en otra delegación", min_value=0, max_value=entregas, step=1)
with col_a3:
    entregas_compartidas = st.number_input("A.3 Entregas compartidas", min_value=0, max_value=entregas, step=1)

# BLOQUE B - OTRAS OPERACIONES
st.markdown("### B. OTRAS OPERACIONES")
col_b1, col_b2 = st.columns(2)
with col_b1:
    compras = st.number_input("B.1 Nº de compras", min_value=0, step=1)
with col_b2:
    vh_cambio = st.number_input("B.2 VH puesto a la venta como cambio", min_value=0, step=1)

# BLOQUE C - GARANTÍAS Y FINANCIACIÓN
st.markdown("### C. GARANTÍAS Y FINANCIACIÓN")
col_c1, col_c2 = st.columns(2)
with col_c1:
    garantias_premium = st.number_input("C.1 Nº garantías premium vendidas", min_value=0, step=1)
    facturacion_garantias = st.number_input("C.2 Facturación total garantías premium (€)", min_value=0, step=100)
with col_c2:
    beneficio_financiero = st.number_input("C.3 Beneficio financiero conseguido (€)", min_value=0, step=100)
    beneficio_financiacion_total = st.number_input("C.4 Importe total beneficio por financiación (€)", min_value=0, step=100)

# BLOQUE D - BONIFICACIONES POR ENTREGA (incluye reseñas)
st.markdown("### D. BONIFICACIONES POR ENTREGA")
col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns(5)
with col_d1:
    entregas_con_financiacion = st.number_input("D.1 Entregas con financiación", min_value=0, max_value=entregas, step=1)
with col_d2:
    entregas_rapidas = st.number_input("D.2 Entregas rápidas O express", min_value=0, max_value=entregas, step=1)
with col_d3:
    entregas_stock_largo = st.number_input("D.3 Entregas con +150 días de stock", min_value=0, max_value=entregas, step=1)
with col_d4:
    entregas_con_descuento = st.number_input("D.4 Entregas con descuento aplicado", min_value=0, max_value=entregas, step=1)
with col_d5:
    resenas = st.number_input("D.5 Nº de reseñas conseguidas", min_value=0, max_value=entregas, step=1)

# Funciones para cálculos
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

def calcular_comision_entregas(total_entregas, entregas_otra_delegacion, es_nueva):
    entregas_normales = total_entregas - entregas_otra_delegacion
    comision = 0
    tarifa_total = calcular_tarifa_entrega(total_entregas)

    if es_nueva and total_entregas <= 5:
        comision += entregas_normales * 20
        comision += entregas_otra_delegacion * 10
    elif not es_nueva and total_entregas <= 5:
        comision = 0
    else:
        comision += entregas_normales * tarifa_total
        comision += entregas_otra_delegacion * (tarifa_total * 0.5)

    return comision

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

# Cálculos principales
comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, nueva_incorporacion)
comision_compras = compras * 60
comision_vh_cambio = vh_cambio * 30

bono_financiacion = entregas_con_financiacion * 10
bono_entrega_rapida = entregas_rapidas * 5
bono_stock_largo = entregas_stock_largo * 5
penalizacion_descuento = entregas_con_descuento * -15

comision_sobre_beneficio = calcular_comision_por_beneficio(beneficio_financiacion_total)
bono_garantias = calcular_incentivo_garantias(facturacion_garantias)

bono_resenas = 0
if entregas > 0 and (resenas / entregas) >= 0.5:
    bono_resenas = resenas * 5

# Bonificación por ventas sobre PVP
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

# Suma antes de penalizaciones
prima_total = (
    comision_entregas + comision_compras + comision_vh_cambio + bono_financiacion + bono_entrega_rapida +
    bono_stock_largo + penalizacion_descuento + comision_sobre_beneficio + bono_resenas + bono_garantias + bono_ventas_sobre_pvp
)

# Penalizaciones desglosadas
penalizacion_total = 0
penalizaciones_detalle = []

if entregas > 0 and (garantias_premium / entregas) < 0.4:
    p = prima_total * 0.10
    penalizacion_total += p
    penalizaciones_detalle.append(("Garantías premium < 40%", p))
if entregas > 0 and (resenas / entregas) <= 0.5:
    p = prima_total * 0.10
    penalizacion_total += p
    penalizaciones_detalle.append(("Reseñas conseguidas ≤ 50%", p))
if beneficio_financiero < 4000:
    p = prima_total * 0.10
    penalizacion_total += p
    penalizaciones_detalle.append(("Beneficio financiero < 4000 €", p))

prima_final = prima_total - penalizacion_total

# Mostrar resultados
st.subheader("• Comisiones base")
st.write(f"Entregas: {comision_entregas:.2f} €")
st.write(f"Compras: {comision_compras:.2f} €")
st.write(f"VH cambio: {comision_vh_cambio:.2f} €")

st.subheader("• Bonificaciones y penalizaciones por entrega")
st.write(f"Bonificación por financiación: {bono_financiacion:.2f} €")
st.write(f"Bonificación por entrega rápida: {bono_entrega_rapida:.2f} €")
st.write(f"Bonificación por stock largo: {bono_stock_largo:.2f} €")
st.write(f"Bonificación por reseñas (>50%): {bono_resenas:.2f} €")
st.write(f"Penalización por descuentos: {penalizacion_descuento:.2f} €")


st.subheader("• Incentivos adicionales")
st.write(f"Comisión por beneficio financiero: {comision_sobre_beneficio:.2f} €")
st.write(f"Incentivo por garantías premium: {bono_garantias:.2f} €")
st.write(f"Bonificación por ventas sobre PVP: {bono_ventas_sobre_pvp:.2f} €")

st.markdown(f"### Prima total antes de penalizaciones: {prima_total:.2f} €")

if penalizacion_total > 0:
    st.markdown("""
        <div style='background-color: #ffcccc; padding: 15px; border: 2px solid red; border-radius: 10px;'>
        <h4 style='color: red;'>⚠️ Penalizaciones aplicadas</h4>
    """, unsafe_allow_html=True)

    for motivo, valor in penalizaciones_detalle:
        st.markdown(f"<p>🔸 {motivo}: <strong>-{valor:.2f} €</strong></p>", unsafe_allow_html=True)

    st.markdown(f"<p><strong>Total penalizaciones: -{penalizacion_total:.2f} €</strong></p></div>", unsafe_allow_html=True)

st.markdown(f"## ✅ Prima final a cobrar: **{prima_final:.2f} €**") 