from flask import Flask, render_template_string, send_from_directory, request, redirect, jsonify
import os, json

app = Flask(__name__)
ARCHIVO = "datos.json"

# DATOS POR DEFECTO - aqui van tus caratulas
DEFAULT = {
 "caratulas": {
  "manada": {"titulo":"Mi Manada","texto":"Togo, Ares y Luna - La familia","foto":"manada.jpg","color":"#FF6B6B"},
  "camara": {"titulo":"Camara en Vivo","texto":"Aqui ves a Togo en vivo","foto":"camara.jpg","color":"#4ECDC4"},
  "momentos": {"titulo":"Momentos","texto":"Los mejores momentos de Togo","foto":"momentos.jpg","color":"#FFD93D"},
  "alerta": {"titulo":"Alerta Togo","texto":"Si Togo se sale, aqui te avisamos","foto":"alerta.jpg","color":"#FF6B35"},
  "chat": {"titulo":"Chat de Togo","texto":"Preguntale lo que quieras a Togo","foto":"chat.jpg","color":"#6C5CE7"},
  "comparar": {"titulo":"Comparar","texto":"Compara a tus perros lado a lado","foto":"comparar.jpg","color":"#00B894"},
  "mapa": {"titulo":"Donde esta Togo","texto":"Ubicacion en vivo de Togo - Tortilleria Alfaro, Nadadores","foto":"mapa.jpg","color":"#0984E3"}
 },
 "perros": [
  {"nombre":"Togo","raza":"Husky Siberiano","edad":"1 año","peso":"22 kg","foto":"togo.jpg","caracter":"Corre mucho, no se cansa, le encanta el piso frio"},
  {"nombre":"Ares","raza":"Husky","edad":"2 años","peso":"25 kg","foto":"ares.jpg","caracter":"Tranquilo, protector"},
  {"nombre":"Luna","raza":"Husky","edad":"1 año","peso":"19 kg","foto":"luna.jpg","caracter":"Juguetona, le gusta la nieve"}
 ],
 "momentos": [
  {"titulo":"Togo en el patio","fecha":"12 Nov 2026","foto":"momento1.jpg"},
  {"titulo":"Togo banado","fecha":"10 Nov 2026","foto":"momento2.jpg"},
  {"titulo":"Togo durmiendo","fecha":"8 Nov 2026","foto":"momento3.jpg"}
 ],
 "ubicacion": {"lugar":"Tortilleria Alfaro, Nadadores, Coahuila","lat":"27.0333","lng":"-101.5833","link":"https://maps.google.com/?q=Nadadores+Coahuila"},
 "config": {"titulo_app":"FOTO TOGO","color_fondo":"#FFF5E1"}
}

def cargar():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO,"r",encoding="utf-8") as f: return json.load(f)
        except: return DEFAULT
    return DEFAULT

def guardar_datos(d):
    with open(ARCHIVO,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)

