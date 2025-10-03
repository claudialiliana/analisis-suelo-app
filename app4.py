import streamlit as st
import os, csv
from datetime import datetime
from openpyxl import Workbook

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
</style>
""", unsafe_allow_html=True)

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
        "excel_button": "📥 Descargar en Excel",
        "csv_file": "analisis_suelos.csv",
        "placeholder": "Seleccionar opción",
        "moisture_opts": ["Seleccionar opción", "Baja", "Media", "Alta"],
        "roots_opts": ["Seleccionar opción", "Ausentes", "Escasas", "Abundantes"],
        "color_opts": ["Seleccionar opción", "rojo-intenso", "rojo-amarillento", "amarillo", "marrón", "pardo-marrón", "negro", "gris", "blanco"],
        "texture_opts": ["Seleccionar opción", "arcilloso", "arenoso", "franco", "limoso"],
        "structure_opts": ["Seleccionar opción", "granular", "migajosa", "bloques", "prismatica-columnar", "laminar", "masiva", "suelto"],
    },
   "pt": {
        "app_title": "🌱 Análise Visual de Solos",
        "start_btn": "🚀 Iniciar análise",
        "intro": """
**Bem-vindo(a) a esta plataforma educativa para explorar o mundo do solo de forma visual e interativa.**
Aqui você poderá analisar algumas de suas principais características físicas e entender como elas influenciam na interpretação do solo.
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
        "excel_button": "📥 Baixar em Excel",
        "csv_file": "analises_solos.csv",
        "placeholder": "Selecionar opção",
        "moisture_opts": ["Selecionar opção", "Baixa", "Média", "Alta"],
        "roots_opts": ["Selecionar opção", "Ausentes", "Escassas", "Abundantes"],
        "color_opts": ["Selecionar opção", "vermelho-intenso", "vermelho-amarelado", "amarelo", "marrom", "pardo-marrom", "preto", "cinza", "branco"],
        "texture_opts": ["Selecionar opção", "argiloso", "arenoso", "franco", "siltoso"],
        "structure_opts": ["Selecionar opção", "granular", "migajosa", "blocos", "prismática-colunar", "laminar", "maciça", "solto"],
    },
}

