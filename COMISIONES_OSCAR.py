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
st.markdown("### 📂 Cargar archivo Excel con oportunidades")
uploaded_file = st.file_uploader("Sube un archivo .xlsx", type=["xlsx"])
st.markdown("</div>", unsafe_allow_html=True)

def limpiar_eur(valor):

    try:
        s = str(valor)
        s = re.sub(r"[^\d,.-]", "", s)  # Quitar todo menos dígitos, coma, punto y guion
        # Aquí asumo que el punto es separador de miles, la coma decimal
        # Primero eliminar puntos que separan miles:
        s = s.replace(".", "")
        # Cambiar la coma decimal a punto decimal para float:
        s = s.replace(",", ".")
        return float(s) if s else 0.0
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

def calcular_comision_entregas(total, otras, es_nuevo, es_jefe):
    normales = total - otras
    if es_jefe:
        tarifa = calcular_tarifa_entrega_jefe(total)
        comision_normales = normales * tarifa
        comision_otras = otras * (tarifa * 0.5)
        return comision_normales + comision_otras
    else:
        tarifa = calcular_tarifa_entrega_vendedor(total)
        if es_nuevo and total <= 6:
            comision_normales = normales * 20
            comision_otras = otras * 10
            return comision_normales + comision_otras
        elif not es_nuevo and total <= 6:
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

def resumen_comision_beneficio(b):
    if b <= 5000:
        comision = 0
        tramo = "≤ 5000 €"
        porcentaje = 0
    elif b <= 8000:
        comision = b * 0.03
        tramo = "5001 € - 8000 €"
        porcentaje = 3
    elif b <= 12000:
        comision = b * 0.04
        tramo = "8001 € - 12000 €"
        porcentaje = 4
    elif b <= 17000:
        comision = b * 0.05
        tramo = "12001 € - 17000 €"
        porcentaje = 5
    elif b <= 25000:
        comision = b * 0.06
        tramo = "17001 € - 25000 €"
        porcentaje = 6
    elif b <= 30000:
        comision = b * 0.07
        tramo = "25001 € - 30000 €"
        porcentaje = 7
    elif b <= 50000:
        comision = b * 0.08
        tramo = "30001 € - 50000 €"
        porcentaje = 8
    else:
        comision = b * 0.09
        tramo = "> 50000 €"
        porcentaje = 9

    return {
        "beneficio": b,
        "tramo": tramo,
        "porcentaje": porcentaje,
        "comision_calculada": comision
    }

if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()

    # Aplicar limpieza del campo beneficio financiación comercial para formato europeo
    df_raw["Beneficio financiación comercial"] = df_raw["Beneficio financiación comercial"].apply(limpiar_eur)

    if "Delegación" not in df_raw.columns:
        df_raw["Delegación"] = df_raw.iloc[:, -1]
    else:
        df_raw["Delegación"] = df_raw["Delegación"]

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

    delegaciones = ["Todas"] + sorted(resumen["delegacion"].dropna().unique().tolist())
    seleccion_delegacion = st.selectbox("Filtrar por Delegación", delegaciones)

    if seleccion_delegacion != "Todas":
        resumen = resumen[resumen["delegacion"] == seleccion_delegacion]

    comerciales_filtrados = ["Todos"] + sorted(resumen["ownername"].unique().tolist())
    seleccion_comercial = st.selectbox("Filtrar por Comercial", comerciales_filtrados)

    if seleccion_comercial != "Todos":
        resumen = resumen[resumen["ownername"] == seleccion_comercial]

    resumen = resumen.sort_values(by=["delegacion", "ownername"]).reset_index(drop=True)

    st.markdown("<div class='result-section'>", unsafe_allow_html=True)

    for i, row in resumen.iterrows():
        nuevo_flag = False
        jefe_flag = False

        # Aquí podrías poner una condición para identificar nuevos comerciales o jefes
        # ejemplo:
        # nuevo_flag = row['ownername'] in lista_nuevos_comerciales
        # jefe_flag = row['ownername'] in lista_jefes

        resultado = calcular_comision_fila(row, nuevo_flag, jefe_flag)

        st.markdown(f"### Comercial: {row['ownername']} - Delegación: {row['delegacion']}")
        st.markdown(f"- Total comisión antes de penalizaciones: {resultado['prima_total']:.2f} €")
        st.markdown(f"- Penalizaciones aplicadas: {', '.join([p[0] for p in resultado['penalizaciones_detalle']]) or 'Ninguna'}")
        st.markdown(f"- Total comisión final: {resultado['prima_final']:.2f} €")

        # Aquí mostramos el resumen de cómo se calcula la comisión por beneficio:
        resumen_beneficio = resumen_comision_beneficio(row["beneficio_financiacion_total"])
        st.markdown("#### Resumen Comisión por Beneficio")
        st.markdown(f"- Beneficio Financiación Total: {resumen_beneficio['beneficio']:.2f} €")
        st.markdown(f"- Tramo aplicable: {resumen_beneficio['tramo']}")
        st.markdown(f"- Porcentaje aplicado: {resumen_beneficio['porcentaje']}%")
        st.markdown(f"- Comisión calculada: {resumen_beneficio['comision_calculada']:.2f} €")

        # Si quieres también el desglose completo de cada concepto:
        st.markdown("#### Desglose completo comisiones y bonos:")
        for clave, valor in resultado['desglose'].items():
            st.markdown(f"- {clave.replace('_',' ').capitalize()}: {valor:.2f} €")

        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)


