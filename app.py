
import streamlit as st
from ddgs import DDGS

st.set_page_config(page_title="ManuBot", page_icon="🔧")
st.title("🔧 ManuBot")
st.write("Tu compa mecánico. Busco en internet por ti, sin filtros.")

if "aprendido" not in st.session_state:
    st.session_state.aprendido = []

def buscar_internet(pregunta):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pregunta, max_results=6))
            return resultados
    except:
        return []

pregunta = st.text_input("Escribe tu pregunta:", placeholder="Ej: ¿Qué es un alternador?")

if st.button("Preguntar"):
    if pregunta.strip() == "":
        st.warning("Escribe algo primero, Manu.")
    else:
        with st.spinner("Buscando en internet..."):
            encontrado = False
            for dato in st.session_state.aprendido:
                for palabra in pregunta.lower().split():
                    if len(palabra) > 3 and palabra in dato.lower():
                        st.success(f"Esto me lo enseñaste tú, Manu:\n\n{dato}")
                        encontrado = True
                        break
                if encontrado:
                    break
            
            resultados = buscar_internet(pregunta)
            if resultados:
                st.subheader("Esto encontré en Internet:")
                for r in resultados:
                    st.write(f"**{r['title']}**")
                    st.write(r['body'])
                    st.write(f"Fuente: {r['href']}")
                    st.divider()
            else:
                st.error("No encontré nada, Manu. Intenta con otras palabras.")

st.divider()
st.subheader("📚 Enseñarle algo a ManuBot")
nuevo_dato = st.text_area("Escribe lo que quieres que aprenda:", placeholder="Ej: Escribe como hablas en el taller, sin censura...")
if st.button("Enseñarle"):
    if nuevo_dato.strip() != "":
        st.session_state.aprendido.append(nuevo_dato)
        st.success("¡Listo Manu! Ya lo aprendí, así como me lo dijiste.")
        st.write("Lo que ya me enseñaste:")
        for d in st.session_state.aprendido:
            st.write(f"- {d}")
