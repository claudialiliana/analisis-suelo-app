import streamlit as st
import os, csv, glob
from datetime import datetime

# ================================
# CONFIG INICIAL (debe ser lo 1º)
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
        "blocos": "bloques",                 # mapea a carpeta 'bloques'
        "prismática-colunar": "prismatica-columnar",
        "laminar": "laminar",
        "maciça": "masiva",
        "solto": "suelto",
    },
}

# ================================
# TEXTOS MULTILINGÜES + OPCIONES (con "Seleccionar opción")
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
# FUNCIÓN CARRUSEL (color/textura/estructura)
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
    st.image(uploaded_file, caption=t["uploaded_caption"], use_column_width=True)

# Selectores con placeholder
color = st.selectbox(t["color_label"], t["color_opts"])
mostrar_referencias("color", color, lang)

textura = st.selectbox(t["texture_label"], t["texture_opts"])
mostrar_referencias("textura", textura, lang)

estructura = st.selectbox(t["aggregation_label"], t["structure_opts"])
mostrar_referencias("forma-estructura", estructura, lang)

humedad = st.selectbox(t["moisture_label"], t["moisture_opts"])
raices = st.selectbox(t["roots_label"], t["roots_opts"])

# ================================
# CONCLUSIÓN EN 3 BLOQUES
# ================================
ready = (
    uploaded_file is not None and
    color != t["placeholder"] and
    textura != t["placeholder"] and
    estructura != t["placeholder"] and
    humedad != t["placeholder"] and
    raices != t["placeholder"]
)

if ready:
    st.markdown(f"## {t['interpret_title']}")
    # Imagen analizada
    st.image(uploaded_file, width=320, caption=t["analysis_image_caption"])
    st.markdown("---")

    # 1) Resumen
    st.markdown(f"### {t['summary_title']}")
    st.write(
        f"- {t['color_label']}: **{color}**  \n"
        f"- {t['texture_label']}: **{textura}**  \n"
        f"- {t['aggregation_label']}: **{estructura}**  \n"
        f"- {t['moisture_label']}: **{humedad}**  \n"
        f"- {t['roots_label']}: **{raices}**"
    )

    # 2) Interpretación técnica (texto explicativo)
    st.markdown(f"### {t['interpret_block_title']}")
    interp = INTERP[lang]
    # Mapear estructura PT a claves del diccionario si es necesario
    estructura_key = estructura
    if lang == "pt" and estructura in ["prismática-colunar"]:
        estructura_key = "prismática-colunar"
    # Construir texto
    partes = []
    # color
    color_key = color
    if lang == "pt":
        # Ajuste de mapeo PT->ES si hiciera falta para coherencia, pero aquí las claves ya están en PT
        pass
    partes.append(interp["color"].get(color_key, ""))
    # textura
    partes.append(interp["texture"].get(textura, ""))
    # estructura
    # Unificar claves para prismatica/colunar
    if lang == "es" and estructura_key == "prismatica-columnar":
        partes.append(interp["structure"].get("prismatica-columnar", ""))
    elif lang == "pt" and estructura_key == "prismática-colunar":
        partes.append(interp["structure"].get("prismática-colunar", ""))
    else:
        partes.append(interp["structure"].get(estructura_key, ""))
    # humedad
    partes.append(interp["moisture"].get(humedad, ""))
    # raíces
    partes.append(interp["roots"].get(raices, ""))

    st.write(" ".join([p for p in partes if p]))

    # 3) Recomendaciones
    st.markdown(f"### {t['recs_title']}")
    # Reglas simples basadas en humedad y textura/estructura
    recs = []
    if (lang == "es" and humedad == "Alta") or (lang == "pt" and humedad == "Alta"):
        recs.append("Mejorar el drenaje (canalización superficial, subsolado selectivo si hay capas densas). / Melhorar a drenagem (canalização superficial, subsolagem seletiva se houver camadas densas).")
    if (lang == "es" and humedad == "Baja") or (lang == "pt" and humedad == "Baixa"):
        recs.append("Aumentar cobertura del suelo y planificar riegos oportunos. / Aumentar cobertura do solo e planejar irrigações oportunas.")
    if (lang == "es" and textura == "arenoso") or (lang == "pt" and textura == "arenoso"):
        recs.append("Incorporar materia orgánica y fraccionar la fertilización para reducir lixiviación. / Incorporar matéria orgânica e fracionar a adubação para reduzir lixiviação.")
    if (lang == "es" and textura == "arcilloso") or (lang == "pt" and textura == "argiloso"):
        recs.append("Evitar labranza en húmedo y promover porosidad biológica con raíces/coberturas. / Evitar preparo do solo úmido e promover porosidade biológica com raízes/coberturas.")
    if (lang == "es" and estructura in ["laminar", "masiva"]) or (lang == "pt" and estructura in ["laminar", "maciça"]):
        recs.append("Aliviar compactación (tráfico controlado, subsolado puntual) y mantener residuos en superficie. / Aliviar compactação (tráfego controlado, subsolagem pontual) e manter resíduos na superfície.")
    if (lang == "es" and raices in ["Ausentes", "Escasas"]) or (lang == "pt" and raices in ["Ausentes", "Escassas"]):
        recs.append("Fomentar raíces finas con abonos verdes y rotaciones; revisar restricciones químicas. / Fomentar raízes finas com adubos verdes e rotações; revisar restrições químicas.")

    if not recs:
        recs.append("Mantener buenas prácticas de conservación y aporte de materia orgánica. / Manter boas práticas de conservação e aporte de matéria orgânica.")
    for r in recs:
        st.write(f"- {r}")

    st.markdown("---")
    # Guardar a CSV
    if st.button(t["save_button"]):
        file_csv = t["csv_file"]
        headers_exist = os.path.exists(file_csv) and os.path.getsize(file_csv) > 0
        with open(file_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not headers_exist:
                writer.writerow(["timestamp", "idioma", "color", "textura", "estructura", "humedad", "raices"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), lang, color, textura, estructura, humedad, raices])
        st.success(t["csv_saved"])

# Descarga CSV (sidebar)
with st.sidebar:
    file_csv = t["csv_file"]
    if os.path.exists(file_csv) and os.path.getsize(file_csv) > 0:
        with open(file_csv, "rb") as f:
            st.download_button(t["download_all"], f, file_name=file_csv, mime="text/csv")
