# app.py
import streamlit as st
import os, csv, glob
from datetime import datetime
from fpdf import FPDF

# ================================
# CONFIG INICIAL (debe ser lo 1º)
# ================================
st.set_page_config(page_title="Análisis de Suelos", page_icon="🌱", layout="wide")
st.sidebar.image("logo.png", use_container_width=True)

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
# TEXTOS MULTILINGÜES + OPCIONES
# ================================
TEXT_CONTENT = {
    "es": {
        "app_title": "🌱 Análisis Visual de Suelos",
        "intro": """
**Bienvenido/a a esta plataforma educativa para explorar el mundo del suelo de manera visual e interactiva.**

👉 Pasos:
1) **Sube una imagen**.  
2) **Selecciona características** (color, textura, estructura, humedad, raíces) apoyándote en las **referencias visuales**.  
3) Revisa el **análisis técnico** y descarga el **reporte PDF**.
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
        "summary_title": "1️⃣ Resumen de la muestra",
        "interpret_block_title": "2️⃣ Interpretación técnica",
        "recs_title": "3️⃣ Recomendaciones de manejo",
        "placeholder": "Seleccionar opción",
        "moisture_opts": ["Seleccionar opción", "Baja", "Media", "Alta"],
        "roots_opts": ["Seleccionar opción", "Ausentes", "Escasas", "Abundantes"],
        "color_opts": ["Seleccionar opción", "rojo-intenso", "rojo-amarillento", "amarillo", "marrón", "pardo-marrón", "negro", "gris", "blanco"],
        "texture_opts": ["Seleccionar opción", "arcilloso", "arenoso", "franco", "limoso"],
        "structure_opts": ["Seleccionar opción", "granular", "migajosa", "bloques", "prismatica-columnar", "laminar", "masiva", "suelto"],
        "csv_saved": "✅ Análisis guardado",
        "csv_file": "analisis_suelos.csv",
        "no_images_msg": "No se encontraron imágenes en la carpeta",
        "no_folder_msg": "No existe carpeta de referencia para",
        "start_btn": "➡️ Comenzar análisis",
        "analysis_image_caption": "Imagen analizada (subida por el usuario)",
        "pdf_button": "📥 Descargar reporte en PDF",
        "tips_refs": "🔎 Compara tu muestra con estas **referencias visuales** para confirmar tu selección."
    },
    "pt": {
        "app_title": "🌱 Análise Visual de Solos",
        "intro": """
**Bem-vindo(a)! Explore o solo de forma visual e interativa.**

👉 Passos:
1) **Envie uma imagem**.  
2) **Selecione as características** (cor, textura, estrutura, umidade, raízes) usando as **referências visuais**.  
3) Veja a **análise técnica** e baixe o **relatório em PDF**.
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
        "summary_title": "1️⃣ Resumo da amostra",
        "interpret_block_title": "2️⃣ Interpretação técnica",
        "recs_title": "3️⃣ Recomendações de manejo",
        "placeholder": "Selecionar opção",
        "moisture_opts": ["Selecionar opção", "Baixa", "Média", "Alta"],
        "roots_opts": ["Selecionar opção", "Ausentes", "Escassas", "Abundantes"],
        "color_opts": ["Selecionar opção", "vermelho-intenso", "vermelho-amarelado", "amarelo", "marrom", "pardo-marrom", "preto", "cinza", "branco"],
        "texture_opts": ["Selecionar opção", "argiloso", "arenoso", "franco", "siltoso"],
        "structure_opts": ["Selecionar opção", "granular", "migajosa", "blocos", "prismática-colunar", "laminar", "maciça", "solto"],
        "csv_saved": "✅ Análise salva",
        "csv_file": "analises_solos.csv",
        "no_images_msg": "Não foram encontradas imagens na pasta",
        "no_folder_msg": "Não existe pasta de referência para",
        "start_btn": "➡️ Iniciar análise",
        "analysis_image_caption": "Imagem analisada (enviada pelo usuário)",
        "pdf_button": "📥 Baixar relatório em PDF",
        "tips_refs": "🔎 Compare sua amostra com estas **referências visuais** para confirmar sua seleção."
    },
}

