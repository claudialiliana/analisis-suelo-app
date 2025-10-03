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
# FUNCIÓN: Generar PDF
# ================================
def generar_pdf(lang_code, resumen, interpretacion, recomendaciones):
    pdf = FPDF()
    pdf.add_page()

    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=80, y=10, w=50)
        pdf.ln(35)

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
# TEXTOS GENERALES
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
        "summary_title": "1️⃣ Resumen del análisis",
        "interpret_block_title": "2️⃣ Interpretación técnica",
        "recs_title": "3️⃣ Recomendaciones de manejo",
        "save_button": "💾 Guardar análisis",
        "pdf_button": "📥 Descargar reporte en PDF",
        "csv_file": "analisis_suelos.csv",
        "placeholder": "Seleccionar opción",
        "analysis_image_caption": "Imagen analizada",
        "csv_saved": "✅ Análisis guardado correctamente.",
        "select_msg": "👉 Selecciona tu opción comparando con la referencia:",
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

Você terá uma experiência guiada passo a passo, como uma “lupa virtual” para compreender melhor o solo. 🚀
""",
        "upload_label": "📤 Enviar imagem do solo",
        "uploaded_caption": "📸 Imagem enviada",
        "color_label": "🎨 Cor do solo",
        "texture_label": "🌾 Textura do solo",
        "aggregation_label": "🧱 Forma / Estrutura",
        "moisture_label": "💧 Umidade",
        "roots_label": "🌱 Presença de raízes",
        "summary_title": "1️⃣ Resumo da análise",
        "interpret_block_title": "2️⃣ Interpretação técnica",
        "recs_title": "3️⃣ Recomendações de manejo",
        "save_button": "💾 Salvar análise",
        "pdf_button": "📥 Baixar relatório em PDF",
        "csv_file": "analises_solos.csv",
        "placeholder": "Selecionar opção",
        "analysis_image_caption": "Imagem analisada",
        "csv_saved": "✅ Análise salva corretamente.",
        "select_msg": "👉 Selecione sua opção comparando com a referência:",
        "no_images_msg": "Não foram encontradas imagens na pasta",
        "no_folder_msg": "Não existe pasta de referência para",
    },
}

# ================================
# INTERPRETACIONES DETALLADAS
# ================================
# Aquí van TODAS las interpretaciones largas que compartiste (color, textura, estructura, humedad, raíces)
# Ejemplo de estructura (debes completar con todos los textos largos que ya tienes):

INTERP = {
    "es": {
        "color": {
            "rojo-intenso": "El color rojo intenso suele reflejar abundancia de óxidos de hierro (hematita)...",
            "rojo-amarillento": "El color rojo-amarillento indica presencia de óxidos de hierro hidratados...",
            "amarillo": "El color amarillo está vinculado a goethita y a veces a condiciones de drenaje menos eficientes...",
            "marrón": "El color marrón suele reflejar contenido moderado de materia orgánica...",
            "pardo-marrón": "El pardo-marrón es una transición con influencia tanto de compuestos férricos...",
            "negro": "El color negro indica alto contenido de carbono orgánico y humificación avanzada...",
            "gris": "El color gris sugiere condiciones reductoras por saturación de agua...",
            "blanco": "El color blanco se relaciona con arenas muy lavadas o acumulación de sales...",
        },
        "texture": {
            "arcilloso": "Textura arcillosa: alta retención de agua y nutrientes; drenaje lento y riesgo de compactación...",
            "arenoso": "Textura arenosa: drenaje muy rápido, baja retención de agua y nutrientes...",
            "franco": "Textura franca: equilibrio entre arena, limo y arcilla...",
            "limoso": "Textura limosa: mayor retención de agua que arenosos...",
        },
        # estructuras, humedad, raíces (igual que antes)
    },
    "pt": {
        "color": {
            "vermelho-intenso": "A cor vermelha intensa reflete abundância de óxidos de ferro (hematita)...",
            "vermelho-amarelado": "A cor vermelho-amarelada indica presença de óxidos de ferro hidratados...",
            "amarelo": "A cor amarela está ligada à goethita e drenagem menos eficiente...",
            "marrom": "A cor marrom reflete teor moderado de matéria orgânica...",
            "pardo-marrom": "O pardo-marrom é transicional...",
            "preto": "A cor preta indica alto teor de carbono orgânico...",
            "cinza": "A cor cinza sugere condições redutoras...",
            "branco": "A cor branca relaciona-se a areias muito lavadas...",
        },
        "texture": {
            "argiloso": "Textura argilosa: alta retenção de água e nutrientes; drenagem lenta...",
            "arenoso": "Textura arenosa: drenagem muito rápida, baixa retenção de água e nutrientes...",
            "franco": "Textura franca: equilíbrio entre areia, silte e argila...",
            "siltoso": "Textura siltosa: maior retenção de água que arenosos...",
        },
        # estructuras, humedad, raíces (igual en PT)
    }
}

# ================================
# FUNCIÓN CARRUSEL
# ================================
def mostrar_referencias(categoria, seleccion, lang_code, t):
    if seleccion == t["placeholder"]:
        return
    base_path = os.path.join("referencias", categoria, seleccion.lower())
    if os.path.exists(base_path):
        imagenes = sorted(glob.glob(os.path.join(base_path, "*.jpg")))
        if imagenes:
            key = f"carousel_{categoria}_{seleccion}"
            if key not in st.session_state:
                st.session_state[key] = 0
            col1, col2, col3 = st.columns([1,3,1])
            with col1:
                if st.button("⬅️", key=f"prev_{key}"):
                    st.session_state[key] = (st.session_state[key]-1)%len(imagenes)
            with col3:
                if st.button("➡️", key=f"next_{key}"):
                    st.session_state[key] = (st.session_state[key]+1)%len(imagenes)
            st.image(imagenes[st.session_state[key]], width=300)

# ================================
# FLUJO PRINCIPAL
# ================================
if "show_intro" not in st.session_state:
    st.session_state["show_intro"] = True

lang = st.sidebar.radio("🌍 Idioma / Language", ["es", "pt"], index=0)
t = TEXT_CONTENT[lang]

if st.session_state["show_intro"]:
    st.title(t["app_title"])
    st.markdown(t["intro"])
    if st.button("👉 Comenzar análisis" if lang=="es" else "👉 Iniciar análise"):
        st.session_state["show_intro"] = False
        st.rerun()
    st.stop()

# Imagen
uploaded_file = st.file_uploader(t["upload_label"], type=["jpg","jpeg","png"])
if uploaded_file:
    st.image(uploaded_file, caption=t["uploaded_caption"], use_column_width=True)

# Selectores
st.write(t["select_msg"])
color = st.selectbox(t["color_label"], t["color_opts"])
mostrar_referencias("color", color, lang, t)

textura = st.selectbox(t["texture_label"], t["texture_opts"])
mostrar_referencias("textura", textura, lang, t)

estructura = st.selectbox(t["aggregation_label"], t["structure_opts"])
mostrar_referencias("estructura", estructura, lang, t)

humedad = st.selectbox(t["moisture_label"], t["moisture_opts"])
raices = st.selectbox(t["roots_label"], t["roots_opts"])

# Resultados
ready = uploaded_file and all(x != t["placeholder"] for x in [color,textura,estructura,humedad,raices])

if ready:
    st.subheader(t["summary_title"])
    resumen_list = [
        f"{t['color_label']}: {color}",
        f"{t['texture_label']}: {textura}",
        f"{t['aggregation_label']}: {estructura}",
        f"{t['moisture_label']}: {humedad}",
        f"{t['roots_label']}: {raices}",
    ]
    for r in resumen_list:
        st.write(f"- {r}")

    st.subheader(t["interpret_block_title"])
    interp = INTERP[lang]
    piezas = [
        interp["color"].get(color,""),
        interp["texture"].get(textura,""),
        interp.get("structure",{}).get(estructura,""),
        interp.get("moisture",{}).get(humedad,""),
        interp.get("roots",{}).get(raices,""),
    ]
    for p in piezas:
        if p: st.write(p)

    st.subheader(t["recs_title"])
    recs = ["✅ Mantener buenas prácticas de conservación."]
    for r in recs:
        st.write(f"- {r}")

    # Guardar CSV
    if st.button(t["save_button"]):
        file_csv = t["csv_file"]
        headers_exist = os.path.exists(file_csv)
        with open(file_csv,"a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            if not headers_exist:
                writer.writerow(["Fecha","Color","Textura","Estructura","Humedad","Raíces"])
            writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M"), color, textura, estructura, humedad, raices])
        st.success(t["csv_saved"])

    # PDF
    pdf_file = generar_pdf(lang, resumen_list, piezas, recs)
    with open(pdf_file,"rb") as f:
        st.download_button(t["pdf_button"], f, file_name=pdf_file, mime="application/pdf")

