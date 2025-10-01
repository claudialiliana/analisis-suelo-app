import streamlit as st
import os, csv, glob

# ================================
# CONFIG INICIAL
# ================================
st.set_page_config(page_title="Análisis de Suelos", page_icon="🌱", layout="wide")

# ================================
# MAPEOS DE CARPETAS (sin tildes)
# ================================
COLOR_FOLDER_MAP = {
    "es": {
        "rojo-intenso": "rojo-intenso",
        "rojo-amarillento": "rojo-amarillento",
        "amarillo": "amarillo",
        "marrón": "marron",
        "pardo-marrón": "pardo-marron",
        "negro": "negro",
        "gris": "gris",
        "blanco": "blanco",
    },
    "pt": {
        "vermelho-intenso": "rojo-intenso",
        "vermelho-amarelado": "rojo-amarillento",
        "amarelo": "amarillo",
        "marrom": "marron",
        "pardo-marrom": "pardo-marron",
        "preto": "negro",
        "cinza": "gris",
        "branco": "blanco",
    },
}

TEXTURE_FOLDER_MAP = {
    "es": {"arcilloso": "arcilloso", "arenoso": "arenoso", "franco": "franco", "limoso": "limoso"},
    "pt": {"argiloso": "arcilloso", "arenoso": "arenoso", "franco": "franco", "siltoso": "limoso"},
}

STRUCTURE_FOLDER_MAP = {
    "es": {
        "granular": "granular",
        "migajosa": "migajosa",
        "bloques": "bloques",
        "prismatica-columnar": "prismatica-columnar",
        "laminar": "laminar",
        "masiva": "masiva",
        "suelto": "suelto",
    },
    "pt": {
        "granular": "granular",
        "migajosa": "migajosa",
        "blocos": "bloques",
        "prismática-colunar": "prismatica-columnar",
        "laminar": "laminar",
        "maciça": "masiva",
        "solto": "suelto",
    },
}

# ================================
# TEXTOS MULTILINGÜES
# ================================
TEXT_CONTENT = {
    "es": {
        "app_title": "🌱 Análisis Visual de Suelos",
        "intro": """
        **Bienvenido/a a esta plataforma educativa para explorar el mundo del suelo de manera visual e interactiva.**  
        Aquí podrás analizar algunas de sus principales características físicas y comprender cómo influyen en su interpretación.  

        👉 Elige primero el **idioma que prefieras** y luego:
        1. **Sube una imagen de suelo** que quieras analizar.  
        2. **Selecciona sus características** (color, textura, estructura, humedad, raíces).  
        3. **Compara con las referencias visuales** que irán apareciendo en cada categoría.  

        De esta manera, tendrás una experiencia guiada paso a paso, como si tuvieras una “lupa virtual” para comprender mejor el suelo. 🚀
        """,
        "upload_label": "📤 Subir imagen de suelo",
        "uploaded_caption": "📸 Imagen subida",
        "color_label": "🎨 Color del suelo",
        "texture_label": "🌾 Textura del suelo",
        "aggregation_label": "🧱 Forma / Estructura",
        "moisture_label": "💧 Humedad",
        "roots_label": "🌱 Presencia de raíces",
        "save_button": "💾 Guardar análisis",
        "download_all": "⬇️ Descargar todos los análisis",
        "interpret_title": "📊 Conclusión del análisis",
        "moisture_opts": ["Baja", "Media", "Alta"],
        "roots_opts": ["Ausentes", "Escasas", "Abundantes"],
        "color_opts": ["rojo-intenso", "rojo-amarillento", "amarillo", "marrón", "pardo-marrón", "negro", "gris", "blanco"],
        "texture_opts": ["arcilloso", "arenoso", "franco", "limoso"],
    },
    "pt": {
        "app_title": "🌱 Análise Visual de Solos",
        "intro": """
        **Bem-vindo(a) a esta plataforma educativa para explorar o mundo do solo de forma visual e interativa.**  
        Aqui você poderá analisar algumas de suas principais características físicas e entender como elas influenciam na interpretação do solo.  

        👉 Primeiro, escolha o **idioma de sua preferência** e depois:
        1. **Envie uma imagem do solo** que deseja analisar.  
        2. **Selecione suas características** (cor, textura, estrutura, umidade, raízes).  
        3. **Compare com as referências visuais** que aparecerão em cada categoria.  

        Assim, você terá uma experiência guiada passo a passo, como se fosse uma “lupa virtual” para compreender melhor o solo. 🚀
        """,
        "upload_label": "📤 Enviar imagem do solo",
        "uploaded_caption": "📸 Imagem enviada",
        "color_label": "🎨 Cor do solo",
        "texture_label": "🌾 Textura do solo",
        "aggregation_label": "🧱 Forma / Estrutura",
        "moisture_label": "💧 Umidade",
        "roots_label": "🌱 Presença de raízes",
        "save_button": "💾 Salvar análise",
        "download_all": "⬇️ Baixar todas as análises",
        "interpret_title": "📊 Conclusão da análise",
        "moisture_opts": ["Baixa", "Média", "Alta"],
        "roots_opts": ["Ausentes", "Escassas", "Abundantes"],
        "color_opts": ["vermelho-intenso", "vermelho-amarelado", "amarelo", "marrom", "pardo-marrom", "preto", "cinza", "branco"],
        "texture_opts": ["argiloso", "arenoso", "franco", "siltoso"],
    },
}

