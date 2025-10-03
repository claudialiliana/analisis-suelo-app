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

/* Botones */
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

/* Cajas */
.box-section {
    background-color: #f9fdfb;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e0ebe4;
    margin-bottom: 16px;
}

/* Encabezados dentro de cajas */
.box-section h3 {
    margin-top: 0;
    margin-bottom: 8px;
}

/* Inputs */
.stSelectbox > div > div {
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# ================================
# LOGO (sidebar y portada PDF)
# ================================
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_column_width=True)
else:
    st.sidebar.markdown("**Kawsaypacha – Tierra Viva**")

# ================================
# MAPEOS DE CARPETAS (para referencias)
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
# TEXTOS MULTILINGÜES + OPCIONES
# ================================
TEXT_CONTENT = {
    "es": {
        "app_title": "🌱 Análisis Visual de Suelos",
        "intro": """
**Bienvenido/a** 👋  
Analiza visualmente tu muestra de suelo con apoyo de **referencias** y recibe un **informe técnico** (PDF).
""",
        "upload_label": "📤 Subir imagen de suelo",
        "uploaded_caption": "📸 Imagen subida",
        "color_label": "🎨 Color del suelo",
        "texture_label": "🌾 Textura del suelo",
        "aggregation_label": "🧱 Forma / Estructura",
        "moisture_label": "💧 Humedad",
        "roots_label": "🌱 Presencia de raíces",
        "interpret_title": "📊 Conclusión del análisis",
        "summary_title": "1️⃣ Resumen de la muestra",
        "interpret_block_title": "2️⃣ Interpretación técnica",
        "recs_title": "3️⃣ Recomendaciones de manejo",
        "save_button": "💾 Guardar análisis",
        "download_all": "⬇️ Descargar todos los análisis (CSV)",
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
        "analysis_image_caption": "Imagen analizada (subida por el usuario)",
        "tips_refs": "🔎 Compara tu muestra con estas **referencias visuales** para confirmar tu selección.",
        "start_btn": "➡️ Comenzar análisis",
        "title_pdf": "Reporte de Análisis Visual de Suelos",
    },
    "pt": {
        "app_title": "🌱 Análise Visual de Solos",
        "intro": """
**Bem-vindo(a)** 👋  
Analise visualmente sua amostra com **referências** e receba um **relatório técnico** (PDF).
""",
        "upload_label": "📤 Enviar imagem do solo",
        "uploaded_caption": "📸 Imagem enviada",
        "color_label": "🎨 Cor do solo",
        "texture_label": "🌾 Textura do solo",
        "aggregation_label": "🧱 Forma / Estrutura",
        "moisture_label": "💧 Umidade",
        "roots_label": "🌱 Presença de raízes",
        "interpret_title": "📊 Conclusão da análise",
        "summary_title": "1️⃣ Resumo da amostra",
        "interpret_block_title": "2️⃣ Interpretação técnica",
        "recs_title": "3️⃣ Recomendações de manejo",
        "save_button": "💾 Salvar análise",
        "download_all": "⬇️ Baixar todas as análises (CSV)",
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
        "analysis_image_caption": "Imagem analisada (enviada pelo usuário)",
        "tips_refs": "🔎 Compare sua amostra com estas **referências visuais** para confirmar sua seleção.",
        "start_btn": "➡️ Iniciar análise",
        "title_pdf": "Relatório de Análise Visual de Solos",
    },
}

