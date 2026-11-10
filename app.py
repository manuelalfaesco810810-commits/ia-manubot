import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="ManuBot", page_icon="🤖")
st.title("🤖 ManuBot")
st.write("Preguntame lo que quieras, de mecanica o de lo que sea.")

try:
    GROQ_KEY = st.secrets["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"]
except:
    GROQ_KEY = ""

ARCHIVO = "aprendizajes.json"

def cargar():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

if "datos" not in st.session_state:
    st.session_state.datos = cargar()

menu = st.sidebar.selectbox("Menu", ["Preguntarle", "Ensenarle algo"])

if menu == "Ensenarle algo":
    st.header("Ensenarle algo nuevo")
    p = st.text_input("Pregunta")
    r = st.text_area("Respuesta")
    if st.button("Ensenar"):
        if p and r:
            st.session_state.datos[p.lower().strip()] = r
            guardar(st.session_state.datos)
            st.success("Ya aprendi!")
        else:
            st.warning("Escribe pregunta y respuesta")
else:
    st.header("Preguntale")
    pregunta = st.text_input("Escribe tu pregunta aqui")
    if st.button("Preguntar"):
        if pregunta:
            clave = pregunta.lower().strip()
            if clave in st.session_state.datos:
                st.success(st.session_state.datos[clave])
            elif GROQ_KEY == "":
                st.error("Falta poner la clave de Groq en Secrets.")
            else:
                with st.spinner("Pensando..."):
                    try:
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
                        data = {
                            "model": "llama-3.1-8b-instant",
                            "messages": [
                                {"role": "system", "content": "Eres ManuBot, un asistente experto en mecanica automotriz y en todo. Explica facil, en espanol."},
                                {"role": "user", "content": pregunta}
                            ]
                        }
                        resp = requests.post(url, headers=headers, json=data, timeout=30)
                        datos_resp = resp.json()
                        if "choices" not in datos_resp:
                            st.error(f"Groq dijo: {datos_resp}")
                        else:
                            st.success(datos_resp["choices"][0]["message"]["content"])
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.warning("Escribe una pregunta")
