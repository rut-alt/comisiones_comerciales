import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Comisiones", layout="wide")

def limpiar_eur(valor):
    try:
        s = str(valor).replace("EUR", "").replace("€", "").strip()
        if s == "":
            return 0.0
        # Quitar puntos de miles y cambiar coma decimal por punto
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
    # Variables base
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

    # Cálculos
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

    # Penalizaciones adicionales
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

st.title("Calculadora de Comisiones Completa")

uploaded_file = st.file_uploader("Sube archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()

    # Limpiar y convertir Beneficio financiación comercial a float
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    # Aquí deberás adaptar estos campos a los nombres exactos de tu Excel:
    # Para evitar errores, si no existen, creamos con 0
    for col in ["entregas_otra_delegacion", "facturacion_garantias", "entregas_con_financiacion",
                "entregas_rapidas", "entregas_stock_largo", "resenas", "garantias_premium",
                "entregas", "entregas_compartidas", "compras", "vh_cambio",
                "entregas_con_descuento", "n_casos_venta_superior"]:
        if col not in df_raw.columns:
            df_raw[col] = 0

    # Agrupamos los datos por Opportunity Owner
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
        "n_casos_venta_superior": "sum",
        "Delegación": "first"  # Para mostrar delegación, usamos first o mode
    }).reset_index()

    resumen.rename(columns={"Beneficio financiación comercial": "beneficio_financiacion_total",
                           "Delegación": "delegacion",
                           "Opportunity Owner": "ownername"}, inplace=True)

    # --- FILTROS ---
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

    # --- CHECKBOXES POR COMERCIAL ---
    st.markdown("### Marcar estado especial por comercial:")
    nueva_incorp = {}
    jefe_tienda = {}
    for idx, fila in resumen.iterrows():
        c1, c2, c3 = st.columns([4, 1, 1])
        with c1:
            st.write(f"**{fila['ownername']}** ({fila['delegacion']})")
        with c2:
            nueva_incorp[fila['ownername']] = st.checkbox("Nueva incorporación", key=f"nueva_{idx}")
        with c3:
            jefe_tienda[fila['ownername']] = st.checkbox("Jefe de tienda", key=f"jefe_{idx}")

    st.markdown("---")
    st.markdown("## Resultados")

    for _, fila in resumen.iterrows():
        nueva = nueva_incorp.get(fila['ownername'], False)
        jefe = jefe_tienda.get(fila['ownername'], False)
        resultado = calcular_comision_fila(fila, nueva, jefe)

        st.markdown(f"### Comercial: {fila['ownername']} ({fila['delegacion']})")
        st.write(f"Prima total antes de penalizaciones: **{resultado['prima_total']:.2f} €**")
        st.write(f"Prima final a cobrar: **{resultado['prima_final']:.2f} €**")

        st.write("**Desglose de conceptos:**")
        for k, v in resultado['desglose'].items():
            st.write(f"- {k.replace('_',' ').capitalize()}: {v:.2f} €")

        if resultado['penalizaciones_detalle']:
            st.write("**Penalizaciones aplicadas:**")
            for desc, val in resultado['penalizaciones_detalle']:
                st.write(f"- {desc}: -{val:.2f} €")

        st.markdown("---")

else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