# ================================
# INTERPRETACIONES DETALLADAS (ES/PT)
# ================================
INTERP = {
    "es": {
        "color": {
            "rojo-intenso": "El rojo intenso refleja abundancia de óxidos de hierro (hematita), asociado a buen drenaje y ambientes bien aireados; puede indicar baja materia orgánica si los tonos son muy vivos.",
            "rojo-amarillento": "Indica presencia de óxidos de hierro hidratados (goethita) y condiciones de oxidación moderadas; sugiere drenaje de medio a bueno.",
            "amarillo": "Vinculado a goethita y, a veces, a drenaje menos eficiente; puede aparecer en suelos lixiviados con fertilidad moderada.",
            "marrón": "Suele reflejar contenido moderado de materia orgánica y complejos Fe-Humus; fertilidad intermedia y actividad biológica moderada.",
            "pardo-marrón": "Transición con influencia tanto de compuestos férricos como de materia orgánica; sugiere fertilidad aceptable y buena estabilidad superficial.",
            "negro": "Alto contenido de carbono orgánico y humificación; suelos fértiles, con alta CICE, pero susceptibles a anegamiento si la estructura es deficiente.",
            "gris": "Sugiere condiciones reductoras por saturación (gley), con hierro reducido; drenaje deficiente y posible anoxia radicular.",
            "blanco": "Arenas muy lavadas o acumulación de sales/carbonatos; baja fertilidad y baja capacidad de retener agua y nutrientes.",
        },
        "texture": {
            "arcilloso": "Alta retención de agua y nutrientes; drenaje lento y riesgo de compactación; plasticidad y pegajosidad elevadas.",
            "arenoso": "Drenaje muy rápido; baja retención de agua y nutrientes; susceptible a sequía y lixiviación.",
            "franco": "Equilibrio entre arena, limo y arcilla; buena aireación y retención; ideal para la mayoría de cultivos.",
            "limoso": "Mayor retención de agua que arenosos, pero estructura menos estable; riesgo de encostramiento superficial.",
        },
        "structure": {
            "granular": "Agregados pequeños y redondeados con alta porosidad; excelente para aireación, infiltración y raíces (común en horizontes A ricos en MO).",
            "migajosa": "Similar a la granular pero más porosa e irregular; muy deseable por equilibrio aire-agua.",
            "bloques": "Agregados cúbicos/poliédricos; pueden restringir raíces si hay compactación.",
            "prismatica-columnar": "Agregados verticales (prismática: tope plano; columnar: tope redondeado, típico en suelos sódicos); limitan movimiento de agua y raíces.",
            "laminar": "Agregados en láminas horizontales; muy restrictiva para infiltración y raíces; típica de compactación.",
            "masiva": "Sin agregación discernible; baja porosidad y drenaje deficiente; limita aireación y desarrollo radicular.",
            "suelto": "Partículas individuales; alta permeabilidad pero baja fertilidad y retención de agua.",
        },
        "moisture": {
            "Baja": "Potencial estrés hídrico y mayor esfuerzo para establecimiento de plántulas.",
            "Media": "Condición intermedia adecuada si la estructura acompaña.",
            "Alta": "Riesgo de anegamiento y anoxia; procesos reductores y pérdida de estructura.",
        },
        "roots": {
            "Ausentes": "Puede indicar limitaciones físicas (compactación) o químicas (toxicidad, salinidad), o manejo reciente.",
            "Escasas": "Actividad biológica limitada; posible restricción de aireación o nutrientes.",
            "Abundantes": "Condición favorable de porosidad y disponibilidad de agua/nutrientes.",
        },
    },
    "pt": {
        "color": {
            "vermelho-intenso": "Vermelho intenso reflete óxidos de ferro (hematita) e boa drenagem/aeração; pode indicar baixa MO se os tons são muito vivos.",
            "vermelho-amarelado": "Presença de goethita e oxidação moderada; drenagem de média a boa.",
            "amarelo": "Ligado à goethita e, às vezes, drenagem menos eficiente; fertilidade moderada.",
            "marrom": "Teor moderado de MO e complexos Fe-Húmus; fertilidade intermediária.",
            "pardo-marrom": "Transição com influência férrica e de MO; estabilidade superficial aceitável.",
            "preto": "Alto carbono orgânico; solos férteis, com alta CTC; podem encharcar se estrutura deficiente.",
            "cinza": "Condições redutoras por saturação (glei), com ferro reduzido; drenagem deficiente.",
            "branco": "Areias muito lavadas ou acúmulo de sais/carbonatos; baixa fertilidade e retenção de água/nutrientes.",
        },
        "texture": {
            "argiloso": "Alta retenção de água/nutrientes; drenagem lenta e risco de compactação.",
            "arenoso": "Drenagem rápida; baixa retenção; suscetível à seca e lixiviação.",
            "franco": "Equilíbrio entre areia, silte e argila; boa aeração e retenção.",
            "siltoso": "Retém mais água que arenosos, porém com estrutura menos estável.",
        },
        "structure": {
            "granular": "Agregados pequenos e arredondados; excelente aeração, infiltração e raízes.",
            "migajosa": "Semelhante à granular, porém mais porosa e irregular; muito desejável.",
            "blocos": "Cúbicos/poliedros; podem restringir raízes quando compactados.",
            "prismática-colunar": "Colunas verticais (prismática: topo plano; colunar: topo arredondado/sódico); limitam água/raízes.",
            "laminar": "Lâminas horizontais; muito restritiva à infiltração/raízes; típica de compactação.",
            "maciça": "Sem agregação discernível; baixa porosidade e drenagem deficiente.",
            "solto": "Partículas individuais; alta permeabilidade e baixa fertilidade/retenção.",
        },
        "moisture": {
            "Baixa": "Possível estresse hídrico; difícil estabelecimento de plântulas.",
            "Média": "Condição intermediária adequada se a estrutura ajudar.",
            "Alta": "Risco de encharcamento/anoxia; processos redutores e perda de estrutura.",
        },
        "roots": {
            "Ausentes": "Pode indicar limitações físicas (compactação) ou químicas (toxicidade, salinidade) ou manejo recente.",
            "Escassas": "Atividade biológica limitada; possível restrição de aeração/nutrientes.",
            "Abundantes": "Boa porosidade e disponibilidade hídrica/nutritiva.",
        },
    },
}

