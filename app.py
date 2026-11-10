import streamlit as st
from ddgs import DDGS
from difflib import SequenceMatcher
import re

st.set_page_config(page_title="ManuBot", page_icon="🔧", layout="centered")
st.title("🔧 ManuBot")
st.write("Tu compa que ya piensa solo, ve imágenes y abre links.")

# --- MEMORIA / INTELIGENCIA PROPIA DE MANUBOT ---
if "aprendido" not in st.session_state:
    # Su cerebro inicial, ya sabe platicar
    st.session_state.aprendido = {
        "hola": "Hola Manu! ¿Qué onda? ¿Qué andamos arreglando hoy?",
        "como estas": "Bien Manu, aquí jalando contigo. ¿Y tú cómo andas?",
        "quien eres": "Soy ManuBot, tu compa del taller que aprende de ti.",
        "que haces": "Aquí ando, viendo tus fotos, tus links y buscando en internet.",
        "adios": "Nos vemos Manu, cuídate. Aquí te espero.",
        "gracias": "De nada Manu, para eso estoy.",
    }
if "ultima_pregunta" not in st.session_state:
    st.session_state.ultima_pregunta = ""
if "ultima_respuesta" not in st.session_state:
    st.session_state.ultima_respuesta = "Hola Manu, soy ManuBot. Pregúntame, mándame una foto o un link y yo te respondo."
if "ultima_imagen" not in st.session_state:
    st.session_state.ultima_imagen = None
if "modo_ensenar" not in st.session_state:
    st.session_state.modo_ensenar = False

# --- SU PROPIA INTELIGENCIA: BUSCA LA RESPUESTA MÁS PARECIDA ---
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

    # 1. TEMAS QUE SIEMPRE BUSCA EN INTERNET
    if any(p in texto_bajo for p in ["llover", "lluvia", "clima", "pronostico", "pronóstico", "tiempo", "calor", "frio"]):
        info = buscar_internet("clima Monterrey hoy pronóstico lluvia")
        if info:
            return f"Manu, esto dice internet del clima ahorita:\n\n{info}\n¿Quieres que te busque el de otra ciudad?"
    if any(p in texto_bajo for p in ["dolar", "dólar"]):
        info = buscar_internet("precio dólar hoy México")
        if info:
            return f"Manu, esto encontré del dólar hoy:\n\n{info}"

    # 2. SU CEREBRO: BUSCA LA RESPUESTA MÁS PARECIDA A TU PREGUNTA
    mejor_puntaje = 0
    mejor_respuesta = ""
    for clave, respuesta in st.session_state.aprendido.items():
        # Revisa palabra por palabra + parecido general
        puntaje = parecido(texto_bajo, clave)
        # Si alguna palabra clave de más de 3 letras coincide, le sube puntaje
        for palabra in clave.split():
            if len(palabra) > 3 and palabra in texto_bajo:
                puntaje += 0.3
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_respuesta = respuesta

    # Si encontró algo con buen parecido, lo responde. Esta es su inteligencia propia.
    if mejor_puntaje > 0.45:
        return mejor_respuesta

    # 3. SI NO LO SABE, BUSCA EN INTERNET Y LO APRENDE SOLO
    info = buscar_internet(pregunta)
    if info:
        st.session_state.aprendido[texto_bajo] = f"Esto encontré en internet, Manu:\n\n{info}"
        return f"Esto encontré en internet, Manu:\n\n{info}\n\nYa lo aprendí, si me vuelves a preguntar lo mismo, ya te lo digo en corto."
    
    return "Mmm Manu, no encontré eso. Platícame más o enséñame picándole a 📚 Enséñame."

# --- AQUÍ SOLO SE VE LA ÚLTIMA PLÁTICA, SE BORRA LA ANTERIOR ---
st.divider()
if st.session_state.ultima_imagen is not None:
    st.image(st.session_state.ultima_imagen, caption="Foto que me mandaste, Manu", use_container_width=True)

st.markdown(f"**Tú:** {st.session_state.ultima_pregunta}" if st.session_state.ultima_pregunta else "")
st.markdown(f"**ManuBot:** {st.session_state.ultima_respuesta}")
st.divider()

