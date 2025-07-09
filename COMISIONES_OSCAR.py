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
    .checkbox-col {
        padding-right: 10px;
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
        # Quitar EUR, puntos de miles y cambiar coma decimal a punto
        s = str(valor).replace("EUR", "").replace(".", "").replace(",", ".").strip()
        return float(s) if s else 0.0
    except:
        return 0.0

def calcular_tarifa_entrega_vendedor(n):
    # Tarifa para vendedor normal (sin jefe tienda)
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
    # Tarifa para jefe de tienda (siempre 20€ hasta 6 entregas)
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

def calcular_comision_entregas(total, otras, es_nuevo, es_jefe):
    normales = total - otras
    if es_jefe:
        tarifa = calcular_tarifa_entrega_jefe(total)
        # Entregas en otra delegación valen la mitad
        comision_normales = normales * tarifa
        comision_otras = otras * (tarifa * 0.5)
        return comision_normales + comision_otras
    else:
        tarifa = calcular_tarifa_entrega_vendedor(total)
        if es_nuevo and total <= 6:
            # Nueva incorporación cobra 20€ por entrega hasta 6 entregas
            comision_normales = normales * 20
            comision_otras = otras * 10
            return comision_normales + comision_otras
        elif not es_nuevo and total <= 6:
            # No cobra comision si no es nuevo y tiene <=6 entregas
            return 0
        else:
            comision_normales = normales * tarifa
            comision_otras = otras * (tarifa * 0.5)
            return comision_normales + comision_otras

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
            'penalizacion_descuento': penalizacion_descuento,
            'bono_garantias': bono_garantias,
            'bono_resenas': bono_resenas,
            'bono_ventas_sobre_pvp': bono_ventas_sobre_pvp
        }
    }

if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()

    # Limpiar el campo beneficio financiación
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    # Delegación (la última columna, o si tienes el nombre "Delegación", usar ese)
    if "Delegación" not in df_raw.columns:
        df_raw["Delegación"] = df_raw.iloc[:, -1]
    else:
        df_raw["Delegación"] = df_raw["Delegación"]

    # Calcular métricas agrupadas por Opportunity Owner
    entregas = df_raw[df_raw["Opportunity Record Type"] == "Venta"].groupby("Opportunity Owner").size()
    entregas_compartidas = df_raw[df_raw["Coopropietario de la Oportunidad"].notna() & (df_raw["Coopropietario de la Oportunidad"] != "")].groupby("Opportunity Owner").size()
    compras = df_raw[df_raw["Opportunity Record Type"] == "Tasación"].groupby("Opportunity Owner").size()
    vh_cambio = df_raw[df_raw["Opportunity Record Type"] == "Cambio"].groupby("Opportunity Owner").size()
    entregas_con_descuento = df_raw[df_raw["Descuento"].notna() & (df_raw["Descuento"].astype(str).str.strip() != "")].groupby("Opportunity Owner").size()
    beneficio_financiacion_total = df_raw.groupby("Opportunity Owner")["Beneficio financiación comercial"].sum()
    delegacion_por_owner = df_raw.groupby("Opportunity Owner")["Delegación"].first()

    resumen = pd.DataFrame({
        "ownername": beneficio_financiacion_total.index,
        "entregas": entregas,
        "entregas_compartidas": entregas_compartidas,
        "compras": compras,
        "vh_cambio": vh_cambio,
        "entregas_con_descuento": entregas_con_descuento,
        "beneficio_financiacion_total": beneficio_financiacion_total,
        "delegacion": delegacion_por_owner
    })

    resumen = resumen.fillna(0).reset_index(drop=True)

    # Filtros
    delegaciones = ["Todas"] + sorted(resumen["delegacion"].dropna().unique().tolist())
    seleccion_delegacion = st.selectbox("Filtrar por Delegación", delegaciones)

    if seleccion_delegacion != "Todas":
        resumen = resumen[resumen["delegacion"] == seleccion_delegacion]

    comerciales_filtrados = ["Todos"] + sorted(resumen["ownername"].unique().tolist())
    seleccion_comercial = st.selectbox("Filtrar por Comercial", comerciales_filtrados)

    if seleccion_comercial != "Todos":
        resumen = resumen[resumen["ownername"] == seleccion_comercial]

    resumen = resumen.sort_values(by=["delegacion", "ownername"]).reset_index(drop=True)

    # Mostrar checkboxes para nueva incorporación y jefe de tienda por comercial
    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### Resultados por Comercial")

    com_nuevo = {}
    com_jefe = {}

    for idx, row in resumen.iterrows():
        owner = row["ownername"]
        col_nuevo, col_jefe = st.columns(2)
        with col_nuevo:
            com_nuevo[owner] = st.checkbox(f"Nuevo incorporación: {owner}", key=f"nuevo_{owner}")
        with col_jefe:
            com_jefe[owner] = st.checkbox(f"Jefe de tienda: {owner}", key=f"jefe_{owner}")

    # Ahora calculamos comisiones con los checkboxes
    for idx, row in resumen.iterrows():
        owner = row["ownername"]
        es_nuevo = com_nuevo.get(owner, False)
        es_jefe = com_jefe.get(owner, False)

        resultado = calcular_comision_fila(row, es_nuevo, es_jefe)

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