# ================================
# INTERPRETACIONES (cortas) ES/PT
# ================================
INTERP = {
    "es": {
        "color": {
            "rojo-intenso": "Abundancia de hematita, buen drenaje y aireación; baja MO si tonos muy vivos.",
            "rojo-amarillento": "Goethita y oxidación moderada; drenaje de medio a bueno.",
            "amarillo": "Goethita y posible drenaje menos eficiente; fertilidad moderada.",
            "marrón": "Contenido moderado de MO y complejos Fe-Humus; fertilidad intermedia.",
            "pardo-marrón": "Transición con influencia férrica y de MO; buena estabilidad superficial.",
            "negro": "Alto carbono orgánico; fértil, pero puede anegarse si la estructura es pobre.",
            "gris": "Condiciones reductoras por saturación; drenaje deficiente.",
            "blanco": "Arenas lavadas o sales/carbonatos; baja fertilidad y CICE.",
        },
        "texture": {
            "arcilloso": "Alta retención de agua/nutrientes; drenaje lento y riesgo de compactación.",
            "arenoso": "Drenaje muy rápido; baja retención de agua y nutrientes.",
            "franco": "Equilibrio entre fracciones; buena aireación y retención.",
            "limoso": "Retiene más agua que arenosos, pero estructura menos estable.",
        },
        "structure": {
            "granular": "Agregados pequeños y redondeados; excelente aireación e infiltración.",
            "migajosa": "Más porosa e irregular; muy deseable para agricultura.",
            "bloques": "Cúbicos/poliédricos; pueden limitar raíces si hay compactación.",
            "prismatica-columnar": "Columnas verticales; limitan agua y raíces (común en B arcillosos/sódicos).",
            "laminar": "Láminas horizontales; muy restrictiva a infiltración y raíces.",
            "masiva": "Sin agregación; baja porosidad y drenaje deficiente.",
            "suelto": "Partículas sueltas; alta permeabilidad pero baja fertilidad.",
        },
        "moisture": {
            "Baja": "Posible estrés hídrico; difícil establecimiento de plántulas.",
            "Media": "Condición intermedia adecuada si la estructura acompaña.",
            "Alta": "Riesgo de anegamiento/anoxia y pérdida de estructura.",
        },
        "roots": {
            "Ausentes": "Limitaciones físicas/químicas o manejo reciente.",
            "Escasas": "Actividad biológica limitada; posible restricción de aireación o nutrientes.",
            "Abundantes": "Indican buena porosidad y disponibilidad hídrica/nutritiva.",
        },
    },
    "pt": {
        "color": {
            "vermelho-intenso": "Muita hematita; boa drenagem/aeração; MO baixa se tons muito vivos.",
            "vermelho-amarelado": "Goethita e oxidação moderada; drenagem média a boa.",
            "amarelo": "Goethita e possível drenagem menos eficiente; fertilidade moderada.",
            "marrom": "MO moderada e complexos Fe-Húmus; fertilidade intermediária.",
            "pardo-marrom": "Transição com influência férrica e de MO; boa estabilidade superficial.",
            "preto": "Alto C orgânico; fértil, porém pode encharcar se a estrutura for pobre.",
            "cinza": "Condições redutoras por saturação; drenagem deficiente.",
            "branco": "Areias lavadas ou sais/carbonatos; baixa fertilidade e CTC.",
        },
        "texture": {
            "argiloso": "Alta retenção de água/nutrientes; drenagem lenta e risco de compactação.",
            "arenoso": "Drenagem muito rápida; baixa retenção de água e nutrientes.",
            "franco": "Equilíbrio entre frações; boa aeração e retenção.",
            "siltoso": "Retém mais água que arenosos, porém estrutura menos estável.",
        },
        "structure": {
            "granular": "Agregados pequenos e arredondados; excelente aeração e infiltração.",
            "migajosa": "Mais porosa e irregular; muito desejável para agricultura.",
            "blocos": "Cúbicos/poliedros; podem limitar raízes se compactados.",
            "prismática-colunar": "Colunas verticais; limitam água e raízes (comum em B argilosos/sódicos).",
            "laminar": "Lâminas horizontais; muito restritiva à infiltração e raízes.",
            "maciça": "Sem agregação; baixa porosidade e drenagem deficiente.",
            "solto": "Partículas soltas; alta permeabilidade e baixa fertilidade.",
        },
        "moisture": {"Baixa": "Possível estresse hídrico.", "Média": "Condição intermediária.", "Alta": "Risco de encharcamento/anoxia."},
        "roots": {"Ausentes": "Limitações físicas/químicas.", "Escassas": "Atividade biológica limitada.", "Abundantes": "Boa porosidade e disponibilidade."},
    },
}

