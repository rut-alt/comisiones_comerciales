import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

def limpiar_eur(valor):
    try:
        s = str(valor).strip()
        s = s.replace("EUR", "").strip()
        s = re.sub(r'\.(?=\d{3},)', '', s)
        s = s.replace(",", ".")
        return float(s)
    except:
        return 0.0

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
    if jefe_tienda:
        tarifa = calcular_tarifa_entrega_jefe(total)
        normales = total - entregas_otra_delegacion
        return normales * tarifa + entregas_otra_delegacion * (tarifa / 2)
    else:
        tarifa = calcular_tarifa_entrega_vendedor(total)
        normales = total - entregas_otra_delegacion
        if nueva_incorporacion and total <= 6:
            return normales * 20 + entregas_otra_delegacion * 10
        elif not nueva_incorporacion and total <= 6:
            return 0
        else:
            return normales * tarifa + entregas_otra_delegacion * (tarifa / 2)

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

def calcular_comision_fila(fila, nueva_incorporacion=False, jefe_tienda=False):
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

    bono_ventas_sobre_pvp = 0

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

# --- App principal ---

st.title("Calculadora de Comisiones")

uploaded_file = st.file_uploader("Sube un archivo Excel (.xlsx) con las oportunidades", type=["xlsx"])

if uploaded_file is not None:

    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()

    # Limpiar campo Beneficio financiación comercial
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    # Delegación
    if "Delegación" not in df_raw.columns:
        df_raw["Delegación"] = df_raw.iloc[:, -1]
    else:
        df_raw["Delegación"] = df_raw["Delegación"]

    # Crear resumen
    resumen = pd.DataFrame()
    resumen["ownername"] = df_raw["Opportunity Owner"].dropna().unique()

    delegacion_por_owner = df_raw.groupby("Opportunity Owner")["Delegación"].first()
    resumen = resumen.set_index("ownername")
    resumen["delegacion"] = delegacion_por_owner
    resumen = resumen.reset_index()

    # Conteos y sumas
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

    # Columnas obligatorias
    for col in [
        "entregas", "entregas_compartidas", "compras", "vh_cambio", "entregas_con_descuento", "beneficio_financiacion_total"
    ]:
        if col not in resumen:
            resumen[col] = 0
    resumen = resumen.fillna(0)
    resumen = resumen.reset_index()

    resumen = resumen.sort_values(by=["delegacion", "ownername"])

    st.markdown("## Comercial y opciones")

    for idx, fila in resumen.iterrows():
        owner = fila["ownername"]
        delegacion = fila["delegacion"]

        with st.expander(f"Delegación: {delegacion} - Comercial: {owner}", expanded=True):
            col1, col2 = st.columns(2)
            nueva_incorporacion = col1.checkbox(f"Nueva incorporación - {owner}", key=f"nueva_{idx}")
            jefe_tienda = col2.checkbox(f"Jefe de tienda - {owner}", key=f"jefe_{idx}")

            resultado = calcular_comision_fila(fila, nueva_incorporacion, jefe_tienda)

            st.markdown(f"**Prima total antes de penalizaciones:** {resultado['prima_total']:.2f} €")
            st.markdown(f"**Prima final a cobrar:** {resultado['prima_final']:.2f} €")

            st.markdown("**Desglose de conceptos:**")
            for concepto, valor in resultado['desglose'].items():
                st.markdown(f"- {concepto.replace('_',' ').capitalize()}: {valor:.2f} €")

            if resultado['penalizaciones_detalle']:
                st.markdown("**Penalizaciones aplicadas:**")
                for desc, val in resultado['penalizaciones_detalle']:
                    st.markdown(f"- {desc}: -{val:.2f} €")

else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
