from flask import Flask, render_template_string, send_from_directory, request, redirect
import os, json

app = Flask(__name__)
ARCHIVO = "datos.json"

def datos_nuevos():
    return {
        "perros": [
            {"nombre": "Ares", "raza": "Husky", "edad": "2 años"},
            {"nombre": "Luna", "raza": "Husky", "edad": "1 año"},
            {"nombre": "Max", "raza": "Bulldog", "edad": "3 años"},
        ],
        "camara": "Aqui va la camara en vivo de Ares",
        "alerta": "Si Ares se sale, aqui te avisamos",
        "chat": "Bienvenido al Chat de la Manada",
        "momentos": [
            {"titulo": "Ares y Luna en el patio", "fecha": "12 Nov 2026"},
            {"titulo": "Ares banado", "fecha": "10 Nov 2026"},
            {"titulo": "Ares durmiendo", "fecha": "8 Nov 2026"},
        ]
    }

def cargar():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return datos_nuevos()
    return datos_nuevos()

def guardar():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(D, f, ensure_ascii=False)

D = cargar()

HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>FOTO ARES</title>
<style>
body{background:#111;color:#fff;font-family:Arial;text-align:center;padding:15px;margin:0}
a{color:#ffcc00;margin:0 7px;font-weight:bold;text-decoration:none;font-size:17px}
.card{background:#222;padding:12px;border-radius:15px;margin:15px auto;max-width:400px}
.card img{width:100%;height:260px;object-fit:cover;border-radius:12px;background:#444}
input{width:92%;padding:12px;border-radius:10px;border:0;margin:6px 0;background:#333;color:#fff;font-size:15px}
button{background:#ffcc00;border:0;padding:13px 20px;border-radius:10px;font-weight:bold;font-size:16px;margin:6px}
h1{color:#ffcc00}
.box{background:#333;padding:10px;border-radius:10px;margin-top:10px}
label{color:#ffcc00;font-size:13px}
</style></head><body>
<h1>FOTO ARES 🐶</h1>
<a href="/">Manada</a><a href="/camara">Camara</a><a href="/momentos">Momentos</a><a href="/alerta">Alerta</a><a href="/chat">Chat</a>

{% if page == 'manada' %}
<h2>Mi Manada</h2>
<div class="card">
<h3>📸 Foto de Portada</h3>
<form method="POST" action="/subir" enctype="multipart/form-data">
<input type="file" name="foto" accept="image/*" required>
<button type="submit">SUBIR FOTO</button>
</form>
</div>
<form method="POST" action="/guardar_manada">
{% for p in D.perros %}
<div class="card">
<img src="/foto/manada.jpg" onerror="this.onerror=null;this.src='https://images.dog.ceo/breeds/husky/n02110185_14112.jpg'">
<h3>{{ p.nombre }}</h3>
<p>{{ p.raza }} - {{ p.edad }}</p>
<div class="box"><label>✏️ Editar aqui mismo</label>
<input name="n{{ loop.index0 }}" value="{{ p.nombre }}">
<input name="r{{ loop.index0 }}" value="{{ p.raza }}">
<input name="e{{ loop.index0 }}" value="{{ p.edad }}">
</div></div>
{% endfor %}
<button type="submit">💾 GUARDAR MANADA</button>
</form>
{% endif %}

{% if page == 'camara' %}
<h2>Camara</h2>
<div class="card"><img src="/foto/manada.jpg" onerror="this.onerror=null;this.src='https://images.dog.ceo/breeds/husky/n02110185_14112.jpg'"><p>{{ D.camara }}</p>
<form method="POST" action="/guardar_texto"><div class="box"><label>✏️ Editar aqui mismo</label><input name="v" value="{{ D.camara }}"><input type="hidden" name="t" value="camara"><button type="submit">GUARDAR</button></div></form></div>
{% endif %}

{% if page == 'momentos' %}
<h2>Momentos</h2>
<form method="POST" action="/guardar_momentos">
{% for m in D.momentos %}
<div class="card"><img src="/foto/manada.jpg" onerror="this.onerror=null;this.src='https://images.dog.ceo/breeds/husky/n02110185_14112.jpg'"><h3>{{ m.titulo }}</h3><p>{{ m.fecha }}</p>
<div class="box"><label>✏️ Editar aqui mismo</label><input name="t{{ loop.index0 }}" value="{{ m.titulo }}"><input name="f{{ loop.index0 }}" value="{{ m.fecha }}"></div></div>
{% endfor %}
<button type="submit">💾 GUARDAR MOMENTOS</button></form>
{% endif %}

{% if page == 'alerta' %}
<h2>Alerta</h2>
<div class="card"><p>{{ D.alerta }}</p><button onclick="alert('Alerta activada')">Activar Alerta</button>
<form method="POST" action="/guardar_texto"><div class="box"><label>✏️ Editar aqui mismo</label><input name="v" value="{{ D.alerta }}"><input type="hidden" name="t" value="alerta"><button type="submit">GUARDAR</button></div></form></div>
{% endif %}

{% if page == 'chat' %}
<h2>Chat Manada</h2>
<div class="card"><p>{{ D.chat }}</p><input placeholder="Escribe un mensaje..."><br><button>Enviar</button>
<form method="POST" action="/guardar_texto"><div class="box"><label>✏️ Editar aqui mismo</label><input name="v" value="{{ D.chat }}"><input type="hidden" name="t" value="chat"><button type="submit">GUARDAR</button></div></form></div>
{% endif %}
</body></html>
"""

@app.route('/foto/<n>')
def foto(n):
    if os.path.exists(n):
        return send_from_directory('.', n)
    return redirect("https://images.dog.ceo/breeds/husky/n02110185_14112.jpg")

@app.route('/')
def manada():
    return render_template_string(HTML, page='manada', D=D)

@app.route('/camara')
def camara():
    return render_template_string(HTML, page='camara', D=D)

@app.route('/momentos')
def momentos():
    return render_template_string(HTML, page='momentos', D=D)

@app.route('/alerta')
def alerta():
    return render_template_string(HTML, page='alerta', D=D)

@app.route('/chat')
def chat():
    return render_template_string(HTML, page='chat', D=D)

@app.route('/subir', methods=['POST'])
def subir():
    f = request.files.get('foto')
    if f:
        f.save('manada.jpg')
    return redirect('/')

@app.route('/guardar_manada', methods=['POST'])
def gm():
    for i in range(3):
        D['perros'][i]['nombre'] = request.form.get(f'n{i}', D['perros'][i]['nombre'])
        D['perros'][i]['raza'] = request.form.get(f'r{i}', D['perros'][i]['raza'])
        D['perros'][i]['edad'] = request.form.get(f'e{i}', D['perros'][i]['edad'])
    guardar()
    return redirect('/')

@app.route('/guardar_momentos', methods=['POST'])
def gmo():
    for i in range(3):
        D['momentos'][i]['titulo'] = request.form.get(f't{i}', D['momentos'][i]['titulo'])
        D['momentos'][i]['fecha'] = request.form.get(f'f{i}', D['momentos'][i]['fecha'])
    guardar()
    return redirect('/momentos')

@app.route('/guardar_texto', methods=['POST'])
def gt():
    t = request.form.get('t')
    v = request.form.get('v')
    if t == 'camara':
        D['camara'] = v
        guardar()
        return redirect('/camara')
    if t == 'alerta':
        D['alerta'] = v
        guardar()
        return redirect('/alerta')
    if t == 'chat':
        D['chat'] = v
        guardar()
        return redirect('/chat')
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
