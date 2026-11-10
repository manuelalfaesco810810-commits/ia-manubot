import streamlit as st
from ddgs import DDGS
from difflib import SequenceMatcher
import re, json, os, base64, io
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS

st.set_page_config(page_title="ManuBot", page_icon="🔧", layout="centered")

# --- ESTILO: BOTONES GRANDES Y DIFERENTES ---
st.markdown("""
<style>
    .stButton > button { height: 70px !important; font-size: 20px !important; font-weight: bold !important; border-radius: 20px !important; color: white !important; border: none !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button { background-color: #22c55e !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button { background-color: #f97316 !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) button { background-color: #ef4444 !important; }
    .guardar button { background-color: #3b82f6 !important; }
    .stTextInput > div > div > input { font-size: 18px !important; height: 55px !important; }
</style>
""", unsafe_allow_html=True)

st.title("🔧 ManuBot")
st.write("Tu compa que te escucha Y te contesta hablando.")

# --- BOTON PARA PRENDER / APAGAR LA VOZ DE MANUBOT ---
hablar = st.toggle("🔊 Que ManuBot me conteste con voz", value=True)
st.write("Si lo apagas, solo te escribe. Si lo prendes, también te habla.")

# --- GUARDADO PERMANENTE ---
ARCHIVO_MEMORIA = "memoria_manubot.json"

def cargar_memoria():
    if os.path.exists(ARCHIVO_MEMORIA):
        try:
            with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {
        "hola": {"texto": "Hola Manu! ¿Qué onda? ¿Qué andamos arreglando hoy?", "imagen": None},
        "como estas": {"texto": "Bien Manu, aquí jalando contigo. ¿Y tú cómo andas?", "imagen": None},
        "quien eres": {"texto": "Soy ManuBot, tu compa del taller que aprende de ti.", "imagen": None},
    }

def guardar_memoria():
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(st.session_state.aprendido, f, ensure_ascii=False, indent=2)

def imagen_a_texto(imagen_file):
    return base64.b64encode(imagen_file.getvalue()).decode("utf-8")

def texto_a_imagen(texto_b64):
    return base64.b64decode(texto_b64)

# --- AQUÍ ESTÁ LO NUEVO, MANU: QUE LEA SUS RESPUESTAS ---
def manubot_habla(texto):
    # Limpia el texto para que suene bien, sin links ni símbolos raros
    texto_limpio = re.sub(r'https?://\S+', '', texto)
    texto_limpio = re.sub(r'[*#•]', '', texto_limpio)
    texto_limpio = texto_limpio[:500]  # Solo lee los primeros 500 caracteres para que no se tarde
    if texto_limpio.strip() == "":
        return None
    try:
        tts = gTTS(text=texto_limpio, lang='es', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except:
        return None

if "aprendido" not in st.session_state:
    st.session_state.aprendido = cargar_memoria()
if "ultima_pregunta" not in st.session_state:
    st.session_state.ultima_pregunta = ""
if "ultima_respuesta" not in st.session_state:
    st.session_state.ultima_respuesta = "Hola Manu, soy ManuBot. Háblame y yo te contesto con voz."
if "ultima_imagen_respuesta" not in st.session_state:
    st.session_state.ultima_imagen_respuesta = None
if "modo_ensenar" not in st.session_state:
    st.session_state.modo_ensenar = False
if "texto_voz" not in st.session_state:
    st.session_state.texto_voz = ""
if "audio_respuesta" not in st.session_state:
    st.session_state.audio_respuesta = None

# --- INTELIGENCIA PROPIA ---
def parecido(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def buscar_internet(pregunta):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pregunta, max_results=4))
            if resultados:
                texto = ""
                for r in resultados:
                    texto += f"• **{r['title']}**: {r['body']}\n\nFuente: {r['href']}\n\n"
                return texto
            return ""
    except:
        return ""

def inteligencia_manubot(pregunta):
    texto_bajo = pregunta.lower().strip()
    if any(p in texto_bajo for p in ["llover", "lluvia", "clima", "pronostico", "pronóstico", "tiempo", "calor", "frio"]):
        info = buscar_internet("clima Monterrey hoy pronóstico lluvia")
        if info:
            return f"Manu, esto dice internet del clima ahorita:\n\n{info}", None
    if any(p in texto_bajo for p in ["dolar", "dólar"]):
        info = buscar_internet("precio dólar hoy México")
        if info:
            return f"Manu, esto encontré del dólar hoy:\n\n{info}", None

    mejor_puntaje = 0
    mejor_dato = None
    for clave, dato in st.session_state.aprendido.items():
        puntaje = parecido(texto_bajo, clave)
        for palabra in clave.split():
            if len(palabra) > 3 and palabra in texto_bajo:
                puntaje += 0.3
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_dato = dato

    if mejor_puntaje > 0.45 and mejor_dato:
        return mejor_dato.get("texto", ""), mejor_dato.get("imagen", None)

    info = buscar_internet(pregunta)
    if info:
        nuevo = {"texto": f"Esto encontré en internet, Manu:\n\n{info}", "imagen": None}
        st.session_state.aprendido[texto_bajo] = nuevo
        guardar_memoria()
        return nuevo["texto"], None
    return "Mmm Manu, no encontré eso. Enséñame picándole a 📚 ENSEÑAME.", None

# --- VOZ: TÚ LE HABLAS ---
st.subheader("🎤 Pregúntame con tu voz")
audio = st.audio_input("Pícale al micrófono y habla, Manu:")
if audio is not None:
    try:
        sonido = AudioSegment.from_file(audio)
        buf = io.BytesIO()
        sonido.export(buf, format="wav")
        buf.seek(0)
        r = sr.Recognizer()
        with sr.AudioFile(buf) as source:
            datos_audio = r.record(source)
            texto_detectado = r.recognize_google(datos_audio, language="es-MX")
            st.session_state.texto_voz = texto_detectado
            st.success(f"Te escuché, Manu. Dijiste: **{texto_detectado}**")
    except:
        st.warning("No te entendí bien, Manu. Intenta de nuevo.")

