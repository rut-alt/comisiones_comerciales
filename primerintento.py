import streamlit as st
from PIL import Image

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# Estilos
st.markdown("""
    <style>
    .input-section { background-color: #2b344d; color: white; padding:20px; border-radius:10px; margin-bottom:25px; }
    .result-section { background-color: #2b344d; color: white; padding:20px; border-radius:10px; margin-top:25px; }
    </style>
""", unsafe_allow_html=True)

# Función reset
def resetear():
    for key in list(st.session_state.keys()):
        if not key.startswith("logo"):
            del st.session_state[key]
    st.experimental_rerun()

st.sidebar.button("🔄 Resetear formulario", on_click=resetear)

# Logo y cabecera
try:
    logo = Image.open("LOGO-HRMOTOR-RGB.png")
except:
    logo = None
col1, col2 = st.columns([3,1])
with col1:
    st.title("CALCULADORA DE COMISIONES VENDEDORES")
with col2:
    if logo: st.image(logo, width=150)

st.markdown("<div class='input-section'>", unsafe_allow_html=True)

# A. ENTREGAS
st.subheader("A. Entregas")
e = st.number_input("A.1 Entregas totales", min_value=0, step=1, key="entregas")
st.number_input("A.2 En otra delegación", min_value=0, max_value=st.session_state.get("entregas",0), step=1, key="entregas_otra_delegacion")
st.number_input("A.3 Entregas compartidas", min_value=0, max_value=st.session_state.get("entregas",0), step=1, key="entregas_compartidas")
nueva = st.checkbox("¿Nueva incorporación?", key="nueva")

# Expander entregas
with st.expander("ℹ️ Escalado de entregas"):
    niveles_e = [(5,20),(8,20),(11,40),(20,60),(25,75),(30,80),(float('inf'),90)]
    nivel_sig_e = None
    for i,(lim,tar) in enumerate(niveles_e):
        if e <= lim:
            nivel_sig_e = niveles_e[i+1] if i+1<len(niveles_e) else None
            st.write(f"Nivel actual: hasta {lim} → {tar}€/unidad")
            break
    if nivel_sig_e:
        falt_e = nivel_sig_e[0] - e
        st.write(f"Faltan {falt_e} entregas para el siguiente nivel ({nivel_sig_e[1]}€/unidad)")
    else:
        st.success("Has alcanzado el nivel máximo de entregas ✅")

# B. OPERACIONES
st.subheader("B. Otras operaciones")
st.number_input("B.1 Nº de compras", min_value=0, step=1, key="compras")
st.number_input("B.2 VH como cambio", min_value=0, step=1, key="vh_cambio")

# C. GARANTIAS & FINANCIACIÓN
st.subheader("C. Garantías y financiación")
st.number_input("C.1 Nº garantías premium", min_value=0, step=1, key="garantias_premium")
st.number_input("C.2 Facturas garantías (€)", min_value=0, step=100, key="fact_garantias")
b = st.number_input("C.3 Beneficio financiero (€)", min_value=0, step=100, key="benef_fin")
st.number_input("C.4 Beneficio financiación total (€)", min_value=0, step=100, key="benef_fin_tot")

# Expander financiación
with st.expander("ℹ️ Escalado de financiación"):
    niveles_b = [(5000,0.02),(8000,0.03),(12000,0.04),(17000,0.05),(25000,0.06),(30000,0.07),(50000,0.08),(float('inf'),0.09)]
    nivel_sig_b = None
    for i,(lim,pct) in enumerate(niveles_b):
        if b <= lim:
            nivel_sig_b = niveles_b[i+1] if i+1<len(niveles_b) else None
            st.write(f"Nivel actual: hasta {lim} → {pct*100:.1f}%")
            break
    if nivel_sig_b:
        falt_b = nivel_sig_b[0] - b
        st.write(f"Faltan {falt_b:.2f} € para el siguiente nivel ({nivel_sig_b[1]*100:.1f}%)")
    else:
        st.success("Has alcanzado el nivel máximo de financiación ✅")

# D. BONIFICACIONES
st.subheader("D. Bonificaciones por entrega")
st.number_input("D.1 Con financiación", min_value=0, max_value=st.session_state.get("entregas",0), key="ent_fin")
st.number_input("D.2 Entregas rápidas", min_value=0, max_value=st.session_state.get("entregas",0), key="ent_rap")
st.number_input("D.3 Stock >150 días", min_value=0, max_value=st.session_state.get("entregas",0), key="ent_stock")
st.number_input("D.4 Con descuento", min_value=0, max_value=st.session_state.get("entregas",0), key="ent_desc")
res = st.number_input("D.5 Nº de reseñas conseguidas", min_value=0, step=1, key="resenas")

