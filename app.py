import streamlit as st
from groq import Groq
from ddgs import DDGS

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="ManuBot", page_icon="🔧")
st.title("🔧 ManuBot")
st.write("Tu compa mecánico. Pregúntame lo que sea del taller.")

# --- CLAVE DE GROQ ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_KEY = ""

if GROQ_KEY == "":
    st.error("Falta poner la clave de Groq en Secrets.")
    st.stop()

cliente = Groq(api_key=GROQ_KEY)

# --- FUNCIÓN PARA BUSCAR EN INTERNET (SIN GROK NI GEMINI) ---
def buscar_internet(pregunta):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pregunta, max_results=5))
            if not resultados:
                return ""
            texto = ""
            for r in resultados:
                texto += f"- {r['title']}: {r['body']} ({r['href']})\n"
            return texto
    except Exception as e:
        return ""

# --- CAJA PARA PREGUNTAR ---
pregunta = st.text_input("Escribe tu pregunta:", placeholder="Ej: ¿Qué es un alternador? ¿Cuánto cuesta un Tsuru?")

if st.button("Preguntar"):
    if pregunta.strip() == "":
        st.warning("Escribe algo primero, Manu.")
    else:
        with st.spinner("Buscando en internet y preguntando..."):
            # 1. Busca en internet
            info_internet = buscar_internet(pregunta)

            # 2. Arma el prompt con esa info
            prompt_final = f"""
            Eres ManuBot, un mecánico experto en México, hablas sencillo como compa de taller.
            El usuario pregunta: {pregunta}

            Información actual de internet:
            {info_internet}

            Responde en español sencillo, paso a paso, sin palabras difíciles.
            Si la info de internet está vacía, responde con lo que sabes de mecánica.
            Al final dame un consejo práctico de taller.
            """

            # 3. Manda a Groq
            try:
                respuesta = cliente.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt_final}],
                    temperature=0.7,
                    max_tokens=1000
                )
                st.success(respuesta.choices[0].message.content)
                
                if info_internet:
                    with st.expander("Ver lo que encontré en internet"):
                        st.write(info_internet)
            except Exception as e:
                st.error(f"Error con Groq: {e}")
