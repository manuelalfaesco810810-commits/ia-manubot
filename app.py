from flask import Flask, render_template_string, send_from_directory, request, redirect
import os
app = Flask(__name__)

# CARATULAS - cada pestaña tiene su propia caratula
caratulas = {
 "manada": {"titulo":"Mi Manada","texto":"Ares, Luna y Max","foto":"manada.jpg"},
 "camara": {"titulo":"Camara en Vivo","texto":"Aqui ves a Togo en vivo","foto":"camara.jpg"},
 "momentos": {"titulo":"Momentos","texto":"Los mejores momentos","foto":"momentos.jpg"},
 "alerta": {"titulo":"Alerta","texto":"Si Togo se sale, aqui te avisamos","foto":"alerta.jpg"},
 "chat": {"titulo":"Chat","texto":"Bienvenido al Chat de Togo","foto":"chat.jpg"},
 "comparar": {"titulo":"Comparar","texto":"Compara a tus perros","foto":"comparar.jpg"},
}

perros = [
 {"nombre":"Togo","raza":"Husky Siberiano","edad":"1 año","peso":"22 kg","foto":"togo.jpg","caracter":"Corre mucho, no se cansa"},
 {"nombre":"Ares","raza":"Husky","edad":"2 años","peso":"25 kg","foto":"ares.jpg","caracter":"Tranquilo, protector"},
 {"nombre":"Luna","raza":"Husky","edad":"1 año","peso":"19 kg","foto":"luna.jpg","caracter":"Juguetona, le gusta la nieve"},
]

