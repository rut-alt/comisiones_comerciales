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

# Cargar y mostrar logo
logo = Image.open("LOGO-HRMOTOR-RGB.png")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color:#2b344d;'>CALCULADORA DE COMISIONES VENDEDORES</h1>", unsafe_allow_html=True)
with col2:
    st.image(logo, width=250)

# --- Entradas ---
nueva_incorporacion = st.checkbox("¿Es nueva incorporación?")
entregas = st.number_input("Nº de entregas totales", min_value=0, step=1)
entregas_otra_delegacion = st.number_input("Entregas en otra delegación", min_value=0, max_value=entregas, step=1)
entregas_compartidas = st.number_input("Entregas compartidas", min_value=0, max_value=entregas, step=1)
compras = st.number_input("Nº de compras", min_value=0, step=1)
vh_cambio = st.number_input("VH puesto a la venta como cambio", min_value=0, step=1)
garantias_premium = st.number_input("Nº de garantías premium vendidas", min_value=0, step=1)
facturacion_garantias = st.number_input("Facturación total en garantías premium (€)", min_value=0, step=100)
resenas = st.number_input("Nº de reseñas conseseguidas", min_value=0, step=1)
beneficio_financiero = st.number_input("Beneficio financiero conseguido (€)", min_value=0, step=100)
entregas_con_financiacion = st.number_input("Entregas con financiación", min_value=0, max_value=entregas, step=1)
entregas_rapidas = st.number_input("Entregas rápidas", min_value=0, max_value=entregas, step=1)
entregas_stock_largo = st.number_input("Entregas con +150 días de stock", min_value=0, max_value=entregas, step=1)
entregas_con_descuento = st.number_input("Entregas con descuento aplicado", min_value=0, max_value=entregas, step=1)
beneficio_financiacion_total = st.number_input("Importe total de beneficio por financiación (€)", min_value=0, step=100)

# --- Funciones ---
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

def calcular_comision_entregas(total, otra_delegacion, es_nueva):
    delegacion = total - otra_delegacion
    comision = 0

    if es_nueva and total <= 5:
        # Si es nueva y total ≤5, cobra todo a 20€
        comision += delegacion * 20
        comision += otra_delegacion * 10
    else:
        # Entregas de su delegación según tramos reales
        tramos = [
            (6, 8, 20),
            (9, 11, 40),
            (12, 20, 60),
            (21, 25, 75),
            (26, 30, 80),
            (31, float("inf"), 90),
        ]

        entregas_restantes = delegacion
        for inicio, fin, tarifa in tramos:
            if entregas_restantes >= inicio:
                cantidad = min(entregas_restantes, fin) - inicio + 1
                comision += cantidad * tarifa

        # Las entregas en otra delegación se pagan al 50% del tramo total
        tarifa_total = calcular_tarifa_entrega(total)
        comision += otra_delegacion * (tarifa_total * 0.5)

        # Bonificación extra si es nueva por entregas 1-5
        if es_nueva and total > 5:
            primeras_5 = min(5, delegacion)
            comision += primeras_5 * 20

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

# --- Cálculos principales ---
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
if entregas > 0 and (resenas / entregas) > 0.5:
    bono_resenas = resenas * 5

# --- Bonificación por ventas sobre PVP ---
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

# --- Prima total ---
prima_total = (
    comision_entregas +
    comision_compras +
    comision_vh_cambio +
    bono_financiacion +
    bono_entrega_rapida +
    bono_stock_largo +
    penalizacion_descuento +
    comision_sobre_beneficio +
    bono_resenas +
    bono_garantias +
    bono_ventas_sobre_pvp
)

# Penalizaciones
penalizacion_total = 0
detalles_penalizaciones = []

if entregas > 0 and (garantias_premium / entregas) < 0.4:
    penalizacion_total += prima_total * 0.10
    detalles_penalizaciones.append("🔻 Garantías premium <40%")

if entregas > 0 and (resenas / entregas) <= 0.5:
    penalizacion_total += prima_total * 0.10
    detalles_penalizaciones.append("🔻 Reseñas ≤ 50%")

if beneficio_financiero < 4000:
    penalizacion_total += prima_total * 0.10
    detalles_penalizaciones.append("🔻 Beneficio financiero <4000 €")

prima_final = prima_total - penalizacion_total

# --- Mostrar resultados ---
st.subheader("💶 Comisiones base")
st.write(f"Entregas: {comision_entregas:.2f} €")
st.write(f"Compras: {comision_compras:.2f} €")
st.write(f"VH cambio: {comision_vh_cambio:.2f} €")

st.subheader("📌 Bonificaciones y penalizaciones por entrega")
st.write(f"Bonificación por financiación: {bono_financiacion:.2f} €")
st.write(f"Bonificación por entrega rápida: {bono_entrega_rapida:.2f} €")
st.write(f"Bonificación por stock largo: {bono_stock_largo:.2f} €")
st.write(f"Penalización por descuentos: {penalizacion_descuento:.2f} €")

st.subheader("📈 Incentivos adicionales")
st.write(f"Comisión por beneficio financiero: {comision_sobre_beneficio:.2f} €")
st.write(f"Bonificación por reseñas (>50%): {bono_resenas:.2f} €")
st.write(f"Incentivo por garantías premium: {bono_garantias:.2f} €")
st.write(f"Bonificación por ventas sobre PVP: {bono_ventas_sobre_pvp:.2f} €")

st.markdown(f"### 💰 Prima total antes de penalizaciones: {prima_total:.2f} €")

if detalles_penalizaciones:
    st.subheader("⚠️ Penalizaciones aplicadas")
    for p in detalles_penalizaciones:
        st.write(p)
    st.write(f"Total penalizaciones: {penalizacion_total:.2f} €")

st.markdown(f"## ✅ Prima final a cobrar: **{prima_final:.2f} €**")
