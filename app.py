import sqlite3
import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(
    page_title="IA.ManuBot - Asistente con Memoria",
    page_icon="🤖",
    layout="centered"
)

# Configuración de la API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ Falta configurar la GEMINI_API_KEY en los Secrets de la plataforma.")

# Base de datos local (SQLite)
def init_db():
    conn = sqlite3.connect("memoria_manubot.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qna_aprendidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT,
            respuesta TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def guardar_aprendizaje(pregunta, respuesta):
    conn = sqlite3.connect("memoria_manubot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO qna_aprendidas (pregunta, respuesta) VALUES (?, ?)", (pregunta, respuesta))
    conn.commit()
    conn.close()

def cargar_memoria_bd():
    conn = sqlite3.connect("memoria_manubot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT pregunta, respuesta FROM qna_aprendidas")
    filas = cursor.fetchall()
    conn.close()
    
    conocimiento = "Base de conocimiento aprendida previamente:\n"
    for p, r in filas:
        conocimiento += f"- Usuario preguntó: {p} | ManuBot respondió: {r}\n"
    return conocimiento

# Interfaz visual
st.title("🤖 IA.ManuBot")
st.caption("Tu asistente personal con aprendizaje dinámico y memoria permanente")

with st.sidebar:
    st.header("🧠 Memoria del Bot")
    if st.button("Ver registros guardados"):
        conn = sqlite3.connect("memoria_manubot.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, pregunta, respuesta FROM qna_aprendidas")
        registros = cursor.fetchall()
        conn.close()
        
        if registros:
            for idx, (db_id, p, r) in enumerate(registros, 1):
                st.markdown(f"**[{db_id}] P:** {p}\n\n**R:** {r}")
                if st.button(f"Eliminar #{db_id}", key=f"del_{db_id}"):
                    conn = sqlite3.connect("memoria_manubot.db")
                    c = conn.cursor()
                    c.execute("DELETE FROM qna_aprendidas WHERE id = ?", (db_id,))
                    conn.commit()
                    conn.close()
                    st.rerun()
                st.markdown("---")
        else:
            st.info("Aún no hay registros en la base de datos.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe algo para IA.ManuBot..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    memoria_actual = cargar_memoria_bd()

    prompt_completo = f"""
    Actúa como IA.ManuBot, un asistente personal inteligente y amigable.
    {memoria_actual}
    
    Instrucción: Responde a la consulta actual del usuario de forma natural. Si te está enseñando un nuevo dato, regla o respuesta, asimílalo para integrarlo.
    
    Consulta actual: {prompt}
    """

    try:
        response = model.generate_content(prompt_completo)
        bot_response = response.text
    except Exception as e:
        bot_response = f"Ocurrió un error al procesar tu solicitud: {e}"

    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    guardar_aprendizaje(prompt, bot_response)
