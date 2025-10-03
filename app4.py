import streamlit as st
import os, csv, glob
from datetime import datetime
from fpdf import FPDF

# ================================
# CONFIG INICIAL
# ================================
st.set_page_config(page_title="Análisis de Suelos", page_icon="🌱", layout="wide")

# ================================
# ESTILOS (CSS)
# ================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: 600;
    transition: 0.25s ease;
    border: 0;
}
div.stButton > button:hover {
    background-color: #3c9442;
    color: #f9f9f9;
    transform: translateY(-1px);
}
.box-section {
    background-color: #f9fdfb;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e0ebe4;
    margin-bottom: 16px;
}
.box-section h3 {
    margin-top: 0;
    margin-bottom: 8px;
}
.stSelectbox > div > div {
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# ================================
# FUNCIÓN: Generar PDF
# ================================
def generar_pdf(lang_code, resumen, interpretacion, recomendaciones):
    pdf = FPDF()
    pdf.add_page()

    # Fuente
    pdf.set_font("Arial", "", 12)

    # Logo
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=80, y=10, w=50)
        pdf.ln(35)

    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "🌱 Análisis de Suelo" if lang_code=="es" else "🌱 Análise de Solo", ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, datetime.now().strftime("%d/%m/%Y %H:%M"), ln=True, align="C")
    pdf.ln(10)

    # Resumen
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "1️⃣ Resumen" if lang_code=="es" else "1️⃣ Resumo", ln=True)
    pdf.set_font("Arial", "", 11)
    for item in resumen:
        pdf.multi_cell(0, 8, f"- {item}")
    pdf.ln(5)

    # Interpretación
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "2️⃣ Interpretación técnica" if lang_code=="es" else "2️⃣ Interpretação técnica", ln=True)
    pdf.set_font("Arial", "", 11)
    for parrafo in interpretacion:
        pdf.multi_cell(0, 8, parrafo)
    pdf.ln(5)

    # Recomendaciones
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "3️⃣ Recomendaciones" if lang_code=="es" else "3️⃣ Recomendações", ln=True)
    pdf.set_font("Arial", "", 11)
    for rec in recomendaciones:
        pdf.multi_cell(0, 8, rec)

    out = f"analisis_suelo_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(out)
    return out

# ================================
# LOGO (sidebar)
# ================================
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
else:
    st.sidebar.markdown("**Kawsaypacha – Tierra Viva**")

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
""",
        "upload_label": "📤 Subir imagen de suelo",
        "uploaded_caption": "📸 Imagen subida",
        "color_label": "🎨 Color del suelo",
        "texture_label": "🌾 Textura del suelo",
        "aggregation_label": "🧱 Forma / Estructura",
        "moisture_label": "💧 Humedad",
        "roots_label": "🌱 Presencia de raíces",
        "interpret_block_title": "2️⃣ Interpretación técnica",
        "recs_title": "3️⃣ Recomendaciones de manejo",
        "save_button": "💾 Guardar análisis",
        "pdf_button": "📥 Descargar reporte en PDF",
        "csv_file": "analisis_suelos.csv",
        "placeholder": "Seleccionar opción",
        "moisture_opts": ["Seleccionar opción","Baja","Media","Alta"],
        "roots_opts": ["Seleccionar opción","Ausentes","Escasas","Abundantes"],
        "color_opts": ["Seleccionar opción","rojo-intenso","rojo-amarillento","amarillo","marrón","pardo-marrón","negro","gris","blanco"],
        "texture_opts": ["Seleccionar opción","arcilloso","arenoso","franco","limoso"],
        "structure_opts": ["Seleccionar opción","granular","migajosa","bloques","prismatica-columnar","laminar","masiva","suelto"],
        "no_images_msg": "No se encontraron imágenes en la carpeta",
        "no_folder_msg": "No existe carpeta de referencia para",
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
""",
        "upload_label": "📤 Enviar imagem do solo",
        "uploaded_caption": "📸 Imagem enviada",
        "color_label": "🎨 Cor do solo",
        "texture_label": "🌾 Textura do solo",
        "aggregation_label": "🧱 Forma / Estrutura",
        "moisture_label": "💧 Umidade",
        "roots_label": "🌱 Presença de raízes",
        "interpret_block_title": "2️⃣ Interpretação técnica",
        "recs_title": "3️⃣ Recomendações de manejo",
        "save_button": "💾 Salvar análise",
        "pdf_button": "📥 Baixar relatório em PDF",
        "csv_file": "analises_solos.csv",
        "placeholder": "Selecionar opção",
        "moisture_opts": ["Selecionar opção","Baixa","Média","Alta"],
        "roots_opts": ["Selecionar opção","Ausentes","Escassas","Abundantes"],
        "color_opts": ["Selecionar opção","vermelho-intenso","vermelho-amarelado","amarelo","marrom","pardo-marrom","preto","cinza","branco"],
        "texture_opts": ["Selecionar opção","argiloso","arenoso","franco","siltoso"],
        "structure_opts": ["Selecionar opção","granular","migajosa","blocos","prismática-colunar","laminar","maciça","solto"],
        "no_images_msg": "Não foram encontradas imagens na pasta",
        "no_folder_msg": "Não existe pasta de referência para",
    },
}

