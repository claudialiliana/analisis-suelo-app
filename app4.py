import streamlit as st
import os, csv, glob

# ================================
# CONFIG INICIAL (debe ser lo 1º)
# ================================
st.set_page_config(page_title="Análisis de Suelos", page_icon="🌱", layout="wide")

# ================================
# MAPEOS DE CARPETAS (color, textura, estructura)
#   -> Tus carpetas quedan en ESPAÑOL
#   -> En PT se mapean a la carpeta en español correspondiente
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
        "app_description": "Sube una foto, selecciona parámetros y compara con referencias Munsell.",
        "upload_label": "Subir imagen de suelo",
        "uploaded_caption": "Imagen subida",
        "color_label": "Color del suelo",
        "texture_label": "Textura del suelo",
        "aggregation_label": "Forma / Estructura",
        "moisture_label": "Humedad",
        "roots_label": "Presencia de raíces",
        "save_button": "💾 Guardar análisis",
        "download_all": "⬇️ Descargar todos los análisis",
        "interpret_title": "📊 Interpretación educativa",
        "moisture_opts": ["Baja", "Media", "Alta"],
        "roots_opts": ["Ausentes", "Escasas", "Abundantes"],
        "color_opts": ["rojo-intenso", "rojo-amarillento", "amarillo", "marrón", "pardo-marrón", "negro", "gris", "blanco"],
        "texture_opts": ["arcilloso", "arenoso", "franco", "limoso"],
    },
    "pt": {
        "app_title": "🌱 Análise Visual de Solos",
        "app_description": "Envie uma foto, selecione parâmetros e compare com referências Munsell.",
        "upload_label": "Enviar imagem do solo",
        "uploaded_caption": "Imagem enviada",
        "color_label": "Cor do solo",
        "texture_label": "Textura do solo",
        "aggregation_label": "Forma / Estrutura",
        "moisture_label": "Umidade",
        "roots_label": "Presença de raízes",
        "save_button": "💾 Salvar análise",
        "download_all": "⬇️ Baixar todas as análises",
        "interpret_title": "📊 Interpretação educativa",
        "moisture_opts": ["Baixa", "Média", "Alta"],
        "roots_opts": ["Ausentes", "Escassas", "Abundantes"],
        "color_opts": ["vermelho-intenso", "vermelho-amarelado", "amarelo", "marrom", "pardo-marrom", "preto", "cinza", "branco"],
        "texture_opts": ["argiloso", "arenoso", "franco", "siltoso"],
    },
}

# ================================
# SESIÓN DE IDIOMA
# ================================
if "lang" not in st.session_state:
    st.session_state["lang"] = "es"

lang = st.sidebar.radio("🌍 Idioma / Language", ["es", "pt"], index=0)
st.session_state["lang"] = lang
t = TEXT_CONTENT[lang]

st.markdown(f"<script>document.title='{t['app_title']}'</script>", unsafe_allow_html=True)
st.title(t["app_title"])
st.write(t["app_description"])
st.write("---")

# ================================
# FUNCIÓN MOSTRAR REFERENCIAS (usa mapeos)
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
        imagenes = glob.glob(os.path.join(base_path, "*.png")) + glob.glob(os.path.join(base_path, "*.jpg")) + glob.glob(os.path.join(base_path, "*.jpeg"))
        if imagenes:
            cols = st.columns(4)
            for i, img in enumerate(sorted(imagenes)):
                with cols[i % 4]:
                    st.image(img, use_column_width=True)
        else:
            st.warning(f"No se encontraron imágenes en la carpeta {base_path}")
    else:
        st.info(f"No existe carpeta de referencia para {seleccion}")

# ================================
# UPLOADER
# ================================
uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption=t["uploaded_caption"], use_column_width=True)

# ================================
# SELECTORES + REFERENCIAS
# ================================
color = st.selectbox(t["color_label"], t["color_opts"])
mostrar_referencias("color", color, lang)

textura = st.selectbox(t["texture_label"], t["texture_opts"])
mostrar_referencias("textura", textura, lang)

