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

# === Cargar archivo Excel comisiones ===
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("### 📂 Cargar archivo Excel con oportunidades")
uploaded_file = st.file_uploader("Sube un archivo .xlsx", type=["xlsx"])
st.markdown("</div>", unsafe_allow_html=True)

# === Funciones ===
def limpiar_eur(valor):
    try:
        s = str(valor).replace("EUR", "").replace("€", "").replace(" ", "").strip()
        s = s.replace(".", "").replace(",", ".")
        return float(s) if s else 0.0
    except:
        return 0.0

def calcular_tarifa_entrega_vendedor(n):
    if n <= 6: return 0
    elif n <= 9: return 20
    elif n <= 11: return 40
    elif n <= 15: return 60
    elif n <= 20: return 65
    elif n <= 25: return 75
    elif n <= 30: return 80
    elif n <= 35: return 90
    else: return 95

def calcular_tarifa_entrega_jefe(n):
    if n <= 6: return 20
    elif n <= 9: return 20
    elif n <= 11: return 40
    elif n <= 15: return 60
    elif n <= 20: return 65
    elif n <= 25: return 75
    elif n <= 30: return 80
    elif n <= 35: return 90
    else: return 95

def calcular_comision_entregas(total, otras, es_nuevo, es_jefe):
    normales = total - otras
    if es_jefe:
        tarifa = calcular_tarifa_entrega_jefe(total)
        return normales * tarifa + otras * (tarifa * 0.5)
    else:
        tarifa = calcular_tarifa_entrega_vendedor(total)
        if es_nuevo and total <= 6:
            return normales * 20 + otras * 10
        elif not es_nuevo and total <= 6:
            return 0
        else:
            return normales * tarifa + otras * (tarifa * 0.5)

def calcular_comision_por_beneficio(b):
    if b <= 5000: return 0
    elif b <= 8000: return b * 0.03
    elif b <= 12000: return b * 0.04
    elif b <= 17000: return b * 0.05
    elif b <= 25000: return b * 0.06
    elif b <= 30000: return b * 0.07
    elif b <= 50000: return b * 0.08
    else: return b * 0.09

def calcular_incentivo_garantias(f):
    if f <= 4500: return f * 0.03
    elif f <= 8000: return f * 0.05
    elif f <= 12000: return f * 0.06
    elif f <= 17000: return f * 0.08
    else: return f * 0.10

def calcular_comision_fila(fila, es_nuevo, es_jefe):
    entregas = int(fila.get('entregas', 0))
    entregas_otra_delegacion = int(fila.get('entregas_otra_delegacion', 0))
    entregas_compartidas = int(fila.get('entregas_compartidas', 0))
    compras = int(fila.get('compras', 0))
    vh_cambio = int(fila.get('vh_cambio', 0))
    garantias_premium = int(fila.get('garantias_premium', 0))
    facturacion_garantias = float(fila.get('facturacion_garantias', 0))
    beneficio_financiacion_total = float(fila.get('beneficio_financiacion_total', 0))
    entregas_con_financiacion = int(fila.get('entregas_con_financiacion', 0))
    entregas_rapidas = int(fila.get('entregas_rapidas', 0))
    entregas_stock_largo = int(fila.get('entregas_stock_largo', 0))
    entregas_con_descuento = int(fila.get('entregas_con_descuento', 0))
    resenas = int(fila.get('resenas', 0))
    n_casos_venta_superior = int(fila.get('n_casos_venta_superior', 0))

    bono_ventas_sobre_pvp = 0

    comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, es_nuevo, es_jefe)
    comision_compras = compras * 60
    comision_vh_cambio = vh_cambio * 30
    bono_financiacion = entregas_con_financiacion * 10
    bono_rapida = entregas_rapidas * 5
    bono_stock = entregas_stock_largo * 5
    penalizacion_descuento = entregas_con_descuento * -15
    comision_beneficio = calcular_comision_por_beneficio(beneficio_financiacion_total)
    bono_garantias = calcular_incentivo_garantias(facturacion_garantias)
    bono_resenas = resenas * 5 if entregas > 0 and (resenas / entregas) >= 0.5 else 0
    comision_entregas_compartidas = entregas_compartidas * 30

    prima_total = sum([
        comision_entregas, comision_entregas_compartidas, comision_compras, comision_vh_cambio,
        bono_financiacion, bono_rapida, bono_stock, penalizacion_descuento,
        comision_beneficio, bono_garantias, bono_resenas, bono_ventas_sobre_pvp
    ])

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
    if beneficio_financiacion_total < 4000:
        p = prima_total * 0.10
        penalizacion_total += p
        penalizaciones_detalle.append(("Beneficio financiero < 4000 €", p))

    prima_final = prima_total - penalizacion_total

    return {
        'prima_total': prima_total,
        'prima_final': prima_final,
        'penalizaciones_detalle': penalizaciones_detalle,
        'desglose': {
            'comision_entregas': comision_entregas,
            'comision_entregas_compartidas': comision_entregas_compartidas,
            'comision_compras': comision_compras,
            'comision_vh_cambio': comision_vh_cambio,
            'comision_beneficio': comision_beneficio,
            'bono_financiacion': bono_financiacion,
            'bono_rapida': bono_rapida,
            'bono_stock': bono_stock,
            'bono_garantias': bono_garantias,
            'bono_resenas': bono_resenas,
            'penalizacion_descuento': penalizacion_descuento
        }
    }

