import streamlit as st
import os
from PIL import Image

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(page_title="Análisis Visual de Suelos", page_icon="🌱", layout="wide")

# ---------------- TEXTOS MULTILINGÜES ----------------
TEXT_CONTENT = {
    "es": {
        "title": "Análisis Visual de Suelos",
        "intro": "Bienvenido a la plataforma educativa de análisis visual de suelos. Aquí podrás subir una imagen, elegir las características del suelo y comparar con referencias visuales. Al final obtendrás un análisis con interpretación técnica y recomendaciones.",
        "upload": "Sube una imagen de suelo",
        "color": "Seleccionar color",
        "texture": "Seleccionar textura",
        "structure": "Seleccionar estructura",
        "moisture": "Seleccionar humedad",
        "roots": "Seleccionar raíces",
        "conclusion": "Conclusión del análisis",
        "summary": "Resumen de la muestra",
        "interpretation": "Interpretación",
        "recommendations": "Recomendaciones"
    },
    "pt": {
        "title": "Análise Visual de Solos",
        "intro": "Bem-vindo à plataforma educativa de análise visual de solos. Aqui você poderá carregar uma imagem, escolher as características do solo e comparar com referências visuais. No final, obterá uma análise com interpretação técnica e recomendações.",
        "upload": "Carregue uma imagem do solo",
        "color": "Selecionar cor",
        "texture": "Selecionar textura",
        "structure": "Selecionar estrutura",
        "moisture": "Selecionar umidade",
        "roots": "Selecionar raízes",
        "conclusion": "Conclusão da análise",
        "summary": "Resumo da amostra",
        "interpretation": "Interpretação",
        "recommendations": "Recomendações"
    }
}

# ---------------- MAPEO DE CARPETAS (evitar tildes/ñ) ----------------
COLOR_FOLDER_MAP = {
    "marrón": "marron",
    "pardo-marrón": "pardo-marron",
    "negro": "negro",
    "rojo-intenso": "rojo-intenso",
    "rojo-amarillento": "rojo-amarillento",
    "gris": "gris",
    "blanco": "blanco",
    "amarillo": "amarillo"
}

# ---------------- INTERPRETACIONES DETALLADAS ----------------
INTERPRETACIONES = {
    "es": {
        "color": {
            "marrón": "El color marrón indica un suelo con contenido moderado de materia orgánica, asociado generalmente a fertilidad intermedia.",
            "negro": "El color negro revela alto contenido de carbono orgánico y fertilidad elevada, común en suelos ricos en humus.",
            "rojo-intenso": "El color rojo indica abundancia de óxidos de hierro, asociado a buen drenaje, aunque con menor materia orgánica.",
            "rojo-amarillento": "El color rojo-amarillento refleja condiciones de oxidación variables y suelos con fertilidad media.",
            "gris": "El color gris indica condiciones reductoras por exceso de humedad (hidromorfismo), típico de suelos anegados.",
            "blanco": "El color blanco se relaciona con arenas pobres o acumulación de sales/carbonatos, con baja fertilidad.",
            "amarillo": "El color amarillo puede asociarse a drenaje deficiente y procesos de lixiviación intensos."
        },
        "texture": {
            "arcilloso": "La textura arcillosa implica alta retención de agua y nutrientes, pero con drenaje lento que puede favorecer la compactación.",
            "arenoso": "La textura arenosa se caracteriza por baja capacidad de retención de agua y nutrientes, lo que limita la fertilidad.",
            "franco": "La textura franca es un equilibrio entre arena, limo y arcilla, considerada ideal para la mayoría de cultivos."
        },
        "structure": {
            "granular": "La estructura granular favorece la aireación, el drenaje y la penetración de raíces.",
            "bloques": "La estructura en bloques puede limitar parcialmente el crecimiento de raíces por compactación moderada.",
            "prismática": "La estructura prismática o columnar limita el drenaje y puede generar capas endurecidas.",
            "laminar": "La estructura laminar refleja fuerte compactación, raíces superficiales y pobre aireación.",
            "masiva": "La estructura masiva carece de agregados definidos, presentando escasa porosidad y baja fertilidad."
        },
        "moisture": {
            "baja": "La humedad baja sugiere riesgo de déficit hídrico y limitación para el crecimiento vegetal.",
            "alta": "La humedad alta indica riesgo de anegamiento, reducción de oxígeno y condiciones reductoras."
        },
        "roots": {
            "abundantes": "La presencia abundante de raíces refleja condiciones favorables para el desarrollo vegetal.",
            "ausentes": "La ausencia de raíces puede indicar limitaciones físicas o químicas que restringen el crecimiento."
        }
    },
    "pt": {
        "color": {
            "marrón": "A cor marrom indica um solo com teor moderado de matéria orgânica, geralmente associado à fertilidade intermediária.",
            "negro": "A cor preta revela alto teor de carbono orgânico e fertilidade elevada, comum em solos ricos em húmus.",
            "rojo-intenso": "A cor vermelha indica abundância de óxidos de ferro, associada a boa drenagem, mas com menor matéria orgânica.",
            "rojo-amarillento": "A cor vermelho-amarelada reflete condições de oxidação variáveis e solos de fertilidade média.",
            "gris": "A cor cinza indica condições redutoras por excesso de umidade (hidromorfismo), típico de solos encharcados.",
            "blanco": "A cor branca está relacionada a areias pobres ou acúmulo de sais/carbonatos, com baixa fertilidade.",
            "amarillo": "A cor amarela pode estar associada a drenagem deficiente e processos intensos de lixiviação."
        },
        "texture": {
            "arcilloso": "A textura argilosa implica alta retenção de água e nutrientes, mas drenagem lenta que pode favorecer a compactação.",
            "arenoso": "A textura arenosa caracteriza-se por baixa capacidade de retenção de água e nutrientes, o que limita a fertilidade.",
            "franco": "A textura franca é um equilíbrio entre areia, silte e argila, considerada ideal para a maioria das culturas."
        },
        "structure": {
            "granular": "A estrutura granular favorece a aeração, a drenagem e a penetração de raízes.",
            "bloques": "A estrutura em blocos pode limitar parcialmente o crescimento de raízes por compactação moderada.",
            "prismática": "A estrutura prismática ou colunar limita a drenagem e pode gerar camadas endurecidas.",
            "laminar": "A estrutura laminar reflete forte compactação, raízes superficiais e pobre aeração.",
            "masiva": "A estrutura maciça carece de agregados definidos, apresentando baixa porosidade e fertilidade reduzida."
        },
        "moisture": {
            "baja": "A baixa umidade sugere risco de déficit hídrico e limitação ao crescimento vegetal.",
            "alta": "A alta umidade indica risco de encharcamento, redução de oxigênio e condições redutoras."
        },
        "roots": {
            "abundantes": "A presença abundante de raízes reflete condições favoráveis ao desenvolvimento vegetal.",
            "ausentes": "A ausência de raízes pode indicar limitações físicas ou químicas que restringem o crescimento."
        }
    }
}

