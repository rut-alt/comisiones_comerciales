import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

def limpiar_eur(valor):
    try:
        texto = str(valor).replace("EUR", "").replace(".", "").replace(",", ".").strip()
        return float(texto) if texto else 0.0
    except:
        return 0.0

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

def calcular_tarifa_entrega(n, es_jefe):
    if es_jefe:
        if n <= 6:
            return 20
        elif n <= 9:
            return 20
        elif n <= 11:
            return 40
        elif n <= 15:
            return 60
        elif n <= 20:
            return 65
        elif n <= 25:
            return 75
        elif n <= 30:
            return 80
        elif n <= 35:
            return 90
        else:
            return 95
    else:
        if n <= 5:
            return 20
        elif n <= 8:
            return 20
        elif n <= 11:
            return 40
        elif n <= 20:
            return 60
        elif n <= 25:
            return 75
        elif n <= 30:
            return 80
        else:
            return 90

def calcular_comision_entregas(total, otras, nueva, es_jefe):
    tarifa = calcular_tarifa_entrega(total, es_jefe)
    normales = total - otras

    if nueva and not es_jefe:
        if total <= 6:
            return normales * 20 + otras * 10 * 0.5
        else:
            return normales * tarifa + otras * tarifa * 0.5
    else:
        if total <= 6 and es_jefe:
            return total * 20
        return normales * tarifa + otras * tarifa * 0.5

def calcular_comision_fila(fila, nueva, jefe):
    entregas = int(fila.get('entregas', 0))
    entregas_otra_delegacion = int(fila.get('entregas_otra_delegacion', 0))
    entregas_compartidas = int(fila.get('entregas_compartidas', 0))
    compras = int(fila.get('compras', 0))
    vh_cambio = int(fila.get('vh_cambio', 0))
    entregas_con_descuento = int(fila.get('entregas_con_descuento', 0))
    beneficio_financiacion_total = float(fila.get('beneficio_financiacion_total', 0))

    comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, nueva, jefe)
    comision_entregas_compartidas = entregas_compartidas * 30
    comision_compras = compras * 60
    comision_vh_cambio = vh_cambio * 30
    penalizacion_descuento = entregas_con_descuento * -15
    comision_beneficio = calcular_comision_por_beneficio(beneficio_financiacion_total)

    prima_total = sum([
        comision_entregas,
        comision_entregas_compartidas,
        comision_compras,
        comision_vh_cambio,
        comision_beneficio,
        penalizacion_descuento,
    ])

    return {
        "prima_total": prima_total,
        "desglose": {
            "comision_entregas": comision_entregas,
            "comision_entregas_compartidas": comision_entregas_compartidas,
            "comision_compras": comision_compras,
            "comision_vh_cambio": comision_vh_cambio,
            "penalizacion_descuento": penalizacion_descuento,
            "comision_beneficio": comision_beneficio,
        }
    }

st.title("Calculadora de Comisiones")

uploaded_file = st.file_uploader("Sube un archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)

    # Limpiar datos
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)
    df_raw["Delegación"] = df_raw["Delegación"].astype(str).str.strip().str.upper()
    df_raw["Opportunity Owner"] = df_raw["Opportunity Owner"].astype(str).str.strip()

    # Eliminar duplicados para evitar suma errónea
    df_raw = df_raw.drop_duplicates()

    # Mostrar datos para Sebastián Machado para depurar
    st.markdown("### Datos para Sebastián Machado (antes de agrupar)")
    st.dataframe(df_raw[df_raw["Opportunity Owner"]=="Sebastian Machado"][["Beneficio financiación comercial", "Delegación", "Opportunity Owner"]])

    # Agrupar datos para resumen
    resumen = df_raw.groupby(["Delegación", "Opportunity Owner"], dropna=False).agg(
        entregas = ("Opportunity Record Type", lambda x: (x == "Venta").sum()),
        entregas_otra_delegacion = ("Delegación", lambda x: (x != x.iloc[0]).sum()),
        entregas_compartidas = ("Coopropietario de la Oportunidad", lambda x: x.notna().sum()),
        compras = ("Opportunity Record Type", lambda x: (x == "Tasación").sum()),
        vh_cambio = ("Opportunity Record Type", lambda x: (x == "Cambio").sum()),
        entregas_con_descuento = ("Descuento", lambda x: x.notna().sum()),
        beneficio_financiacion_total = ("Beneficio financiación comercial", "sum"),
    ).reset_index()

    # Ordenar
    resumen = resumen.sort_values(by=["Delegación", "Opportunity Owner"])

    # Filtros
    delegaciones = resumen["Delegación"].unique().tolist()
    seleccion_delegacion = st.selectbox("Filtrar por Delegación", options=["Todas"] + delegaciones)

    if seleccion_delegacion != "Todas":
        resumen = resumen[resumen["Delegación"] == seleccion_delegacion]

    comerciales = resumen["Opportunity Owner"].unique().tolist()
    seleccion_comercial = st.selectbox("Filtrar por Comercial", options=["Todos"] + comerciales)

    if seleccion_comercial != "Todos":
        resumen = resumen[resumen["Opportunity Owner"] == seleccion_comercial]

    # Checkbox para cada comercial
    nuevos_dict = {}
    jefe_dict = {}

    st.markdown("### Comisiones por Comercial")

    resultados = []

    for idx, fila in resumen.iterrows():
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(f"**{fila['Opportunity Owner']}** (Delegación: {fila['Delegación']})")
            st.write(f"Entregas: {fila['entregas']}")
            st.write(f"Entregas en otra delegación: {fila['entregas_otra_delegacion']}")
            st.write(f"Entregas compartidas: {fila['entregas_compartidas']}")
            st.write(f"Compras: {fila['compras']}")
            st.write(f"VH Cambio: {fila['vh_cambio']}")
            st.write(f"Entregas con descuento: {fila['entregas_con_descuento']}")
            st.write(f"Beneficio financiación comercial total: {fila['beneficio_financiacion_total']:.2f} €")
        with col2:
            nuevos_dict[f"nuevo_{idx}"] = st.checkbox("Nueva incorporación", key=f"nuevo_{idx}")
        with col3:
            jefe_dict[f"jefe_{idx}"] = st.checkbox("Jefe de tienda", key=f"jefe_{idx}")

    st.markdown("---")

    for idx, fila in resumen.iterrows():
        nueva = nuevos_dict.get(f"nuevo_{idx}", False)
        jefe = jefe_dict.get(f"jefe_{idx}", False)

        resultado = calcular_comision_fila(fila, nueva, jefe)
        resultados.append({
            "comercial": fila["Opportunity Owner"],
            "delegacion": fila["Delegación"],
            "prima_total": resultado["prima_total"],
            "desglose": resultado["desglose"]
        })

    for r in resultados:
        st.markdown(f"## Comercial: **{r['comercial']}** (Delegación: {r['delegacion']})")
        st.markdown(f"### Prima total: {r['prima_total']:.2f} €")
        st.markdown("**Desglose:**")
        for clave, valor in r["desglose"].items():
            st.write(f"- {clave.replace('_', ' ').capitalize()}: {valor:.2f} €")
        st.markdown("---")

else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para calcular las comisiones.")
