from flask import Flask, render_template_string, send_from_directory, request, redirect
import os, json
app = Flask(__name__)
ARCHIVO = "datos.json"

def nuevos():
    return {
        "loki_nombre": "Loki",
        "loki_raza": "Siberian Husky",
        "loki_edad": "2 años",
        "p0": "Cumpleaños de Loki",
        "p1": "Primera vez que corrió",
        "p2": "Primera vez que huyó",
        "p3": "Primera vez en la nieve",
        "pestana_activa": "Cumpleaños de Loki",
        "fotos_count": "25 / 25 fotos",
        "camara_porcentaje": "92% ES LOKI",
        "camara_coincide": "Coincide: ojos azules, mancha en nariz",
        "camara_verificada": "FOTO VERIFICADA - Tomada con FOTO ARES - Parque Fundidora Monterrey, Hoy 13 Nov 2026 12:35 pm",
        "alerta_titulo": "ALERTA - Loki Perdido",
        "alerta_busca": "SE BUSCA LOKI",
        "alerta_detalle": "Perdido hace 2 horas",
        "alerta_ubicacion": "Ultima ubicacion - Parque Fundidora Monterrey",
        "alerta_collar": "Collar azul",
        "alerta_vecinos": "Alerta enviada a 124 vecinos cerca de ti",
        "alerta_radio": "Radio 5 km",
        "chat_titulo": "Chat - Loki - 92% coincidencia",
        "chat_msg1": "Creo que vi a Loki en Parque Fundidora",
        "chat_msg2": "¿Sigue ahí?",
        "chat_msg3": "Sí, corrió hacia el estacionamiento, te comparto ubicación",
        "chat_ubicacion": "Parque Fundidora, Monterrey",
        "chat_verificada": "FOTO VERIFICADA - 92% ES LOKI - Parque Fundidora - Hoy 12:35 pm"
    }

def cargar():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO,"r",encoding="utf-8") as f: return json.load(f)
        except: return nuevos()
    return nuevos()
def guardar():
    with open(ARCHIVO,"w",encoding="utf-8") as f: json.dump(D,f,ensure_ascii=False)
D = cargar()
HUSKY = "https://images.dog.ceo/breeds/husky/n02110185_14112.jpg"

HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>FOTO ARES</title>
<style>
body{background:#f5f5f5;color:#111;font-family:Arial;margin:0;padding-bottom:90px}
.top{background:#fff;padding:12px;text-align:center;box-shadow:0 2px 8px #0002;position:sticky;top:0;z-index:10}
.nav{display:flex;justify-content:space-around;background:#fff;padding:10px 0;position:fixed;bottom:0;left:0;right:0;z-index:20;border-top:1px solid #eee}
.nav a{color:#111;text-decoration:none;font-size:13px;text-align:center}
.nav a.activo{color:#2563eb;font-weight:bold}
.card{background:#fff;border-radius:16px;margin:14px auto;max-width:430px;padding:14px;box-shadow:0 2px 10px #0001}
.card img{width:100%;height:280px;object-fit:cover;border-radius:12px}
input,textarea{width:93%;padding:11px;border-radius:10px;border:1px solid #ddd;margin:6px 0;font-size:15px;background:#f9f9f9}
button{padding:12px 18px;border-radius:20px;border:0;font-weight:bold;font-size:15px;margin:5px}
.btn-azul{background:#2563eb;color:#fff;width:95%}
.btn-rojo{background:#e11d48;color:#fff;width:95%}
.btn-verde{background:#16a34a;color:#fff}
.btn-blanco{background:#fff;border:1px solid #2563eb;color:#2563eb}
.edit{background:#dbeafe;color:#2563eb;padding:8px;border-radius:20px;font-size:13px;display:block;text-align:center;margin:8px 0}
label{color:#2563eb;font-size:12px;font-weight:bold}
.pill{display:inline-block;background:#e8e8e8;padding:8px 10px;border-radius:10px;margin:4px;font-size:13px}
.msg{background:#eee;padding:10px;border-radius:12px;margin:8px 0;text-align:left}
.msg.der{background:#2563eb;color:#fff;margin-left:40px}
.verde{background:#16a34a;color:#fff;padding:12px;border-radius:12px}
.rojo-banner{background:#e11d48;color:#fff;padding:14px;border-radius:12px;font-size:24px;font-weight:bold;text-align:center}
</style></head><body>

{% if page=='manada' %}
<div class="top"><h1>FOTO ARES</h1></div>
<div class="card"><img src="/foto/manada.jpg" onerror="this.src='{{HUSKY}}'"><h2>{{D.loki_nombre}} - {{D.loki_raza}}</h2>
<form method="POST" action="/subir" enctype="multipart/form-data"><input type="hidden" name="cual" value="manada"><input type="file" name="foto" required><button class="btn-azul">SUBIR FOTO MANADA</button></form></div>
{% endif %}

{% if page=='momentos' %}
<div class="top"><h1>Momentos de Loki</h1><span class="edit">✏️ Modo Edición activado - Todo se edita aqui</span></div>
<div class="card"><h3>{{D.pestana_activa}} - {{D.fotos_count}}</h3><div>{% for p in [D.p0,D.p1,D.p2,D.p3] %}<span class="pill">{{p}} ✏️</span>{% endfor %}<span class="pill" style="background:#fde68a">♾️ Nueva Pestaña - INFINITA</span></div><p>♾️ / ♾️ fotos - ♾️ +999</p>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px">{% for i in range(9) %}<img src="/foto/manada.jpg" onerror="this.src='{{HUSKY}}'" style="height:90px">{% endfor %}</div>
<center><button class="btn-azul">Agregar Foto +</button><button class="btn-blanco">Cambiar nombre</button></center></div>
{% endif %}

{% if page=='camara' %}
<div class="top"><h1>FOTO ARES 📷 - Camara</h1></div>
<div class="card" style="background:#111;color:#fff"><img src="/foto/camara.jpg" onerror="this.src='{{HUSKY}}'"><div style="background:#000a;padding:12px;border-radius:12px;text-align:center"><b style="font-size:28px">{{D.camara_porcentaje}}</b><br>{{D.camara_coincide}}</div><br><div class="verde">✅ {{D.camara_verificada}}</div><br><center><button class="btn-verde">✅ Confirmar Avistamiento</button><button class="btn-blanco">Tomar otra foto</button></center>
<form method="POST" action="/subir" enctype="multipart/form-data"><input type="hidden" name="cual" value="camara"><input type="file" name="foto" required><button class="btn-azul">SUBIR FOTO CAMARA</button></form></div>
{% endif %}

{% if page=='alerta' %}
<div class="top"><h1>FOTO ARES</h1></div>
<div class="card"><h2>{{D.alerta_titulo}}</h2><div class="rojo-banner">⚠️ {{D.alerta_busca}}</div><br><div style="background:#cfe8d8;height:150px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:bold;text-align:center">📍 Parque Fundidora<br>{{D.alerta_radio}}</div>
<p>🕐 {{D.alerta_detalle}}</p><p>📍 {{D.alerta_ubicacion}}</p><p>🎗️ {{D.alerta_collar}}</p><div style="background:#fee2e2;padding:10px;border-radius:10px">📢 {{D.alerta_vecinos}}</div><br><button class="btn-rojo">📢 Activar Alerta para todos</button><br><button class="btn-blanco">📤 Compartir Alerta</button><button class="btn-blanco">❗ Reportar Avistamiento</button></div>
{% endif %}

{% if page=='chat' %}
<div class="top"><h1>{{D.chat_titulo}}</h1><p>FOTO ARES • En vivo • Seguro</p></div>
<div class="card"><h3>Loki • Siberian Husky perdido - Activo ahora</h3>
<div class="msg"><b>@LUNA-2310 • finder</b><br>{{D.chat_msg1}}</div>
<div class="msg der"><b>@MANU-8472 • propietario</b><br>{{D.chat_msg2}}</div>
<div class="msg"><b>@LUNA-2310 • finder</b><br>{{D.chat_msg3}}</div>
<div class="msg">📍 {{D.chat_ubicacion}}<br><small>Hace 2 min • Compartir ubicación en vivo</small></div>
<div class="msg" style="border:1px solid #16a34a">✅ {{D.chat_verificada}}<br><img src="/foto/chat.jpg" onerror="this.src='{{HUSKY}}'" style="height:150px"></div>
<input placeholder="Escribe un mensaje..."><br><center><button class="btn-azul">➤ Enviar</button></center></div>
{% endif %}

<!-- ===== EDITAR TODO DESDE LA APP - APARECE EN TODAS LAS SECCIONES ===== -->
<div class="card" style="border:2px solid #2563eb">
<h2 style="color:#2563eb">✏️ EDITAR TODO DESDE AQUI</h2>
<p>Toca cualquier cuadrito, cambia el texto y dale GUARDAR. Ya queda cambiado sin entrar a GitHub.</p>
<form method="POST" action="/guardar">
<label>Nombre de Loki</label><input name="loki_nombre" value="{{D.loki_nombre}}">
<label>Raza</label><input name="loki_raza" value="{{D.loki_raza}}">
<label>Edad</label><input name="loki_edad" value="{{D.loki_edad}}">
<label>Pestaña 1 - Momentos</label><input name="p0" value="{{D.p0}}">
<label>Pestaña 2</label><input name="p1" value="{{D.p1}}">
<label>Pestaña 3</label><input name="p2" value="{{D.p2}}">
<label>Pestaña 4</label><input name="p3" value="{{D.p3}}">
<label>Pestaña activa / Título Momentos</label><input name="pestana_activa" value="{{D.pestana_activa}}">
<label>Conteo fotos</label><input name="fotos_count" value="{{D.fotos_count}}">
<label>Camara - Porcentaje</label><input name="camara_porcentaje" value="{{D.camara_porcentaje}}">
<label>Camara - Coincide</label><input name="camara_coincide" value="{{D.camara_coincide}}">
<label>Camara - Texto verde verificado</label><textarea name="camara_verificada">{{D.camara_verificada}}</textarea>
<label>Alerta - Título</label><input name="alerta_titulo" value="{{D.alerta_titulo}}">
<label>Alerta - Banner rojo</label><input name="alerta_busca" value="{{D.alerta_busca}}">
<label>Alerta - Detalle</label><input name="alerta_detalle" value="{{D.alerta_detalle}}">
<label>Alerta - Ubicación</label><input name="alerta_ubicacion" value="{{D.alerta_ubicacion}}">
<label>Alerta - Collar</label><input name="alerta_collar" value="{{D.alerta_collar}}">
<label>Alerta - Vecinos</label><input name="alerta_vecinos" value="{{D.alerta_vecinos}}">
<label>Alerta - Radio</label><input name="alerta_radio" value="{{D.alerta_radio}}">
<label>Chat - Título</label><input name="chat_titulo" value="{{D.chat_titulo}}">
<label>Chat - Mensaje Luna 1</label><textarea name="chat_msg1">{{D.chat_msg1}}</textarea>
<label>Chat - Mensaje Manu</label><textarea name="chat_msg2">{{D.chat_msg2}}</textarea>
<label>Chat - Mensaje Luna 2</label><textarea name="chat_msg3">{{D.chat_msg3}}</textarea>
<label>Chat - Ubicación</label><input name="chat_ubicacion" value="{{D.chat_ubicacion}}">
<label>Chat - Foto verificada</label><textarea name="chat_verificada">{{D.chat_verificada}}</textarea>
<button class="btn-azul" type="submit">💾 GUARDAR TODO - YA QUEDO</button>
</form>
<p style="font-size:13px;color:#666">Al darle GUARDAR, te regresa a la misma sección y ya se ve el cambio.</p>
</div>

<div class="nav">
<a href="/" class="{% if page=='manada' %}activo{% endif %}">🐾<br>Manada</a>
<a href="/camara" class="{% if page=='camara' %}activo{% endif %}">📷<br>Camara</a>
<a href="/momentos" class="{% if page=='momentos' %}activo{% endif %}">✨<br>Momentos</a>
<a href="/alerta" class="{% if page=='alerta' %}activo{% endif %}">🔔<br>Alerta</a>
<a href="/chat" class="{% if page=='chat' %}activo{% endif %}">💬<br>Chat</a>
</div>
</body></html>
"""

@app.route('/foto/<n>')
def foto(n):
    p = n + ".jpg"
    if os.path.exists(p): return send_from_directory('.', p)
    return redirect(HUSKY)

@app.route('/')
def a(): return render_template_string(HTML, page='manada', D=D, HUSKY=HUSKY)
@app.route('/camara')
def b(): return render_template_string(HTML, page='camara', D=D, HUSKY=HUSKY)
@app.route('/momentos')
def c(): return render_template_string(HTML, page='momentos', D=D, HUSKY=HUSKY)
@app.route('/alerta')
def d(): return render_template_string(HTML, page='alerta', D=D, HUSKY=HUSKY)
@app.route('/chat')
def e(): return render_template_string(HTML, page='chat', D=D, HUSKY=HUSKY)

@app.route('/subir', methods=['POST'])
def subir():
    cual = request.form.get('cual','manada')
    f = request.files.get('foto')
    if f: f.save(f'{cual}.jpg')
    return redirect(request.referrer or '/')

@app.route('/guardar', methods=['POST'])
def gt():
    for k in list(D.keys()):
        if request.form.get(k): D[k] = request.form.get(k)
    guardar()
    return redirect(request.referrer or '/')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