# ================================
# INFO LARGA (expanders) ESTRUCTURA
# ================================
INFO_ESTRUCTURA_LONG = {
    "es": {
        "granular": """**Estructura Granular**
- Forma: agregados pequeños, esféricos o poliédricos irregulares.
- Formación: MO, raíces, microorganismos, ciclos de humedecimiento-secado.
- Uso: excelente para infiltración, aireación y raíces.""",
        "migajosa": """**Estructura Migajosa**
- Forma: muy porosa e irregular, se desmenuza como migas.
- Formación: alta MO, intensa biología y ciclos de humedad-sequía.
- Uso: muy deseable por equilibrio aire-agua.""",
        "bloques": """**Estructura en Bloques**
- Tipos: angulares (caras planas/aristas agudas) y subangulares (más redondeadas).
- Ubicación: común en horizontes B.
- Efecto: mejores que masiva, pero pueden restringir raíces/agua vs. granular.""",
        "prismatica-columnar": """**Estructura Prismática/Columnar**
- Forma: columnas verticales.
- Prismática: tope plano | Columnar: tope redondeado (suelos sódicos).
- Ubicación: B o C; pueden dificultar agua y raíces.""",
        "laminar": """**Estructura Laminar (Platy)**
- Forma: láminas horizontales (compactación/lixiviación).
- Efecto: restringe severamente infiltración, aire y raíces.""",
        "suelto": """**Estructura Suelta (Grano Simple)**
- Forma: partículas individuales (arena), sin agregación.
- Efecto: buen drenaje, baja retención de agua/nutrientes.""",
        "masiva": """**Estructura Masiva (Sin Estructura)**
- Forma: masa sólida sin planos de debilidad.
- Efecto: la más desfavorable; limita raíces, agua y aire.""",
    },
    "pt": {
        "granular": """**Estrutura Granular**
- Forma: agregados pequenos, esféricos ou poliedros irregulares.
- Formação: MO, raízes, microrganismos e ciclos de umedecimento-secagem.
- Uso: excelente infiltração, aeração e raízes.""",
        "migajosa": """**Estrutura Migajosa**
- Forma: muito porosa/irregular; esfarela como migalhas.
- Formação: alta MO, intensa biologia e ciclos de umidade-seca.
- Uso: muito desejável na agricultura.""",
        "blocos": """**Estrutura em Blocos**
- Tipos: angulares e subangulares.
- Local: comum em horizontes B.
- Efeito: melhores que maciça, porém podem restringir raízes/água vs. granular.""",
        "prismática-colunar": """**Estrutura Prismática/Colunar**
- Forma: colunas verticais; topos planos (prismática) ou arredondados (colunar).
- Local: B ou C; podem dificultar água e raízes.""",
        "laminar": """**Estrutura Laminar (Platy)**
- Forma: lâminas horizontais (compactação/lixiviação).
- Efeito: restringe fortemente água, ar e raízes.""",
        "solto": """**Estrutura Solta (Grão Simples)**
- Forma: partículas individuais (areia), sem agregação.
- Efeito: drenagem alta e baixa retenção de água/nutrientes.""",
        "maciça": """**Estrutura Maciça (Sem Estrutura)**
- Forma: massa sólida coesa, sem planos de fraqueza.
- Efeito: a mais desfavorável; limita raízes, água e ar.""",
    },
}

# ================================
# CONTROL INTRO/WIZARD
# ================================
if "show_intro" not in st.session_state:
    st.session_state["show_intro"] = True

lang = st.sidebar.radio("🌍 Idioma / Language", ["es", "pt"], index=0)
t = TEXT_CONTENT[lang]

