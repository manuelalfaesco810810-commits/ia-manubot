import streamlit as st
import json
import os
import requests
import urllib.parse
import re

st.set_page_config(page_title="ManuBot - Con IA Gratis", page_icon="🤖")
st.title("🤖 ManuBot")
st.write("Preguntame lo que sea, lo busco en Internet y te lo explico, Manu.")

# --- BUSCA EN INTERNET ---
def buscar_en_internet(pregunta):
    q = urllib.parse.quote(pregunta)
    contexto = ""
    # Wikipedia
    try:
        url_buscar = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={q}&format=json"
        r = requests.get(url_buscar, timeout=7, headers={"User-Agent": "ManuBot"}).json()
        if r.get("query", {}).get("search"):
            titulo = r["query"]["search"][0]["title"]
            url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(titulo)}"
            r2 = requests.get(url, timeout=7, headers={"User-Agent": "ManuBot"}).json()
            if "extract" in r2:
                contexto += f"Wikipedia - {titulo}: {r2['extract']}\n"
    except: pass
    # DuckDuckGo
    try:
        html = requests.get(f"https://html.duckduckgo.com/html/?q={q}", timeout=8, headers={"User-Agent": "Mozilla/5.0"}).text
        resultados = re.findall(r'class="result__a"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        for titulo, snippet in resultados[:3]:
            titulo = re.sub('<[^>]+>', '', titulo).strip()
            snippet = re.sub('<[^>]+>', '', snippet).strip()
            contexto += f"{titulo}: {snippet}\n"
    except: pass
    return contexto

# --- PREGUNTA A LA IA GRATIS DE GROQ ---
def preguntar_a_ia(pregunta, contexto):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        return None
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        mensaje = f"Eres ManuBot, un asistente amigable de Coahuila, Mexico. Respondes en espanol sencillo, como si le explicaras a tu amigo Manu. Usa esta informacion de Internet para responder tal cual la pregunta.\n\nPregunta de Manu: {pregunta}\n\nInformacion de Internet:\n{contexto}\n\nSi la informacion no es suficiente, responde con lo que sabes como IA, pero siempre responde la pregunta, nunca digas que no sabes."
        data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": mensaje}], "temperature": 0.7, "max_tokens": 800}
        r = requests.post(url, headers=headers, json=data, timeout=25)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"No pude conectar con la IA ahorita, Manu. Pero encontre esto en Internet:\n\n{contexto}"

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

opcion = st.sidebar.radio("Que quieres hacer?", ["Preguntarle", "Ensenarle algo"])

if opcion == "Preguntarle":
    for msg in st.session_state.chat:
        with st.chat_message(msg["rol"]): st.write(msg["texto"])
    pregunta = st.chat_input("Preguntame lo que sea...")
    if pregunta:
        st.session_state.chat.append({"rol": "user", "texto": pregunta})
        with st.chat_message("user"): st.write(pregunta)
        with st.spinner("Buscando en Internet y pensando..."):
            respuesta = None
            for a in st.session_state.aprendizajes:
                if pregunta.lower() in a["pregunta"].lower() or a["pregunta"].lower() in pregunta.lower():
                    respuesta = f"Eso me lo ensenaste tu, Manu:\n\n{a['respuesta']}"
                    break
            if not respuesta:
                contexto = buscar_en_internet(pregunta)
                respuesta_ia = preguntar_a_ia(pregunta, contexto)
                if respuesta_ia:
                    respuesta = respuesta_ia
                elif contexto:
                    respuesta = contexto
                else:
                    respuesta = "No encontre nada, Manu. Intenta de otra forma."
        st.session_state.chat.append({"rol": "assistant", "texto": respuesta})
        with st.chat_message("assistant"): st.write(respuesta)
else:
    preg = st.text_input("Pregunta:")
    resp = st.text_area("Respuesta:")
    if st.button("Ensenarle esto"):
        if preg and resp:
            st.session_state.aprendizajes.append({"pregunta": preg.strip(), "respuesta": resp.strip()})
            guardar(st.session_state.aprendizajes); st.success("Listo! Ya aprendi.")
        else: st.warning("Ponle pregunta Y respuesta.")
