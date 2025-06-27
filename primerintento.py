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

# === BLOQUE DE RESULTADOS ===
st.markdown("""<div class='result-section'>""", unsafe_allow_html=True)
st.markdown("### RESUMEN Y RESULTADO DE LA COMISIÓN")

comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, nueva_incorporacion)
comision_entregas_compartidas = entregas_compartidas * 30
comision_compras = compras * 60
comision_vh_cambio = vh_cambio * 30
bono_financiacion = entregas_con_financiacion * 10
bono_rapida = entregas_rapidas * 5
bono_stock = entregas_stock_largo * 5
penalizacion_descuento = entregas_con_descuento * -15
comision_beneficio = calcular_comision_por_beneficio(beneficio_financiacion_total)
bono_garantias = calcular_incentivo_garantias(facturacion_garantias)
bono_resenas = resenas * 5 if entregas > 0 and resenas / entregas >= 0.5 else 0

prima_total = sum([
    comision_entregas,
    comision_entregas_compartidas,
    comision_compras,
    comision_vh_cambio,
    bono_financiacion,
    bono_rapida,
    bono_stock,
    penalizacion_descuento,
    comision_beneficio,
    bono_garantias,
    bono_resenas,
    bono_ventas_sobre_pvp
])

# Penalizaciones
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

# === MOSTRAR RESULTADOS ===
st.subheader("🧾 Desglose de la Prima Total")
st.markdown(f"**Comisión** por entregas: {comision_entregas:.2f} €")
st.markdown(f"**Comisión** por entregas compartidas: {comision_entregas_compartidas:.2f} €")
st.markdown(f"**Comisión** por compras: {comision_compras:.2f} €")
st.markdown(f"**Comisión** por VH como cambio: {comision_vh_cambio:.2f} €")
st.markdown(f"**Bonificación** por financiación: {bono_financiacion:.2f} €")
st.markdown(f"**Bonificación** por entregas rápidas: {bono_rapida:.2f} €")
st.markdown(f"**Bonificación** por stock >150 días: {bono_stock:.2f} €")
st.markdown(f"**Penalización** por entregas con descuento: {penalizacion_descuento:.2f} €")
st.markdown(f"**Comisión** sobre beneficio financiero: {comision_beneficio:.2f} €")
st.markdown(f"**Bonificación** por garantías premium: {bono_garantias:.2f} €")
st.markdown(f"**Bonificación** por reseñas: {bono_resenas:.2f} €")
st.markdown(f"**Bonificación** por ventas sobre PVP: {bono_ventas_sobre_pvp:.2f} €")

st.markdown(f"### 💰 Prima total antes de penalizaciones: **{prima_total:.2f} €**")

if penalizaciones_detalle:
    st.markdown("""
        <div style='background-color: #ffcccc; padding: 15px; border: 2px solid red; border-radius: 10px;'>
        <h4 style='color: red;'>⚠️ Penalizaciones aplicadas</h4>
    """, unsafe_allow_html=True)
    for motivo, valor in penalizaciones_detalle:
        st.markdown(f"<p>🔸 <strong>{motivo}</strong>: -{valor:.2f} €</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Total penalizaciones: -{penalizacion_total:.2f} €</strong></p></div>", unsafe_allow_html=True)
else:
    st.info("✅ No se aplican penalizaciones.")

st.markdown(f"## ✅ Prima final a cobrar = **{prima_final:.2f} €**")

# === BOTÓN DE REINICIO ===
st.markdown("---")
if st.button("🔄 Reiniciar formulario"):
    reset_form()

st.markdown("""</div>""", unsafe_allow_html=True)
