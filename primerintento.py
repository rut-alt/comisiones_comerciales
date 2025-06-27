import streamlit as st
from PIL import Image

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# --- Botón de Reset seguro ---
def resetear():
    for key in list(st.session_state.keys()):
        if not key.startswith("logo"):  # si usas claves tipo 'logo', puedes excluirlas
            del st.session_state[key]
    st.experimental_rerun()

# Mostrar botón arriba a la derecha
col_reset, _ = st.columns([1, 6])
with col_reset:
    st.button("🔄 Resetear formulario", on_click=resetear)

# Logo y cabecera
try:
    logo = Image.open("LOGO-HRMOTOR-RGB.png")
except:
    logo = None
col1, col2 = st.columns([3, 1])
with col1:
    st.title("CALCULADORA DE COMISIONES VENDEDORES")
with col2:
    if logo:
        st.image(logo, width=150)

st.markdown("<div class='input-section'>", unsafe_allow_html=True)

# === A. ENTREGAS ===
st.subheader("A. Entregas")
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    e = st.number_input("Totales", min_value=0, step=1, key="entregas")
with col_a2:
    st.number_input("En otra delegación", min_value=0, max_value=e, step=1, key="entregas_otra_delegacion")
with col_a3:
    st.number_input("Compartidas", min_value=0, max_value=e, step=1, key="entregas_compartidas")
st.checkbox("¿Nueva incorporación?", key="nueva")

with st.expander("ℹ️ Escalado entregas"):
    niveles = [(5, 20), (8, 20), (11, 40), (20, 60), (25, 75), (30, 80), (float('inf'), 90)]
    for i, (lim, tarifa) in enumerate(niveles):
        if e <= lim:
            st.write(f"Nivel actual: hasta {lim} → {tarifa}€/unidad")
            if i + 1 < len(niveles):
                falta = niveles[i+1][0] - e
                st.info(f"Faltan {falta} entregas para llegar al siguiente tramo ({niveles[i+1][1]}€/unidad)")
            else:
                st.success("Has alcanzado el nivel máximo de entregas ✅")
            break

# === B. OPERACIONES ===
st.subheader("B. Otras operaciones")
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.number_input("Compras", min_value=0, step=1, key="compras")
with col_b2:
    st.number_input("VH como cambio", min_value=0, step=1, key="vh_cambio")

# === C. GARANTÍAS Y FINANCIACIÓN ===
st.subheader("C. Garantías y financiación")
col_c1, col_c2 = st.columns(2)
with col_c1:
    st.number_input("Garantías premium", min_value=0, step=1, key="garantias_premium")
    st.number_input("Facturación garantías (€)", min_value=0, step=100, key="fact_garantias")
with col_c2:
    bf = st.number_input("Beneficio financiero (€)", min_value=0, step=100, key="benef_fin")
    st.number_input("Beneficio financiación total (€)", min_value=0, step=100, key="benef_fin_tot")

with st.expander("ℹ️ Escalado beneficio financiero"):
    niveles_bf = [(5000, 0.02), (8000, 0.03), (12000, 0.04), (17000, 0.05),
                  (25000, 0.06), (30000, 0.07), (50000, 0.08), (float('inf'), 0.09)]
    for i, (lim, pct) in enumerate(niveles_bf):
        if bf <= lim:
            st.write(f"Nivel actual: hasta {lim}€ → {pct*100:.1f}%")
            if i + 1 < len(niveles_bf):
                falta_bf = niveles_bf[i+1][0] - bf
                st.info(f"Faltan {falta_bf:.2f} € para el siguiente tramo ({niveles_bf[i+1][1]*100:.1f}%)")
            else:
                st.success("Has alcanzado el nivel máximo ✅")
            break

# === D. BONIFICACIONES ===
st.subheader("D. Bonificaciones por entrega")
col_d1, col_d2, col_d3, col_d4 = st.columns(4)
with col_d1:
    st.number_input("Con financiación", min_value=0, max_value=e, key="ent_fin")
with col_d2:
    st.number_input("Entregas rápidas", min_value=0, max_value=e, key="ent_rap")
with col_d3:
    st.number_input("Stock >150 días", min_value=0, max_value=e, key="ent_stock")
with col_d4:
    st.number_input("Con descuento", min_value=0, max_value=e, key="ent_desc")
res = st.number_input("Nº de reseñas", min_value=0, step=1, key="resenas")

