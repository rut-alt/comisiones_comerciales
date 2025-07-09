import streamlit as st
from PIL import Image
import pandas as pd

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

try:
    logo = Image.open("LOGO-HRMOTOR-RGB.png")
except:
    logo = None

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color:#2b344d;'>CALCULADORA DE COMISIONES VENDEDORES</h1>", unsafe_allow_html=True)
with col2:
    if logo:
        st.image(logo, width=250)

st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("### 📂 Cargar archivo Excel con oportunidades")
uploaded_file = st.file_uploader("Sube un archivo .xlsx", type=["xlsx"])
st.markdown("</div>", unsafe_allow_html=True)

# Limpieza segura de importes con formato europeo
def limpiar_eur(valor):
    try:
        s = str(valor).replace("EUR", "").replace("€", "").replace(" ", "").strip()
        s = s.replace(".", "").replace(",", ".")
        return float(s) if s else 0.0
    except:
        return 0.0

# --- FUNCIONES DE COMISIÓN ---
def calcular_tarifa_entrega_vendedor(n): ...
def calcular_tarifa_entrega_jefe(n): ...
def calcular_comision_entregas(total, otras, es_nuevo, es_jefe): ...
def calcular_comision_por_beneficio(b): ...
def calcular_incentivo_garantias(f): ...

# ✅ NUEVA: Comisión por compras de tasador
def comision_compras_tasador(n):
    if n <= 7: return 0
    elif 8 <= n <= 10: return n * 30
    elif 11 <= n <= 15: return n * 60
    elif 16 <= n <= 20: return n * 65
    elif 21 <= n <= 25: return n * 70
    elif 26 <= n <= 30: return n * 75
    elif 31 <= n <= 35: return n * 80
    else: return n * 85

# ✅ NUEVA: Comisión beneficio financiación para tasadores
def comision_beneficio_tasador(b):
    return b * 0.03 if b > 0 else 0

# ✅ NUEVA: Función principal de cálculo para tasadores
def calcular_comision_tasador(fila):
    entregas = int(fila.get("entregas", 0))
    compras = int(fila.get("compras", 0))
    beneficio_financiacion_total = float(fila.get("beneficio_financiacion_total", 0))

    comision_ventas = entregas * 60
    comision_compras = comision_compras_tasador(compras)
    comision_beneficio = comision_beneficio_tasador(beneficio_financiacion_total)

    prima_total = comision_ventas + comision_compras + comision_beneficio

    return {
        'prima_total': prima_total,
        'prima_final': prima_total,  # sin penalizaciones por ahora
        'penalizaciones_detalle': [],
        'desglose': {
            'comision_ventas': comision_ventas,
            'comision_compras': comision_compras,
            'comision_beneficio': comision_beneficio
        }
    }
def calcular_comision_fila(fila, es_nuevo, es_jefe): 
    # (Tu función anterior completa, sin cambios)
    ...

if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    if "Delegación" not in df_raw.columns:
        df_raw["Delegación"] = df_raw.iloc[:, -1]
    else:
        df_raw["Delegación"] = df_raw["Delegación"]

    entregas = df_raw[df_raw["Opportunity Record Type"] == "Venta"].groupby("Opportunity Owner").size()
    compras = df_raw[df_raw["Opportunity Record Type"] == "Tasación"].groupby("Opportunity Owner").size()
    beneficio_financiacion_total = df_raw.groupby("Opportunity Owner")["Beneficio financiación comercial"].sum()
    delegacion_por_owner = df_raw.groupby("Opportunity Owner")["Delegación"].first()

    resumen = pd.DataFrame({
        "ownername": beneficio_financiacion_total.index,
        "entregas": entregas,
        "compras": compras,
        "beneficio_financiacion_total": beneficio_financiacion_total,
        "delegacion": delegacion_por_owner
    }).fillna(0).reset_index(drop=True)

    seleccion_delegacion = st.selectbox("Filtrar por Delegación", ["Todas"] + sorted(resumen["delegacion"].dropna().unique().tolist()))
    if seleccion_delegacion != "Todas":
        resumen = resumen[resumen["delegacion"] == seleccion_delegacion]

    seleccion_comercial = st.selectbox("Filtrar por Comercial", ["Todos"] + sorted(resumen["ownername"].unique().tolist()))
    if seleccion_comercial != "Todos":
        resumen = resumen[resumen["ownername"] == seleccion_comercial]

    resumen = resumen.sort_values(by=["delegacion", "ownername"]).reset_index(drop=True)

    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### Resultados por Comercial")

    for idx, row in resumen.iterrows():
        owner = row["ownername"]
        key_nuevo = f"nuevo_{owner}"
        key_jefe = f"jefe_{owner}"
        key_tasador = f"tasador_{owner}"

        if key_nuevo not in st.session_state:
            st.session_state[key_nuevo] = False
        if key_jefe not in st.session_state:
            st.session_state[key_jefe] = False
        if key_tasador not in st.session_state:
            st.session_state[key_tasador] = False

        cols = st.columns([1, 1, 1])
        nuevo_flag = cols[0].checkbox("Nuevo incorporación", key=key_nuevo)
        jefe_flag = cols[1].checkbox("Jefe de tienda", key=key_jefe)
        tasador_flag = cols[2].checkbox("Tasador", key=key_tasador)

        if tasador_flag:
            resultado = calcular_comision_tasador(row)
        else:
            resultado = calcular_comision_fila(row, nuevo_flag, jefe_flag)

        st.markdown(f"## Comercial: **{owner}**")
        st.markdown(f"- Delegación: {row['delegacion']}")
        st.markdown(f"- Prima total antes de penalizaciones: {resultado['prima_total']:.2f} €")
        st.markdown(f"- Prima final a cobrar: **{resultado['prima_final']:.2f} €**")
        st.markdown("**Desglose de conceptos:**")
        for k, v in resultado['desglose'].items():
            st.markdown(f"  - {k.replace('_', ' ').capitalize()}: {v:.2f} €")
        if resultado['penalizaciones_detalle']:
            st.markdown("**Penalizaciones:**")
            for pen in resultado['penalizaciones_detalle']:
                st.markdown(f"  - {pen[0]}: {pen[1]:.2f} €")
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