# ---------------- FUNCIÓN CARRUSEL ----------------
def mostrar_referencias(categoria, seleccion, carpeta_base="referencias"):
    folder = None
    if categoria == "color":
        folder = COLOR_FOLDER_MAP.get(seleccion, seleccion)
        folder_path = os.path.join(carpeta_base, categoria, folder)
    else:
        folder_path = os.path.join(carpeta_base, categoria, seleccion)

    if os.path.exists(folder_path):
        imagenes = [f for f in os.listdir(folder_path) if f.endswith((".png", ".jpg"))]
        if imagenes:
            if f"{categoria}_{seleccion}" not in st.session_state:
                st.session_state[f"{categoria}_{seleccion}"] = 0
            idx = st.session_state[f"{categoria}_{seleccion}]
            img = Image.open(os.path.join(folder_path, imagenes[idx]))
            st.image(img, width=250, caption=f"{seleccion} ({idx+1}/{len(imagenes)})")
            col1, col2 = st.columns(2)
            if col1.button("⏪", key=f"prev_{categoria}_{seleccion}"):
                st.session_state[f"{categoria}_{seleccion}"] = (idx - 1) % len(imagenes)
                st.rerun()
            if col2.button("⏩", key=f"next_{categoria}_{seleccion}"):
                st.session_state[f"{categoria}_{seleccion}"] = (idx + 1) % len(imagenes)
                st.rerun()

# ---------------- INTERFAZ ----------------
lang = st.sidebar.radio("🌎 Idioma / Language", ["es", "pt"])
t = TEXT_CONTENT[lang]

st.title(t["title"])
st.write(t["intro"])

# Subida de imagen
uploaded_file = st.file_uploader(t["upload"], type=["png", "jpg", "jpeg"])

# Selectores con opción inicial
color = st.selectbox(t["color"], ["Seleccionar opción", "marrón", "pardo-marrón", "negro", "rojo-intenso", "rojo-amarillento", "gris", "blanco", "amarillo"])
texture = st.selectbox(t["texture"], ["Seleccionar opción", "arcilloso", "arenoso", "franco"])
structure = st.selectbox(t["structure"], ["Seleccionar opción", "granular", "bloques", "prismática", "laminar", "masiva"])
moisture = st.selectbox(t["moisture"], ["Seleccionar opción", "baja", "alta"])
roots = st.selectbox(t["roots"], ["Seleccionar opción", "abundantes", "ausentes"])

# Mostrar referencias
if color != "Seleccionar opción":
    mostrar_referencias("color", color)
if texture != "Seleccionar opción":
    mostrar_referencias("texture", texture)
if structure != "Seleccionar opción":
    mostrar_referencias("structure", structure)

# ---------------- CONCLUSIÓN ----------------
if uploaded_file and all(s != "Seleccionar opción" for s in [color, texture, structure, moisture, roots]):
    st.subheader(t["conclusion"])
    img = Image.open(uploaded_file)
    st.image(img, width=300, caption="Imagen analizada")

    st.markdown(f"**{t['summary']}:** {color}, {texture}, {structure}, {moisture}, {roots}")

    st.markdown(f"**{t['interpretation']}:**")
    interp = INTERPRETACIONES[lang]
    texto = []
    texto.append(interp["color"][color])
    texto.append(interp["texture"][texture])
    texto.append(interp["structure"][structure])
    texto.append(interp["moisture"][moisture])
    texto.append(interp["roots"][roots])
    st.write(" ".join(texto))

    st.markdown(f"**{t['recommendations']}:**")
    if moisture == "baja":
        st.write("👉 Mantener cobertura del suelo y considerar riego suplementario.")
    elif moisture == "alta":
        st.write("👉 Mejorar drenaje y evitar compactación excesiva.")
    else:
        st.write("👉 Incorporar materia orgánica y prácticas de conservación.")

