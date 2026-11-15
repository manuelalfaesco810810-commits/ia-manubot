from flask import Flask, render_template_string, send_from_directory, request, redirect
app = Flask(__name__)

datos = {"camara":"Aqui va la camara de Ares","alerta":"Si Ares se sale, aqui te avisamos","chat":"Bienvenido al Chat"}

perros = [
 {"nombre":"Ares","raza":"Husky","edad":"2 años"},
 {"nombre":"Luna","raza":"Husky","edad":"1 año"},
 {"nombre":"Max","raza":"Bulldog","edad":"3 años"},
]
momentos = [
 {"titulo":"Ares y Luna en el patio","fecha":"12 Nov 2026"},
 {"titulo":"Ares banado","fecha":"10 Nov 2026"},
 {"titulo":"Ares durmiendo","fecha":"8 Nov 2026"},
]

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{background:#111;color:#fff;font-family:Arial;text-align:center;padding:20px}
a{color:#ffcc00;margin:0 8px;font-weight:bold;text-decoration:none}
.card{background:#222;padding:12px;border-radius:15px;margin:15px auto;max-width:400px}
.card img{width:100%;border-radius:12px;height:260px;object-fit:cover}
input{width:90%;padding:12px;border-radius:10px;border:0;margin:6px 0;background:#333;color:#fff}
button{background:#ffcc00;border:0;padding:12px 20px;border-radius:10px;font-weight:bold}
</style></head><body>
<h1 style="color:#ffcc00">FOTO ARES</h1>
<a href="/">Manada</a><a href="/camara">Camara</a><a href="/momentos">Momentos</a><a href="/alerta">Alerta</a><a href="/chat">Chat</a>
{% if page=='manada' %}
<h2>Mi Manada</h2>
<div class="card"><h3>Subir Foto</h3><form method="POST" action="/subir" enctype="multipart/form-data"><input type="file" name="foto" required><button>SUBIR FOTO</button></form></div>
<form method="POST" action="/guardar_manada">
{% for p in perros %}<div class="card"><img src="/foto/manada.jpg"><h3>{{p.nombre}}</h3><p>{{p.raza}} - {{p.edad}}</p><input name="n{{loop.index0}}" value="{{p.nombre}}"><input name="r{{loop.index0}}" value="{{p.raza}}"><input name="e{{loop.index0}}" value="{{p.edad}}"></div>{% endfor %}
<button>GUARDAR MANADA</button></form>
{% endif %}
{% if page=='camara' %}<h2>Camara</h2><div class="card"><img src="/foto/manada.jpg"><p>{{datos.camara}}</p><form method="POST" action="/guardar_texto"><input name="v" value="{{datos.camara}}"><input type="hidden" name="t" value="camara"><button>GUARDAR</button></form></div>{% endif %}
{% if page=='momentos' %}<h2>Momentos</h2><form method="POST" action="/guardar_momentos">{% for m in momentos %}<div class="card"><img src="/foto/manada.jpg"><h3>{{m.titulo}}</h3><p>{{m.fecha}}</p><input name="t{{loop.index0}}" value="{{m.titulo}}"><input name="f{{loop.index0}}" value="{{m.fecha}}"></div>{% endfor %}<button>GUARDAR MOMENTOS</button></form>{% endif %}
{% if page=='alerta' %}<h2>Alerta</h2><div class="card"><p>{{datos.alerta}}</p><form method="POST" action="/guardar_texto"><input name="v" value="{{datos.alerta}}"><input type="hidden" name="t" value="alerta"><button>GUARDAR</button></form></div>{% endif %}
{% if page=='chat' %}<h2>Chat</h2><div class="card"><p>{{datos.chat}}</p><form method="POST" action="/guardar_texto"><input name="v" value="{{datos.chat}}"><input type="hidden" name="t" value="chat"><button>GUARDAR</button></form></div>{% endif %}
</body></html>
"""

@app.route('/foto/<n>')
def foto(n):
    return send_from_directory('.', n)
@app.route('/')
def a(): return render_template_string(HTML, page='manada', perros=perros, momentos=momentos, datos=datos)
@app.route('/camara')
def b(): return render_template_string(HTML, page='camara', perros=perros, momentos=momentos, datos=datos)
@app.route('/momentos')
def c(): return render_template_string(HTML, page='momentos', perros=perros, momentos=momentos, datos=datos)
@app.route('/alerta')
def d(): return render_template_string(HTML, page='alerta', perros=perros, momentos=momentos, datos=datos)
@app.route('/chat')
def e(): return render_template_string(HTML, page='chat', perros=perros, momentos=momentos, datos=datos)
@app.route('/subir', methods=['POST'])
def subir():
    f=request.files.get('foto')
    if f: f.save('manada.jpg')
    return redirect('/')
@app.route('/guardar_manada', methods=['POST'])
def gm():
    for i in range(3):
        perros[i]['nombre']=request.form.get(f'n{i}',perros[i]['nombre'])
        perros[i]['raza']=request.form.get(f'r{i}',perros[i]['raza'])
        perros[i]['edad']=request.form.get(f'e{i}',perros[i]['edad'])
    return redirect('/')
@app.route('/guardar_momentos', methods=['POST'])
def gmo():
    for i in range(3):
        momentos[i]['titulo']=request.form.get(f't{i}',momentos[i]['titulo'])
        momentos[i]['fecha']=request.form.get(f'f{i}',momentos[i]['fecha'])
    return redirect('/momentos')
@app.route('/guardar_texto', methods=['POST'])
def gt():
    t=request.form.get('t'); v=request.form.get('v')
    if t=='camara': datos['camara']=v; return redirect('/camara')
    if t=='alerta': datos['alerta']=v; return redirect('/alerta')
    if t=='chat': datos['chat']=v; return redirect('/chat')
    return redirect('/')
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