if st.session_state["show_intro"]:
    st.title(t["app_title"])
    st.markdown(t["intro"])
    if st.button(t["start_btn"], use_container_width=True):
        st.session_state["show_intro"] = False
        st.rerun()
    st.stop()

# ================================
# FUNCIÓN: referencias con carrusel
# ================================
def mostrar_referencias(categoria: str, seleccion: str, lang_code: str):
    """Muestra un carrusel de imágenes de referencias según la categoría y selección."""
    if seleccion == TEXT_CONTENT[lang_code]["placeholder"]:
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
            key_carousel = f"carousel_{categoria}_{seleccion}"
            if key_carousel not in st.session_state:
                st.session_state[key_carousel] = 0

            st.caption(t["tips_refs"])
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                if st.button("⬅️", key=f"prev_{key_carousel}", use_container_width=True):
                    st.session_state[key_carousel] = (st.session_state[key_carousel] - 1) % len(imagenes)
            with col3:
                if st.button("➡️", key=f"next_{key_carousel}", use_container_width=True):
                    st.session_state[key_carousel] = (st.session_state[key_carousel] + 1) % len(imagenes)

            img_path = imagenes[st.session_state[key_carousel]]
            st.image(img_path, caption=f"{seleccion} ({st.session_state[key_carousel]+1}/{len(imagenes)})", use_container_width=True)
        else:
            st.warning(f"{t['no_images_msg']} {base_path}")
    else:
        st.info(f"{t['no_folder_msg']} {seleccion}")

# ================================
# PÁGINA PRINCIPAL
# ================================
st.title(t["app_title"])

uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption=t["uploaded_caption"], use_container_width=True)

# Selectores + Referencias
color = st.selectbox(t["color_label"], t["color_opts"])
mostrar_referencias("color", color, lang)

textura = st.selectbox(t["texture_label"], t["texture_opts"])
mostrar_referencias("textura", textura, lang)

estructura = st.selectbox(t["aggregation_label"], t["structure_opts"])
mostrar_referencias("forma-estructura", estructura, lang)

# Info larga de estructura (ℹ️)
if estructura != t["placeholder"]:
    info_key = estructura
    if lang == "pt" and estructura == "prismática-colunar":
        info_key = "prismática-colunar"
    st.markdown("**ℹ️**")
    with st.expander("Más información / Mais informações"):
        st.markdown(INFO_ESTRUCTURA_LONG[lang].get(info_key, ""))

humedad = st.selectbox(t["moisture_label"], t["moisture_opts"])
raices = st.selectbox(t["roots_label"], t["roots_opts"])

# ================================
# ANÁLISIS (resumen, interpretación, recomendaciones)
# ================================
ready = (
    uploaded_file is not None
    and color != t["placeholder"]
    and textura != t["placeholder"]
    and estructura != t["placeholder"]
    and humedad != t["placeholder"]
    and raices != t["placeholder"]
)

