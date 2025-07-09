import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Comisiones con checkboxes en resultados", layout="wide")

def limpiar_eur(valor):
    try:
        s = str(valor).replace("EUR", "").replace("€", "").strip()
        if s == "":
            return 0.0
        # Convertir formato europeo: puntos miles a nada, coma decimal a punto
        if s.count(",") == 1:
            partes = s.split(",")
            parte_entera = partes[0].replace(".", "")
            parte_decimal = partes[1]
            s = parte_entera + "." + parte_decimal
        else:
            s = s.replace(".", "")
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

    comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, nueva_incorporacion, jefe_tienda)
    comision_entregas_compartidas = entregas_compartidas * 30
    comision_compras = compras * 60
    comision_vh_cambio = vh_cambio * 30
    bono_financiacion = entregas_con_financiacion * 10
    bono_rapida = entregas_rapidas * 5
    bono_stock = entregas_stock_largo * 5
    penalizacion_descuento = entregas_con_descuento * -15
    comision_beneficio = calcular_comision_por_beneficio(beneficio_financiacion_total)
    bono_garantias = calcular_incentivo_garantias(facturacion_garantias)
    bono_resenas = 0
    if entregas > 0 and (resenas / entregas) >= 0.5:
        bono_resenas = resenas * 5

    prima_total = (
        comision_entregas + comision_entregas_compartidas + comision_compras +
        comision_vh_cambio + bono_financiacion + bono_rapida + bono_stock +
        penalizacion_descuento + comision_beneficio + bono_garantias + bono_resenas
    )

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

def limpiar_y_preparar_df(df_raw):
    df_raw.columns = df_raw.columns.str.strip()
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    for col in ["entregas", "entregas_otra_delegacion", "entregas_compartidas", "compras",
                "vh_cambio", "garantias_premium", "facturacion_garantias", "entregas_con_financiacion",
                "entregas_rapidas", "entregas_stock_largo", "entregas_con_descuento", "resenas"]:
        if col not in df_raw.columns:
            df_raw[col] = 0

    return df_raw

st.title("Calculadora de Comisiones con checkboxes en resultados")

uploaded_file = st.file_uploader("Sube archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw = limpiar_y_preparar_df(df_raw)

    resumen = df_raw.groupby("Opportunity Owner").agg({
        "entregas": "sum",
        "entregas_otra_delegacion": "sum",
        "entregas_compartidas": "sum",
        "compras": "sum",
        "vh_cambio": "sum",
        "garantias_premium": "sum",
        "facturacion_garantias": "sum",
        "Beneficio financiación comercial": "sum",
        "entregas_con_financiacion": "sum",
        "entregas_rapidas": "sum",
        "entregas_stock_largo": "sum",
        "entregas_con_descuento": "sum",
        "resenas": "sum",
        "Delegación": "first"
    }).reset_index()

    resumen.rename(columns={"Beneficio financiación comercial": "beneficio_financiacion_total",
                           "Opportunity Owner": "ownername",
                           "Delegación": "delegacion"}, inplace=True)

    # Filtros en columnas
    col1, col2 = st.columns(2)
    delegaciones_unicas = sorted(resumen["delegacion"].dropna().unique())
    seleccion_delegacion = col1.selectbox("Filtrar por Delegación", options=["Todas"] + delegaciones_unicas)
    if seleccion_delegacion != "Todas":
        resumen = resumen[resumen["delegacion"] == seleccion_delegacion]

    comerciales_unicos = sorted(resumen["ownername"].unique())
    seleccion_comercial = col2.selectbox("Filtrar por Comercial", options=["Todos"] + comerciales_unicos)
    if seleccion_comercial != "Todos":
        resumen = resumen[resumen["ownername"] == seleccion_comercial]

    resumen = resumen.sort_values(by=["delegacion", "ownername"])

    # Mostrar resultados con checkbox en cada uno para recalcular individual
    for idx, fila in resumen.iterrows():
        st.markdown(f"## Comercial: {fila['ownername']} ({fila['delegacion']})")

        # Checkbox para cada comercial
        col_nueva, col_jefe = st.columns(2)
        nueva = col_nueva.checkbox("Nueva incorporación", key=f"nueva_{idx}")
        jefe = col_jefe.checkbox("Jefe de tienda", key=f"jefe_{idx}")

        resultado = calcular_comision_fila(fila, nueva, jefe)

        st.write(f"**Prima total antes de penalizaciones:** {resultado['prima_total']:.2f} €")
        st.write(f"**Prima final a cobrar:** {resultado['prima_final']:.2f} €")

        st.write("**Desglose de conceptos:**")
        for k, v in resultado['desglose'].items():
            st.write(f"- {k.replace('_',' ').capitalize()}: {v:.2f} €")

        if resultado['penalizaciones_detalle']:
            st.write("**Penalizaciones aplicadas:**")
            for desc, val in resultado['penalizaciones_detalle']:
                st.write(f"- {desc}: -{val:.2f} €")

        st.markdown("---")

else:
    st.info("Sube un archivo Excel para empezar")


