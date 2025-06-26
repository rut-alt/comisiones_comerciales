import streamlit as st

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")
st.title("🧮 Calculadora de Comisiones de Vendedores")

# Entrada de datos generales
nueva_incorporacion = st.checkbox("¿Es nueva incorporación?")

entregas = st.number_input("Nº de entregas totales", min_value=0, step=1)
entregas_otra_delegacion = st.number_input("Entregas en otra delegación", min_value=0, max_value=entregas, step=1)
entregas_compartidas = st.number_input("Entregas compartidas", min_value=0, max_value=entregas, step=1)
compras = st.number_input("Nº de compras", min_value=0, step=1)
vh_cambio = st.number_input("VH puesto a la venta como cambio", min_value=0, step=1)

# Penalizaciones y bonificaciones
garantias_premium = st.number_input("Nº de garantías premium vendidas", min_value=0, step=1)
facturacion_garantias = st.number_input("Facturación total en garantías premium (€)", min_value=0, step=100)
resenas = st.number_input("Nº de reseñas conseguidas", min_value=0, step=1)
beneficio_financiero = st.number_input("Beneficio financiero conseguido (€)", min_value=0, step=100)

# Bonificaciones y penalizaciones por entrega
entregas_con_financiacion = st.number_input("Entregas con financiación", min_value=0, max_value=entregas, step=1)
entregas_rapidas = st.number_input("Entregas rápidas", min_value=0, max_value=entregas, step=1)
entregas_stock_largo = st.number_input("Entregas con +150 días de stock", min_value=0, max_value=entregas, step=1)
entregas_con_descuento = st.number_input("Entregas con descuento aplicado", min_value=0, max_value=entregas, step=1)

# NUEVA ENTRADA: Importe beneficio de financiación
beneficio_financiacion_total = st.number_input("Importe total de beneficio por financiación (€)", min_value=0, step=100)


# ------------------ FUNCIONES ------------------

def calcular_comision_entregas(total, compartidas, otra_delegacion, es_nueva):
    comision = 0
    entregas_normales = total - compartidas - otra_delegacion

    if es_nueva and total <= 5:
        comision += total * 20
        return comision

    tramos = [
        (6, 8, 20),
        (9, 11, 40),
        (12, 20, 60),
        (21, 25, 75),
        (26, 30, 80),
        (31, float("inf"), 90),
    ]

    entregas_restantes = entregas_normales
    for inicio, fin, tarifa in tramos:
        if entregas_restantes >= inicio:
            cantidad = min(entregas_restantes, fin) - inicio + 1
            comision += cantidad * tarifa

    tarifa_aplicable = calcular_tarifa_entrega(total)
    comision += compartidas * (tarifa_aplicable * 0.5)
    comision += otra_delegacion * (tarifa_aplicable * 0.5)

    return comision

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


# ------------------ CÁLCULOS ------------------

comision_entregas = calcular_comision_entregas(entregas, entregas_compartidas, entregas_otra_delegacion, nueva_incorporacion)
comision_compras = compras * 60
comision_vh_cambio = vh_cambio * 30

# Bonificaciones / penalizaciones por entrega
bono_financiacion = entregas_con_financiacion * 10
bono_entrega_rapida = entregas_rapidas * 5
bono_stock_largo = entregas_stock_largo * 5
penalizacion_descuento = entregas_con_descuento * -15

# Comisión adicional por beneficio financiación
comision_sobre_beneficio = calcular_comision_por_beneficio(beneficio_financiacion_total)

# Bonificación por garantías premium (facturación)
bono_garantias = calcular_incentivo_garantias(facturacion_garantias)

# Bonificación por reseñas (>50%)
bono_resenas = 0
if entregas > 0:
    porcentaje_resenas = resenas / entregas
    if porcentaje_resenas > 0.5:
        bono_resenas = resenas * 5

# Bonificación por vender por encima del PVP
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

# Penalizaciones rendimiento
penalizacion_total = 0
detalles_penalizaciones = []

if entregas > 0 and (garantias_premium / entregas) < 0.4:
    p = prima_total * 0.10
    penalizacion_total += p
    detalles_penalizaciones.append("🔻 Garantías premium <40%")

if entregas > 0 and (resenas / entregas) <= 0.5:
    p = prima_total * 0.10
    penalizacion_total += p
    detalles_penalizaciones.append("🔻 Reseñas ≤ 50%")

if beneficio_financiero < 4000:
    p = prima_total * 0.10
    penalizacion_total += p
    detalles_penalizaciones.append("🔻 Beneficio financiero <4000 €")

# Resultado final
prima_final = prima_total - penalizacion_total


# ------------------ MOSTRAR RESULTADOS ------------------

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