# E. Bonus PVP
st.subheader("E. Bonificación por PVP")
n_pvp = st.number_input("¿Cuántos casos por encima del PVP?", min_value=0, step=1, key="n_pvp")
bono_pvp = 0
for i in range(n_pvp):
    p = st.number_input(f"PVP coche {i+1}", min_value=0, step=100, key=f"pvp{i}")
    v = st.number_input(f"Venta coche {i+1}", min_value=0, step=100, key=f"vta{i}")
    if v>p:
        bono = (v-p)*0.05
        bono_pvp += bono
        st.success(f"Bono coche {i+1}: {bono:.2f}€")

st.markdown("</div>", unsafe_allow_html=True)

# Funciones cálculo
def tarifa_ent(n):
    if n<=5: return 20
    if n<=8: return 20
    if n<=11: return 40
    if n<=20: return 60
    if n<=25: return 75
    if n<=30: return 80
    return 90

def com_ent(n,o,nw):
    t = tarifa_ent(n)
    norm = n - o
    if nw and n<=5: return norm*20 + o*10
    if not nw and n<=5: return 0
    return norm*t + o*(t*0.5)

def com_ben(b):
    if b<=5000: return b*0.02
    if b<=8000: return b*0.03
    if b<=12000: return b*0.04
    if b<=17000: return b*0.05
    if b<=25000: return b*0.06
    if b<=30000: return b*0.07
    if b<=50000: return b*0.08
    return b*0.09

def inc_gar(f):
    if f<=4500: return f*0.03
    if f<=8000: return f*0.05
    if f<=12000: return f*0.06
    if f<=17000: return f*0.08
    return f*0.10

# Valores
ce = com_ent(e, st.session_state.get("entregas_otra_delegacion",0), st.session_state.get("nueva",False))
cc = st.session_state.get("compras",0)*60
ch = st.session_state.get("vh_cambio",0)*30
bf = com_ben(st.session_state.get("benef_fin_tot",0))
bg = inc_gar(st.session_state.get("fact_garantias",0))
br = res*5 if e>0 and res/e>=0.5 else 0
cef = st.session_state.get("ent_fin",0)*10
cer = st.session_state.get("ent_rap",0)*5
ces = st.session_state.get("ent_stock",0)*5
ced = st.session_state.get("ent_desc",0)*-15
cec = st.session_state.get("entregas_compartidas",0)*30

prima = sum([ce,cec,cc,ch,bf,bg,br,cef,cer,ces,ced,bono_pvp])

# Penalizaciones
pen = 0
det = []
if e>0 and st.session_state.get("garantias_premium",0)/e<0.4:
    p = prima*0.1; pen+=p; det.append(("Garantías<40%",p))
if e>0 and res/e<=0.5:
    p = prima*0.1; pen+=p; det.append(("Reseñas≤50%",p))
if st.session_state.get("benef_fin",0)<4000:
    p = prima*0.1; pen+=p; det.append(("Beneficio<4000€",p))

final = prima - pen

# Resultados
st.markdown("<div class='result-section'>", unsafe_allow_html=True)
st.subheader("🧾 Resumen")
st.write(f"- Comisión entregas: {ce:.2f}€")
st.write(f"- Entregas compartidas: {cec:.2f}€")
st.write(f"- Compras: {cc:.2f}€")
st.write(f"- VH cambio: {ch:.2f}€")
st.write(f"- Sobre beneficio: {bf:.2f}€")
st.write(f"- Garantías premium: {bg:.2f}€")
st.write(f"- Reseñas: {br:.2f}€")
st.write(f"- Financiación entrega: {cef:.2f}€")
st.write(f"- Entrega rápida: {cer:.2f}€")
st.write(f"- Stock largo: {ces:.2f}€")
st.write(f"- Penalización descuento: {ced:.2f}€")
st.write(f"- Bono PVP: {bono_pvp:.2f}€")
st.write(f"**Prima total antes penalizaciones**: {prima:.2f}€")
if det:
    st.warning("⚠️ Penalizaciones:")
    for motivo,v in det:
        st.write(f"• {motivo}: -{v:.2f}€")
st.write(f"## ✅ Prima final: {final:.2f}€")
st.markdown("</div>", unsafe_allow_html=True)
