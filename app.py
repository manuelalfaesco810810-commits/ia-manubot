import streamlit as st
import json
import os
import requests
import urllib.parse

st.set_page_config(page_title="ManuBot - Busca en Internet", page_icon="🤖")
st.title("🤖 ManuBot")
st.write("Si no lo se, lo busco en Internet por ti, Manu. Sin Gemini, gratis.")

# --- TUS LUGARES DE COAHUILA ---
LUGARES = {
    "nadadores": "Nadadores, Coahuila - Direccion: Plaza Principal, Centro de Nadadores - Que hay: Presidencia, Plaza, Iglesia, Rio Nadadores - Mapa: https://www.openstreetmap.org/search?query=Nadadores%20Coahuila",
    "san buenaventura": "San Buenaventura, Coahuila - Direccion: Centro, Carr. Federal 30 - Que hay: Presidencia, Plaza, Banos de Santa Rita, La Cascada - Mapa: https://www.openstreetmap.org/search?query=San%20Buenaventura%20Coahuila",
    "monclova": "Monclova, Coahuila - Direccion: Centro, Blvd. Harold R. Pape - Que hay: Presidencia, Plaza Principal, Parque Xochipilli - Mapa: https://www.openstreetmap.org/search?query=Monclova%20Coahuila",
}

def buscar_en_internet(pregunta):
    q = urllib.parse.quote(pregunta)
    # 1. Intenta en Wikipedia
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{q}"
        r = requests.get(url, timeout=6, headers={"User-Agent": "ManuBot"}).json()
        if "extract" in r and r["extract"]:
            return f"Segun Wikipedia:\n\n{r['extract']}\n\nFuente: {r.get('content_urls', {}).get('desktop', {}).get('page', '')}"
    except:
        pass
    # 2. Intenta en DuckDuckGo - busca en todo Internet
    try:
        url2 = f"https://api.duckduckgo.com/?q={q}&format=json&no_html=1&skip_disambig=1"
        r2 = requests.get(url2, timeout=6, headers={"User-Agent": "ManuBot"}).json()
        if r2.get("AbstractText"):
            return f"Encontre en Internet:\n\n{r2['AbstractText']}\n\nFuente: {r2.get('AbstractURL', '')}"
        if r2.get("RelatedTopics"):
            for t in r2["RelatedTopics"]:
                if isinstance(t, dict) and t.get("Text"):
                    return f"Encontre en Internet:\n\n{t['Text']}\n\nFuente: {t.get('FirstURL', '')}"
    except:
        pass
    # 3. Intenta buscar direccion / lugar en OpenStreetMap
    try:
        url3 = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
        r3 = requests.get(url3, timeout=6, headers={"User-Agent": "ManuBot"}).json()
        if r3:
            return f"Encontre este lugar en el mapa:\n\n{r3[0]['display_name']}\n\nVer mapa: https://www.openstreetmap.org/?mlat={r3[0]['lat']}&mlon={r3[0]['lon']}"
    except:
        pass
    return None

ARCHIVO = "aprendizajes.json"
def cargar():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []
def guardar(lista):
    with open(ARCHIVO, "w", encoding="utf-8") as f: json.dump(lista, f, ensure_ascii=False, indent=2)

if "aprendizajes" not in st.session_state: st.session_state.aprendizajes = cargar()
if "chat" not in st.session_state: st.session_state.chat = []

opcion = st.sidebar.radio("Que quieres hacer?", ["Preguntarle", "Ensenarle algo", "Lugares de Coahuila"])

if opcion == "Preguntarle":
    for msg in st.session_state.chat:
        with st.chat_message(msg["rol"]): st.write(msg["texto"])
    pregunta = st.chat_input("Preguntame lo que sea...")
    if pregunta:
        st.session_state.chat.append({"rol": "user", "texto": pregunta})
        with st.chat_message("user"): st.write(pregunta)
        with st.spinner("Buscando en Internet..."):
            respuesta = None
            # 1. Primero lo que tu le ensenaste
            for a in st.session_state.aprendizajes:
                if pregunta.lower() in a["pregunta"].lower() or a["pregunta"].lower() in pregunta.lower():
                    respuesta = f"Eso me lo ensenaste tu, Manu:\n\n{a['respuesta']}"
                    break
            # 2. Luego tus lugares de Coahuila
            if not respuesta:
                for clave, texto in LUGARES.items():
                    if clave in pregunta.lower():
                        respuesta = texto
                        break
            # 3. Si no lo sabe, lo investiga en Internet
            if not respuesta:
                encontrada = buscar_en_internet(pregunta)
                if encontrada:
                    respuesta = encontrada
                else:
                    respuesta = "Busque en Internet y no encontre nada claro, Manu. Ensenamelo tu en 'Ensenarle algo' y ya me lo aprendo."
        st.session_state.chat.append({"rol": "assistant", "texto": respuesta})
        with st.chat_message("assistant"): st.write(respuesta)

elif opcion == "Ensenarle algo":
    preg = st.text_input("Pregunta:")
    resp = st.text_area("Respuesta:")
    if st.button("Ensenarle esto"):
        if preg and resp:
            st.session_state.aprendizajes.append({"pregunta": preg.strip(), "respuesta": resp.strip()})
            guardar(st.session_state.aprendizajes); st.success("Listo! Ya aprendi.")
            st.balloons()
        else: st.warning("Ponle pregunta Y respuesta.")
else:
    for texto in LUGARES.values():
        st.write(texto)
        st.write("---")
