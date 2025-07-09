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

# Función para limpiar y convertir importes en formato europeo (EUR2.496,90 -> 2496.90)
def limpiar_eur(valor):
    try:
        s = str(valor).replace("EUR", "").replace("€", "").strip()
        s = s.replace(".", "").replace(",", ".")
        return float(s)
    except:
        return 0.0

# Funciones de cálculo

def calcular_tarifa_entrega_vendedor(n):
    if n <= 6:
        return 0
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

def calcular_comision_entregas(total, entregas_otra_delegacion, nueva_incorporacion, jefe_tienda):
    normales = total - entregas_otra_delegacion
    if jefe_tienda:
        tarifa = calcular_tarifa_entrega_jefe(total)
        # Entregas en otra delegación a mitad tarifa
        return normales * tarifa + entregas_otra_delegacion * tarifa * 0.5
    else:
        tarifa = calcular_tarifa_entrega_vendedor(total)
        if nueva_incorporacion and total <= 6:
            # Solo producto, cobran 20€ por entrega
            return normales * 20 + entregas_otra_delegacion * 10
        elif not nueva_incorporacion and total <= 6:
            return 0
        else:
            # Para entregas en otra delegación a mitad tarifa
            return normales * tarifa + entregas_otra_delegacion * tarifa * 0.5

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

def calcular_comision_fila(fila, nueva_incorporacion, jefe_tienda):
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

    comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, nueva_incorporacion, jefe_tienda)
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
        comision_beneficio, bono_garantias, bono_resenas
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
            'bono_resenas': bono_resenas
        }
    }


if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()  # quitar espacios

    # Limpiar campo Beneficio financiación comercial
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    # Agrupar por Opportunity Owner para resumen
    resumen = pd.DataFrame()
    resumen["ownername"] = df_raw["Opportunity Owner"].dropna().unique()
    resumen = resumen.set_index("ownername")

    # Entregas = tipo Venta
    entregas = df_raw[df_raw["Opportunity Record Type"] == "Venta"].groupby("Opportunity Owner").size()
    resumen["entregas"] = entregas

    # Entregas compartidas = hay copropietario
    compartidas = df_raw[df_raw["Coopropietario de la Oportunidad"].notna() & (df_raw["Coopropietario de la Oportunidad"] != "")].groupby("Opportunity Owner").size()
    resumen["entregas_compartidas"] = compartidas

    # Compras = tipo Tasación
    compras = df_raw[df_raw["Opportunity Record Type"] == "Tasación"].groupby("Opportunity Owner").size()
    resumen["compras"] = compras

    # VH como cambio = tipo Cambio
    cambios = df_raw[df_raw["Opportunity Record Type"] == "Cambio"].groupby("Opportunity Owner").size()
    resumen["vh_cambio"] = cambios

    # Con descuento = descuento marcado como distinto de vacío o nulo
    con_descuento = df_raw[df_raw["Descuento"].notna() & (df_raw["Descuento"].astype(str).str.strip() != "")].groupby("Opportunity Owner").size()
    resumen["entregas_con_descuento"] = con_descuento

    # Beneficio financiero (suma de Beneficio financiación comercial)
    beneficio = df_raw.groupby("Opportunity Owner")["Beneficio financiación comercial"].sum()
    resumen["beneficio_financiacion_total"] = beneficio

    # Rellenar columnas faltantes con ceros
    for col in [
        "entregas", "entregas_compartidas", "compras", "vh_cambio", "beneficio_financiacion_total", "entregas_con_descuento"
    ]:
        if col not in resumen:
            resumen[col] = 0
    resumen.fillna(0, inplace=True)

    # Añadir columnas vacías necesarias para función cálculo
    resumen["entregas_otra_delegacion"] = 0
    resumen["facturacion_garantias"] = 0
    resumen["entregas_con_financiacion"] = 0
    resumen["entregas_rapidas"] = 0
    resumen["entregas_stock_largo"] = 0
    resumen["resenas"] = 0
    resumen["garantias_premium"] = 0
    resumen["n_casos_venta_superior"] = 0

    # Obtener delegación única para cada comercial (valor más frecuente)
    delegacion_map = df_raw.groupby("Opportunity Owner")["Delegación"].agg(lambda x: x.mode().iat[0] if not x.mode().empty else x.iloc[0])
    resumen["delegacion"] = resumen.index.map(delegacion_map)

    resumen = resumen.reset_index()

    # FILTROS en la UI
    delegaciones_unicas = sorted(resumen["delegacion"].dropna().unique())
    seleccion_delegacion = st.selectbox("Filtrar por delegación", options=["Todas"] + delegaciones_unicas)

    if seleccion_delegacion != "Todas":
        resumen = resumen[resumen["delegacion"] == seleccion_delegacion]

    resumen = resumen.sort_values(["delegacion", "ownername"])

    comerciales_unicos = resumen["ownername"].tolist()
    seleccion_comercial = st.selectbox("Filtrar por comercial", options=["Todos"] + comerciales_unicos)

    if seleccion_comercial != "Todos":
        resumen = resumen[resumen["ownername"] == seleccion_comercial]

    # Checkboxes para nueva incorporación y jefe de tienda por comercial
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("### Configuración especial por comercial")
    nueva_incorporacion_map = {}
    jefe_tienda_map = {}

    for i, fila in resumen.iterrows():
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(f"**{fila['ownername']}** - {fila['delegacion']}")
        with col2:
            nueva_incorporacion_map[fila['ownername']] = st.checkbox("Nueva incorporación", key=f"nueva_{i}")
        with col3:
            jefe_tienda_map[fila['ownername']] = st.checkbox("Jefe de tienda", key=f"jefe_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Calcular comisiones con configuraciones
    resultados = []
    for _, fila in resumen.iterrows():
        nueva = nueva_incorporacion_map.get(fila['ownername'], False)
        jefe = jefe_tienda_map.get(fila['ownername'], False)
        resultado = calcular_comision_fila(fila, nueva, jefe)
        resultados.append({
            'ownername': fila['ownername'],
            'delegacion': fila['delegacion'],
            'prima_final': resultado['prima_final'],
            'prima_total': resultado['prima_total'],
            'penalizaciones_detalle': resultado['penalizaciones_detalle'],
            'desglose': resultado['desglose']
        })

    # Mostrar resultados
    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### Resultados por Comercial")

    for r in resultados:
        st.markdown(f"## Comercial: **{r['ownername']}** ({r['delegacion']})")
        st.markdown(f"### Prima total antes de penalizaciones: {r['prima_total']:.2f} €")
        st.markdown(f"### Prima final a cobrar: **{r['prima_final']:.2f} €**")

        st.markdown("#### Desglose de conceptos:")
        desglose = r['desglose']
        for k, v in desglose.items():
            st.markdown(f"- {k.replace('_', ' ').capitalize()}: {v:.2f} €")

        if r['penalizaciones_detalle']:
            st.markdown("#### Penalizaciones aplicadas:")
            for desc, val in r['penalizaciones_detalle']:
                st.markdown(f"- {desc}: -{val:.2f} €")
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
