from flask import Flask, render_template_string, send_from_directory, request, redirect
import os

app = Flask(__name__)

datos = {
    "titulo": "FOTO ARES",
    "texto_camara": "Aqui va la camara en vivo de Ares",
    "texto_alerta": "Si Ares se sale, aqui te avisamos",
    "texto_chat": "Bienvenido al Chat de la Manada",
}

perros = [
    {"nombre": "Ares", "raza": "Husky", "edad": "2 años", "foto": "/foto/manada.jpg"},
    {"nombre": "Luna", "raza": "Husky", "edad": "1 año", "foto": "/foto/manada.jpg"},
    {"nombre": "Max", "raza": "Bulldog", "edad": "3 años", "foto": "/foto/manada.jpg"},
]

momentos = [
    {"titulo": "Ares y Luna en el patio", "fecha": "12 Nov 2026", "foto": "/foto/manada.jpg"},
    {"titulo": "Ares bañado", "fecha": "10 Nov 2026", "foto": "/foto/manada.jpg"},
    {"titulo": "Ares durmiendo", "fecha": "8 Nov 2026", "foto": "/foto/manada.jpg"},
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
.nav a{color:#ffcc00;text-decoration:none;margin:0 8px;font-weight:bold;font-size:17px}
.card{background:#222;padding:10px;border-radius:15px;margin:15px auto;max-width:400px;overflow:hidden}
.card img{width:100%;border-radius:12px;height:260px;object-fit:cover}
h1{color:#ffcc00}
button{background:#ffcc00;border:0;padding:12px 20px;border-radius:10px;font-weight:bold;font-size:16px;margin:5px}
input{width:90%;padding:12px;border-radius:10px;border:0;margin:6px 0;background:#333;color:#fff}
.editar-btn{background:#fff;color:#000;padding:8px 15px;border-radius:20px;text-decoration:none;font-weight:bold;display:inline-block;margin-bottom:10px}
label{color:#ffcc00;font-size:13px}
</style>
</head>
<body>
<h1>{{ datos.titulo }} 🐶</h1>
<a class="editar-btn" href="/editar">⚙️ Editar Todo</a>
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
<div class="card">
<img src="{{ p.foto }}?v=1" onerror="this.src='https://images.dog.ceo/breeds/husky/n02110185_14112.jpg'">
<h3>{{ p.nombre }}</h3>
<p>{{ p.raza }} - {{ p.edad }}</p>
</div>
{% endfor %}
{% endif %}

{% if page == 'camara' %}
<h2>Camara</h2>
<div class="card"><img src="/foto/manada.jpg"><p>{{ datos.texto_camara }}</p></div>
{% endif %}

{% if page == 'momentos' %}
<h2>Momentos</h2>
{% for m in momentos %}
<div class="card">
<img src="{{ m.foto }}">
<h3>{{ m.titulo }}</h3>
<p>{{ m.fecha }}</p>
</div>
{% endfor %}
{% endif %}

{% if page == 'alerta' %}
<h2>Alerta</h2>
<div class="card"><p>{{ datos.texto_alerta }}</p><button>Activar Alerta</button></div>
{% endif %}

{% if page == 'chat' %}
<h2>Chat Manada</h2>
<div class="card"><p>{{ datos.texto_chat }}</p><input placeholder="Escribe un mensaje..."><br><button>Enviar</button></div>
{% endif %}

{% if page == 'editar' %}
<h2>⚙️ Editar Todo</h2>

<h3>📸 Subir Foto de Portada / Manada</h3>
<div class="card">
<p>Elige la foto de tus Huskys desde tu celular o compu</p>
<form method="POST" action="/subir_foto" enctype="multipart/form-data">
<input type="file" name="foto" accept="image/*" required>
<br><button type="submit">📸 SUBIR FOTO</button>
</form>
<p style="font-size:12px;color:#aaa">Después de subirla, recarga la página de Manada</p>
</div>

<form method="POST" action="/guardar">
<div class="card">
<label>TITULO DE LA APP</label><br>
<input name="titulo" value="{{ datos.titulo }}">
<label>TEXTO CAMARA</label><br>
<input name="texto_camara" value="{{ datos.texto_camara }}">
<label>TEXTO ALERTA</label><br>
<input name="texto_alerta" value="{{ datos.texto_alerta }}">
<label>TEXTO CHAT</label><br>
<input name="texto_chat" value="{{ datos.texto_chat }}">
</div>
<h3>Manada - Perro 1</h3>
<div class="card">
<input name="p0_nombre" value="{{ perros[0].nombre }}">
<input name="p0_raza" value="{{ perros[0].raza }}">
<input name="p0_edad" value="{{ perros[0].edad }}">
</div>
<h3>Manada - Perro 2</h3>
<div class="card">
<input name="p1_nombre" value="{{ perros[1].nombre }}">
<input name="p1_raza" value="{{ perros[1].raza }}">
<input name="p1_edad" value="{{ perros[1].edad }}">
</div>
<h3>Manada - Perro 3</h3>
<div class="card">
<input name="p2_nombre" value="{{ perros[2].nombre }}">
<input name="p2_raza" value="{{ perros[2].raza }}">
<input name="p2_edad" value="{{ perros[2].edad }}">
</div>
<h3>Momentos - 1</h3>
<div class="card">
<input name="m0_titulo" value="{{ momentos[0].titulo }}">
<input name="m0_fecha" value="{{ momentos[0].fecha }}">
</div>
<h3>Momentos - 2</h3>
<div class="card">
<input name="m1_titulo" value="{{ momentos[1].titulo }}">
<input name="m1_fecha" value="{{ momentos[1].fecha }}">
</div>
<h3>Momentos - 3</h3>
<div class="card">
<input name="m2_titulo" value="{{ momentos[2].titulo }}">
<input name="m2_fecha" value="{{ momentos[2].fecha }}">
</div>
<button type="submit">💾 GUARDAR TODO</button><br><br>
<a href="/" style="color:#fff">Cancelar</a>
</form>
{% endif %}
</body>
</html>
"""

@app.route('/foto/<nombre>')
def foto(nombre):
    return send_from_directory('.', nombre)

@app.route('/')
def manada():
    return render_template_string(HTML, page='manada', perros=perros, momentos=momentos, datos=datos)

@app.route('/camara')
def camara():
    return render_template_string(HTML, page='camara', perros=perros, momentos=momentos, datos=datos)

@app.route('/momentos')
def momentos_page():
    return render_template_string(HTML, page='momentos', perros=perros, momentos=momentos, datos=datos)

@app.route('/alerta')
def alerta():
    return render_template_string(HTML, page='alerta', perros=perros, momentos=momentos, datos=datos)

@app.route('/chat')
def chat():
    return render_template_string(HTML, page='chat', perros=perros, momentos=momentos, datos=datos)

@app.route('/editar')
def editar():
    return render_template_string(HTML, page='editar', perros=perros, momentos=momentos, datos=datos)

@app.route('/subir_foto', methods=['POST'])
def subir_foto():
    f = request.files.get('foto')
    if f:
        f.save('manada.jpg')
    return redirect('/editar')

@app.route('/guardar', methods=['POST'])
def guardar():
    datos['titulo'] = request.form.get('titulo', datos['titulo'])
    datos['texto_camara'] = request.form.get('texto_camara', datos['texto_camara'])
    datos['texto_alerta'] = request.form.get('texto_alerta', datos['texto_alerta'])
    datos['texto_chat'] = request.form.get('texto_chat', datos['texto_chat'])
    for i in range(3):
        perros[i]['nombre'] = request.form.get(f'p{i}_nombre', perros[i]['nombre'])
        perros[i]['raza'] = request.form.get(f'p{i}_raza', perros[i]['raza'])
        perros[i]['edad'] = request.form.get(f'p{i}_edad', perros[i]['edad'])
    for i in range(3):
        momentos[i]['titulo'] = request.form.get(f'm{i}_titulo', momentos[i]['titulo'])
        momentos[i]['fecha'] = request.form.get(f'm{i}_fecha', momentos[i]['fecha'])
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
