# FOTO ARES - Versión Web con Python + Flask
# Para abrir en tu celular
from flask import Flask, render_template_string

app = Flask(__name__)

# Tus perritos
perros = [
    {"nombre": "ARES", "color": "Gris con blanco", "edad": "2 años y medio", "estado": "En casa"},
    {"nombre": "ATENA", "color": "Negro con blanco", "edad": "1 año", "estado": "En casa"},
]

momentos = [
    {"nombre": "Cumpleaños de Ares", "desc": "Celebramos su primer año con pastel.", "fotos": 25, "limite": 25},
    {"nombre": "Primera vez que corrió", "desc": "Corrió 2 km en Parque Fundidora.", "fotos": 25, "limite": 25},
    {"nombre": "Primera vez que huyó", "desc": "Se escapó por la puerta, lo encontramos en 1 hora.", "fotos": 25, "limite": 25},
    {"nombre": "Primera vez en la nieve", "desc": "Jugó en la nieve por primera vez.", "fotos": 25, "limite": 25},
    {"nombre": "Nueva Pestaña - INFINITA ♾️", "desc": "Sin límite de fotos. Fotos ilimitadas.", "fotos": 999, "limite": "♾️"},
]

HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>FOTO ARES</title>
<style>
body{font-family:Arial;background:#111;color:white;margin:0;padding:15px;padding-bottom:80px}
.card{background:white;color:black;border-radius:15px;padding:15px;margin:10px 0}
.btn{display:block;background:#e63946;color:white;text-align:center;padding:13px;border-radius:12px;text-decoration:none;font-weight:bold;margin:8px 0}
.btn-dark{background:#1e293b}.btn-green{background:#16a34a}.btn-gold{background:#facc15;color:black}
.nav{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:12px}
.nav a{color:#111;text-decoration:none;font-weight:bold;font-size:13px}
.badge{background:#e63946;color:white;padding:3px 8px;border-radius:8px;font-size:12px}
img{width:100%;border-radius:12px}
h1{font-size:24px}
</style></head><body>
<h1>🐾 FOTO ARES</h1>

{% if page == 'manada' %}
<h2>Manada</h2><p style="color:#aaa">Tu manada se adapta a ti.</p>
{% for p in perros %}
<div class="card"><img src="https://images.unsplash.com/photo-1605568427561-40e23f9fa5ed?w=800"><h2>{{p.nombre}} <span class="badge">{{p.estado}}</span></h2><p>{{p.color}} - {{p.edad}}</p></div>
{% endfor %}
<div class="card"><b>+ Agregar otro perro</b><br><input style="width:95%;padding:10px;margin:8px 0;border-radius:10px" placeholder="Nombre ej: Luna"><a class="btn btn-dark" href="#">Agregar perro +</a></div>

{% elif page == 'camara' %}
<h2>📸 Cámara</h2>
<div class="card"><img src="https://images.unsplash.com/photo-1605568427561-40e23f9fa5ed?w=800"><h1 style="font-size:32px">92% ES ARES</h1><p>Coincide: ojos azules, mancha en nariz</p><p style="background:#16a34a;color:white;padding:10px;border-radius:10px">✅ FOTO VERIFICADA - Tomada con FOTO ARES</p><p>📍 Parque Fundidora Monterrey, Hoy 13 Nov 2026 12:35 pm<br>Hace 2 min • FOTO FRESCA VE AHORA</p><a class="btn btn-green" href="#">✅ Confirmar Avistamiento</a></div>

{% elif page == 'momentos' %}
<h2>📂 Momentos de Ares</h2>
{% for m in momentos %}
<div class="card"><b>{{m.nombre}}</b><p>{{m.desc}}</p><b>{{m.fotos}} / {{m.limite}} fotos</b><br><a class="btn btn-green" href="#">Agregar Foto +</a><a class="btn btn-dark" href="#">✏️ Cambiar nombre</a></div>
{% endfor %}

{% elif page == 'alerta' %}
<div class="card" style="background:#e63946;color:white;text-align:center"><h1>⚠️ SE BUSCA ARES</h1></div>
<div class="card"><b>Detalles</b><p>🕐 Perdido hace 2 horas<br>📍 Parque Fundidora Monterrey<br>🔵 Collar azul<br>📍 Mapa: Radio 5 km</p></div>
<div class="card"><b>📢 Alerta enviada a 124 vecinos cerca de ti</b><p>Los miembros cercanos han sido notificados ahora</p></div>
<a class="btn" href="#">📢 Activar Alerta para todos</a>
<a class="btn btn-dark" href="#">Compartir Alerta</a>

{% elif page == 'chat' %}
<h2>💬 Chat - Alerta Ares</h2>
<div class="card"><b>@LUNA-2310</b><p>Lo vi cerca de la puerta 4 hace 10 min, husky con collar rojo!</p></div>
<div class="card" style="background:#111;color:white"><b>Tú</b><p>Voy para allá ahora, llevo croquetas</p></div>
<input style="width:95%;padding:12px;border-radius:10px" placeholder="Escribe un mensaje..."><a class="btn btn-dark" href="#">Enviar</a>
{% endif %}

<div class="nav">
<a href="/">Manada</a><a href="/camara">Cámara</a><a href="/momentos">Momentos</a><a href="/alerta">Alerta</a><a href="/chat">Chat</a>
</div>
</body></html>
"""

@app.route('/')
def manada():
    return render_template_string(HTML, page='manada', perros=perros, momentos=momentos)

@app.route('/camara')
def camara():
    return render_template_string(HTML, page='camara', perros=perros, momentos=momentos)

@app.route('/momentos')
def momentos_page():
    return render_template_string(HTML, page='momentos', perros=perros, momentos=momentos)

@app.route('/alerta')
def alerta():
    return render_template_string(HTML, page='alerta', perros=perros, momentos=momentos)

@app.route('/chat')
def chat():
    return render_template_string(HTML, page='chat', perros=perros, momentos=momentos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
"""

**2. Instala Flask y córrelo:**

```bash
pip install flask
python app.py