# --- SOLO SE VE LA ÚLTIMA PLÁTICA + AQUÍ HABLA MANUBOT ---
st.divider()
if st.session_state.ultima_imagen_respuesta:
    st.image(texto_a_imagen(st.session_state.ultima_imagen_respuesta), caption="Esto te respondo con foto, Manu", use_container_width=True)
if st.session_state.ultima_pregunta:
    st.markdown(f"**Tú:** {st.session_state.ultima_pregunta}")
st.markdown(f"**ManuBot:** {st.session_state.ultima_respuesta}")

# AQUÍ SUENA SU VOZ, MANU
if hablar and st.session_state.audio_respuesta is not None:
    st.audio(st.session_state.audio_respuesta, format="audio/mp3", autoplay=True)
    st.write("🔊 ManuBot te está hablando...")

st.divider()

valor_inicial = st.session_state.texto_voz if st.session_state.texto_voz else ""
pregunta = st.text_input("💬 Escríbele o pega un link:", value=valor_inicial, placeholder="Ej: hola, ¿va a llover?", key="caja_principal")

col1, col2, col3 = st.columns(3)
with col1:
    boton_enviar = st.button("➤  ENVIAR\nPREGUNTA", use_container_width=True)
with col2:
    boton_ensenar = st.button("📚  ENSEÑAME\nQUE APRENDA", use_container_width=True)
with col3:
    boton_limpiar = st.button("🗑️  BORRAR\nPLÁTICA", use_container_width=True)

imagen_pregunta = st.file_uploader("📷 Subir foto para preguntar", type=["jpg", "jpeg", "png", "webp"])
if imagen_pregunta is not None:
    st.session_state.ultima_pregunta = "Te mandé una foto, ManuBot"
    st.session_state.ultima_respuesta = "Ya vi tu foto, Manu. ¿Qué tiene? ¿Qué le falla? Dime qué es y te ayudo."
    st.session_state.ultima_imagen_respuesta = imagen_a_texto(imagen_pregunta)
    # TAMBIÉN HABLA CUANDO VE TU FOTO
    if hablar:
        st.session_state.audio_respuesta = manubot_habla(st.session_state.ultima_respuesta)
    st.session_state.texto_voz = ""
    st.rerun()

if boton_limpiar:
    st.session_state.ultima_pregunta = ""
    st.session_state.ultima_respuesta = "Listo Manu, ya borré la plática. ¿Qué me preguntas ahora?"
    st.session_state.ultima_imagen_respuesta = None
    st.session_state.audio_respuesta = None
    st.session_state.texto_voz = ""
    st.rerun()

if boton_ensenar:
    st.session_state.modo_ensenar = not st.session_state.modo_ensenar
    st.rerun()

if st.session_state.modo_ensenar:
    st.subheader("📚 Enséñame, Manu - Ya no se borra")
    pregunta_ensenar = st.text_input("1️⃣ PREGUNTA / Palabra clave:", placeholder="Ej: que es un alternador", key="p_ens")
    respuesta_ensenar = st.text_area("2️⃣ RESPUESTA que debo dar:", placeholder="Ej: El alternador es el que carga la batería...", key="r_ens")
    st.write("3️⃣ (Opcional) Sube una foto como respuesta:")
    imagen_respuesta = st.file_uploader("📷 Foto que debo responder cuando me pregunten eso", type=["jpg", "jpeg", "png", "webp"], key="img_resp")
    st.markdown('<div class="guardar">', unsafe_allow_html=True)
    boton_guardar = st.button("💾  GUARDAR LO QUE ME ENSEÑASTE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if boton_guardar:
        if pregunta_ensenar.strip() != "":
            imagen_b64 = imagen_a_texto(imagen_respuesta) if imagen_respuesta is not None else None
            st.session_state.aprendido[pregunta_ensenar.lower().strip()] = {"texto": respuesta_ensenar, "imagen": imagen_b64}
            guardar_memoria()
            st.session_state.ultima_respuesta = f"Listo Manu, ya lo guardé para siempre. Cuando me preguntes '{pregunta_ensenar}' te voy a responder con lo que me enseñaste."
            if hablar:
                st.session_state.audio_respuesta = manubot_habla(st.session_state.ultima_respuesta)
            st.session_state.modo_ensenar = False
            st.session_state.texto_voz = ""
            st.rerun()
        else:
            st.warning("Escribe al menos la pregunta, Manu.")

if boton_enviar and pregunta.strip() != "":
    links = re.findall(r'https?://\S+', pregunta)
    if links:
        link = links[0]
        st.session_state.ultima_pregunta = pregunta
        st.session_state.ultima_respuesta = f"Ya vi tu link, Manu. Aquí está:\n\n{link}"
        st.session_state.ultima_imagen_respuesta = None
        st.markdown(f"[🔗 Abrir link]({link})")
    else:
        respuesta, img_resp = inteligencia_manubot(pregunta)
        st.session_state.ultima_pregunta = pregunta
        st.session_state.ultima_respuesta = respuesta
        st.session_state.ultima_imagen_respuesta = img_resp
    # AQUÍ ES DONDE HABLA, MANU
    if hablar:
        st.session_state.audio_respuesta = manubot_habla(st.session_state.ultima_respuesta)
    st.session_state.texto_voz = ""
    st.rerun()

st.divider()
st.write(f"🧠 Cosas que ya aprendí y guardé: {len(st.session_state.aprendido)} - Ya no se borran al actualizar")
