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

# Logo
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

# Subida de Excel
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("### 📂 Cargar archivo Excel con oportunidades")
uploaded_file = st.file_uploader("Sube un archivo .xlsx", type=["xlsx"])
st.markdown("</div>", unsafe_allow_html=True)

def limpiar_eur(valor):
    try:
        return float(str(valor).replace("EUR", "").replace(".", "").replace(",", ".").strip())
    except:
        return 0.0

# Funciones para calcular tarifas y comisiones según nuevo criterio
def calcular_tarifa_entrega_vendedor(n):
    # Tarifas para vendedores
    if n <= 6:
        return 0  # no cobra (excepto nueva incorporación)
    elif 7 <= n <= 9:
        return 20
    elif 10 <= n <= 11:
        return 40
    elif 12 <= n <= 15:
        return 60
    elif 16 <= n <= 20:
        return 65
    elif 21 <= n <= 25:
        return 75
    elif 26 <= n <= 30:
        return 80
    elif 31 <= n <= 35:
        return 90
    else:
        return 95

def calcular_tarifa_entrega_jefe(n):
    # Tarifas para jefes de tienda
    if n <= 6:
        return 20
    elif 7 <= n <= 9:
        return 20
    elif 10 <= n <= 11:
        return 40
    elif 12 <= n <= 15:
        return 60
    elif 16 <= n <= 20:
        return 65
    elif 21 <= n <= 25:
        return 75
    elif 26 <= n <= 30:
        return 80
    elif 31 <= n <= 35:
        return 90
    else:
        return 95

def calcular_comision_entregas(total, otras, nueva, jefe):
    normales = total - otras
    if jefe:
        tarifa = calcular_tarifa_entrega_jefe(total)
        return normales * tarifa + otras * (tarifa * 0.5)
    else:
        tarifa = calcular_tarifa_entrega_vendedor(total)
        if nueva and total <= 6:
            return normales * 20 + otras * 10
        elif not nueva and total <= 6:
            return 0
        else:
            return normales * tarifa + otras * (tarifa * 0.5)

def calcular_comision_por_beneficio(b):
    if b <= 5000:
        return 0
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

def calcular_comision_fila(fila, nueva, jefe):
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

    comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, nueva, jefe)
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
            'penalizacion_descuento': penalizacion_descuento,
            'bono_garantias': bono_garantias,
            'bono_resenas': bono_resenas,
            'bono_ventas_sobre_pvp': bono_ventas_sobre_pvp
        }
    }

if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()

    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    # Aseguramos columna Delegación
    if "Delegación" not in df_raw.columns:
        df_raw["Delegación"] = df_raw.iloc[:, -1]
    else:
        df_raw["Delegación"] = df_raw["Delegación"]

    # Construimos resumen inicial
    resumen = pd.DataFrame()
    resumen["ownername"] = df_raw["Opportunity Owner"].dropna().unique()
    delegacion_por_owner = df_raw.groupby("Opportunity Owner")["Delegación"].first()
    resumen = resumen.set_index("ownername")
    resumen["delegacion"] = delegacion_por_owner
    resumen = resumen.reset_index()

    # === FILTROS ===
    delegaciones = ["Todas"] + sorted(resumen["delegacion"].dropna().unique().tolist())
    seleccion_delegacion = st.selectbox("Filtrar por Delegación", delegaciones)

    if seleccion_delegacion != "Todas":
        resumen_filtrado = resumen[resumen["delegacion"] == seleccion_delegacion]
    else:
        resumen_filtrado = resumen.copy()

    comerciales_filtrados = ["Todos"] + sorted(resumen_filtrado["ownername"].unique().tolist())
    seleccion_comercial = st.selectbox("Filtrar por Comercial", comerciales_filtrados)

    # Añadimos columnas de datos numéricos
    resumen_entregas = df_raw[df_raw["Opportunity Record Type"] == "Venta"].groupby("Opportunity Owner").size()
    resumen_compartidas = df_raw[df_raw["Coopropietario de la Oportunidad"].notna() & (df_raw["Coopropietario de la Oportunidad"] != "")].groupby("Opportunity Owner").size()
    resumen_compras = df_raw[df_raw["Opportunity Record Type"] == "Tasación"].groupby("Opportunity Owner").size()
    resumen_vh_cambio = df_raw[df_raw["Opportunity Record Type"] == "Cambio"].groupby("Opportunity Owner").size()
    resumen_descuentos = df_raw[df_raw["Descuento"].notna() & (df_raw["Descuento"].astype(str).str.strip() != "")].groupby("Opportunity Owner").size()
    resumen_beneficio = df_raw.groupby("Opportunity Owner")["Beneficio financiación comercial"].sum()

    resumen = resumen.set_index("ownername")
    resumen["entregas"] = resumen_entregas
    resumen["entregas_compartidas"] = resumen_compartidas
    resumen["compras"] = resumen_compras
    resumen["vh_cambio"] = resumen_vh_cambio
    resumen["entregas_con_descuento"] = resumen_descuentos
    resumen["beneficio_financiacion_total"] = resumen_beneficio
    resumen = resumen.fillna(0)
    resumen = resumen.reset_index()

    # Aplicar filtro comercial final
    if seleccion_comercial != "Todos":
        resumen = resumen[resumen["ownername"] == seleccion_comercial]
    else:
        resumen = resumen.copy()

    resumen = resumen.sort_values(by=["delegacion", "ownername"])

    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### Resultados por Comercial")

    # Diccionarios para almacenar estado checkbox (Streamlit lo mantiene automáticamente si usamos key distinto)
    nueva_incorporacion_dict = {}
    jefe_tienda_dict = {}

    for idx, fila in resumen.iterrows():
        owner = fila["ownername"]
        deleg = fila["delegacion"]

        # Checkbox por comercial para nueva incorporacion y jefe tienda
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(f"### Comercial: **{owner}**  _(Delegación: {deleg})_")
        with col2:
            nueva_incorporacion_dict[owner] = st.checkbox("Nueva incorporación", key=f"nueva_{owner}")
        with col3:
            jefe_tienda_dict[owner] = st.checkbox("Jefe de tienda", key=f"jefe_{owner}")

        # Obtener valores checkbox para el comercial actual
        nueva = nueva_incorporacion_dict.get(owner, False)
        jefe = jefe_tienda_dict.get(owner, False)

        resultado = calcular_comision_fila(fila, nueva, jefe)

        st.markdown(f"**Prima total antes de penalizaciones:** {resultado['prima_total']:.2f} €")
        st.markdown(f"**Prima final a cobrar:** {resultado['prima_final']:.2f} €")

        st.markdown("**Desglose de conceptos:**")
        desglose = resultado['desglose']
        for concepto, valor in desglose.items():
            st.markdown(f"- {concepto.replace('_', ' ').capitalize()}: {valor:.2f} €")

        if resultado['penalizaciones_detalle']:
            st.markdown("**Penalizaciones:**")
            for pen, val in resultado['penalizaciones_detalle']:
                st.markdown(f"- {pen}: -{val:.2f} €")

        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