# ================================
# ESTRUCTURAS DE SUELO (diccionarios reales, NO sets)
# ================================
estructuras_dict = {
    "es": {
        "granular": "Agregados pequeños y redondeados, muy porosos. Excelente aireación y penetración de raíces. Comunes en horizontes A ricos en materia orgánica.",
        "migajosa": "Agregados irregulares y porosos, semejantes a migas de pan. Muy deseables en suelos agrícolas fértiles.",
        "bloques": "Agregados cúbicos/poliédricos. Subangulares: bordes redondeados. Angulares: caras bien definidas. Comunes en horizontes B arcillosos.",
        "prismatica-columnar": "Agregados verticales. Prismática: tope plano (árido/semiárido). Columnar: tope redondeado (suelos sódicos).",
        "laminar": "Agregados planos superpuestos en láminas. Dificultan infiltración y crecimiento radicular (compactación/horizontes E).",
        "masiva": "Masa sólida sin agregados discernibles. Muy compactada, drenaje y aireación pobres.",
        "suelto": "Sin estructura (partículas individuales). Alta permeabilidad, baja fertilidad y retención de agua (suelos arenosos).",
    },
    "pt": {
        "granular": "Agregados pequenos e arredondados, muito porosos. Excelente aeração e penetração de raízes. Comuns em horizontes A ricos em matéria orgânica.",
        "migajosa": "Agregados irregulares e porosos, semelhantes a migalhas de pão. Muito desejáveis em solos agrícolas férteis.",
        "bloques": "Agregados cúbicos/poliédricos. Subangulares: bordas arredondadas. Angulares: faces bem definidas. Comuns em horizontes B argilosos.",
        "prismatica-columnar": "Agregados verticais. Prismática: topo plano (árido/semiárido). Colunar: topo arredondado (solos sódicos).",
        "laminar": "Agregados planos em camadas. Dificultam infiltração e crescimento radicular (compactação/horizontes E).",
        "masiva": "Massa sólida sem agregados discerníveis. Muito compactada, drenagem e aeração pobres.",
        "suelto": "Sem estrutura (partículas individuais). Alta permeabilidade, baixa fertilidade e retenção de água (solos arenosos).",
    },
}

estructura = st.selectbox(t["aggregation_label"], list(estructuras_dict[lang].keys()))
mostrar_referencias("forma-estructura", estructura, lang)
st.markdown(f"📖 **{t['aggregation_label']}:** {estructuras_dict[lang][estructura]}")

# ================================
# OTROS PARÁMETROS
# ================================
humedad = st.selectbox(t["moisture_label"], t["moisture_opts"])
raices = st.selectbox(t["roots_label"], t["roots_opts"])

# ================================
# INTERPRETACIONES SIMPLES
# ================================
interpretaciones = {
    "es": {
        "color": {
            "rojo-intenso": "Presencia de óxidos de hierro, buen drenaje.",
            "rojo-amarillento": "Hierro oxidado, drenaje moderado.",
            "amarillo": "Suelos jóvenes, fertilidad moderada.",
            "marrón": "Materia orgánica + minerales; color intermedio.",
            "pardo-marrón": "Intermedio; fertilidad aceptable.",
            "negro": "Alta materia orgánica, muy fértil.",
            "gris": "Posible mal drenaje (gley).",
            "blanco": "Arenoso o lavado, baja fertilidad.",
        },
        "textura": {
            "arcilloso": "Alta retención de agua; drenaje lento.",
            "arenoso": "Muy buen drenaje; baja retención y nutrientes.",
            "franco": "Equilibrio arena-limo-arcilla.",
            "limoso": "Retiene más agua que arenoso; menor estabilidad estructural.",
        },
        "raices": {
            "Ausentes": "Poca actividad biológica.",
            "Escasas": "Actividad biológica limitada.",
            "Abundantes": "Buena aereación y biología activa.",
        },
    },
    "pt": {
        "color": {
            "vermelho-intenso": "Presença de óxidos de ferro, boa drenagem.",
            "vermelho-amarelado": "Ferro oxidado, drenagem moderada.",
            "amarelo": "Solos jovens, fertilidade moderada.",
            "marrom": "Matéria orgânica + minerais; cor intermediária.",
            "pardo-marrom": "Intermediário; fertilidade aceitável.",
            "preto": "Alta matéria orgânica, muito fértil.",
            "cinza": "Possível má drenagem (glei).",
            "branco": "Arenoso ou lixiviado, baixa fertilidade.",
        },
        "textura": {
            "argiloso": "Alta retenção de água; drenagem lenta.",
            "arenoso": "Ótima drenagem; baixa retenção e nutrientes.",
            "franco": "Equilíbrio areia-silte-argila.",
            "siltoso": "Retém mais água que arenoso; menor estabilidade.",
        },
        "raices": {
            "Ausentes": "Pouca atividade biológica.",
            "Escassas": "Atividade biológica limitada.",
            "Abundantes": "Boa aeração e biologia ativa.",
        },
    },
}

