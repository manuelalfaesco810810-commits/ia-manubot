from flask import Flask, render_template_string, send_from_directory, request, redirect
import os, json

app = Flask(__name__)
ARCHIVO = "datos.json"

def datos_nuevos():
    return {
        "perros": [
            {"nombre": "Loki", "raza": "Husky", "edad": "2 años", "foto": "https://images.dog.ceo/breeds/husky/n02110185_14112.jpg"},
            {"nombre": "Luna", "raza": "Husky", "edad": "1 año", "foto": "https://images.dog.ceo/breeds/husky/n02110185_10047.jpg"},
            {"nombre": "Ares", "raza": "Husky", "edad": "2 años", "foto": "https://images.dog.ceo/breeds/husky/n02110185_1469.jpg"},
        ],
        "camara": "Camara en vivo de Loki",
        "alerta": "Si Loki se sale, aqui te avisamos",
        "chat": "Bienvenido al Chat de la Manada",
        "momentos": [
            {"titulo": "Loki en el patio", "fecha": "13 Nov 2026"},
            {"titulo": "Loki banado", "fecha": "12 Nov 2026"},
            {"titulo": "Loki durmiendo", "fecha": "11 Nov 2026"},
            {"titulo": "Loki y Luna jugando", "fecha": "10 Nov 2026"},
            {"titulo": "Loki en el campo", "fecha": "9 Nov 2026"},
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
body{background:#0f0f0f;color:#fff;font-family:Arial;text-align:center;padding:0;margin:0;padding-bottom:30px}
.top{background:#1a1a1a;padding:15px;position:sticky;top:0;z-index:10}
.top h1{color:#ffcc00;margin:0;font-size:26px}
.nav a{color:#ffcc00;margin:0 6px;font-weight:bold;text-decoration:none;font-size:14px}
.card{background:#222;padding:12px;border-radius:18px;margin:15px auto;max-width:420px}
.card img{width:100%;height:280px;object-fit:cover;border-radius:14px;background:#444}
.card.grande img{height:340px}
input{width:92%;padding:12px;border-radius:10px;border:0;margin:6px 0;background:#333;color:#fff;font-size:15px}
button{background:#ffcc00;border:0;padding:12px 20px;border-radius:12px;font-weight:bold;font-size:16px;margin:6px}
.btn-mas{background:#ffcc00;color:#000;font-size:28px;width:55px;height:55px;border-radius:50%;line-height:1}
.box{background:#333;padding:10px;border-radius:10px;margin-top:10px}
label{color:#ffcc00;font-size:13px}
.alerta-box{background:#ff2222;padding:20px;border-radius:18px;margin:15px auto;max-width:420px}
.chat-box{background:#222;padding:12px;border-radius:18px;margin:15px auto;max-width:420px;text-align:left}
.msg{background:#333;padding:10px;border-radius:12px;margin:8px 0}
.msg b{color:#ffcc00}
.scroll{max-height:600px;overflow-y:auto;padding:5px}
</style></head><body>
<div class="top"><h1>🐶 FOTO ARES</h1><div class="nav"><a href="/">MANADA</a><a href="/camara">CAMARA</a><a href="/momentos">MOMENTOS</a><a href="/alerta">ALERTA</a><a href="/chat">CHAT</a></div></div>

{% if page == 'manada' %}
<h2>🐾 Mi Manada</h2>
<!-- 1. MANADA - Solo Loki en grande -->
<div class="card grande">
<img src="/foto/manada.jpg" onerror="this.onerror=null;this.src='{{ D.perros[0].foto }}'">
<h2>{{ D.perros[0].nombre }} 🐾</h2>
<p>{{ D.perros[0].raza }} - {{ D.perros[0].edad }}</p>
</div>

<form method="POST" action="/guardar_manada">
{% for p in D.perros %}
<div class="card">
<img src="/foto/manada.jpg" onerror="this.onerror=null;this.src='{{ p.foto }}'">
<h3>{{ p.nombre }}</h3><p>{{ p.raza }} - {{ p.edad }}</p>
<div class="box"><label>✏️ Editar aqui mismo</label>
<input name="n{{ loop.index0 }}" value="{{ p.nombre }}">
<input name="r{{ loop.index0 }}" value="{{ p.raza }}">
<input name="e{{ loop.index0 }}" value="{{ p.edad }}">
</div></div>
{% endfor %}
<button type="submit">💾 GUARDAR MANADA</button>
</form>

<div class="card">
<h3>➕ Agregar Perro</h3>
<form method="POST" action="/agregar_perro">
<input name="nombre" placeholder="Nombre del perro" required>
<input name="raza" placeholder="Raza" required>
<input name="edad" placeholder="Edad ej: 1 año" required>
<button type="submit">+ AGREGAR</button>
</form>
</div>
<div><button class="btn-mas" onclick="window.scrollTo(0,document.body.scrollHeight)">+</button></div>
{% endif %}

{% if page == 'camara' %}
<h2>📸 Camara</h2>
<div class="card grande">
<img src="/foto/manada.jpg" onerror="this.onerror=null;this.src='https://images.dog.ceo/breeds/husky/n02110185_14112.jpg'">
<p>🔴 EN VIVO - {{ D.camara }}</p>
<button onclick="alert('Camara activada')">▶ Ver Camara</button>
<form method="POST" action="/guardar_texto"><div class="box"><label>✏️ Editar aqui mismo</label><input name="v" value="{{ D.camara }}"><input type="hidden" name="t" value="camara"><button type="submit">GUARDAR</button></div></form>
</div>
<div class="card"><h3>📸 Subir Foto de Camara</h3><form method="POST" action="/subir" enctype="multipart/form-data"><input type="file" name="foto" accept="image/*" required><button type="submit">SUBIR FOTO</button></form></div>
{% endif %}

{% if page == 'momentos' %}
<h2>✨ Momentos - Pestaña Infinita</h2>
<div class="scroll">
<form method="POST" action="/guardar_momentos">
{% for m in D.momentos %}
<div class="card"><img src="/foto/manada.jpg" onerror="this.onerror=null;this.src='https://images.dog.ceo/breeds/husky/n02110185_14112.jpg'"><h3>{{ m.titulo }}</h3><p>{{ m.fecha }}</p>
<div class="box"><label>✏️ Editar aqui mismo</label><input name="t{{ loop.index0 }}" value="{{ m.titulo }}"><input name="f{{ loop.index0 }}" value="{{ m.fecha }}"></div></div>
{% endfor %}
<button type="submit">💾 GUARDAR MOMENTOS</button></form>
{% for i in range(5) %}
<div class="card"><img src="https://images.dog.ceo/breeds/husky/n02110185_14112.jpg"><h3>Momento extra {{ i+1 }}</h3><p>Desliza para ver mas...</p></div>
{% endfor %}
<p>⬇️ Sigue bajando, es infinita ⬇️</p>
</div>
{% endif %}

{% if page == 'alerta' %}
<h2>🔴 Alerta</h2>
<div class="alerta-box">
<h1>🚨 ALERTA</h1>
<p style="font-size:18px">{{ D.alerta }}</p>
<button style="background:#fff;color:#ff2222" onclick="alert('¡Alerta enviada a Manu!')">🚨 ACTIVAR ALERTA</button>
</div>
<div class="card"><form method="POST" action="/guardar_texto"><div class="box"><label>✏️ Editar aqui mismo</label><input name="v" value="{{ D.alerta }}"><input type="hidden" name="t" value="alerta"><button type="submit">GUARDAR</button></div></form></div>
{% endif %}

{% if page == 'chat' %}
<h2>💬 Chat Manada</h2>
<div class="chat-box">
<div class="msg"><b>@LUNA-2310:</b> Hola Manu! Loki ya comió 🐶</div>
<div class="msg"><b>@MANU-8472:</b> Perfecto, gracias Luna!</div>
<div class="msg"><b>@LUNA-2310:</b> Está jugando en el patio ahora ✨</div>
<div class="msg"><b>@MANU-8472:</b> Le tomo foto ahorita 📸</div>
<p style="text-align:center;color:#aaa">{{ D.chat }}</p>
<input placeholder="Escribe como @MANU-8472..."><br><center><button>Enviar</button></center>
<form method="POST" action="/guardar_texto"><div class="box"><label>✏️ Editar aqui mismo</label><input name="v" value="{{ D.chat }}"><input type="hidden" name="t" value="chat"><button type="submit">GUARDAR</button></div></form>
</div>
{% endif %}
</body></html>
"""

@app.route('/foto/<n>')
def foto(n):
    if os.path.exists(n):
        return send_from_directory('.', n)
    return redirect("https://images.dog.ceo/breeds/husky/n02110185_14112.jpg")

@app.route('/')
def manada(): return render_template_string(HTML, page='manada', D=D)
@app.route('/camara')
def camara(): return render_template_string(HTML, page='camara', D=D)
@app.route('/momentos')
def momentos(): return render_template_string(HTML, page='momentos', D=D)
@app.route('/alerta')
def alerta(): return render_template_string(HTML, page='alerta', D=D)
@app.route('/chat')
def chat(): return render_template_string(HTML, page='chat', D=D)

@app.route('/subir', methods=['POST'])
def subir():
    f = request.files.get('foto')
    if f: f.save('manada.jpg')
    return redirect('/')

@app.route('/guardar_manada', methods=['POST'])
def gm():
    for i in range(len(D['perros'])):
        D['perros'][i]['nombre'] = request.form.get(f'n{i}', D['perros'][i]['nombre'])
        D['perros'][i]['raza'] = request.form.get(f'r{i}', D['perros'][i]['raza'])
        D['perros'][i]['edad'] = request.form.get(f'e{i}', D['perros'][i]['edad'])
    guardar()
    return redirect('/')

@app.route('/agregar_perro', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    if nombre:
        D['perros'].append({"nombre": nombre, "raza": request.form.get('raza','Husky'), "edad": request.form.get('edad','1 año'), "foto": "https://images.dog.ceo/breeds/husky/n02110185_14112.jpg"})
        guardar()
    return redirect('/')

@app.route('/guardar_momentos', methods=['POST'])
def gmo():
    for i in range(len(D['momentos'])):
        D['momentos'][i]['titulo'] = request.form.get(f't{i}', D['momentos'][i]['titulo'])
        D['momentos'][i]['fecha'] = request.form.get(f'f{i}', D['momentos'][i]['fecha'])
    guardar()
    return redirect('/momentos')

@app.route('/guardar_texto', methods=['POST'])
def gt():
    t = request.form.get('t'); v = request.form.get('v')
    if t == 'camara': D['camara'] = v; guardar(); return redirect('/camara')
    if t == 'alerta': D['alerta'] = v; guardar(); return redirect('/alerta')
    if t == 'chat': D['chat'] = v; guardar(); return redirect('/chat')
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
