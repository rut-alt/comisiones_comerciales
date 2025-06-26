import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Calculadora de Comisiones", layout="centered")

# Estilos generales con bloques diferenciados
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
    .input-section label,
    .input-section input,
    .input-section div[data-baseweb="input"] input {
        color: white !important;
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

# Cargar y mostrar logo
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

st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("### 📂 Cargar datos desde CSV con columna 'ownername'")

uploaded_file = st.file_uploader("Sube un archivo CSV con los datos", type=["csv"])

# Funciones de cálculo

def calcular_tarifa_entrega(n):
    if n <= 5:
        return 20
    elif 6 <= n <= 8:
        return 20
    elif 9 <= n <= 11:
        return 40
    elif 12 <= n <= 20:
        return 60
    elif 21 <= n <= 25:
        return 75
    elif 26 <= n <= 30:
        return 80
    else:
        return 90

def calcular_comision_entregas(total, otras, nueva):
    normales = total - otras
    tarifa = calcular_tarifa_entrega(total)
    if nueva and total <= 5:
        return normales * 20 + otras * 10
    elif not nueva and total <= 5:
        return 0
    else:
        return normales * tarifa + otras * (tarifa * 0.5)

def calcular_comision_por_beneficio(b):
    if b <= 5000:
        return b * 0.02
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
    # Extraemos y convertimos con seguridad
    entregas = int(fila.get('entregas', 0))
    entregas_otra_delegacion = int(fila.get('entregas_otra_delegacion', 0))
    entregas_compartidas = int(fila.get('entregas_compartidas', 0))
    nueva_incorporacion = bool(fila.get('nueva_incorporacion', False))
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

    bono_ventas_sobre_pvp = 0  # Si quieres puedes mejorar aquí para sumar bonificaciones por coche, pero necesitas info adicional en csv

    comision_entregas = calcular_comision_entregas(entregas, entregas_otra_delegacion, nueva_incorporacion)
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

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if 'ownername' not in df.columns:
        st.error("El CSV debe tener la columna 'ownername'.")
    else:
        st.markdown("<div class='result-section'>", unsafe_allow_html=True)
        st.markdown("### Resultados por Comercial")

        # Aplicar cálculo fila a fila
        resultados = []
        for i, fila in df.iterrows():
            resultado = calcular_comision_fila(fila)
            resultados.append({
                'ownername': fila['ownername'],
                'prima_final': resultado['prima_final'],
                'prima_total': resultado['prima_total'],
                'penalizaciones_detalle': resultado['penalizaciones_detalle'],
                'desglose': resultado['desglose']
            })

        # Convertimos a DataFrame para agrupar
        res_df = pd.DataFrame(resultados)

        # Agrupamos por ownername sumando las primas
        agrupado = res_df.groupby('ownername').agg({
            'prima_final': 'sum',
            'prima_total': 'sum',
        }).reset_index()

        for _, row in agrupado.iterrows():
            st.markdown(f"## Comercial: **{row['ownername']}**")
            st.markdown(f"### Prima total antes de penalizaciones: {row['prima_total']:.2f} €")
            st.markdown(f"### Prima final a cobrar: **{row['prima_final']:.2f} €**")
            st.markdown("---")

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Por favor, sube un archivo CSV con los datos para calcular las comisiones.")





