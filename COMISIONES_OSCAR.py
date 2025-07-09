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

# Función para limpiar el formato europeo EUR2.496,90 -> 2496.90
def limpiar_eur(valor):
    try:
        valor_limpio = str(valor).replace("EUR", "").replace(".", "").replace(",", ".").strip()
        return float(valor_limpio)
    except:
        return 0.0

# Funciones de cálculo de comisiones

def calcular_tarifa_entrega_vendedor(n):
    if n <= 6:
        return 0  # No cobra (salvo nueva incorporacion)
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

def calcular_comision_entregas(total, entregas_otra_delegacion, nueva, jefe):
    normales = total - entregas_otra_delegacion
    if jefe:
        tarifa = calcular_tarifa_entrega_jefe(total)
        # Entregas en otra delegación a la mitad
        return normales * tarifa + entregas_otra_delegacion * tarifa * 0.5
    else:
        tarifa = calcular_tarifa_entrega_vendedor(total)
        if nueva and total <= 6:
            return normales * 20 + entregas_otra_delegacion * 10
        elif not nueva and total <= 6:
            return 0 + entregas_otra_delegacion * 10  # No cobra si no nueva, pero entregas otra delegacion sí?
        else:
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

def calcular_comision_fila(fila, nueva, jefe):
    entregas = int(fila.get('entregas', 0))
    entregas_otra_delegacion = int(fila.get('entregas_otra_delegacion', 0))
    entregas_compartidas = int(fila.get('entregas_compartidas', 0))
    compras = int(fila.get('compras', 0))
    vh_cambio = int(fila.get('vh_cambio', 0))
    garantias_premium = int(fila.get('garantias_premium', 0))
    facturacion_garantias = float(fila.get('facturacion_garantias', 0))
    beneficio_financiero = float(fila.get('beneficio_financiero', 0))
    beneficio_financiacion_total = float(fila.get('beneficio_financiacion_total', 0))
    entregas_con_financiacion = int(fila.get('entregas_con_financiacion', 0))
    entregas_rapidas = int(fila.get('entregas_rapidas', 0))
    entregas_stock_largo = int(fila.get('entregas_stock_largo', 0))
    entregas_con_descuento = int(fila.get('entregas_con_descuento', 0))
    resenas = int(fila.get('resenas', 0))
    n_casos_venta_superior = int(fila.get('n_casos_venta_superior', 0))

    bono_ventas_sobre_pvp = 0  # Si hay reglas, aquí se añaden

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
    if beneficio_financiero < 4000:
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

# Subida de Excel y filtro delegación, comercial

st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("### 📂 Cargar archivo Excel con oportunidades")
uploaded_file = st.file_uploader("Sube un archivo .xlsx", type=["xlsx"])