DATOS = cargar()

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{background:#FFF5E1;font-family:Arial;margin:0;padding-bottom:90px}
.top{background:linear-gradient(90deg,#FF6B6B,#FFD93D,#4ECDC4,#6C5CE7);padding:18px 10px;text-align:center;position:sticky;top:0;z-index:10}
.top h1{margin:0;color:#fff;text-shadow:1px 1px 3px #000;font-size:26px}
.top p{margin:2px;color:#fff;font-weight:bold}
.tabs{display:flex;overflow-x:auto;gap:8px;padding:10px;background:#fff;position:sticky;top:78px;z-index:10;box-shadow:0 2px 8px #0002}
.tab{flex:0 0 auto;padding:12px 16px;border-radius:25px;color:#fff;font-weight:bold;text-decoration:none;font-size:14px}
.tab.manada{background:#FF6B6B}.tab.camara{background:#4ECDC4}.tab.momentos{background:#FDCB6E;color:#333}.tab.alerta{background:#FF6B35}.tab.chat{background:#6C5CE7}.tab.comparar{background:#00B894}.tab.mapa{background:#0984E3}
.caratula{border-radius:20px;padding:16px;margin:14px;color:#fff;text-align:center}
.caratula img{width:100%;height:250px;object-fit:cover;border-radius:15px;background:#fff}
.card{background:#fff;border-radius:18px;padding:14px;margin:14px;box-shadow:0 3px 10px #0001}
.card img{width:100%;height:230px;object-fit:cover;border-radius:14px}
input,textarea,select{width:100%;padding:12px;border-radius:12px;border:2px solid #eee;margin:6px 0;font-size:15px}
button{border:0;padding:13px 18px;border-radius:14px;font-weight:bold;font-size:15px;cursor:pointer}
.btn-guardar-todo{background:#00B894;color:#fff;width:100%;font-size:18px;padding:16px;position:fixed;bottom:10px;left:10px;right:10px;z-index:20;box-shadow:0 4px 12px #0003}
.btn-color{background:#FFD93D}
.btn-camara{background:#4ECDC4;color:#fff}
video{width:100%;border-radius:15px;background:#000}
.flex{display:flex;gap:10px}.flex .card{flex:1}
.mapa{width:100%;height:350px;border:0;border-radius:15px}
.badge{display:inline-block;background:#fff;color:#333;padding:5px 12px;border-radius:20px;font-size:12px;font-weight:bold}
</style></head><body>

<div class="top"><h1>🐶 {{datos.config.titulo_app}}</h1><p>✨ Toca cualquier campo y cambialo - Todo se guarda con un boton ✨</p></div>

<div class="tabs">
<a class="tab manada" href="/">🐶 Manada</a>
<a class="tab camara" href="/camara">📷 Camara</a>
<a class="tab momentos" href="/momentos">⭐ Momentos</a>
<a class="tab alerta" href="/alerta">🚨 Alerta</a>
<a class="tab chat" href="/chat">💬 Chat</a>
<a class="tab comparar" href="/comparar">⚖️ Comparar</a>
<a class="tab mapa" href="/mapa">📍 Mapa</a>
</div>

<!-- FORMULARIO GIGANTE - GUARDA TODO CON UN SOLO BOTON -->
<form method="POST" action="/guardar_todo" enctype="multipart/form-data" id="formTodo">

<!-- CARATULA DE ESTA PESTAÑA -->
<div class="caratula" style="background:{{caratula.color}}">
<span class="badge">⭐ CARATULA - {{page.upper()}} - Cambiala aqui</span>
<img src="/foto/{{caratula.foto}}">
<label>Titulo de la caratula</label><input name="car_titulo" value="{{caratula.titulo}}">
<label>Texto de la caratula</label><textarea name="car_texto">{{caratula.texto}}</textarea>
<label>Color de la caratula</label><input type="color" name="car_color" value="{{caratula.color}}">
<label>Cambiar foto de caratula</label><input type="file" name="car_foto">
<input type="hidden" name="pagina" value="{{page}}">
</div>

{% if page=='manada' %}
<h2 style="text-align:center">🐶 Mi Manada - Edita todo aqui</h2>
{% for p in datos.perros %}
<div class="card"><img src="/foto/{{p.foto}}"><h3>🐶 {{p.nombre}}</h3>
<label>Nombre</label><input name="perro_nombre_{{loop.index0}}" value="{{p.nombre}}">
<label>Raza</label><input name="perro_raza_{{loop.index0}}" value="{{p.raza}}">
<label>Edad</label><input name="perro_edad_{{loop.index0}}" value="{{p.edad}}">
<label>Peso</label><input name="perro_peso_{{loop.index0}}" value="{{p.peso}}">
<label>Caracter</label><textarea name="perro_caracter_{{loop.index0}}">{{p.caracter}}</textarea>
<label>Cambiar foto</label><input type="file" name="perro_foto_{{loop.index0}}">
</div>{% endfor %}
{% endif %}

{% if page=='camara' %}
<div class="card"><h2>📷 Camara Activada</h2><video id="v" autoplay playsinline></video><br>
<button type="button" class="btn-camara" onclick="prender()">📷 PRENDER CAMARA</button>
<button type="button" onclick="tomar()">📸 TOMAR FOTO</button><canvas id="c" style="display:none"></canvas>
<p id="msg">Picale PRENDER CAMARA y dale permitir</p></div>
<script>
async function prender(){try{let s=await navigator.mediaDevices.getUserMedia({video:true});document.getElementById('v').srcObject=s;document.getElementById('msg').innerText='Camara prendida - Aqui esta Togo en vivo';}catch(e){document.getElementById('msg').innerText='No dio permiso, dale permitir a la camara arriba';}}
function tomar(){let v=document.getElementById('v');let c=document.getElementById('c');c.width=v.videoWidth;c.height=v.videoHeight;c.getContext('2d').drawImage(v,0,0);let a=document.createElement('a');a.download='togo.jpg';a.href=c.toDataURL('image/jpeg');a.click();}
</script>
{% endif %}

{% if page=='momentos' %}
<h2 style="text-align:center">⭐ Momentos</h2>
{% for m in datos.momentos %}
<div class="card"><img src="/foto/{{m.foto}}"><label>Titulo</label><input name="mom_titulo_{{loop.index0}}" value="{{m.titulo}}"><label>Fecha</label><input name="mom_fecha_{{loop.index0}}" value="{{m.fecha}}"><label>Cambiar foto</label><input type="file" name="mom_foto_{{loop.index0}}"></div>{% endfor %}
{% endif %}

{% if page=='comparar' %}
<div class="card"><h2>⚖️ Comparar</h2>
<label>Perro 1</label><select name="comp_a">{% for p in datos.perros %}<option value="{{loop.index0}}">{{p.nombre}}</option>{% endfor %}</select>
<label>Perro 2</label><select name="comp_b">{% for p in datos.perros %}<option value="{{loop.index0}}">{{p.nombre}}</option>{% endfor %}</select>
<p>Elige los 2 y dale GUARDAR TODO, te los muestra abajo</p></div>
{% if pa %}<div class="flex"><div class="card"><img src="/foto/{{pa.foto}}"><h3>{{pa.nombre}}</h3><p>{{pa.raza}} - {{pa.edad}} - {{pa.peso}}</p><p>{{pa.caracter}}</p></div><div class="card"><img src="/foto/{{pb.foto}}"><h3>{{pb.nombre}}</h3><p>{{pb.raza}} - {{pb.edad}} - {{pb.peso}}</p><p>{{pb.caracter}}</p></div></div>{% endif %}
{% endif %}

{% if page=='mapa' %}
<div class="card"><h2>📍 Donde esta Togo</h2>
<label>Lugar</label><input name="ubi_lugar" value="{{datos.ubicacion.lugar}}">
<label>Latitud</label><input name="ubi_lat" id="lat" value="{{datos.ubicacion.lat}}">
<label>Longitud</label><input name="ubi_lng" id="lng" value="{{datos.ubicacion.lng}}">
<button type="button" onclick="miUbicacion()" style="background:#0984E3;color:#fff;width:100%">📍 USAR MI UBICACION ACTUAL</button>
<iframe class="mapa" src="https://maps.google.com/maps?q={{datos.ubicacion.lat}},{{datos.ubicacion.lng}}&z=15&output=embed"></iframe>
<a href="https://maps.google.com/?q={{datos.ubicacion.lat}},{{datos.ubicacion.lng}}" target="_blank"><button type="button" style="background:#0984E3;color:#fff;width:100%;margin-top:10px">ABRIR EN GOOGLE MAPS 🗺️</button></a>
</div>
<script>function miUbicacion(){if(navigator.geolocation){navigator.geolocation.getCurrentPosition(p=>{document.getElementById('lat').value=p.coords.latitude;document.getElementById('lng').value=p.coords.longitude;alert('Ubicacion lista! Ahora dale GUARDAR TODO');});}else{alert('Tu cel no tiene GPS activado');}}</script>
{% endif %}

{% if page=='alerta' %}<div class="card"><h2>🚨 Alerta</h2><p>Si Togo se sale, aqui te avisamos. Cambia el texto en la caratula de arriba.</p></div>{% endif %}
{% if page=='chat' %}<div class="card"><h2>💬 Chat</h2><p>{{caratula.texto}}</p><input placeholder="Escribele algo a Togo..."><button type="button">ENVIAR</button></div>{% endif %}

<!-- BOTON MAGICO - GUARDA TODO -->
<button class="btn-guardar-todo">💾 GUARDAR TODO - Picale aqui y se guarda todo</button>
</form>

<div style="text-align:center;padding:10px;color:#888">Si cambias algo en cualquier pestaña, dale GUARDAR TODO y ya queda guardado</div>
</body></html>
"""

@app.route('/foto/<n>')
def foto(n):
    if os.path.exists(n): return send_from_directory('.', n)
    return send_from_directory('.', 'manada.jpg') if os.path.exists('manada.jpg') else ("",404)

def pagina(p, pa=None, pb=None):
    return render_template_string(HTML, page=p, caratula=DATOS['caratulas'][p], datos=DATOS, pa=pa, pb=pb)

@app.route('/')
def a(): return pagina('manada')
@app.route('/camara')
def b(): return pagina('camara')
@app.route('/momentos')
def c(): return pagina('momentos')
@app.route('/alerta')
def d(): return pagina('alerta')
@app.route('/chat')
def e(): return pagina('chat')
@app.route('/comparar')
def f():
    ai=int(request.args.get('a',0)); bi=int(request.args.get('b',1))
    return pagina('comparar', DATOS['perros'][ai], DATOS['perros'][bi])
@app.route('/mapa')
def g(): return pagina('mapa')

@app.route('/guardar_todo', methods=['POST'])
def guardar_todo():
    global DATOS
    pag = request.form.get('pagina','manada')
    # Caratula
    if request.form.get('car_titulo'):
        DATOS['caratulas'][pag]['titulo']=request.form.get('car_titulo')
        DATOS['caratulas'][pag]['texto']=request.form.get('car_texto')
        DATOS['caratulas'][pag]['color']=request.form.get('car_color')
        f=request.files.get('car_foto')
        if f and f.filename:
            f.save(DATOS['caratulas'][pag]['foto'])
    # Perros - se guardan desde cualquier pestaña si vienen
    for i in range(len(DATOS['perros'])):
        if f"perro_nombre_{i}" in request.form:
            DATOS['perros'][i]['nombre']=request.form.get(f"perro_nombre_{i}")
            DATOS['perros'][i]['raza']=request.form.get(f"perro_raza_{i}")
            DATOS['perros'][i]['edad']=request.form.get(f"perro_edad_{i}")
            DATOS['perros'][i]['peso']=request.form.get(f"perro_peso_{i}")
            DATOS['perros'][i]['caracter']=request.form.get(f"perro_caracter_{i}")
            ff=request.files.get(f"perro_foto_{i}")
            if ff and ff.filename: ff.save(DATOS['perros'][i]['foto'])
    # Momentos
    for i in range(len(DATOS['momentos'])):
        if f"mom_titulo_{i}" in request.form:
            DATOS['momentos'][i]['titulo']=request.form.get(f"mom_titulo_{i}")
            DATOS['momentos'][i]['fecha']=request.form.get(f"mom_fecha_{i}")
            ff=request.files.get(f"mom_foto_{i}")
            if ff and ff.filename: ff.save(DATOS['momentos'][i]['foto'])
    # Ubicacion Maps
    if request.form.get('ubi_lugar'):
        DATOS['ubicacion']['lugar']=request.form.get('ubi_lugar')
        DATOS['ubicacion']['lat']=request.form.get('ubi_lat')
        DATOS['ubicacion']['lng']=request.form.get('ubi_lng')
    guardar_datos(DATOS)
    # Si es comparar, regresa con los elegidos
    if pag=='comparar':
        ai=request.form.get('comp_a','0'); bi=request.form.get('comp_b','1')
        return redirect(f"/comparar?a={ai}&b={bi}")
    if pag=='manada': return redirect('/')
    return redirect('/'+pag)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