momentos = [
 {"titulo":"Togo en el patio","fecha":"12 Nov 2026","foto":"momento1.jpg"},
 {"titulo":"Togo banado","fecha":"10 Nov 2026","foto":"momento2.jpg"},
 {"titulo":"Togo durmiendo","fecha":"8 Nov 2026","foto":"momento3.jpg"},
]

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#111;color:#fff;font-family:Arial;text-align:center;padding:15px}
a{color:#ffcc00;margin:0 6px;font-weight:bold;text-decoration:none;display:inline-block;padding:5px}
.caratula{background:#222;border-radius:20px;padding:15px;margin:15px auto;max-width:420px;border:2px solid #ffcc00}
.caratula img{width:100%;border-radius:15px;height:260px;object-fit:cover}
.card{background:#222;padding:12px;border-radius:15px;margin:15px auto;max-width:420px}
.card img{width:100%;border-radius:12px;height:240px;object-fit:cover}
input,textarea,select{width:92%;padding:11px;border-radius:10px;border:0;margin:5px 0;background:#333;color:#fff}
button{background:#ffcc00;border:0;padding:12px 18px;border-radius:10px;font-weight:bold;margin:5px}
video{width:100%;border-radius:15px;background:#000}
.flex{display:flex;gap:10px;justify-content:center}
.flex .card{flex:1}
</style></head><body>
<h1 style="color:#ffcc00">FOTO TOGO</h1>
<a href="/">Manada</a><a href="/camara">Camara</a><a href="/momentos">Momentos</a><a href="/alerta">Alerta</a><a href="/chat">Chat</a><a href="/comparar">Comparar</a>

<!-- CARATULA DE ESTA PESTAÑA - SE PUEDE CAMBIAR TODO -->
<div class="caratula">
<h2>⭐ CARATULA - {{page.upper()}}</h2>
<img src="/foto/{{caratula.foto}}">
<h2>{{caratula.titulo}}</h2><p>{{caratula.texto}}</p>
<form method="POST" action="/guardar_caratula" enctype="multipart/form-data">
<input name="titulo" value="{{caratula.titulo}}" placeholder="Titulo de la caratula">
<textarea name="texto">{{caratula.texto}}</textarea>
<p>Cambiar foto de la caratula:</p><input type="file" name="foto">
<input type="hidden" name="pagina" value="{{page}}">
<button>GUARDAR CARATULA</button></form></div>

{% if page=='manada' %}
<h2>Mi Manada - Cambia todo aqui</h2>
{% for p in perros %}<div class="card"><img src="/foto/{{p.foto}}"><h3>{{p.nombre}}</h3><p>{{p.raza}} - {{p.edad}} - {{p.peso}}</p><p>{{p.caracter}}</p>
<form method="POST" action="/guardar_perro" enctype="multipart/form-data">
<input name="nombre" value="{{p.nombre}}"><input name="raza" value="{{p.raza}}"><input name="edad" value="{{p.edad}}"><input name="peso" value="{{p.peso}}"><input name="caracter" value="{{p.caracter}}">
<input type="file" name="foto"><input type="hidden" name="i" value="{{loop.index0}}"><button>GUARDAR {{p.nombre}}</button></form></div>{% endfor %}
{% endif %}

{% if page=='camara' %}
<h2>Camara Activada</h2>
<div class="card"><video id="v" autoplay playsinline></video><br>
<button onclick="prender()">PRENDER CAMARA</button>
<button onclick="tomar()">TOMAR FOTO</button><canvas id="c" style="display:none"></canvas>
<p id="msg">Picale PRENDER CAMARA y te va a pedir permiso</p>
<form method="POST" action="/guardar_caratula" enctype="multipart/form-data"><input name="titulo" value="{{caratula.titulo}}"><textarea name="texto">{{caratula.texto}}</textarea><input type="hidden" name="pagina" value="camara"><button>GUARDAR TEXTO CAMARA</button></form></div>
<script>
async function prender(){try{let s=await navigator.mediaDevices.getUserMedia({video:true});document.getElementById('v').srcObject=s;document.getElementById('msg').innerText='Camara prendida - Aqui esta Togo en vivo';}catch(e){document.getElementById('msg').innerText='No dio permiso, dale permitir a la camara';}}
function tomar(){let v=document.getElementById('v');let c=document.getElementById('c');c.width=v.videoWidth;c.height=v.videoHeight;c.getContext('2d').drawImage(v,0,0);let a=document.createElement('a');a.download='togo.jpg';a.href=c.toDataURL('image/jpeg');a.click();}
</script>
{% endif %}

{% if page=='momentos' %}
<h2>Momentos - Cambia todo</h2>
{% for m in momentos %}<div class="card"><img src="/foto/{{m.foto}}"><h3>{{m.titulo}}</h3><p>{{m.fecha}}</p>
<form method="POST" action="/guardar_momento" enctype="multipart/form-data"><input name="titulo" value="{{m.titulo}}"><input name="fecha" value="{{m.fecha}}"><input type="file" name="foto"><input type="hidden" name="i" value="{{loop.index0}}"><button>GUARDAR MOMENTO</button></form></div>{% endfor %}
{% endif %}

{% if page=='comparar' %}
<h2>Comparar - Elige 2 perros</h2>
<form method="GET" action="/comparar"><select name="a">{% for p in perros %}<option value="{{loop.index0}}">{{p.nombre}}</option>{% endfor %}</select>
<select name="b">{% for p in perros %}<option value="{{loop.index0}}">{{p.nombre}}</option>{% endfor %}</select><button>COMPARAR</button></form>
<div class="flex"><div class="card"><img src="/foto/{{pa.foto}}"><h3>{{pa.nombre}}</h3><p>{{pa.raza}}</p><p>Edad: {{pa.edad}}</p><p>Peso: {{pa.peso}}</p><p>{{pa.caracter}}</p></div>
<div class="card"><img src="/foto/{{pb.foto}}"><h3>{{pb.nombre}}</h3><p>{{pb.raza}}</p><p>Edad: {{pb.edad}}</p><p>Peso: {{pb.peso}}</p><p>{{pb.caracter}}</p></div></div>
{% endif %}

{% if page=='alerta' %}<div class="card"><h2>Alerta</h2><p>{{caratula.texto}}</p><form method="POST" action="/guardar_caratula" enctype="multipart/form-data"><input name="titulo" value="{{caratula.titulo}}"><textarea name="texto">{{caratula.texto}}</textarea><input type="file" name="foto"><input type="hidden" name="pagina" value="alerta"><button>GUARDAR ALERTA</button></form></div>{% endif %}
{% if page=='chat' %}<div class="card"><h2>Chat</h2><p>{{caratula.texto}}</p><form method="POST" action="/guardar_caratula" enctype="multipart/form-data"><input name="titulo" value="{{caratula.titulo}}"><textarea name="texto">{{caratula.texto}}</textarea><input type="file" name="foto"><input type="hidden" name="pagina" value="chat"><button>GUARDAR CHAT</button></form></div>{% endif %}
</body></html>
"""

@app.route('/foto/<n>')
def foto(n):
    try: return send_from_directory('.', n)
    except: return send_from_directory('.', 'manada.jpg')
@app.route('/')
def a(): return render_template_string(HTML, page='manada', caratula=caratulas['manada'], perros=perros, momentos=momentos)
@app.route('/camara')
def b(): return render_template_string(HTML, page='camara', caratula=caratulas['camara'], perros=perros, momentos=momentos)
@app.route('/momentos')
def c(): return render_template_string(HTML, page='momentos', caratula=caratulas['momentos'], perros=perros, momentos=momentos)
@app.route('/alerta')
def d(): return render_template_string(HTML, page='alerta', caratula=caratulas['alerta'], perros=perros, momentos=momentos)
@app.route('/chat')
def e(): return render_template_string(HTML, page='chat', caratula=caratulas['chat'], perros=perros, momentos=momentos)
@app.route('/comparar')
def f():
    ai=int(request.args.get('a',0)); bi=int(request.args.get('b',1))
    return render_template_string(HTML, page='comparar', caratula=caratulas['comparar'], perros=perros, momentos=momentos, pa=perros[ai], pb=perros[bi])

@app.route('/guardar_caratula', methods=['POST'])
def gc():
    pag=request.form.get('pagina'); caratulas[pag]['titulo']=request.form.get('titulo'); caratulas[pag]['texto']=request.form.get('texto')
    f=request.files.get('foto')
    if f and f.filename: f.save(caratulas[pag]['foto'])
    return redirect('/'+pag if pag!='manada' else '/')
@app.route('/guardar_perro', methods=['POST'])
def gp():
    i=int(request.form.get('i')); perros[i]['nombre']=request.form.get('nombre'); perros[i]['raza']=request.form.get('raza'); perros[i]['edad']=request.form.get('edad'); perros[i]['peso']=request.form.get('peso'); perros[i]['caracter']=request.form.get('caracter')
    f=request.files.get('foto')
    if f and f.filename: f.save(perros[i]['foto'])
    return redirect('/')
@app.route('/guardar_momento', methods=['POST'])
def gmo():
    i=int(request.form.get('i')); momentos[i]['titulo']=request.form.get('titulo'); momentos[i]['fecha']=request.form.get('fecha')
    f=request.files.get('foto')
    if f and f.filename: f.save(momentos[i]['foto'])
    return redirect('/momentos')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
