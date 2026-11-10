import streamlit as st
import json
import os
import difflib
import requests

st.set_page_config(page_title="ManuBot - Aprende de ti", page_icon="🤖")
st.title("🤖 ManuBot")
st.write("Yo se lo que Manu me ensena y lo que hay en Coahuila. Sin Gemini, gratis.")

LUGARES = {
    "nadadores": {"nombre": "Nadadores, Coahuila", "direccion": "Plaza Principal, Centro de Nadadores, Coahuila", "que_hay": "Presidencia Municipal, Plaza Principal, Iglesia, Rio Nadadores", "mapa": "https://www.openstreetmap.org/search?query=Nadadores%20Coahuila"},
    "san buenaventura": {"nombre": "San Buenaventura, Coahuila", "direccion": "Centro de San Buenaventura, Coahuila, Carr. Federal 30", "que_hay": "Presidencia Municipal, Plaza, Banos de Santa Rita, La Cascada", "mapa": "https://www.openstreetmap.org/search?query=San%20Buenaventura%20Coahuila"},
    "monclova": {"nombre": "Monclova, Coahuila", "direccion": "Centro de Monclova, Coahuila, Blvd. Harold R. Pape", "que_hay": "Presidencia Municipal, Plaza Principal, Parque Xochipilli", "mapa": "https://www.openstreetmap.org/search?query=Monclova%20Coahuila"},
}

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
    pregunta = st.chat_input("Escribele algo a ManuBot...")
    if pregunta:
        st.session_state.chat.append({"rol": "user", "texto": pregunta})
        respuesta = None
        for a in st.session_state.aprendizajes:
            if pregunta.lower() in a["pregunta"].lower():
                respuesta = a["respuesta"]; break
        if not respuesta:
            for clave, lugar in LUGARES.items():
                if clave in pregunta.lower():
                    respuesta = f"{lugar['nombre']} - Direccion: {lugar['direccion']} - Que hay: {lugar['que_hay']} - Mapa: {lugar['mapa']}"
                    break
        if not respuesta:
            try:
                url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{pregunta}"
                r = requests.get(url, timeout=5).json()
                if "extract" in r: respuesta = r["extract"]
                else: respuesta = "Eso todavia no me lo has ensenado, Manu."
            except: respuesta = "No pude buscar en Internet ahorita, Manu."
        st.session_state.chat.append({"rol": "assistant", "texto": respuesta})
        with st.chat_message("assistant"): st.write(respuesta)
elif opcion == "Ensenarle algo":
    preg = st.text_input("Pregunta:")
    resp = st.text_area("Respuesta:")
    if st.button("Ensenarle esto"):
        if preg and resp:
            st.session_state.aprendizajes.append({"pregunta": preg.strip(), "respuesta": resp.strip()})
            guardar(st.session_state.aprendizajes); st.success("Listo! Ya aprendi.")
        else: st.warning("Ponle pregunta Y respuesta.")
else:
    for lugar in LUGARES.values():
        st.write(f"**{lugar['nombre']}** - {lugar['direccion']}")
        st.write(f"Que hay: {lugar['que_hay']}")
        st.write(f"[Ver en mapa]({lugar['mapa']})")