# ================================
# REGLAS COMBINADAS (20) ES/PT
# ================================
reglas_combinadas = {
    "es": [
        (("rojo-intenso", "arcilloso", "Alta"), "Suelo con hierro y arcilla; fertilidad aceptable pero riesgo de encharcamiento."),
        (("rojo-intenso", "arcilloso", "Media"), "Buen suelo agrícola; drenaje moderado."),
        (("rojo-intenso", "arenoso", "Baja"), "Bien drenado pero pobre en nutrientes."),
        (("negro", "franco", "Media"), "Suelo fértil y equilibrado: excelente para cultivos."),
        (("negro", "arcilloso", "Alta"), "Muy fértil pero con riesgo de compactación y mal drenaje."),
        (("negro", "arenoso", "Baja"), "A pesar de la MO, pierde agua rápidamente."),
        (("gris", "arcilloso", "Alta"), "Problemas de drenaje; posible gleyzación."),
        (("gris", "limoso", "Media"), "Encharcamiento estacional; aireación limitada."),
        (("gris", "arenoso", "Baja"), "Pobre; riesgo de salinización en climas áridos."),
        (("blanco", "arenoso", "Baja"), "Muy pobre; escasa retención de agua."),
        (("blanco", "franco", "Baja"), "Fertilidad limitada; añadir materia orgánica."),
        (("amarillo", "limoso", "Media"), "Jóvenes; retienen agua; fertilidad moderada."),
        (("amarillo", "arenoso", "Baja"), "Baja fertilidad; apto para pastos resistentes."),
        (("amarillo", "franco", "Media"), "Aceptable para cultivos de ciclo corto."),
        (("marrón", "franco", "Media"), "Buen equilibrio de nutrientes y drenaje."),
        (("marrón", "arcilloso", "Alta"), "Productivo pero tiende a compactarse."),
        (("pardo-marrón", "franco", "Media"), "Fertilidad aceptable; estructura estable."),
        (("pardo-marrón", "limoso", "Media"), "Productivo pero susceptible a erosión."),
        (("rojo-amarillento", "arenoso", "Baja"), "Buen drenaje; fertilidad baja; fraccionar fertilización."),
        (("negro", "franco", "Alta"), "Excelente fertilidad; vigilar anegamiento."),
    ],
    "pt": [
        (("vermelho-intenso", "argiloso", "Alta"), "Solo com ferro e argila; fertilidade aceitável, risco de encharcamento."),
        (("vermelho-intenso", "argiloso", "Média"), "Bom solo agrícola; drenagem moderada."),
        (("vermelho-intenso", "arenoso", "Baixa"), "Bem drenado porém pobre em nutrientes."),
        (("preto", "franco", "Média"), "Solo fértil e equilibrado: excelente para cultivos."),
        (("preto", "argiloso", "Alta"), "Muito fértil porém com risco de compactação e má drenagem."),
        (("preto", "arenoso", "Baixa"), "Apesar da MO, perde água rapidamente."),
        (("cinza", "argiloso", "Alta"), "Problemas de drenagem; possível gleização."),
        (("cinza", "siltoso", "Média"), "Encharcamento sazonal; aeração limitada."),
        (("cinza", "arenoso", "Baixa"), "Pobre; risco de salinização em climas áridos."),
        (("branco", "arenoso", "Baixa"), "Muito pobre; pouca retenção de água."),
        (("branco", "franco", "Baixa"), "Fertilidade limitada; adicionar matéria orgânica."),
        (("amarelo", "siltoso", "Média"), "Jovens; retêm água; fertilidade moderada."),
        (("amarelo", "arenoso", "Baixa"), "Baixa fertilidade; adequado para pastagens resistentes."),
        (("amarelo", "franco", "Média"), "Aceitável para cultivos de ciclo curto."),
        (("marrom", "franco", "Média"), "Bom equilíbrio de nutrientes e drenagem."),
        (("marrom", "argiloso", "Alta"), "Produtivo porém tende a compactar."),
        (("pardo-marrom", "franco", "Média"), "Fertilidade aceitável; estrutura estável."),
        (("pardo-marrom", "siltoso", "Média"), "Produtivo porém sujeito à erosão."),
        (("vermelho-amarelado", "arenoso", "Baixa"), "Boa drenagem; baixa fertilidade; fracionar adubação."),
        (("preto", "franco", "Alta"), "Excelente fertilidade; atenção ao encharcamento."),
    ],
}

# ================================
# MOSTRAR INTERPRETACIONES
# ================================
st.subheader(t["interpret_title"])
st.write(f"🎨 **{t['color_label']}:** {interpretaciones[lang]['color'].get(color, '')}")
st.write(f"🧱 **{t['texture_label']}:** {interpretaciones[lang]['textura'].get(textura, '')}")
st.write(f"🌱 **{t['roots_label']}:** {interpretaciones[lang]['raices'].get(raices, '')}")

for (c, txt, h), explicacion in reglas_combinadas[lang]:
    if c == color and txt == textura and h == humedad:
        st.markdown(f"💡 **{explicacion}**")

# ================================
# GUARDAR Y DESCARGAR
# ================================
if st.button(t["save_button"]):
    with open("analisis_suelos.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([color, textura, estructura, humedad, raices])
    st.success("✅ Análisis guardado")

with st.sidebar:
    if os.path.exists("analisis_suelos.csv"):
        with open("analisis_suelos.csv", "rb") as f:
            st.download_button(t["download_all"], f, file_name="analisis_suelos.csv")

