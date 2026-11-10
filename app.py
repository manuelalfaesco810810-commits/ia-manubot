import streamlit as st
from ddgs import DDGS
import re

st.set_page_config(page_title="ManuBot", page_icon="🔧")
st.title("🔧 ManuBot - Tu compa que platica")

# --- MEMORIA ---
if "chat" not in st.session_state:
    st.session_state.chat = []
if "aprendido" not in st.session_state:
    st.session_state.aprendido = {}  # {palabra_clave: respuesta}
if "modo_ensenar" not in st.session_state:
    st.session_state.modo_ensenar = False

# --- BUSCAR EN INTERNET, NUNCA SE QUEDA CALLADO ---
def buscar_internet(pregunta):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pregunta, max_results=4))
            if resultados:
                texto = ""
                for r in resultados:
                    texto += f"• {r['title']}: {r['body']}\n\n"
                return texto
            return ""
    except:
        return ""

def responder(pregunta_original):
    texto_bajo = pregunta_original.lower()

    # 1. TEMAS ESPECIALES: CLIMA / LLUVIA / DÓLAR
    # Para que siempre tenga respuesta de internet
    if "llover" in texto_bajo or "lluvia" in texto_bajo or "clima" in texto_bajo or "pronostico" in texto_bajo or "pronóstico" in texto_bajo or "tiempo" in texto_bajo:
        info = buscar_internet("clima Monterrey hoy pronóstico lluvia")
        if info:
            return f"Manu, esto dice internet del clima ahorita:\n\n{info}\nSi quieres, dime tu ciudad y te busco el de ahí."
    
    if "dolar" in texto_bajo or "dólar" in texto_bajo or "billete" in texto_bajo:
        info = buscar_internet("precio dólar hoy México")
        if info:
            return f"Manu, esto encontré del dólar hoy:\n\n{info}"
    
    if "hola" in texto_bajo:
        return "Hola Manu! ¿Qué onda? ¿Cómo andas? ¿Qué hacemos hoy, platicamos del clima, del dólar o del taller?"
    if "como estas" in texto_bajo or "cómo estás" in texto_bajo:
        return "Bien Manu, aquí jalando contigo. ¿Y tú cómo andas? ¿Hace calor allá en Monterrey?"
    if "adios" in texto_bajo or "adiós" in texto_bajo:
        return "Nos vemos Manu, cuídate. Aquí te espero para seguir platicando."

    # 2. BUSCA EN LO QUE LE ENSEÑASTE - ASOCIA PALABRAS CLAVES
    # Si una palabra clave de lo que le enseñaste está en tu pregunta, responde eso
    for clave, respuesta_guardada in st.session_state.aprendido.items():
        # Separa la clave en palabras, si alguna coincide, responde
        palabras_clave = clave.lower().split()
        for palabra in palabras_clave:
            if len(palabra) > 3 and palabra in texto_bajo:
                return respuesta_guardada

    # 3. SI NO LO SABE, BUSCA EN INTERNET Y LO APRENDE
    info = buscar_internet(pregunta_original)
    if info:
        # Lo guarda para la próxima vez, así aprende
        st.session_state.aprendido[texto_bajo] = f"Esto encontré en internet, Manu:\n\n{info}"
        return f"Esto encontré en internet, Manu:\n\n{info}\n\nYa lo aprendí, si me vuelves a preguntar lo mismo, ya te lo digo en corto."
    
    # 4. NUNCA SE QUEDA CALLADO
    return "Mmm Manu, no encontré eso en internet ahorita, pero platícame más. ¿De qué ciudad quieres saber? ¿O me lo enseñas? Pícale al botón de Enséñame y me dices qué responder cuando te pregunten eso."

# --- MOSTRAR CHAT LARGO ---
for m in st.session_state.chat:
    if m["quien"] == "tu":
        st.write(f"**Tú:** {m['texto']}")
    else:
        st.write(f"**ManuBot:** {m['texto']}")

st.divider()

# --- CAJA PARA PLATICAR ---
pregunta = st.text_input("Escríbele a ManuBot:", placeholder="Ej: hola, ¿cómo está el día?, ¿va a llover?, ¿cuánto está el dólar?", key="caja_chat")

col1, col2 = st.columns(2)
with col1:
    if st.button("Enviar ➤", use_container_width=True):
        if pregunta.strip() != "":
            st.session_state.chat.append({"quien": "tu", "texto": pregunta})
            respuesta = responder(pregunta)
            st.session_state.chat.append({"quien": "bot", "texto": respuesta})
            st.rerun()

with col2:
    if st.button("📚 Enséñame", use_container_width=True):
        st.session_state.modo_ensenar = not st.session_state.modo_ensenar
        st.rerun()

# --- MODO ENSEÑAR: SALEN 2 BOTONCITOS / CAJITAS ---
if st.session_state.modo_ensenar:
    st.subheader("📚 Modo Enseñar")
    st.write("Aquí me enseñas, Manu. Tú pones la pregunta y la respuesta, y yo asocio las palabras.")
    
    # Botoncito 1: Pregunta
    pregunta_ensenar = st.text_input("1️⃣ Pregunta / Palabra clave:", placeholder="Ej: que es un alternador", key="preg_ens")
    # Botoncito 2: Respuesta
    respuesta_ensenar = st.text_area("2️⃣ Respuesta que debo dar:", placeholder="Ej: El alternador es el que carga la batería, Manu...", key="resp_ens")
    
    if st.button("💾 Guardar lo que me enseñaste"):
        if pregunta_ensenar.strip() != "" and respuesta_ensenar.strip() != "":
            # Guarda la clave completa y también cada palabra clave por separado
            clave = pregunta_ensenar.lower().strip()
            st.session_state.aprendido[clave] = respuesta_ensenar
            st.success(f"¡Listo Manu! Ya aprendí. Cuando me preguntes '{pregunta_ensenar}' te voy a decir lo que me enseñaste.")
            st.session_state.modo_ensenar = False
            st.rerun()
        else:
            st.warning("Llena los dos, Manu. Pregunta y respuesta.")

    if st.button("Cerrar modo enseñar"):
        st.session_state.modo_ensenar = False
        st.rerun()

st.divider()
st.write("**Lo que ya me enseñaste:**")
for k, v in st.session_state.aprendido.items():
    st.write(f"- Si me preguntas **{k}** → te digo: {v[:80]}...")
