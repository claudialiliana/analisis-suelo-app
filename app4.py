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

    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    if os.path.exists(font_path):
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", "", 12)
    else:
        pdf.set_font("Arial", "", 12)

    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=80, y=10, w=50)
        pdf.ln(35)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "🌱 Análisis de Suelo" if lang_code=="es" else "🌱 Análise de Solo", ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, datetime.now().strftime("%d/%m/%Y %H:%M"), ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "1️⃣ Resumen" if lang_code=="es" else "1️⃣ Resumo", ln=True)
    pdf.set_font("Arial", "", 11)
    for item in resumen:
        pdf.multi_cell(0, 8, f"- {item}")
    pdf.ln(5)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "2️⃣ Interpretación técnica" if lang_code=="es" else "2️⃣ Interpretação técnica", ln=True)
    pdf.set_font("Arial", "", 11)
    for parrafo in interpretacion:
        pdf.multi_cell(0, 8, parrafo)
    pdf.ln(5)

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
# TEXTOS
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

Tendrás una experiencia guiada paso a paso, como si fuera una “lupa virtual” para comprender mejor el suelo. 🚀
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

Você terá uma experiência guiada passo a passo, como uma “lupa virtual” para compreender melhor o solo. 🚀
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
    },
}

# ================================
# INTERPRETACIONES
# ================================
INTERP = {
    "es": {
        "color": {
            "rojo-intenso":"Óxidos de hierro abundantes, buen drenaje y aireación.",
            "negro":"Alto carbono orgánico, fértil pero riesgo de anegamiento.",
        },
        "texture": {
            "arcilloso":"Alta retención de agua y nutrientes, riesgo de compactación.",
            "arenoso":"Drenaje rápido, baja fertilidad.",
            "franco":"Equilibrio ideal para cultivos.",
        },
        "structure": {
            "granular":"Agregados pequeños, alta porosidad, excelente aireación.",
            "masiva":"Sin agregación, drenaje deficiente.",
        },
        "moisture": {
            "Baja":"Posible estrés hídrico.",
            "Alta":"Riesgo de anegamiento y pérdida de estructura.",
        },
        "roots": {
            "Ausentes":"Posibles limitaciones físicas o químicas.",
            "Abundantes":"Condición favorable para el desarrollo del suelo.",
        },
    },
    "pt": {
        "color": {
            "vermelho-intenso":"Óxidos de ferro abundantes, boa drenagem.",
            "preto":"Alto carbono orgânico, fértil mas risco de encharcamento.",
        },
        "texture": {
            "argiloso":"Alta retenção de água, risco de compactação.",
            "arenoso":"Drenagem rápida, baixa fertilidade.",
            "franco":"Equilíbrio ideal para cultivos.",
        },
        "structure": {
            "granular":"Agregados pequenos, excelente infiltração e aeração.",
            "maciça":"Sem agregação, drenagem deficiente.",
        },
        "moisture": {
            "Baixa":"Possível estresse hídrico.",
            "Alta":"Risco de encharcamento.",
        },
        "roots": {
            "Ausentes":"Limitações físicas ou químicas.",
            "Abundantes":"Boa porosidade e fertilidade.",
        },
    },
}

# ================================
# CONTROL INTRO
# ================================
if "show_intro" not in st.session_state:
    st.session_state["show_intro"] = True

lang = st.sidebar.radio("🌍 Idioma / Language", ["es","pt"], index=0)
t = TEXT_CONTENT[lang]

if st.session_state["show_intro"]:
    st.title(t["app_title"])
    st.markdown(t["intro"])
    if st.button("➡️ Continuar", use_container_width=True):
        st.session_state["show_intro"] = False
        st.rerun()
    st.stop()

# ================================
# PÁGINA PRINCIPAL
# ================================
st.title(t["app_title"])

uploaded_file = st.file_uploader(t["upload_label"], type=["jpg","jpeg","png"])
if uploaded_file:
    st.image(uploaded_file, caption=t["uploaded_caption"], use_container_width=True)

color = st.selectbox(t["color_label"], t["color_opts"])
textura = st.selectbox(t["texture_label"], t["texture_opts"])
estructura = st.selectbox(t["aggregation_label"], t["structure_opts"])
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

    # PDF
    pdf_file = generar_pdf(lang, resumen_list, piezas, recs)
    with open(pdf_file,"rb") as f:
        st.download_button(t["pdf_button"], f, file_name=pdf_file, mime="application/pdf", use_container_width=True)

