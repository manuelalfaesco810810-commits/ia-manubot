from flask import Flask, render_template_string, send_from_directory, request, redirect
import os, json
app = Flask(__name__)
ARCHIVO = "datos.json"

def nuevos():
    return {
        "loki_nombre": "Loki", "loki_raza": "Siberian Husky", "loki_edad": "2 años",
        "p0": "Cumpleaños de Loki", "p1": "Primera vez que corrió", "p2": "Primera vez que huyó", "p3": "Primera vez en la nieve",
        "pestana_activa": "Cumpleaños de Loki", "fotos_count": "25 / 25 fotos",
        "camara_porcentaje": "92% ES LOKI", "camara_coincide": "Coincide: ojos azules, mancha en nariz",
        "camara_verificada": "FOTO VERIFICADA - Tomada con FOTO ARES - Parque Fundidora Monterrey, Hoy 13 Nov 2026 12:35 pm",
        "alerta_titulo": "ALERTA - Loki Perdido", "alerta_busca": "SE BUSCA LOKI",
        "alerta_detalle": "Perdido hace 2 horas", "alerta_ubicacion": "Ultima ubicacion - Parque Fundidora Monterrey",
        "alerta_collar": "Collar azul", "alerta_vecinos": "Alerta enviada a 124 vecinos cerca de ti", "alerta_radio": "Radio 5 km",
        "chat_titulo": "Chat - Loki - 92% coincidencia",
        "chat_msg1": "Creo que vi a Loki en Parque Fundidora", "chat_msg2": "¿Sigue ahí?",
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
video{width:100%;height:280px;background:#000;border-radius:12px;object-fit:cover}
canvas{width:100%;border-radius:12px}
input,textarea{width:93%;padding:11px;border-radius:10px;border:1px solid #ddd;margin:6px 0;font-size:15px}
button{padding:12px 18px;border-radius:20px;border:0;font-weight:bold;font-size:15px;margin:5px}
.btn-azul{background:#2563eb;color:#fff;width:95%}
.btn-rojo{background:#e11d48;color:#fff;width:95%}
.btn-verde{background:#16a34a;color:#fff}
.btn-negro{background:#111;color:#fff}
.btn-blanco{background:#fff;border:1px solid #2563eb;color:#2563eb}
.edit{background:#dbeafe;color:#2563eb;padding:8px;border-radius:20px;font-size:13px;display:block;text-align:center;margin:8px 0}
label{color:#2563eb;font-size:12px;font-weight:bold}
.pill{display:inline-block;background:#e8e8e8;padding:8px 10px;border-radius:10px;margin:4px;font-size:13px}
.msg{background:#eee;padding:10px;border-radius:12px;margin:8px 0;text-align:left}
.msg.der{background:#2563eb;color:#fff;margin-left:40px}
.verde{background:#16a34a;color:#fff;padding:12px;border-radius:12px}
.rojo-banner{background:#e11d48;color:#fff;padding:14px;border-radius:12px;font-size:24px;font-weight:bold;text-align:center}
.permiso{background:#fff3cd;border:1px solid #f59e0b;padding:10px;border-radius:10px;font-size:13px;margin:8px 0}
.ok{background:#d1fae5;padding:10px;border-radius:10px;font-size:13px;margin:8px 0}
#avisoGuardado{position:fixed;top:70px;left:50%;transform:translateX(-50%);background:#16a34a;color:#fff;padding:12px 20px;border-radius:20px;font-weight:bold;display:none;z-index:100;box-shadow:0 4px 12px #0003}
</style></head><body>
<div id="avisoGuardado">✅ GUARDADO PERMANENTE EN TU CELULAR</div>

{% if page=='manada' %}
<div class="top"><h1>🐾 FOTO ARES</h1><p>Husky Loki</p></div>
<div class="card"><img id="imgManada" src="/foto/manada.jpg" onerror="this.src='{{HUSKY}}'"><h2><span data-show="loki_nombre">{{D.loki_nombre}}</span> - <span data-show="loki_raza">{{D.loki_raza}}</span> - <span data-show="loki_edad">{{D.loki_edad}}</span></h2>
<div class="permiso">📷 Galería para foto de portada</div>
<input type="file" accept="image/*" onchange="guardarFotoLocal(event,'manada','imgManada')"><p style="font-size:12px">La foto queda guardada en tu celular, no se borra.</p></div>
{% endif %}

{% if page=='momentos' %}
<div class="top"><h1>Momentos de Loki</h1><span class="edit">✏️ Todo se edita y se guarda permanente</span></div>
<div class="card"><h3><span data-show="pestana_activa">{{D.pestana_activa}}</span> - <span data-show="fotos_count">{{D.fotos_count}}</span></h3>
<div><span class="pill"><span data-show="p0">{{D.p0}}</span> ✏️</span><span class="pill"><span data-show="p1">{{D.p1}}</span> ✏️</span><span class="pill"><span data-show="p2">{{D.p2}}</span> ✏️</span><span class="pill"><span data-show="p3">{{D.p3}}</span> ✏️</span><span class="pill" style="background:#fde68a">♾️ Nueva Pestaña - INFINITA</span></div>
<p>♾️ / ♾️ fotos - ♾️ +999</p>
<div id="gridMomentos" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px">{% for i in range(9) %}<img src="/foto/manada.jpg" onerror="this.src='{{HUSKY}}'" style="height:90px">{% endfor %}</div>
<div class="permiso">🖼️ Galería: Al dar Agregar Foto te abrirá tus fotos.</div>
<input type="file" accept="image/*" onchange="guardarFotoLocal(event,'momentos','gridMomentos')">
<center><button class="btn-azul" onclick="alert('Elige una foto de tu galería arriba')">+ Agregar Foto +</button></center></div>
{% endif %}

{% if page=='camara' %}
<div class="top"><h1>FOTO ARES 📷 - Camara</h1></div>
<div class="card" style="background:#111;color:#fff">
<div class="permiso" style="color:#111">📷 Permiso CÁMARA: Dale Permitir cuando te pregunte.</div>
<video id="video" autoplay playsinline style="display:none"></video><canvas id="canvas" style="display:none"></canvas>
<img id="fotoCamara" src="/foto/camara.jpg" onerror="this.src='{{HUSKY}}'">
<div id="estadoCamara" class="ok" style="display:none">✅ Cámara activada</div>
<div style="background:#000a;padding:12px;border-radius:12px;text-align:center"><b style="font-size:28px"><span data-show="camara_porcentaje">{{D.camara_porcentaje}}</span></b><br><span data-show="camara_coincide">{{D.camara_coincide}}</span></div><br>
<div class="verde">✅ <span data-show="camara_verificada">{{D.camara_verificada}}</span></div><br>
<center><button class="btn-verde" onclick="activarCamara()">📷 ACTIVAR CÁMARA</button><button class="btn-negro" onclick="tomarFoto()">📸 TOMAR FOTO</button><button class="btn-blanco" onclick="cerrarCamara()">❌ Cerrar</button></center><br><center><button class="btn-verde">✅ Confirmar Avistamiento</button></center>
</div>
{% endif %}

{% if page=='alerta' %}
<div class="top"><h1>FOTO ARES</h1></div>
<div class="card"><h2><span data-show="alerta_titulo">{{D.alerta_titulo}}</span></h2><div class="rojo-banner">⚠️ <span data-show="alerta_busca">{{D.alerta_busca}}</span></div><br>
<div class="permiso">📍 Permiso UBICACIÓN: Dale Permitir para que te ubique.</div>
<div id="miUbicacion" style="background:#cfe8d8;padding:14px;border-radius:12px;text-align:center">📍 <span data-show="alerta_ubicacion">{{D.alerta_ubicacion}}</span><br><span data-show="alerta_radio">{{D.alerta_radio}}</span></div>
<p>🕐 <span data-show="alerta_detalle">{{D.alerta_detalle}}</span></p><p>📍 <span data-show="alerta_ubicacion">{{D.alerta_ubicacion}}</span></p><p>🎗️ <span data-show="alerta_collar">{{D.alerta_collar}}</span></p>
<div style="background:#fee2e2;padding:10px;border-radius:10px">📢 <span data-show="alerta_vecinos">{{D.alerta_vecinos}}</span></div><br>
<button class="btn-rojo" onclick="activarUbicacion()">📍 ACTIVAR UBICACIÓN Y ALERTA</button><br><button class="btn-blanco" onclick="compartirAlerta()">📤 Compartir Alerta</button><button class="btn-blanco" onclick="alert('Avistamiento reportado!')">❗ Reportar Avistamiento</button></div>
{% endif %}

{% if page=='chat' %}
<div class="top"><h1><span data-show="chat_titulo">{{D.chat_titulo}}</span></h1><p>FOTO ARES • En vivo • Seguro</p></div>
<div class="card"><h3>Loki • Siberian Husky perdido - Activo ahora</h3>
<div class="msg"><b>@LUNA-2310 • finder</b><br><span data-show="chat_msg1">{{D.chat_msg1}}</span></div>
<div class="msg der"><b>@MANU-8472 • propietario</b><br><span data-show="chat_msg2">{{D.chat_msg2}}</span></div>
<div class="msg"><b>@LUNA-2310 • finder</b><br><span data-show="chat_msg3">{{D.chat_msg3}}</span></div>
<div class="msg" id="ubicacionChat">📍 <span data-show="chat_ubicacion">{{D.chat_ubicacion}}</span></div>
<div class="msg" style="border:1px solid #16a34a">✅ <span data-show="chat_verificada">{{D.chat_verificada}}</span><br><img src="/foto/chat.jpg" onerror="this.src='{{HUSKY}}'" style="height:150px"></div>
<div class="permiso">📍 Ubicación + Galería para el chat</div>
<input id="inputChat" placeholder="Escribe un mensaje..."><br><center><button class="btn-azul" onclick="enviarChat()">➤ Enviar</button></center><div id="chatExtra"></div><br>
<center><button class="btn-blanco" onclick="activarUbicacion()">📍 Compartir Ubicación</button><button class="btn-blanco" onclick="alert('Caso Cerrado - Loki encontrado!')">✅ Caso Cerrado</button></center>
<br><label>Foto en el chat - Galería o Cámara:</label><input type="file" accept="image/*" capture="environment" onchange="guardarFotoLocal(event,'chat','chatExtra')">
</div>
{% endif %}

<!-- EDITAR TODO - GUARDADO PERMANENTE EN TU CELULAR -->
<div class="card" style="border:2px solid #2563eb">
<h2 style="color:#2563eb">✏️ EDITAR TODO - GUARDADO PERMANENTE</h2>
<p style="font-size:13px">✅ Ahora se guarda en <b>tu celular</b>, no solo en Render. Aunque Render se reinicie, tus datos siguen.</p>
<form id="formEditar" method="POST" action="/guardar" onsubmit="guardarPermanente(event)">
<label>Nombre Loki</label><input name="loki_nombre" data-save="loki_nombre" value="{{D.loki_nombre}}">
<label>Raza</label><input name="loki_raza" data-save="loki_raza" value="{{D.loki_raza}}">
<label>Edad</label><input name="loki_edad" data-save="loki_edad" value="{{D.loki_edad}}">
<label>Pestaña 1</label><input name="p0" data-save="p0" value="{{D.p0}}">
<label>Pestaña 2</label><input name="p1" data-save="p1" value="{{D.p1}}">
<label>Pestaña 3</label><input name="p2" data-save="p2" value="{{D.p2}}">
<label>Pestaña 4</label><input name="p3" data-save="p3" value="{{D.p3}}">
<label>Pestaña activa</label><input name="pestana_activa" data-save="pestana_activa" value="{{D.pestana_activa}}">
<label>Conteo fotos</label><input name="fotos_count" data-save="fotos_count" value="{{D.fotos_count}}">
<label>Camara %</label><input name="camara_porcentaje" data-save="camara_porcentaje" value="{{D.camara_porcentaje}}">
<label>Camara coincide</label><input name="camara_coincide" data-save="camara_coincide" value="{{D.camara_coincide}}">
<label>Camara verificada</label><textarea name="camara_verificada" data-save="camara_verificada">{{D.camara_verificada}}</textarea>
<label>Alerta titulo</label><input name="alerta_titulo" data-save="alerta_titulo" value="{{D.alerta_titulo}}">
<label>Alerta busca</label><input name="alerta_busca" data-save="alerta_busca" value="{{D.alerta_busca}}">
<label>Alerta detalle</label><input name="alerta_detalle" data-save="alerta_detalle" value="{{D.alerta_detalle}}">
<label>Alerta ubicacion</label><input name="alerta_ubicacion" data-save="alerta_ubicacion" value="{{D.alerta_ubicacion}}">
<label>Alerta collar</label><input name="alerta_collar" data-save="alerta_collar" value="{{D.alerta_collar}}">
<label>Alerta vecinos</label><input name="alerta_vecinos" data-save="alerta_vecinos" value="{{D.alerta_vecinos}}">
<label>Alerta radio</label><input name="alerta_radio" data-save="alerta_radio" value="{{D.alerta_radio}}">
<label>Chat titulo</label><input name="chat_titulo" data-save="chat_titulo" value="{{D.chat_titulo}}">
<label>Chat Luna 1</label><textarea name="chat_msg1" data-save="chat_msg1">{{D.chat_msg1}}</textarea>
<label>Chat Manu</label><textarea name="chat_msg2" data-save="chat_msg2">{{D.chat_msg2}}</textarea>
<label>Chat Luna 2</label><textarea name="chat_msg3" data-save="chat_msg3">{{D.chat_msg3}}</textarea>
<label>Chat ubicacion</label><input name="chat_ubicacion" data-save="chat_ubicacion" value="{{D.chat_ubicacion}}">
<label>Chat verificada</label><textarea name="chat_verificada" data-save="chat_verificada">{{D.chat_verificada}}</textarea>
<button class="btn-azul" type="submit">💾 GUARDAR TODO PERMANENTE</button>
</form>
<center><button class="btn-blanco" onclick="borrarTodo()">🗑️ Borrar todo y volver a fábrica</button></center>
</div>

<div class="nav">
<a href="/" class="{% if page=='manada' %}activo{% endif %}">🐾<br>Manada</a>
<a href="/camara" class="{% if page=='camara' %}activo{% endif %}">📷<br>Camara</a>
<a href="/momentos" class="{% if page=='momentos' %}activo{% endif %}">✨<br>Momentos</a>
<a href="/alerta" class="{% if page=='alerta' %}activo{% endif %}">🔔<br>Alerta</a>
<a href="/chat" class="{% if page=='chat' %}activo{% endif %}">💬<br>Chat</a>
</div>

<script>
// ===== GUARDADO PERMANENTE EN TU CELULAR =====
const KEY = 'FOTO_ARES_DATOS_PERMANENTES';
function leerLocal(){ try{ return JSON.parse(localStorage.getItem(KEY) || '{}'); }catch(e){ return {}; } }
function mostrarAviso(){ let a=document.getElementById('avisoGuardado'); a.style.display='block'; setTimeout(()=>a.style.display='none', 2500); }
// Al entrar, cargar lo que guardaste antes en tu celular
window.addEventListener('load', function(){
  let datos = leerLocal();
  if(Object.keys(datos).length===0) return;
  document.querySelectorAll('[data-save]').forEach(el=>{ if(datos[el.getAttribute('data-save')]) el.value = datos[el.getAttribute('data-save')]; });
  document.querySelectorAll('[data-show]').forEach(el=>{ let k=el.getAttribute('data-show'); if(datos[k]) el.textContent = datos[k]; });
});
function guardarPermanente(e){
  // 1. Guardar en tu celular - NUNCA se borra
  let datos = leerLocal();
  document.querySelectorAll('[data-save]').forEach(el=>{ datos[el.getAttribute('data-save')] = el.value; });
  localStorage.setItem(KEY, JSON.stringify(datos));
  // 2. Actualizar lo que se ve arriba sin recargar
  document.querySelectorAll('[data-show]').forEach(el=>{ let k=el.getAttribute('data-show'); if(datos[k]) el.textContent = datos[k]; });
  mostrarAviso();
  // 3. Tambien intentar guardar en Render (aunque se borre, ya esta en tu celular)
  // No bloqueamos, dejamos que el form siga
}
function borrarTodo(){ if(confirm('¿Borrar todo y volver a Collar azul, Loki, etc?')){ localStorage.removeItem(KEY); location.reload(); } }
function guardarFotoLocal(e, cual, destinoId){
  let f=e.target.files[0]; if(!f) return;
  let r=new FileReader(); r.onload=function(){
    try{ localStorage.setItem('FOTO_ARES_FOTO_'+cual, r.result); }catch(err){ alert('Foto muy grande para guardar en celular, usa una mas pequeña'); return; }
    let dest=document.getElementById(destinoId);
    if(dest && dest.tagName==='IMG'){ dest.src=r.result; } else if(dest){ dest.innerHTML='<img src="'+r.result+'" style="height:150px;border-radius:12px">'; }
    mostrarAviso();
  }; r.readAsDataURL(f);
}
// Cargar fotos guardadas en celular al entrar
window.addEventListener('load', function(){
  let fm=localStorage.getItem('FOTO_ARES_FOTO_manada'); if(fm){ let im=document.getElementById('imgManada'); if(im) im.src=fm; let fc=document.getElementById('fotoCamara'); if(fc) fc.src=fm; }
});
let stream=null;
async function activarCamara(){ try{ stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:'environment'},audio:false}); let v=document.getElementById('video'); v.srcObject=stream; v.style.display='block'; document.getElementById('fotoCamara').style.display='none'; document.getElementById('estadoCamara').style.display='block'; }catch(e){ alert('Dale PERMITIR a la cámara. Si le diste No, ve a Chrome > Permisos > Cámara > Permitir.'); } }
function tomarFoto(){ let v=document.getElementById('video'); if(!v.srcObject){ alert('Primero ACTIVAR CÁMARA'); return; } let c=document.getElementById('canvas'); c.width=v.videoWidth; c.height=v.videoHeight; c.getContext('2d').drawImage(v,0,0); let img=document.getElementById('fotoCamara'); img.src=c.toDataURL('image/jpeg'); img.style.display='block'; v.style.display='none'; try{ localStorage.setItem('FOTO_ARES_FOTO_camara', img.src); }catch(e){} alert('📸 Foto tomada y guardada en tu celular!'); if(stream) stream.getTracks().forEach(t=>t.stop()); }
function cerrarCamara(){ if(stream) stream.getTracks().forEach(t=>t.stop()); document.getElementById('video').style.display='none'; document.getElementById('fotoCamara').style.display='block'; }
function activarUbicacion(){ if(!navigator.geolocation){ alert('Activa GPS'); return; } navigator.geolocation.getCurrentPosition(function(pos){ let lat=pos.coords.latitude.toFixed(5), lon=pos.coords.longitude.toFixed(5); let texto='📍 Tu ubicación: '+lat+', '+lon+' - Cerca de Parque Fundidora - Radio 5 km'; let el=document.getElementById('miUbicacion'); if(el) el.innerHTML=texto+'<br><a href="https://maps.google.com/?q='+lat+','+lon+'" target="_blank">Ver en Maps</a>'; let chat=document.getElementById('ubicacionChat'); if(chat) chat.innerHTML='📍 Mi ubicación: '+lat+', '+lon; let datos=leerLocal(); datos['alerta_ubicacion']='Ubicación actual: '+lat+', '+lon; datos['chat_ubicacion']='Ubicación actual: '+lat+', '+lon; localStorage.setItem(KEY, JSON.stringify(datos)); alert('✅ Ubicación guardada permanente: '+lat+', '+lon); }, function(){ alert('Dale PERMITIR a Ubicación.'); }, {enableHighAccuracy:true}); }
function compartirAlerta(){ if(navigator.share){ navigator.share({title:'SE BUSCA LOKI', text:'Se busca Loki - Parque Fundidora', url:window.location.href}); } else { alert('Copia el link: '+window.location.href); } }
function enviarChat(){ let v=document.getElementById('inputChat').value; if(!v) return; document.getElementById('chatExtra').innerHTML+='<div class="msg der"><b>@MANU-8472</b><br>'+v+'</div>'; document.getElementById('inputChat').value=''; }
</script>
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