# ================================
# CONTROL DE PANTALLA INTRO
# ================================
if "show_intro" not in st.session_state:
    st.session_state["show_intro"] = True

lang = st.sidebar.radio("🌍 Idioma / Language", ["es", "pt"], index=0)
t = TEXT_CONTENT[lang]

if st.session_state["show_intro"]:
    st.title(t["app_title"])
    st.markdown(t["intro"])
    if st.button("➡️ Comenzar análisis" if lang == "es" else "➡️ Iniciar análise"):
        st.session_state["show_intro"] = False
        st.experimental_rerun()
    st.stop()

# ================================
# FUNCIÓN CARRUSEL
# ================================
def mostrar_referencias(categoria: str, seleccion: str, lang_code: str):
    if categoria == "color":
        carpeta = COLOR_FOLDER_MAP[lang_code].get(seleccion, seleccion.lower())
    elif categoria == "textura":
        carpeta = TEXTURE_FOLDER_MAP[lang_code].get(seleccion, seleccion.lower())
    elif categoria == "forma-estructura":
        carpeta = STRUCTURE_FOLDER_MAP[lang_code].get(seleccion, seleccion.lower())
    else:
        carpeta = seleccion.lower()

    base_path = os.path.join("referencias", categoria, carpeta)
    if os.path.exists(base_path):
        imagenes = sorted(
            glob.glob(os.path.join(base_path, "*.png")) +
            glob.glob(os.path.join(base_path, "*.jpg")) +
            glob.glob(os.path.join(base_path, "*.jpeg"))
        )

        if imagenes:
            key_carousel = f"carousel_{categoria}_{seleccion}"
            if key_carousel not in st.session_state:
                st.session_state[key_carousel] = 0

            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                if st.button("⬅️", key=f"prev_{key_carousel}"):
                    st.session_state[key_carousel] = (st.session_state[key_carousel] - 1) % len(imagenes)
            with col3:
                if st.button("➡️", key=f"next_{key_carousel}"):
                    st.session_state[key_carousel] = (st.session_state[key_carousel] + 1) % len(imagenes)

            img_path = imagenes[st.session_state[key_carousel]]
            st.image(img_path, caption=f"{seleccion} ({st.session_state[key_carousel]+1}/{len(imagenes)})", width=300)

# ================================
# PÁGINA PRINCIPAL
# ================================
st.title(t["app_title"])

# Imagen subida siempre arriba
uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption=t["uploaded_caption"], use_column_width=True)

# Selectores y carruseles
color = st.selectbox(t["color_label"], t["color_opts"])
mostrar_referencias("color", color, lang)

textura = st.selectbox(t["texture_label"], t["texture_opts"])
mostrar_referencias("textura", textura, lang)

estructura = st.selectbox(t["aggregation_label"], list(STRUCTURE_FOLDER_MAP[lang].keys()))
mostrar_referencias("forma-estructura", estructura, lang)

humedad = st.selectbox(t["moisture_label"], t["moisture_opts"])
raices = st.selectbox(t["roots_label"], t["roots_opts"])

# Conclusión destacada
st.markdown(f"### {t['interpret_title']}")
st.success(f"El análisis seleccionado muestra: {color}, {textura}, {estructura}, humedad {humedad}, raíces {raices}.")

# Recomendaciones extra
st.markdown("#### 🌱 Recomendaciones / Recomendações:")
st.write("• Mejorar drenaje en caso de exceso de humedad. / Melhorar a drenagem em caso de excesso de umidade.")
st.write("• Incorporar materia orgánica para aumentar la fertilidad. / Incorporar matéria orgânica para aumentar a fertilidade.")
