# ...

# --- Mostrar resultados dentro de bloque azul ---
st.markdown("<div class='input-blue-block'>", unsafe_allow_html=True)
st.markdown("<h3>RESUMEN Y RESULTADO</h3>")

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

st.markdown(f"### ✔Prima total antes de penalizaciones: {prima_total:.2f} €")

if penalizacion_total > 0:
    st.markdown("""
        <div style='background-color: #ffcccc; padding: 15px; border: 2px solid red; border-radius: 10px;'>
        <h4 style='color: red;'>⚠️ Penalizaciones aplicadas</h4>
    """, unsafe_allow_html=True)

    for motivo, valor in penalizaciones_detalle:
        st.markdown(f"<p>🔸 {motivo}: <strong>-{valor:.2f} €</strong></p>", unsafe_allow_html=True)

    st.markdown(f"<p><strong>Total penalizaciones: -{penalizacion_total:.2f} €</strong></p></div>", unsafe_allow_html=True)

st.markdown(f"## ✅ Prima final a cobrar: **{prima_final:.2f} €**")
st.markdown("</div>", unsafe_allow_html=True)  # Cerrar div azul