# ================================
# MAPEOS DE CARPETAS PARA REFERENCIAS
# ================================
COLOR_FOLDER_MAP = {
    "es": {"rojo-intenso":"rojo-intenso","rojo-amarillento":"rojo-amarillento","amarillo":"amarillo","marrón":"marron","pardo-marrón":"pardo-marron","negro":"negro","gris":"gris","blanco":"blanco"},
    "pt": {"vermelho-intenso":"rojo-intenso","vermelho-amarelado":"rojo-amarillento","amarelo":"amarillo","marrom":"marron","pardo-marrom":"pardo-marron","preto":"negro","cinza":"gris","branco":"blanco"}
}
TEXTURE_FOLDER_MAP = {
    "es":{"arcilloso":"arcilloso","arenoso":"arenoso","franco":"franco","limoso":"limoso"},
    "pt":{"argiloso":"arcilloso","arenoso":"arenoso","franco":"franco","siltoso":"limoso"}
}
STRUCTURE_FOLDER_MAP = {
    "es":{"granular":"granular","migajosa":"migajosa","bloques":"bloques","prismatica-columnar":"prismatica-columnar","laminar":"laminar","masiva":"masiva","suelto":"suelto"},
    "pt":{"granular":"granular","migajosa":"migajosa","blocos":"bloques","prismática-colunar":"prismatica-columnar","laminar":"laminar","maciça":"masiva","solto":"suelto"}
}

# ================================
# CONTROL INTRO
# ================================
if "show_intro" not in st.session_state:
    st.session_state["show_intro"] = True

lang = st.sidebar.radio("🌍 Idioma / Language", ["es", "pt"], index=0)
t = TEXT_CONTENT[lang]

if st.session_state["show_intro"]:
    st.title(t["app_title"])
    st.markdown(t["intro"])
    if st.button("➡️ Iniciar" if lang=="es" else "➡️ Iniciar análise"):
        st.session_state["show_intro"] = False
        st.rerun()
    st.stop()

# ================================
# FUNCIÓN CARRUSEL
# ================================
def mostrar_referencias(categoria: str, seleccion: str, lang_code: str):
    if seleccion == TEXT_CONTENT[lang_code]["placeholder"]:
        return
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
        imagenes = sorted(glob.glob(os.path.join(base_path,"*.png"))+glob.glob(os.path.join(base_path,"*.jpg"))+glob.glob(os.path.join(base_path,"*.jpeg")))
        if imagenes:
            key_carousel = f"carousel_{categoria}_{seleccion}"
            if key_carousel not in st.session_state:
                st.session_state[key_carousel] = 0
            col1,col2,col3 = st.columns([1,3,1])
            with col1:
                if st.button("⬅️", key=f"prev_{key_carousel}"):
                    st.session_state[key_carousel] = (st.session_state[key_carousel]-1)%len(imagenes)
            with col3:
                if st.button("➡️", key=f"next_{key_carousel}"):
                    st.session_state[key_carousel] = (st.session_state[key_carousel]+1)%len(imagenes)
            img_path = imagenes[st.session_state[key_carousel]]
            st.image(img_path, caption=f"{seleccion} ({st.session_state[key_carousel]+1}/{len(imagenes)})", width=300)
        else:
            st.warning(f"{t['no_images_msg']} {base_path}")
    else:
        st.info(f"{t['no_folder_msg']} {seleccion}")

# ================================
# PÁGINA PRINCIPAL
# ================================
st.title(t["app_title"])

uploaded_file = st.file_uploader(t["upload_label"], type=["jpg","jpeg","png"])
if uploaded_file:
    st.image(uploaded_file, caption=t["uploaded_caption"], use_container_width=True)

# Selectores con carrusel
color = st.selectbox(t["color_label"], t["color_opts"])
mostrar_referencias("color", color, lang)

textura = st.selectbox(t["texture_label"], t["texture_opts"])
mostrar_referencias("textura", textura, lang)

estructura = st.selectbox(t["aggregation_label"], t["structure_opts"])
mostrar_referencias("forma-estructura", estructura, lang)

humedad = st.selectbox(t["moisture_label"], t["moisture_opts"])
raices = st.selectbox(t["roots_label"], t["roots_opts"])

# ================================
# ANÁLISIS
# ================================
ready = uploaded_file and color!=t["placeholder"] and textura!=t["placeholder"] and estructura!=t["placeholder"] and humedad!=t["placeholder"] and raices!=t["placeholder"]

if ready:
    resumen_list = [
        f"{t['color_label']}: {color}",
        f"{t['texture_label']}: {textura}",
        f"{t['aggregation_label']}: {estructura}",
        f"{t['moisture_label']}: {humedad}",
        f"{t['roots_label']}: {raices}",
    ]

    interp = INTERP[lang]
    piezas = [
        interp["color"].get(color,""),
        interp["texture"].get(textura,""),
        interp["structure"].get(estructura,""),
        interp["moisture"].get(humedad,""),
        interp["roots"].get(raices,""),
    ]

    recs = []
    if humedad in ["Alta","Baixa"]:
        recs.append("⚠️ Revisar drenaje del suelo.")
    if humedad in ["Baja","Baixa"]:
        recs.append("💧 Implementar riego o cobertura vegetal.")
    if textura in ["arcilloso","argiloso"]:
        recs.append("🌱 Evitar laboreo en húmedo, usar raíces y coberturas.")
    if textura in ["arenoso","arenoso"]:
        recs.append("🌱 Aumentar MO y fraccionar fertilización.")
    if not recs:
        recs.append("✅ Mantener buenas prácticas de manejo.")

    # Mostrar interpretación y recomendaciones
    st.subheader(t["interpret_block_title"])
    for p in piezas: st.info(p)

    st.subheader(t["recs_title"])
    for r in recs: st.warning(r)

    # PDF
    pdf_file = generar_pdf(lang, resumen_list, piezas, recs)
    with open(pdf_file,"rb") as f:
        st.download_button(t["pdf_button"], f, file_name=pdf_file, mime="application/pdf", use_container_width=True)


