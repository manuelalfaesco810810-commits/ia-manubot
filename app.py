import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="ManuBot", page_icon="🤖")
st.title("🤖 ManuBot")
st.write("Pregúntame lo que quieras, de mecánica o de lo que sea.")

# --- Clave de Groq ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
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

menu = st.sidebar.selectbox("Menú", ["Preguntarle", "Enseñarle algo"])

if menu == "Enseñarle algo":
    st.header("Enseñarle algo nuevo")
    p = st.text_input("Pregunta")
    r = st.text_area("Respuesta")
    if st.button("Enseñar"):
        if p and r:
            st.session_state.datos[p.lower().strip()] = r
            guardar(st.session_state.datos)
            st.success("¡Ya aprendí!")
        else:
            st.warning("Escribe pregunta y respuesta")

else:
    st.header("Pregúntale")
    pregunta = st.text_input("Escribe tu pregunta aquí")
    if st.button("Preguntar"):
        if pregunta:
            clave = pregunta.lower().strip()
            # 1. Primero busca lo que tú le enseñaste
            if clave in st.session_state.datos:
                st.success(st.session_state.datos[clave])
            # 2. Si no lo sabe, pregunta a Groq
            elif GROQ_KEY == "":
                st.error("Falta poner la clave de Groq en Secrets. GROQ_API_KEY")
            else:
                with st.spinner("Pensando..."):
                    try:
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
                        data = {
                            "model": "llama-3.3-70b-versatile",
                            "messages": [
                                {"role": "system", "content": "Eres ManuBot, un asistente experto en mecánica automotriz y en todo. Explica fácil, en español, como si le hablaras a un amigo mecánico."},
                                {"role": "user", "content": pregunta}
                            ]
                        }
                        resp = requests.post(url, headers=headers, json=data, timeout=30)
                        respuesta = resp.json()["choices"][0]["message"]["content"]
                        st.success(respuesta)
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.warning("Escribe una pregunta")