# === E. VENTA SOBRE PVP ===
st.subheader("E. Bonificación por PVP")
n_pvp = st.number_input("Nº ventas por encima de PVP", min_value=0, step=1, key="n_pvp")
bono_pvp = 0
for i in range(n_pvp):
    pvp = st.number_input(f"PVP coche {i+1}", min_value=0, step=100, key=f"pvp{i}")
    venta = st.number_input(f"Venta coche {i+1}", min_value=0, step=100, key=f"venta{i}")
    if venta > pvp:
        bono = (venta - pvp) * 0.05
        bono_pvp += bono
        st.success(f"Bono coche {i+1}: {bono:.2f}€")
    else:
        st.warning("❌ Sin bonificación (venta ≤ PVP)")

st.markdown("</div>", unsafe_allow_html=True)

# === CÁLCULOS ===
def tarifa_entregas(n):
    if n <= 5: return 20
    elif n <= 8: return 20
    elif n <= 11: return 40
    elif n <= 20: return 60
    elif n <= 25: return 75
    elif n <= 30: return 80
    return 90

def com_entregas(n, otras, nueva):
    normales = n - otras
    tarifa = tarifa_entregas(n)
    if nueva and n <= 5: return normales * 20 + otras * 10
    if not nueva and n <= 5: return 0
    return normales * tarifa + otras * (tarifa * 0.5)

def com_beneficio(b):
    if b <= 5000: return b * 0.02
    elif b <= 8000: return b * 0.03
    elif b <= 12000: return b * 0.04
    elif b <= 17000: return b * 0.05
    elif b <= 25000: return b * 0.06
    elif b <= 30000: return b * 0.07
    elif b <= 50000: return b * 0.08
    return b * 0.09

def inc_garantias(f):
    if f <= 4500: return f * 0.03
    elif f <= 8000: return f * 0.05
    elif f <= 12000: return f * 0.06
    elif f <= 17000: return f * 0.08
    return f * 0.10

# Totales
ce = com_entregas(e, st.session_state["entregas_otra_delegacion"], st.session_state["nueva"])
cec = st.session_state["entregas_compartidas"] * 30
cc = st.session_state["compras"] * 60
ch = st.session_state["vh_cambio"] * 30
cf = com_beneficio(st.session_state["benef_fin_tot"])
cg = inc_garantias(st.session_state["fact_garantias"])
cr = res * 5 if e > 0 and res / e >= 0.5 else 0
bf1 = st.session_state["ent_fin"] * 10
bf2 = st.session_state["ent_rap"] * 5
bf3 = st.session_state["ent_stock"] * 5
pen_desc = st.session_state["ent_desc"] * -15

prima = sum([ce, cec, cc, ch, cf, cg, cr, bf1, bf2, bf3, pen_desc, bono_pvp])

# Penalizaciones
penal = 0
if e > 0 and st.session_state["garantias_premium"] / e < 0.4:
    penal += prima * 0.1
if e > 0 and res / e <= 0.5:
    penal += prima * 0.1
if st.session_state["benef_fin"] < 4000:
    penal += prima * 0.1
prima_final = prima - penal

# === RESULTADOS ===
st.markdown("<div class='result-section'>", unsafe_allow_html=True)
st.subheader("🧾 Resultado final")
st.markdown(f"- Comisión entregas: {ce:.2f} €")
st.markdown(f"- Entregas compartidas: {cec:.2f} €")
st.markdown(f"- Compras: {cc:.2f} €")
st.markdown(f"- VH cambio: {ch:.2f} €")
st.markdown(f"- Financiación total: {cf:.2f} €")
st.markdown(f"- Garantías: {cg:.2f} €")
st.markdown(f"- Reseñas: {cr:.2f} €")
st.markdown(f"- Bonos (fin, rápida, stock): {bf1+bf2+bf3:.2f} €")
st.markdown(f"- Bonificación PVP: {bono_pvp:.2f} €")
st.markdown(f"- Penalización descuento: {pen_desc:.2f} €")
st.markdown(f"**Prima total antes de penalizaciones: {prima:.2f} €**")

if penal > 0:
    st.error(f"Penalizaciones aplicadas: -{penal:.2f} €")
else:
    st.success("✅ Sin penalizaciones")

st.markdown(f"## ✅ Prima final: **{prima_final:.2f} €**")
st.markdown("</div>", unsafe_allow_html=True)
