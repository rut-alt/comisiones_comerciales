import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Comisiones", layout="wide")

# Estilo
st.markdown("""
    <style>
    .main { background-color: white; color: black; }
    .input-section, .result-section {
        background-color: #2b344d;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 1px solid #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# Función para limpiar valores en formato europeo
def limpiar_eur(valor):
    try:
        s = str(valor).replace("EUR", "").replace("€", "").strip()
        s = s.replace(".", "").replace(",", ".")
        return float(s)
    except:
        return 0.0

# Tarifa entrega vendedor
def calcular_tarifa_entrega_vendedor(n):
    if n <= 5:
        return 20
    elif 6 <= n <= 8:
        return 20
    elif 9 <= n <= 11:
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

# Comisión por beneficio
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

# Incentivo garantías
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

# Cálculo de comisión completa
def calcular_comision_fila(fila, nueva, jefe):
    entregas = int(fila.get('entregas', 0))
    entregas_otra_delegacion = int(fila.get('entregas_otra_delegacion', 0))
    entregas_compartidas = int(fila.get('entregas_compartidas', 0))
    compras = int(fila.get('compras', 0))
    vh_cambio = int(fila.get('vh_cambio', 0))
    garantias_premium = int(fila.get('garantias_premium', 0))
    facturacion_garantias = float(fila.get('facturacion_garantias', 0))
    beneficio_financiero = float(fila.get('beneficio_financiero', 0))
    entregas_con_financiacion = int(fila.get('entregas_con_financiacion', 0))
    entregas_rapidas = int(fila.get('entregas_rapidas', 0))
    entregas_stock_largo = int(fila.get('entregas_stock_largo', 0))
    entregas_con_descuento = int(fila.get('entregas_con_descuento', 0))
    resenas = int(fila.get('resenas', 0))
    n_casos_venta_superior = int(fila.get('n_casos_venta_superior', 0))

    tarifa = calcular_tarifa_entrega_vendedor(entregas)
    normales = entregas - entregas_otra_delegacion

    if jefe:
        comision_entregas = entregas * tarifa
    elif nueva and entregas <= 5:
        comision_entregas = entregas * 20
    elif not nueva and entregas <= 5:
        comision_entregas = 0
    else:
        comision_entregas = normales * tarifa + entregas_otra_delegacion * (tarifa * 0.5)

    comision_compras = compras * 60
    comision_vh_cambio = vh_cambio * 30
    bono_financiacion = entregas_con_financiacion * 10
    bono_rapida = entregas_rapidas * 5
    bono_stock = entregas_stock_largo * 5
    penalizacion_descuento = entregas_con_descuento * -15
    comision_beneficio = calcular_comision_por_beneficio(beneficio_financiero)
    bono_garantias = calcular_incentivo_garantias(facturacion_garantias)
    bono_resenas = resenas * 5 if entregas > 0 and (resenas / entregas) >= 0.5 else 0
    comision_entregas_compartidas = entregas_compartidas * 30

    prima_total = sum([
        comision_entregas, comision_entregas_compartidas, comision_compras, comision_vh_cambio,
        bono_financiacion, bono_rapida, bono_stock, penalizacion_descuento,
        comision_beneficio, bono_garantias, bono_resenas
    ])

    penalizacion_total = 0
    penalizaciones = []
    if entregas > 0 and garantias_premium / entregas < 0.4:
        p = prima_total * 0.10
        penalizacion_total += p
        penalizaciones.append(("Garantías premium < 40%", p))
    if entregas > 0 and resenas / entregas <= 0.5:
        p = prima_total * 0.10
        penalizacion_total += p
        penalizaciones.append(("Reseñas ≤ 50%", p))
    if beneficio_financiero < 4000:
        p = prima_total * 0.10
        penalizacion_total += p
        penalizaciones.append(("Beneficio financiero < 4000 €", p))

    prima_final = prima_total - penalizacion_total

    return prima_final, prima_total, comision_beneficio, penalizaciones

# Subida de archivo
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    df["Beneficio financiación comercial"] = df["Beneficio financiación comercial"].apply(limpiar_eur)

    if "Delegación" not in df.columns:
        df["Delegación"] = "Sin delegación"

    df["Opportunity Owner"] = df["Opportunity Owner"].astype(str)
    df["Delegación"] = df["Delegación"].astype(str)

    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        filtro_delegacion = st.selectbox("Filtrar por delegación", ["Todas"] + sorted(df["Delegación"].unique()))
    with col2:
        filtro_comercial = st.selectbox("Filtrar por comercial", ["Todos"] + sorted(df["Opportunity Owner"].unique()))
    st.markdown("</div>", unsafe_allow_html=True)

    if filtro_delegacion != "Todas":
        df = df[df["Delegación"] == filtro_delegacion]
    if filtro_comercial != "Todos":
        df = df[df["Opportunity Owner"] == filtro_comercial]

    grouped = df.groupby(["Delegación", "Opportunity Owner"])["Beneficio financiación comercial"].sum().reset_index()
    grouped.columns = ["Delegación", "ownername", "beneficio_financiero"]
    grouped = grouped.sort_values(["Delegación", "ownername"])

    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("## 💰 Resultados de Comisiones")

    for _, fila in grouped.iterrows():
        with st.expander(f"{fila['Delegación']} - {fila['ownername']}"):
            nueva = st.checkbox("¿Nueva incorporación?", key=f"nueva_{fila['ownername']}")
            jefe = st.checkbox("¿Jefe de tienda?", key=f"jefe_{fila['ownername']}")

            datos = {
                "entregas": 10,  # Puedes adaptar
                "entregas_otra_delegacion": 2,
                "entregas_compartidas": 1,
                "compras": 2,
                "vh_cambio": 1,
                "facturacion_garantias": 4000,
                "beneficio_financiero": fila["beneficio_financiero"],
                "entregas_con_financiacion": 3,
                "entregas_rapidas": 2,
                "entregas_stock_largo": 1,
                "entregas_con_descuento": 2,
                "resenas": 5,
                "garantias_premium": 3,
                "n_casos_venta_superior": 0
            }

            prima_final, prima_total, comision_beneficio, penalizaciones = calcular_comision_fila(datos, nueva, jefe)

            st.markdown(f"**Beneficio total:** {fila['beneficio_financiero']:.2f} €")
            st.markdown(f"**Comisión por beneficio:** {comision_beneficio:.2f} €")
            st.markdown(f"**Prima total (antes de penalizaciones):** {prima_total:.2f} €")
            st.markdown(f"**Prima final a cobrar:** {prima_final:.2f} €")

            if penalizaciones:
                st.markdown("### ❌ Penalizaciones:")
                for motivo, cantidad in penalizaciones:
                    st.markdown(f"- {motivo}: {cantidad:.2f} €")
            else:
                st.markdown("✅ Sin penalizaciones.")

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Por favor, sube un archivo Excel para calcular las comisiones.")