# --- 1. CAJA PARA ESCRIBIR + LINKS ---
pregunta = st.text_input("💬 Escríbele a ManuBot, o pega un link:", placeholder="Ej: hola, ¿va a llover?, https://youtube.com/...", key="caja_principal")

# --- 2. BOTONES GRANDES E INTUITIVOS ---
col1, col2, col3 = st.columns(3)
with col1:
    boton_enviar = st.button("➤ ENVIAR", use_container_width=True)
with col2:
    boton_ensenar = st.button("📚 ENSEÑAME", use_container_width=True)
with col3:
    boton_limpiar = st.button("🗑️ BORRAR", use_container_width=True)

# --- 3. SUBIR IMAGEN ---
imagen = st.file_uploader("📷 Subir foto / imagen", type=["jpg", "jpeg", "png", "webp"], key="subir_foto")
if imagen is not None:
    st.session_state.ultima_imagen = imagen
    st.session_state.ultima_pregunta = "Te mandé una foto, ManuBot"
    st.session_state.ultima_respuesta = "Ya vi tu foto, Manu. Se ve bien. ¿Qué tiene? ¿Qué le falla? Dime qué es y te ayudo a diagnosticarlo. Y ya la guardé para que la veamos."
    st.rerun()

if boton_limpiar:
    st.session_state.ultima_pregunta = ""
    st.session_state.ultima_respuesta = "Listo Manu, ya borré la plática. ¿Qué me preguntas ahora?"
    st.session_state.ultima_imagen = None
    st.rerun()

if boton_ensenar:
    st.session_state.modo_ensenar = not st.session_state.modo_ensenar
    st.rerun()

# --- MODO ENSEÑAR: 2 CAJITAS ---
if st.session_state.modo_ensenar:
    st.subheader("📚 Enséñame, Manu")
    pregunta_ensenar = st.text_input("1️⃣ PREGUNTA / Palabra clave:", placeholder="Ej: que es un alternador", key="p_ens")
    respuesta_ensenar = st.text_area("2️⃣ RESPUESTA que debo dar:", placeholder="Ej: El alternador es el que carga la batería...", key="r_ens")
    if st.button("💾 GUARDAR LO QUE ME ENSEÑASTE", use_container_width=True):
        if pregunta_ensenar.strip() != "" and respuesta_ensenar.strip() != "":
            st.session_state.aprendido[pregunta_ensenar.lower().strip()] = respuesta_ensenar
            st.session_state.ultima_respuesta = f"Listo Manu, ya aprendí. Cuando me preguntes '{pregunta_ensenar}' te voy a decir lo que me enseñaste."
            st.session_state.modo_ensenar = False
            st.rerun()
        else:
            st.warning("Llena los dos, Manu. Pregunta y respuesta.")

# --- CUANDO LE ENVÍAS ALGO ---
if boton_enviar and pregunta.strip() != "":
    # DETECTA SI ES UN LINK
    links = re.findall(r'https?://\S+', pregunta)
    if links:
        link = links[0]
        # SE BORRA LA PREGUNTA ANTERIOR Y SOLO QUEDA ESTA
        st.session_state.ultima_pregunta = pregunta
        st.session_state.ultima_respuesta = f"Ya vi tu link, Manu. Aquí está para que lo abras:\n\n{link}\n\n¿Qué quieres que haga con ese link? ¿Te lo resumo? Dime y lo busco en internet."
        st.session_state.ultima_imagen = None
        st.markdown(f"[🔗 Abrir link]({link})")
    else:
        respuesta = inteligencia_manubot(pregunta)
        # AQUÍ SE BORRA AUTOMÁTICAMENTE LA PREGUNTA ANTERIOR
        st.session_state.ultima_pregunta = pregunta
        st.session_state.ultima_respuesta = respuesta
        st.session_state.ultima_imagen = None
    st.rerun()

st.divider()
st.write(f"🧠 Cosas que ya aprendí: {len(st.session_state.aprendido)}")
