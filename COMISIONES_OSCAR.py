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

# Función limpieza para valores con "EUR" y formato europeo
def limpiar_eur(valor):
    try:
        texto = str(valor).replace("EUR", "").replace(".", "").replace(",", ".").strip()
        return float(texto) if texto != "" else 0.0
    except:
        return 0.0

# Funciones cálculo comisiones

def calcular_tarifa_entrega_vendedor(n):
    # Escalado para vendedores
    if n <= 6:
        return 0  # no cobra por entregas si no es nueva incorporación
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
    # Escalado para jefes de tienda
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

def calcular_comision_fila(fila):
    entregas = int(fila.get('entregas', 0))
    entregas_otra_delegacion = int(fila.get('entregas_otra_delegacion', 0))
    entregas_compartidas = int(fila.get('entregas_compartidas', 0))
    nueva_incorporacion = bool(fila.get('nueva_incorporacion', False))
    jefe_de_tienda = bool(fila.get('jefe_de_tienda', False))
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

    comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, nueva_incorporacion, jefe_de_tienda)
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
    # Cargar archivo Excel
    df_raw = pd.read_excel(uploaded_file)

    # Limpiar columnas de texto y valores
    df_raw.columns = df_raw.columns.str.strip()

    # Limpiar nombres comerciales y delegación
    df_raw["Opportunity Owner"] = df_raw["Opportunity Owner"].astype(str).str.strip().str.title()
    df_raw["Delegación"] = df_raw["Delegación"].astype(str).str.strip().str.upper()

    # Limpiar campo beneficio y eliminar duplicados
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)
    df_raw = df_raw.drop_duplicates()

    # Debug: mostrar suma real de beneficio por comercial
    suma_beneficio_por_comercial = df_raw.groupby("Opportunity Owner")["Beneficio financiación comercial"].sum()
    st.write("### Suma beneficio financiación comercial por comercial (para debug):")
    st.dataframe(suma_beneficio_por_comercial)

    # Crear resumen base agrupado por comercial y delegación
    resumen = df_raw.groupby(["Delegación", "Opportunity Owner"]).agg(
        entregas = ("Opportunity Record Type", lambda x: (x=="Venta").sum()),
        entregas_compartidas = ("Coopropietario de la Oportunidad", lambda x: x.notna().sum()),
        compras = ("Opportunity Record Type", lambda x: (x=="Tasación").sum()),
        vh_cambio = ("Opportunity Record Type", lambda x: (x=="Cambio").sum()),
        entregas_con_descuento = ("Descuento", lambda x: x.notna().sum()),
        beneficio_financiacion_total = ("Beneficio financiación comercial", "sum"),
    ).reset_index()

    # Agregar columnas necesarias
    resumen["nueva_incorporacion"] = False
    resumen["jefe_de_tienda"] = False
    resumen["facturacion_garantias"] = 0
    resumen["entregas_otra_delegacion"] = 0
    resumen["entregas_con_financiacion"] = 0
    resumen["entregas_rapidas"] = 0
    resumen["entregas_stock_largo"] = 0
    resumen["resenas"] = 0
    resumen["garantias_premium"] = 0
    resumen["n_casos_venta_superior"] = 0

    # Filtros de delegación y comercial
    delegaciones_unicas = resumen["Delegación"].unique().tolist()
    delegacion_filtrada = st.selectbox("Filtrar por Delegación", options=["Todas"] + delegaciones_unicas)

    resumen_filtrado = resumen.copy()
    if delegacion_filtrada != "Todas":
        resumen_filtrado = resumen_filtrado[resumen_filtrado["Delegación"] == delegacion_filtrada]

    comerciales_unicos = resumen_filtrado["Opportunity Owner"].unique().tolist()
    comercial_filtrado = st.selectbox("Filtrar por Comercial", options=["Todos"] + comerciales_unicos)

    if comercial_filtrado != "Todos":
        resumen_filtrado = resumen_filtrado[resumen_filtrado["Opportunity Owner"] == comercial_filtrado]

    resumen_filtrado = resumen_filtrado.sort_values(by=["Delegación", "Opportunity Owner"])

    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### Resultados por Comercial")

    # Checkbox para cada comercial para nueva incorporación y jefe de tienda
    for idx, fila in resumen_filtrado.iterrows():
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            st.markdown(f"## Comercial: **{fila['Opportunity Owner']}** ({fila['Delegación']})")
        with col2:
            nueva = st.checkbox("Nueva incorporación", key=f"nueva_{idx}")
        with col3:
            jefe = st.checkbox("Jefe de tienda", key=f"jefe_{idx}")

        # Actualizar fila con valores de checkbox
        fila_dict = fila.to_dict()
        fila_dict["nueva_incorporacion"] = nueva
        fila_dict["jefe_de_tienda"] = jefe

        resultado = calcular_comision_fila(fila_dict)

        st.markdown(f"### Prima total antes de penalizaciones: {resultado['prima_total']:.2f} €")
        st.markdown(f"### Prima final a cobrar: **{resultado['prima_final']:.2f} €**")
        st.markdown("### Desglose de conceptos:")
        for concepto, valor in resultado["desglose"].items():
            st.markdown(f"- {concepto.replace('_',' ').capitalize()}: {valor:.2f} €")

        if resultado["penalizaciones_detalle"]:
            st.markdown("### Penalizaciones:")
            for penal, val in resultado["penalizaciones_detalle"]:
                st.markdown(f"- {penal}: -{val:.2f} €")
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