# ================================
# INFO LARGA (expanders) ESTRUCTURA
# ================================
INFO_ESTRUCTURA_LONG = {
    "es": {
        "granular": """**Estructura Granular**
- *Forma:* agregados pequeños, más o menos esféricos o poliédricos irregulares.
- *Formación:* materia orgánica, raíces, microorganismos y ciclos de humedecimiento-secado.
- *Uso:* excelente para infiltración, aireación y crecimiento radicular.""",
        "migajosa": """**Estructura Migajosa**
- *Forma:* muy porosa e irregular; se desmenuza fácilmente como migas.
- *Formación:* alta MO, intensa biología (lombrices, microbios) y ciclos de humedad-sequía.
- *Uso:* muy deseable en agricultura por equilibrio aire-agua.""",
        "bloques": """**Estructura en Bloques**
- *Tipos:* angulares (caras planas, aristas agudas) y subangulares (aristas más redondeadas).
- *Ubicación:* común en horizontes B.
- *Efecto:* mejores que masiva pero pueden restringir raíces/agua versus granular.""",
        "prismatica-columnar": """**Estructura Prismática/Columnar**
- *Forma:* columnas verticales.
- *Prismática:* tope plano. *Columnar:* tope redondeado (frecuente en suelos sódicos).
- *Ubicación:* horizontes B o C; pueden dificultar agua y raíces.""",
        "laminar": """**Estructura Laminar (Platy)**
- *Forma:* láminas horizontales, suele resultar de compactación/lixiviación.
- *Efecto:* restringe severamente el movimiento vertical de agua, aire y raíces.""",
        "suelto": """**Estructura Suelto (Grano Simple)**
- *Forma:* partículas individuales (típicamente arena), sin agregación.
- *Efecto:* muy buen drenaje pero baja retención de agua/nutrientes.""",
        "masiva": """**Estructura Masiva (Sin Estructura)**
- *Forma:* masa sólida y cohesiva sin planos de debilidad.
- *Efecto:* la más desfavorable: limita raíces, agua y aire; drenaje muy pobre.""",
    },
    "pt": {
        "granular": """**Estrutura Granular**
- *Forma:* agregados pequenos, esféricos ou poliedros irregulares.
- *Formação:* MO, raízes, microrganismos e ciclos de umedecimento-secagem.
- *Uso:* excelente infiltração, aeração e crescimento radicular.""",
        "migajosa": """**Estrutura Migajosa**
- *Forma:* muito porosa e irregular; esfarela como migalhas.
- *Formação:* alta MO, intensa biologia (minhocas, micróbios) e ciclos de umidade-seca.
- *Uso:* muito desejável na agricultura.""",
        "blocos": """**Estrutura em Blocos**
- *Tipos:* angulares e subangulares.
- *Local:* comum em horizontes B.
- *Efeito:* melhores que maciça, porém podem restringir raízes/água vs. granular.""",
        "prismática-colunar": """**Estrutura Prismática/Colunar**
- *Forma:* colunas verticais; topos planos (prismática) ou arredondados (colunar).
- *Local:* B ou C; podem dificultar água e raízes.""",
        "laminar": """**Estrutura Laminar (Platy)**
- *Forma:* lâminas horizontais (compactação/lixiviação).
- *Efeito:* restringe fortemente água, ar e raízes.""",
        "solto": """**Estrutura Solta (Grão Simples)**
- *Forma:* partículas individuais (areia), sem agregação.
- *Efeito:* drenagem alta e baixa retenção de água/nutrientes.""",
        "maciça": """**Estrutura Maciça (Sem Estrutura)**
- *Forma:* massa sólida coesa, sem planos de fraqueza.
- *Efeito:* a mais desfavorável; limita raízes, água e ar.""",
    },
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
    if st.button(t["start_btn"], use_container_width=True):
        st.session_state["show_intro"] = False
        st.rerun()
    st.stop()

# ================================
# FUNCIÓN: referencias con carrusel
# ================================
def mostrar_referencias(categoria: str, seleccion: str, lang_code: str):
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
            glob.glob(os.path.join(base_path, "*.png"))
            + glob.glob(os.path.join(base_path, "*.jpg"))
            + glob.glob(os.path.join(base_path, "*.jpeg"))
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

# Imagen subida (siempre arriba)
uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption=t["uploaded_caption"], use_container_width=True)

# Selectores + referencias
color = st.selectbox(t["color_label"], t["color_opts"])
mostrar_referencias("color", color, lang)

textura = st.selectbox(t["texture_label"], t["texture_opts"])
mostrar_referencias("textura", textura, lang)

estructura = st.selectbox(t["aggregation_label"], t["structure_opts"])
mostrar_referencias("forma-estructura", estructura, lang)

