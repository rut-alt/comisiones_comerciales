import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# Función robusta para convertir formato europeo a float
def limpiar_eur(valor):
    try:
        s = str(valor).replace("EUR", "").replace("€", "").strip()
        # Para números grandes con miles: quitar puntos excepto el último (antes de la coma decimal)
        # Ejemplo: '51.563,90' -> '51563,90'
        if s.count(",") == 1:
            partes = s.split(",")
            parte_entera = partes[0].replace(".", "")
            parte_decimal = partes[1]
            s = parte_entera + "." + parte_decimal
        else:
            # No tiene coma decimal, solo quitar puntos
            s = s.replace(".", "")
        return float(s)
    except Exception:
        return 0.0

# Funciones para calcular tarifas y comisiones
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
        return normales * tarifa + entregas_otra_delegacion * tarifa * 0.5
    else:
        tarifa = calcular_tarifa_entrega_vendedor(total)
        if nueva_incorporacion and total <= 6:
            return normales * 20 + entregas_otra_delegacion * 10
        elif not nueva_incorporacion and total <= 6:
            return 0
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


# --- INTERFAZ STREAMLIT ---

st.title("Calculadora de Comisiones")

uploaded_file = st.file_uploader("Sube archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()

    # Limpiar Beneficio financiación comercial
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    # Agrupar resumen por Opportunity Owner
    resumen = pd.DataFrame()
    resumen["ownername"] = df_raw["Opportunity Owner"].dropna().unique()
    resumen = resumen.set_index("ownername")

    # Preparar métricas
    entregas = df_raw[df_raw["Opportunity Record Type"] == "Venta"].groupby("Opportunity Owner").size()
    resumen["entregas"] = entregas

    compartidas = df_raw[df_raw["Coopropietario de la Oportunidad"].notna() & (df_raw["Coopropietario de la Oportunidad"] != "")].groupby("Opportunity Owner").size()
    resumen["entregas_compartidas"] = compartidas

    compras = df_raw[df_raw["Opportunity Record Type"] == "Tasación"].groupby("Opportunity Owner").size()
    resumen["compras"] = compras

    cambios = df_raw[df_raw["Opportunity Record Type"] == "Cambio"].groupby("Opportunity Owner").size()
    resumen["vh_cambio"] = cambios

    con_descuento = df_raw[df_raw["Descuento"].notna() & (df_raw["Descuento"].astype(str).str.strip() != "")].groupby("Opportunity Owner").size()
    resumen["entregas_con_descuento"] = con_descuento

    beneficio = df_raw.groupby("Opportunity Owner")["Beneficio financiación comercial"].sum()
    resumen["beneficio_financiacion_total"] = beneficio

    resumen.fillna(0, inplace=True)

    # Añadir columnas vacías para campos adicionales
    for col in ["entregas_otra_delegacion", "facturacion_garantias", "entregas_con_financiacion", 
                "entregas_rapidas", "entregas_stock_largo", "resenas", "garantias_premium", "n_casos_venta_superior"]:
        resumen[col] = 0

    # Obtener delegación más frecuente para cada comercial
    delegacion_map = df_raw.groupby("Opportunity Owner")["Delegación"].agg(lambda x: x.mode().iat[0] if not x.mode().empty else x.iloc[0])
    resumen["delegacion"] = resumen.index.map(delegacion_map)

    resumen = resumen.reset_index()

    # --- CHECKBOXES AL PRINCIPIO ---
    st.markdown("### Configuración especial por comercial")
    nueva_incorporacion_map = {}
    jefe_tienda_map = {}

    for i, fila in resumen.iterrows():
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.markdown(f"**{fila['ownername']}** - {fila['delegacion']}")
        with col2:
            nueva_incorporacion_map[fila['ownername']] = st.checkbox("Nueva incorporación", key=f"nueva_{i}")
        with col3:
            jefe_tienda_map[fila['ownername']] = st.checkbox("Jefe de tienda", key=f"jefe_{i}")

    # --- FILTROS ---
    delegaciones_unicas = sorted(resumen["delegacion"].dropna().unique())
    seleccion_delegacion = st.selectbox("Filtrar por delegación", options=["Todas"] + delegaciones_unicas)

    if seleccion_delegacion != "Todas":
        resumen = resumen[resumen["delegacion"] == seleccion_delegacion]

    resumen = resumen.sort_values(["delegacion", "ownername"])

    comerciales_unicos = resumen["ownername"].tolist()
    seleccion_comercial = st.selectbox("Filtrar por comercial", options=["Todos"] + comerciales_unicos)

    if seleccion_comercial != "Todos":
        resumen = resumen[resumen["ownername"] == seleccion_comercial]

    # Calcular comisiones y mostrar resultados
    st.markdown("---")
    st.markdown("## Resultados por Comercial")

    for _, fila in resumen.iterrows():
        nueva = nueva_incorporacion_map.get(fila['ownername'], False)
        jefe = jefe_tienda_map.get(fila['ownername'], False)
        resultado = calcular_comision_fila(fila, nueva, jefe)

        st.markdown(f"### Comercial: **{fila['ownername']}** ({fila['delegacion']})")
        st.markdown(f"**Prima total antes de penalizaciones:** {resultado['prima_total']:.2f} €")
        st.markdown(f"**Prima final a cobrar:** {resultado['prima_final']:.2f} €")

        st.markdown("#### Desglose de conceptos:")
        for k, v in resultado['desglose'].items():
            st.markdown(f"- {k.replace('_', ' ').capitalize()}: {v:.2f} €")

        if resultado['penalizaciones_detalle']:
            st.markdown("#### Penalizaciones aplicadas:")
            for desc, val in resultado['penalizaciones_detalle']:
                st.markdown(f"- {desc}: -{val:.2f} €")

        st.markdown("---")

else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