if ready:
    resumen_list = [
        f"{t['color_label']}: {color}",
        f"{t['texture_label']}: {textura}",
        f"{t['aggregation_label']}: {estructura}",
        f"{t['moisture_label']}: {humedad}",
        f"{t['roots_label']}: {raices}",
    ]
    pdf_file = generar_pdf(lang, resumen_list, piezas, recs)
    with open(pdf_file,"rb") as f:
        st.download_button(t["pdf_button"], f, file_name=pdf_file, mime="application/pdf")


    # INTERPRETACIÓN TÉCNICA
    st.markdown(f"<div class='box-section'><h3>{t['interpret_block_title']}</h3>", unsafe_allow_html=True)
    interp = INTERP[lang]
    piezas = [
        interp["color"].get(color, ""),
        interp["texture"].get(textura, ""),
        interp["structure"].get(estructura, ""),
        interp["moisture"].get(humedad, ""),
        interp["roots"].get(raices, ""),
    ]
    st.info(" ".join([p for p in piezas if p]))
    st.markdown("</div>", unsafe_allow_html=True)

    # RECOMENDACIONES (reglas)
    st.markdown(f"<div class='box-section'><h3>{t['recs_title']}</h3>", unsafe_allow_html=True)
    recs = []
    if (lang == "es" and humedad == "Alta") or (lang == "pt" and humedad == "Alta"):
        recs.append("Mejorar drenaje (canalización superficial, subsolado selectivo si hay capas densas). / Melhorar a drenagem (canalização superficial, subsolagem seletiva).")
    if (lang == "es" and humedad == "Baja") or (lang == "pt" and humedad == "Baixa"):
        recs.append("Aumentar cobertura del suelo y planificar riegos oportunos. / Aumentar cobertura do solo e planejar irrigações oportunas.")
    if (lang == "es" and textura == "arenoso") or (lang == "pt" and textura == "arenoso"):
        recs.append("Incorporar materia orgánica y fraccionar la fertilización para reducir lixiviación. / Incorporar MO e fracionar a adubação.")
    if (lang == "es" and textura == "arcilloso") or (lang == "pt" and textura == "argiloso"):
        recs.append("Evitar labranza en húmedo y promover porosidad biológica con raíces/coberturas. / Evitar preparo úmido e promover porosidade biológica.")
    if (lang == "es" and estructura in ["laminar", "masiva"]) or (lang == "pt" and estructura in ["laminar", "maciça"]):
        recs.append("Aliviar compactación (tráfico controlado, subsolado puntual) y mantener residuos en superficie. / Aliviar compactação e manter resíduos na superfície.")
    if (lang == "es" and raices in ["Ausentes", "Escasas"]) or (lang == "pt" and raices in ["Ausentes", "Escassas"]):
        recs.append("Fomentar raíces finas con abonos verdes y rotaciones; revisar restricciones químicas. / Fomentar raízes finas com adubos verdes e rotações; revisar restrições químicas.")
    if not recs:
        recs.append("Mantener buenas prácticas de conservación y aporte de MO. / Manter boas práticas de conservação e aporte de MO.")
    for r in recs:
        st.warning(r)
    st.markdown("</div>", unsafe_allow_html=True)

    # ================================
    # Guardar a CSV
    # ================================
    if st.button(t["save_button"], use_container_width=True):
        file_csv = t["csv_file"]
        headers_exist = os.path.exists(file_csv) and os.path.getsize(file_csv) > 0
        with open(file_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not headers_exist:
                writer.writerow(["timestamp", "idioma", "color", "textura", "estructura", "humedad", "raices"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), lang, color, textura, estructura, humedad, raices])
        st.success("✅ " + ("Análisis guardado" if lang=="es" else "Análise salva"))

    # ================================
    # Generar PDF (solo texto)
    # ================================
   def generar_pdf(lang_code, resumen, interpretacion, recomendaciones):
    pdf = FPDF()
    pdf.add_page()

    # === Fuente DejaVu para UTF-8 ===
    # Streamlit Cloud suele traerla instalada, si no, súbela a tu repo
    pdf.add_font("DejaVu", "", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 12)

    # === Logo (si existe en el repo) ===
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=80, y=10, w=50)
        pdf.ln(35)

    # === Título ===
    pdf.set_font("DejaVu", "", 16)
    pdf.cell(0, 10, "🌱 Análisis de Suelo" if lang_code=="es" else "🌱 Análise de Solo", ln=True, align="C")

    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 10, datetime.now().strftime("%d/%m/%Y %H:%M"), ln=True, align="C")
    pdf.ln(10)

    # === Resumen ===
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 10, "1️⃣ Resumen" if lang_code=="es" else "1️⃣ Resumo", ln=True)
    pdf.set_font("DejaVu", "", 11)
    for item in resumen:
        pdf.multi_cell(0, 8, f"- {item}")
    pdf.ln(5)

    # === Interpretación ===
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 10, "2️⃣ Interpretación técnica" if lang_code=="es" else "2️⃣ Interpretação técnica", ln=True)
    pdf.set_font("DejaVu", "", 11)
    for parrafo in interpretacion:
        pdf.multi_cell(0, 8, parrafo)
    pdf.ln(5)

    # === Recomendaciones ===
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 10, "3️⃣ Recomendaciones" if lang_code=="es" else "3️⃣ Recomendações", ln=True)
    pdf.set_font("DejaVu", "", 11)
    for rec in recomendaciones:
        pdf.multi_cell(0, 8, rec)

    # === Guardar PDF ===
    out = "analisis_suelo.pdf"
    pdf.output(out)
    return out

# ================================
# Descarga CSV en sidebar
# ================================
with st.sidebar:
    file_csv = TEXT_CONTENT[lang]["csv_file"]
    if os.path.exists(file_csv) and os.path.getsize(file_csv) > 0:
        with open(file_csv, "rb") as f:
            st.download_button(TEXT_CONTENT[lang]["download_all"], f, file_name=file_csv, mime="text/csv", use_container_width=True)


