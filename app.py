# ============================================================
# MANUBOT - APRENDE DE LO QUE TÚ LE ENSEÑAS
# INSTRUCCIONES:
# 1. Este código NO usa Gemini, NO usa llave, NO gasta créditos.
# 2. Es 100% GRATIS. GitHub + Streamlit son gratis.
# 3. Para ENSEÑARLE: Entra a la app, menú de la izquierda
#    -> "Enseñarle algo" -> Escribe pregunta y respuesta -> Botón Enseñar.
# 4. Para PREGUNTARLE: Menú -> "Preguntarle" -> Escribe tu pregunta.
# 5. Para EDITAR ESTE CÓDIGO: Solo en GitHub, en el navegador,
#    no necesitas ninguna app de paga.
# ============================================================

import streamlit as st
import json
import os
import difflib

st.set_page_config(page_title="ManuBot - Aprende de ti", page_icon="🤖")

st.title("🤖 ManuBot")
st.write("Yo solo sé lo que Manu me enseña. Sin Gemini, sin créditos, sin pagar nada.")

ARCHIVO = "aprendizajes.json"

# --- Cargar lo que ya sabe ---
def cargar():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# --- Guardar lo nuevo ---
def guardar(lista):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

if "aprendizajes" not in st.session_state:
    st.session_state.aprendizajes = cargar()

if "chat" not in st.session_state:
    st.session_state.chat = []

# --- INSTRUCCIONES VISIBLES EN LA APP ---
with st.expander("📖 INSTRUCCIONES - Léeme primero, Manu"):
    st.write("""
    **¿Cómo le enseño?**
    1. En el menú de la izquierda dale a '📚 Enseñarle algo'
    2. Escribe la pregunta y la respuesta que quieres que aprenda
    3. Dale al botón 'Enseñarle esto'

    **¿Cómo le pregunto?**
    1. Dale a '💬 Preguntarle'
    2. Escríbele abajo y te contesta con lo que le enseñaste

    **¿Esto cuesta?**
    NO. No usa Gemini, no usa llave, no usa créditos. Es gratis.
    """)

# --- Menú ---
opcion = st.sidebar.radio("¿Qué quieres hacer?", ["💬 Preguntarle", "📚 Enseñarle algo", "🧠 Ver lo que ya sabe"])

# ========== 1. PREGUNTARLE ==========
if opcion == "💬 Preguntarle":
    st.subheader("Pregúntame algo")

    for msg in st.session_state.chat:
        with st.chat_message(msg["rol"]):
            st.write(msg["texto"])

    pregunta = st.chat_input("Escríbele algo a ManuBot...")
    if pregunta:
        st.session_state.chat.append({"rol": "user", "texto": pregunta})
        with st.chat_message("user"):
            st.write(pregunta)

        respuesta = None
        preguntas_guardadas = [a["pregunta"] for a in st.session_state.aprendizajes]
        parecida = difflib.get_close_matches(pregunta.lower(), [p.lower() for p in preguntas_guardadas], n=1, cutoff=0.5)

        if parecida:
            for a in st.session_state.aprendizajes:
                if a["pregunta"].lower() == parecida[0]:
                    respuesta = a["respuesta"]
                    break
        else:
            for a in st.session_state.aprendizajes:
                if any(palabra in a["pregunta"].lower() for palabra in pregunta.lower().split() if len(palabra) > 3):
                    respuesta = a["respuesta"]
                    break

        if not respuesta:
            respuesta = "Eso todavía no me lo has enseñado, Manu. Ve a 'Enseñarle algo' y enséñamelo y ya lo aprendo."

        st.session_state.chat.append({"rol": "assistant", "texto": respuesta})
        with st.chat_message("assistant"):
            st.write(respuesta)

# ========== 2. ENSEÑARLE ==========
elif opcion == "📚 Enseñarle algo":
    st.subheader("Enséñale algo nuevo a ManuBot")
    st.write("INSTRUCCIÓN: Tú le pones la pregunta y la respuesta, y él ya no se le olvida.")

    preg = st.text_input("1. Pregunta que le pueden hacer:")
    resp = st.text_area("2. Respuesta que debe dar:")

    if st.button("✅ Enseñarle esto"):
        if preg and resp:
            st.session_state.aprendizajes.append({"pregunta": preg.strip(), "respuesta": resp.strip()})
            guardar(st.session_state.aprendizajes)
            st.success(f"¡Listo! Ya aprendí que cuando me pregunten '{preg}' debo contestar eso.")
            st.balloons()
        else:
            st.warning("Manu, ponle pregunta Y respuesta.")

# ========== 3. VER LO QUE SABE ==========
else:
    st.subheader(f"Ya me has enseñado {len(st.session_state.aprendizajes)} cosas:")
    for i, a in enumerate(st.session_state.aprendizajes):
        st.write(f"**{i+1}. P:** {a['pregunta']}")
        st.write(f"**R:** {a['respuesta']}")
        st.write("---")
    if st.button("🗑️ Borrar todo lo aprendido"):
        st.session_state.aprendizajes = []
        guardar([])
        st.rerun()
