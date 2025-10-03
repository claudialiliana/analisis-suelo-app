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
</style>
""", unsafe_allow_html=True)

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
        "start_btn": "🚀 Comenzar análisis",
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
        "select_phrase": "👉 Selecciona tu opción comparando con la referencia:",
        "summary_title": "1️⃣ Resumen",
        "interpret_block_title": "2️⃣ Interpretación técnica",
        "recs_title": "3️⃣ Recomendaciones de manejo",
        "save_button": "💾 Guardar análisis",
        "pdf_button": "📥 Descargar reporte en PDF",
        "csv_file": "analisis_suelos.csv",
        "placeholder": "Seleccionar opción",
        "moisture_opts": ["Seleccionar opción", "Baja", "Media", "Alta"],
        "roots_opts": ["Seleccionar opción", "Ausentes", "Escasas", "Abundantes"],
        "color_opts": ["Seleccionar opción", "rojo-intenso", "rojo-amarillento", "amarillo", "marrón", "pardo-marrón", "negro", "gris", "blanco"],
        "texture_opts": ["Seleccionar opción", "arcilloso", "arenoso", "franco", "limoso"],
        "structure_opts": ["Seleccionar opción", "granular", "migajosa", "bloques", "prismatica-columnar", "laminar", "masiva", "suelto"],
        "no_images_msg": "No se encontraron imágenes en la carpeta",
        "no_folder_msg": "No existe carpeta de referencia para",
    },
   "pt": {
        "app_title": "🌱 Análise Visual de Solos",
        "start_btn": "🚀 Iniciar análise",
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
        "select_phrase": "👉 Selecione sua opção comparando com a referência:",
        "summary_title": "1️⃣ Resumo",
        "interpret_block_title": "2️⃣ Interpretação técnica",
        "recs_title": "3️⃣ Recomendações de manejo",
        "save_button": "💾 Salvar análise",
        "pdf_button": "📥 Baixar relatório em PDF",
        "csv_file": "analises_solos.csv",
        "placeholder": "Selecionar opção",
        "moisture_opts": ["Selecionar opção", "Baixa", "Média", "Alta"],
        "roots_opts": ["Selecionar opção", "Ausentes", "Escassas", "Abundantes"],
        "color_opts": ["Selecionar opção", "vermelho-intenso", "vermelho-amarelado", "amarelo", "marrom", "pardo-marrom", "preto", "cinza", "branco"],
        "texture_opts": ["Selecionar opção", "argiloso", "arenoso", "franco", "siltoso"],
        "structure_opts": ["Selecionar opção", "granular", "migajosa", "blocos", "prismática-colunar", "laminar", "maciça", "solto"],
        "no_images_msg": "Não foram encontradas imagens na pasta",
        "no_folder_msg": "Não existe pasta de referência para",
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
    if st.button(t["start_btn"]):
        st.session_state["show_intro"] = False
        st.rerun()
    st.stop()
# ================================
# INTERPRETACIONES DETALLADAS
# ================================
INTERP = {
    "es": {
        "color": {
            "rojo-intenso": "El color rojo intenso refleja la presencia predominante de hematita...",
            "rojo-amarillento": "El color rojo-amarillento está vinculado a goethita hidratada...",
            "amarillo": "El amarillo indica suelos lixiviados con goethita...",
            "marrón": "El marrón refleja materia orgánica moderada y complejos Fe-Humus...",
            "pardo-marrón": "El pardo-marrón es de transición...",
            "negro": "El negro indica alto carbono orgánico...",
            "gris": "El gris indica condiciones reductoras (gley)...",
            "blanco": "El blanco puede deberse a arenas lavadas o sales...",
        },
        "texture": {
            "arcilloso": "Suelos con textura arcillosa presentan alta retención de agua...",
            "arenoso": "Los suelos arenosos drenan muy rápido...",
            "franco": "Los francos son equilibrados en arena, limo y arcilla...",
            "limoso": "Los limosos retienen agua pero se encostran fácilmente...",
        },
        "structure": {
            "granular": "Estructura granular, muy favorable para raíces...",
            "migajosa": "Estructura migajosa, excelente equilibrio aire-agua...",
            "bloques": "Bloques subangulares/angulares con posible restricción radicular...",
            "prismatica-columnar": "Prismática/columnares, asociadas a arcillas y sodicidad...",
            "laminar": "Laminada, restrictiva para infiltración y raíces...",
            "masiva": "Masiva, sin agregación, drenaje deficiente...",
            "suelto": "Suelto, típico de arenas, muy permeable pero pobre en nutrientes...",
        },
        "moisture": {
            "Baja": "Baja humedad, estrés hídrico posible...",
            "Media": "Humedad media, adecuada en la mayoría de cultivos...",
            "Alta": "Alta humedad, riesgo de anoxia y pérdida de estructura...",
        },
        "roots": {
            "Ausentes": "Sin raíces: limitaciones físicas o químicas posibles...",
            "Escasas": "Escasas raíces, actividad biológica reducida...",
            "Abundantes": "Abundantes raíces, suelo favorable para crecimiento...",
        },
    },
    "pt": {
        "color": {
            "vermelho-intenso": "Cor vermelha intensa indica hematita predominante...",
            "vermelho-amarelado": "Cor vermelho-amarelada associada a goethita hidratada...",
            "amarelo": "Amarelo sugere solos lixiviados com goethita...",
            "marrom": "Marrom reflete matéria orgânica moderada...",
            "pardo-marrom": "Pardo-marrom é transicional...",
            "preto": "Preto indica alto carbono orgânico...",
            "cinza": "Cinza indica condições redutoras (glei)...",
            "branco": "Branco pode estar ligado a areias lavadas ou sais...",
        },
        "texture": {
            "argiloso": "Solos argilosos retêm muita água...",
            "arenoso": "Arenosos drenam muito rápido...",
            "franco": "Franco tem bom equilíbrio de areia, silte e argila...",
            "siltoso": "Siltosos retêm água mas podem encrostar...",
        },
        "structure": {
            "granular": "Estrutura granular, muito favorável...",
            "migajosa": "Estrutura migajosa, boa para aeração...",
            "blocos": "Blocos angulares/subangulares...",
            "prismática-colunar": "Prismática/colunar associada a solos argilosos...",
            "laminar": "Laminar, restritiva para infiltração...",
            "maciça": "Maciça, sem estrutura definida...",
            "solto": "Solto, típico de areias, pobre em nutrientes...",
        },
        "moisture": {
            "Baixa": "Baixa umidade, risco de estresse hídrico...",
            "Média": "Umidade média, geralmente adequada...",
            "Alta": "Alta umidade, risco de encharcamento...",
        },
        "roots": {
            "Ausentes": "Ausência de raízes, possíveis limitações físicas...",
            "Escassas": "Raízes escassas, baixa atividade biológica...",
            "Abundantes": "Muitas raízes, solo fértil e bem estruturado...",
        },
    }
}

# ================================
# FUNCIÓN: Generar PDF
# ================================
def generar_pdf(lang_code, resumen, interpretacion, recomendaciones):
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=80, y=10, w=50)
        pdf.ln(35)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, TEXT_CONTENT[lang_code]["app_title"], ln=True, align="C")
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, datetime.now().strftime("%d/%m/%Y %H:%M"), ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, TEXT_CONTENT[lang_code]["summary_title"], ln=True)
    pdf.set_font("Arial", "", 11)
    for item in resumen:
        pdf.multi_cell(0, 8, f"- {item}")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, TEXT_CONTENT[lang_code]["interpret_block_title"], ln=True)
    pdf.set_font("Arial", "", 11)
    for parrafo in interpretacion:
        pdf.multi_cell(0, 8, parrafo)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, TEXT_CONTENT[lang_code]["recs_title"], ln=True)
    pdf.set_font("Arial", "", 11)
    for rec in recomendaciones:
        pdf.multi_cell(0, 8, rec)
    out = f"analisis_suelo_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(out)
    return out

# ================================
# FUNCIÓN CARRUSEL
# ================================
def mostrar_referencias(categoria: str, seleccion: str, lang_code: str):
    if not seleccion or seleccion == TEXT_CONTENT[lang_code]["placeholder"]:
        return
    if categoria == "color":
        carpeta = COLOR_FOLDER_MAP[lang_code].get(seleccion, str(seleccion).lower())
    elif categoria == "textura":
        carpeta = TEXTURE_FOLDER_MAP[lang_code].get(seleccion, str(seleccion).lower())
    elif categoria == "forma-estructura":
        carpeta = STRUCTURE_FOLDER_MAP[lang_code].get(seleccion, str(seleccion).lower())
    else:
        carpeta = str(seleccion).lower()
    base_path = os.path.join("referencias", categoria, carpeta)
    if os.path.exists(base_path):
        imagenes = sorted(
            glob.glob(os.path.join(base_path, "*.png")) +
            glob.glob(os.path.join(base_path, "*.jpg")) +
            glob.glob(os.path.join(base_path, "*.jpeg"))
        )
        if imagenes:
            key_carousel = f"carousel_{categoria}_{carpeta}"
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
            st.image(img_path, caption=f"{seleccion} ({st.session_state[key_carousel]+1}/{len(imagenes)})", width=320)
        else:
            st.warning(f"{TEXT_CONTENT[lang_code]['no_images_msg']}: {base_path}")
    else:
        st.info(f"{TEXT_CONTENT[lang_code]['no_folder_msg']} «{seleccion}» → {base_path}")

# ================================
# APP
# ================================
lang = st.sidebar.radio("🌍 Idioma / Language", ["es", "pt"], index=0)
t = TEXT_CONTENT[lang]

st.title(t["app_title"])

uploaded_file = st.file_uploader(t["upload_label"], type=["jpg","jpeg","png"])
if uploaded_file:
    st.image(uploaded_file, caption=t["uploaded_caption"], use_container_width=True)

# Selección con carrusel
st.markdown(f"**{t['select_phrase']}**")
color = st.selectbox(t["color_label"], t["color_opts"])
mostrar_referencias("color", color, lang)

st.markdown(f"**{t['select_phrase']}**")
textura = st.selectbox(t["texture_label"], t["texture_opts"])
mostrar_referencias("textura", textura, lang)

st.markdown(f"**{t['select_phrase']}**")
estructura = st.selectbox(t["aggregation_label"], t["structure_opts"])
mostrar_referencias("forma-estructura", estructura, lang)

humedad = st.selectbox(t["moisture_label"], t["moisture_opts"])
raices = st.selectbox(t["roots_label"], t["roots_opts"])

# ================================
# RESULTADOS
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
        interp["color"].get(color, ""),
        interp["texture"].get(textura, ""),
        interp["structure"].get(estructura, ""),
        interp["moisture"].get(humedad, ""),
        interp["roots"].get(raices, ""),
    ]
    recs = []
    if humedad in ["Alta","Baixa","Alta"]: recs.append("⚠️ Atención al manejo de agua")
    if not recs: recs.append("Mantener buenas prácticas de conservación.")
    st.markdown(f"### {t['summary_title']}")
    for r in resumen_list: st.write(f"- {r}")
    st.markdown(f"### {t['interpret_block_title']}")
    st.write(" ".join(piezas))
    st.markdown(f"### {t['recs_title']}")
    for r in recs: st.write(f"- {r}")
    # Guardar CSV
    if st.button(t["save_button"]):
        file_csv = t["csv_file"]
        headers_exist = os.path.exists(file_csv) and os.path.getsize(file_csv)>0
        with open(file_csv,"a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            if not headers_exist: writer.writerow(["Fecha","Idioma","Color","Textura","Estructura","Humedad","Raíces"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lang,color,textura,estructura,humedad,raices])
        st.success("✅ Análisis guardado en CSV")
    # PDF
    pdf_file = generar_pdf(lang,resumen_list,piezas,recs)
    with open(pdf_file,"rb") as f:
        st.download_button(t["pdf_button"],f,file_name=pdf_file,mime="application/pdf")