st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:

    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()  # limpiar espacios

    # Limpiar beneficio financiación comercial con formato europeo
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    # Crear resumen agrupado por Opportunity Owner y Delegación
    resumen = df_raw.groupby(["Opportunity Owner", "Delegación"]).agg({
        "Opportunity Owner": "first",
        "Delegación": "first",
        "Opportunity Record Type": list,
        "Beneficio financiación comercial": "sum",
        "Descuento": list,
        "Coopropietario de la Oportunidad": list
    }).reset_index(drop=True)

    # Ahora contamos las métricas necesarias por comercial (Opportunity Owner)
    # Entregas: tipo Venta
    entregas = df_raw[df_raw["Opportunity Record Type"] == "Venta"].groupby("Opportunity Owner").size()
    entregas_compartidas = df_raw[(df_raw["Coopropietario de la Oportunidad"].notna()) & (df_raw["Coopropietario de la Oportunidad"] != "")].groupby("Opportunity Owner").size()
    compras = df_raw[df_raw["Opportunity Record Type"] == "Tasación"].groupby("Opportunity Owner").size()
    vh_cambio = df_raw[df_raw["Opportunity Record Type"] == "Cambio"].groupby("Opportunity Owner").size()
    entregas_con_descuento = df_raw[(df_raw["Descuento"].notna()) & (df_raw["Descuento"].astype(str).str.strip() != "")].groupby("Opportunity Owner").size()
    beneficio = df_raw.groupby("Opportunity Owner")["Beneficio financiación comercial"].sum()

    # Crear DataFrame resumen completo
    resumen = pd.DataFrame()
    resumen["ownername"] = df_raw["Opportunity Owner"].dropna().unique()
    resumen["delegacion"] = resumen["ownername"].map(df_raw.set_index("Opportunity Owner")["Delegación"])
    resumen["entregas"] = resumen["ownername"].map(entregas).fillna(0).astype(int)
    resumen["entregas_compartidas"] = resumen["ownername"].map(entregas_compartidas).fillna(0).astype(int)
    resumen["compras"] = resumen["ownername"].map(compras).fillna(0).astype(int)
    resumen["vh_cambio"] = resumen["ownername"].map(vh_cambio).fillna(0).astype(int)
    resumen["entregas_con_descuento"] = resumen["ownername"].map(entregas_con_descuento).fillna(0).astype(int)
    resumen["beneficio_financiacion_total"] = resumen["ownername"].map(beneficio).fillna(0).astype(float)

    # Añadir columnas que no vienen en Excel, inicializadas a cero
    resumen["nueva_incorporacion"] = False
    resumen["jefe_tienda"] = False
    resumen["facturacion_garantias"] = 0
    resumen["garantias_premium"] = 0
    resumen["beneficio_financiero"] = resumen["beneficio_financiacion_total"]
    resumen["entregas_con_financiacion"] = 0
    resumen["entregas_rapidas"] = 0
    resumen["entregas_stock_largo"] = 0
    resumen["resenas"] = 0
    resumen["n_casos_venta_superior"] = 0
    resumen["entregas_otra_delegacion"] = 0

    # Filtros delegacion y comercial antes de mostrar resultados
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    col_del, col_com = st.columns(2)
    delegaciones = sorted(resumen["delegacion"].dropna().unique())
    seleccion_delegacion = col_del.selectbox("Filtrar por delegación", ["Todas"] + delegaciones)
    if seleccion_delegacion != "Todas":
        resumen = resumen[resumen["delegacion"] == seleccion_delegacion]

    comerciales = sorted(resumen["ownername"].dropna().unique())
    seleccion_comercial = col_com.selectbox("Filtrar por comercial", ["Todos"] + comerciales)
    if seleccion_comercial != "Todos":
        resumen = resumen[resumen["ownername"] == seleccion_comercial]
    st.markdown("</div>", unsafe_allow_html=True)

    # Ordenar por delegación y luego por nombre
    resumen = resumen.sort_values(by=["delegacion", "ownername"])

    # Mostrar checkboxes para nueva incorporacion y jefe de tienda
    nueva_dict = {}
    jefe_dict = {}
    for idx, row in resumen.iterrows():
        col1, col2 = st.columns([1,1])
        with col1:
            nueva_dict[row["ownername"]] = st.checkbox(f"Nueva incorporación: {row['ownername']}", key=f"nueva_{row['ownername']}")
        with col2:
            jefe_dict[row["ownername"]] = st.checkbox(f"Jefe de tienda: {row['ownername']}", key=f"jefe_{row['ownername']}")

    # Calcular comisiones
    resultados = []
    for idx, fila in resumen.iterrows():
        nueva = nueva_dict.get(fila["ownername"], False)
        jefe = jefe_dict.get(fila["ownername"], False)
        resultado = calcular_comision_fila(fila, nueva, jefe)
        resultados.append({
            'ownername': fila["ownername"],
            'delegacion': fila["delegacion"],
            'prima_total': resultado['prima_total'],
            'prima_final': resultado['prima_final'],
            'penalizaciones_detalle': resultado['penalizaciones_detalle'],
            'desglose': resultado['desglose']
        })

    # Mostrar resultados
    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### Resultados por Comercial")

    for r in resultados:
        st.markdown(f"## Comercial: **{r['ownername']}** - Delegación: {r['delegacion']}")
        st.markdown(f"### Prima total antes de penalizaciones: {r['prima_total']:.2f} €")
        st.markdown(f"### Prima final a cobrar: **{r['prima_final']:.2f} €**")
        st.markdown("### Desglose de conceptos:")
        desglose = r['desglose']
        for k, v in desglose.items():
            st.markdown(f"- {k.replace('_', ' ').capitalize()}: {v:.2f} €")
        if r['penalizaciones_detalle']:
            st.markdown("### Penalizaciones:")
            for desc, val in r['penalizaciones_detalle']:
                st.markdown(f"- {desc}: -{val:.2f} €")
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