# === Proceso Principal ===
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    comerciales = df['nombre'].dropna().unique().tolist()
    comerciales.sort()

    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    seleccion_comercial = st.selectbox("Selecciona un comercial", ["Todos"] + comerciales)
    st.markdown("</div>", unsafe_allow_html=True)

    df_filtrado = df if seleccion_comercial == "Todos" else df[df["nombre"] == seleccion_comercial]

    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    for _, fila in df_filtrado.iterrows():
        nombre = fila.get("nombre", "Desconocido")
        es_nuevo = bool(fila.get("es_nuevo", False))
        es_jefe = bool(fila.get("es_jefe", False))

        resultado = calcular_comision_fila(fila, es_nuevo, es_jefe)

        st.markdown(f"### {nombre}")
        st.markdown(f"- Prima total sin penalizaciones: {resultado['prima_total']:.2f} €")
        st.markdown(f"- Penalizaciones: {sum(p[1] for p in resultado['penalizaciones_detalle']):.2f} €")
        for detalle, valor in resultado['penalizaciones_detalle']:
            st.markdown(f"  - {detalle}: {valor:.2f} €")
        st.markdown(f"#### 👉 Prima final: **{resultado['prima_final']:.2f} €**")
    st.markdown("</div>", unsafe_allow_html=True)

# === Segundo archivo: oportunidades stock largo ===
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("### 📂 Cargar archivo Excel de oportunidades en stock largo")
uploaded_stock_file = st.file_uploader("Sube archivo con oportunidades (stock largo >150 días)", type=["xlsx"], key="stock")
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_stock_file is not None:
    df_stock = pd.read_excel(uploaded_stock_file)
    df_stock.columns = df_stock.columns.str.strip()
    df_stock_filtrado = df_stock[df_stock["dias en stock"] > 150]

    filas_por_comercial = df_stock_filtrado.groupby("Opportunity Owner").size().reset_index(name="filas_stock_mayor_150")

    if seleccion_comercial != "Todos":
        filas_por_comercial = filas_por_comercial[filas_por_comercial["Opportunity Owner"] == seleccion_comercial]

    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### Filas con días en stock > 150 por Comercial")
    if not filas_por_comercial.empty:
        for _, row in filas_por_comercial.iterrows():
            st.markdown(f"- Comercial: **{row['Opportunity Owner']}** → Filas con stock >150 días: {row['filas_stock_mayor_150']}")
    else:
        st.markdown("No hay filas con días en stock >150 para la selección actual.")
    st.markdown("</div>", unsafe_allow_html=True)