# Info larga de ESTRUCTURA (expanders ℹ️)
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
    st.markdown(f"## {t['interpret_title']}")
    col_img, col_sum = st.columns([1, 2])
    with col_img:
        st.image(uploaded_file, caption=t["analysis_image_caption"], use_container_width=True)
    with col_sum:
        st.success(
            f"""
**{t['summary_title']}**
- {t['color_label']}: **{color}**
- {t['texture_label']}: **{textura}**
- {t['aggregation_label']}: **{estructura}**
- {t['moisture_label']}: **{humedad}**
- {t['roots_label']}: **{raices}**
"""
        )

    st.markdown(f"### {t['interpret_block_title']}")
    interp = INTERP[lang]
    piezas = [
        interp["color"].get(color, ""),
        interp["texture"].get(textura, ""),
        interp["structure"].get(estructura, ""),
        interp["moisture"].get(humedad, ""),
        interp["roots"].get(raices, ""),
    ]
    st.info(" ".join([p for p in piezas if p]))

    st.markdown(f"### {t['recs_title']}")
    recs = []
    if (lang == "es" and humedad == "Alta") or (lang == "pt" and humedad == "Alta"):
        recs.append("• Mejorar drenaje / Melhorar a drenagem (canalización superficial, subsolado seletivo).")
    if (lang == "es" and humedad == "Baja") or (lang == "pt" and humedad == "Baixa"):
        recs.append("• Aumentar cobertura del suelo y planificar riegos oportunos. / Aumentar cobertura do solo e planejar irrigações oportunas.")
    if (lang == "es" and textura == "arenoso") or (lang == "pt" and textura == "arenoso"):
        recs.append("• Incorporar materia orgánica y fraccionar la fertilización. / Incorporar MO e fracionar a adubação.")
    if (lang == "es" and textura == "arcilloso") or (lang == "pt" and textura == "argiloso"):
        recs.append("• Evitar labranza en húmedo y promover porosidad biológica. / Evitar preparo úmido e promover porosidade biológica.")
    if (lang == "es" and estructura in ["laminar", "masiva"]) or (lang == "pt" and estructura in ["laminar", "maciça"]):
        recs.append("• Aliviar compactación (tráfico controlado, subsolado puntual) y mantener residuos. / Aliviar compactação e manter resíduos.")
    if (lang == "es" and raices in ["Ausentes", "Escasas"]) or (lang == "pt" and raices in ["Ausentes", "Escassas"]):
        recs.append("• Fomentar raíces finas con abonos verdes y rotaciones; revisar restricciones químicas. / Fomentar raízes finas com adubos verdes e rotações; revisar restrições químicas.")
    if not recs:
        recs.append("• Mantener buenas prácticas de conservación y aporte de MO. / Manter boas práticas de conservação e aporte de MO.")

    for r in recs:
        st.warning(r)

    st.markdown("---")
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
        st.success(t["csv_saved"])

    # ================================
    # Generar PDF (solo texto)
    # ================================
    def generar_pdf(lang_code, resumen, interpretacion, recomendaciones):
        pdf = FPDF()
        pdf.add_page()
        # Portada y título
        if os.path.exists("logo.png"):
            pdf.image("logo.png", x=80, y=10, w=50)
            pdf.ln(35)
        pdf.set_font("Arial", "B", 16)
        titulo = "Reporte de Análisis Visual de Suelos" if lang_code == "es" else "Relatório de Análise Visual de Solos"
        pdf.cell(0, 10, titulo, ln=True, align="C")
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, datetime.now().strftime("%d/%m/%Y %H:%M"), ln=True, align="C")
        pdf.ln(6)

        # Resumen
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, t["summary_title"].split(' ',1)[1], ln=True)  # texto sin emoji
        pdf.set_font("Arial", "", 11)
        for linea in resumen:
            pdf.multi_cell(0, 7, linea)
        pdf.ln(2)

        # Interpretación
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, t["interpret_block_title"].split(' ',1)[1], ln=True)
        pdf.set_font("Arial", "", 11)
        for parrafo in interpretacion:
            if parrafo:
                pdf.multi_cell(0, 7, parrafo)
        pdf.ln(2)

        # Recomendaciones
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, t["recs_title"].split(' ',1)[1], ln=True)
        pdf.set_font("Arial", "", 11)
        for rec in recomendaciones:
            pdf.multi_cell(0, 7, f"- {rec}")

        out = "analisis_suelo.pdf" if lang_code == "es" else "analise_solo.pdf"
        pdf.output(out)
        return out

    resumen_list = [
        f"- {t['color_label']}: {color}",
        f"- {t['texture_label']}: {textura}",
        f"- {t['aggregation_label']}: {estructura}",
        f"- {t['moisture_label']}: {humedad}",
        f"- {t['roots_label']}: {raices}",
    ]
    pdf_file = generar_pdf(lang, resumen_list, piezas, recs)
    with open(pdf_file, "rb") as f:
        st.download_button(t["pdf_button"], f, file_name=pdf_file, mime="application/pdf", use_container_width=True)

# Descarga CSV (sidebar)
with st.sidebar:
    file_csv = t["csv_file"]
    if os.path.exists(file_csv) and os.path.getsize(file_csv) > 0:
        with open(file_csv, "rb") as f:
            st.download_button(t["download_all"], f, file_name=file_csv, mime="text/csv", use_container_width=True)