# ================================
# INTERPRETACIONES DETALLADAS (ES/PT)
# ================================
INTERP = {
    "es": {
        "color": {
            "rojo-intenso": "El color rojo intenso suele reflejar abundancia de óxidos de hierro (hematita), asociado a buen drenaje y ambientes bien aireados; puede indicar baja materia orgánica si los tonos son muy vivos.",
            "rojo-amarillento": "El color rojo-amarillento indica presencia de óxidos de hierro hidratados (goethita) y condiciones de oxidación moderadas; sugiere drenaje de medio a bueno.",
            "amarillo": "El color amarillo está vinculado a goethita y a veces a condiciones de drenaje menos eficientes; puede aparecer en suelos lixiviados con fertilidad moderada.",
            "marrón": "El color marrón suele reflejar contenido moderado de materia orgánica y complejos Fe-Humus; frecuentemente asociado a fertilidad intermedia y actividad biológica moderada.",
            "pardo-marrón": "El pardo-marrón es una transición con influencia tanto de compuestos férricos como de materia orgánica; sugiere fertilidad aceptable y buena estabilidad estructural superficial.",
            "negro": "El color negro indica alto contenido de carbono orgánico y humificación avanzada; suelos fértiles, con alta capacidad de intercambio catiónico pero susceptibles a anegamiento si la estructura es deficiente.",
            "gris": "El color gris sugiere condiciones reductoras por saturación de agua (gley), con hierro reducido; drenaje deficiente y posible anoxia radicular.",
            "blanco": "El color blanco se relaciona con arenas muy lavadas o acumulación de sales/carbonatos; indica baja fertilidad y escasa capacidad de retener agua y nutrientes.",
        },
        "texture": {
            "arcilloso": "Textura arcillosa: alta retención de agua y nutrientes; drenaje lento y riesgo de compactación; plasticidad y pegajosidad elevadas.",
            "arenoso": "Textura arenosa: drenaje muy rápido, baja retención de agua y nutrientes; susceptible a sequía y lixiviación de fertilizantes.",
            "franco": "Textura franca: equilibrio entre arena, limo y arcilla; buena aireación y retención, ideal para la mayoría de cultivos.",
            "limoso": "Textura limosa: mayor retención de agua que arenosos, pero estructura menos estable; riesgo de encostramiento superficial.",
        },
        "structure": {
            "granular": "Estructura granular: agregados pequeños y redondeados con alta porosidad; excelente para aireación, infiltración y crecimiento radicular (común en horizontes A ricos en MO).",
            "migajosa": "Estructura migajosa: similar a la granular pero más porosa e irregular; muy deseable en suelos agrícolas por equilibrio aire-agua.",
            "bloques": "Estructura en bloques (subangular/angular): agregados cúbicos/poliédricos; moderada a fuerte; puede restringir el crecimiento radicular si se compacta.",
            "prismatica-columnar": "Estructura prismática/columnar: agregados verticales con tope plano (prismática) o redondeado (columnar); asociados a horizontes B con arcillas y/o sodicidad; drenaje limitado.",
            "laminar": "Estructura laminar: agregados en láminas horizontales; muy restrictiva para infiltración y raíces; típica de compactación o horizontes E.",
            "masiva": "Estructura masiva: sin agregación discernible; baja porosidad y drenaje deficiente; limita la aireación y el desarrollo radicular.",
            "suelto": "Sin estructura (suelto): partículas individuales; alta permeabilidad pero baja fertilidad y escasa retención de agua (típico de suelos arenosos).",
        },
        "moisture": {
            "Baja": "Humedad baja: potencial estrés hídrico, mayor esfuerzo para establecimiento de plántulas.",
            "Media": "Humedad media: condición intermedia adecuada para la mayoría de cultivos si la estructura acompaña.",
            "Alta": "Humedad alta: riesgo de anegamiento y anoxia; procesos reductores y pérdida de estructura.",
        },
        "roots": {
            "Ausentes": "Raíces ausentes: puede indicar limitaciones físicas (compactación) o químicas (toxicidad, salinidad), o manejo reciente del suelo.",
            "Escasas": "Raíces escasas: actividad biológica limitada y posible restricción de aireación o nutrientes.",
            "Abundantes": "Raíces abundantes: condición favorable de aireación, porosidad y disponibilidad de agua/nutrientes.",
        },
    },
    "pt": {
        "color": {
            "vermelho-intenso": "A cor vermelha intensa reflete abundância de óxidos de ferro (hematita), associada a boa drenagem e aeração; pode indicar baixa matéria orgânica quando os tons são muito vivos.",
            "vermelho-amarelado": "A cor vermelho-amarelada indica presença de óxidos de ferro hidratados (goethita) e condições de oxidação moderadas; drenagem de média a boa.",
            "amarelo": "A cor amarela está ligada à goethita e, às vezes, a drenagem menos eficiente; pode ocorrer em solos lixiviados com fertilidade moderada.",
            "marrom": "A cor marrom reflete teor moderado de matéria orgânica e complexos Fe-Humus; frequentemente associada à fertilidade intermediária e atividade biológica moderada.",
            "pardo-marrom": "O pardo-marrom é transicional com influência de compostos férricos e de MO; sugere fertilidade aceitável e boa estabilidade estrutural superficial.",
            "preto": "A cor preta indica alto teor de carbono orgânico e humificação avançada; solos férteis, com alta CTC, porém suscetíveis a encharcamento se a estrutura for deficiente.",
            "cinza": "A cor cinza sugere condições redutoras por saturação hídrica (glei), com ferro reduzido; drenagem deficiente e possível anoxia radicular.",
            "branco": "A cor branca relaciona-se a areias muito lavadas ou acúmulo de sais/carbonatos; baixa fertilidade e fraca retenção de água e nutrientes.",
        },
        "texture": {
            "argiloso": "Textura argilosa: alta retenção de água e nutrientes; drenagem lenta e risco de compactação; elevada plasticidade e pegajosidade.",
            "arenoso": "Textura arenosa: drenagem muito rápida, baixa retenção de água e nutrientes; suscetível à seca e à lixiviação de fertilizantes.",
            "franco": "Textura franca: equilíbrio entre areia, silte e argila; boa aeração e retenção, ideal para a maioria das culturas.",
            "siltoso": "Textura siltosa: maior retenção de água que arenosos, mas estrutura menos estável; risco de formação de crostas superficiais.",
        },
        "structure": {
            "granular": "Estrutura granular: agregados pequenos e arredondados com alta porosidade; excelente para aeração, infiltração e crescimento radicular.",
            "migajosa": "Estrutura migajosa: semelhante à granular, porém mais porosa e irregular; muito desejável em solos agrícolas.",
            "blocos": "Estrutura em blocos (subangular/angular): agregados cúbicos/poliedros; moderada a forte; pode restringir o crescimento radicular se compactada.",
            "prismática-colunar": "Estrutura prismática/colunar: agregados verticais com topo plano (prismática) ou arredondado (colunar); associados a horizontes B argilosos e/ou sódicos; drenagem limitada.",
            "laminar": "Estrutura laminar: agregados em lâminas horizontais; muito restritiva à infiltração e às raízes; típica de compactação ou horizontes E.",
            "maciça": "Estrutura maciça: sem agregação discernível; baixa porosidade e drenagem deficiente; limita a aeração e o desenvolvimento radicular.",
            "solto": "Sem estrutura (solto): partículas individuais; alta permeabilidade, baixa fertilidade e retenção de água (solos arenosos).",
        },
        "moisture": {
            "Baixa": "Baixa umidade: potencial estresse hídrico e dificuldade de estabelecimento de plântulas.",
            "Média": "Umidade média: condição intermediária adequada para a maioria das culturas se a estrutura ajudar.",
            "Alta": "Alta umidade: risco de encharcamento e anoxia; processos redutores e perda de estrutura.",
        },
        "roots": {
            "Ausentes": "Raízes ausentes: pode indicar limitações físicas (compactação) ou químicas (toxicidade, salinidade) ou manejo recente do solo.",
            "Escassas": "Raízes escassas: atividade biológica limitada e possível restrição de aeração ou nutrientes.",
            "Abundantes": "Raízes abundantes: condição favorável de aeração, porosidade e disponibilidade de água/nutrientes.",
        },
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
# FUNCIÓN: Generar Excel
# ================================
def generar_excel(lang_code, resumen, interpretacion, recomendaciones):
    wb = Workbook()
    ws = wb.active
    ws.title = "Análisis de suelo"

    ws.append([TEXT_CONTENT[lang_code]["app_title"]])
    ws.append([datetime.now().strftime("%d/%m/%Y %H:%M")])
    ws.append([])

    ws.append([TEXT_CONTENT[lang_code]["summary_title"]])
    for item in resumen:
        ws.append([item])
    ws.append([])

    ws.append([TEXT_CONTENT[lang_code]["interpret_block_title"]])
    for parrafo in interpretacion:
        ws.append([parrafo])
    ws.append([])

    ws.append([TEXT_CONTENT[lang_code]["recs_title"]])
    for rec in recomendaciones:
        ws.append([rec])

    out = f"analisis_suelo_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    wb.save(out)
    return out

# ================================
# APP
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
    recs = ["Mantener buenas prácticas de conservación."]

    # --- Mostrar en pantalla ---
    st.markdown(f"### {t['summary_title']}")
    st.image(uploaded_file, caption="🖼️ Imagen analizada", width=250)
    for r in resumen_list:
        st.write(f"- {r}")

    st.markdown(f"### {t['interpret_block_title']}")
    for p in piezas:
        if p:
            st.write(f"- {p}")

    st.markdown(f"### {t['recs_title']}")
    for r in recs: 
        st.write(f"- {r}")

    # Guardar CSV
    if st.button(t["save_button"]):
        file_csv = t["csv_file"]
        headers_exist = os.path.exists(file_csv) and os.path.getsize(file_csv)>0
        with open(file_csv,"a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            if not headers_exist: 
                writer.writerow(["Fecha","Idioma","Color","Textura","Estructura","Humedad","Raíces"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lang,color,textura,estructura,humedad,raices])
        st.success("✅ Análisis guardado en CSV")

    # Descargar Excel
    excel_file = generar_excel(lang, resumen_list, piezas, recs)
    with open(excel_file,"rb") as f:
        st.download_button(t["excel_button"], f, file_name=excel_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")








