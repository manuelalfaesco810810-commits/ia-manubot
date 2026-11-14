from flask import Flask, render_template_string

app = Flask(__name__)

perros = [
    {"nombre": "Ares", "raza": "Pitbull", "edad": "2 años"},
    {"nombre": "Luna", "raza": "Pastor", "edad": "1 año"},
    {"nombre": "Max", "raza": "Bulldog", "edad": "3 años"},
]

momentos = [
    {"titulo": "Ares en el parque", "fecha": "12 Nov 2026"},
    {"titulo": "Ares bañado", "fecha": "10 Nov 2026"},
    {"titulo": "Ares durmiendo", "fecha": "8 Nov 2026"},
]

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FOTO ARES</title>
<style>
body{font-family:Arial;background:#111;color:#fff;margin:0;padding:20px;text-align:center}
.nav a{color:#ffcc00;text-decoration:none;margin:0 10px;font-weight:bold;font-size:18px}
.card{background:#222;padding:15px;border-radius:15px;margin:10px auto;max-width:400px}
h1{color:#ffcc00}
button{background:#ffcc00;border:0;padding:12px 20px;border-radius:10px;font-weight:bold;font-size:16px}
input{width:90%;padding:12px;border-radius:10px;border:0;margin:10px 0}
</style>
</head>
<body>
<h1>FOTO ARES</h1>
<div class="nav">
<a href="/">Manada</a>
<a href="/camara">Camara</a>
<a href="/momentos">Momentos</a>
<a href="/alerta">Alerta</a>
<a href="/chat">Chat</a>
</div>
{% if page == 'manada' %}
<h2>Mi Manada</h2>
{% for p in perros %}
<div class="card"><h3>{{ p.nombre }}</h3><p>{{ p.raza }} - {{ p.edad }}</p></div>
{% endfor %}
{% endif %}
{% if page == 'camara' %}
<h2>Camara</h2>
<div class="card"><p>Aqui va la camara en vivo de Ares</p></div>
{% endif %}
{% if page == 'momentos' %}
<h2>Momentos</h2>
{% for m in momentos %}
<div class="card"><h3>{{ m.titulo }}</h3><p>{{ m.fecha }}</p></div>
{% endfor %}
{% endif %}
{% if page == 'alerta' %}
<h2>Alerta</h2>
<div class="card"><p>Si Ares se sale, aqui te avisamos</p><button>Activar Alerta</button></div>
{% endif %}
{% if page == 'chat' %}
<h2>Chat Manada</h2>
<div class="card"><input placeholder="Escribe un mensaje..."><br><button>Enviar</button></div>
{% endif %}
</body>
</html>
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
