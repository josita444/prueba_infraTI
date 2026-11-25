import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


tareas = [
    {"id": 1, "titulo": "Programar la lógica principal en Python", "materia": "Programación", "dificultad": "Alta", "minutos": 45, "xp": 150},
    {"id": 2, "titulo": "Sincronizar ramas develop y main en GitHub", "materia": "Infraestructura TI", "dificultad": "Media", "minutos": 25, "xp": 90},
    {"id": 3, "titulo": "Pulir diseño y verificar enlaces del README", "materia": "Documentación", "dificultad": "Baja", "minutos": 15, "xp": 50}
]

misiones_sorpresa = [
    {"titulo": "Sprint Relámpago: 15 min sin mirar el celular", "materia": "Enfoque Total", "dificultad": "Media", "minutos": 15, "xp": 80},
    {"titulo": "Reto Git: Revisar estado del repositorio y commits", "materia": "Infraestructura TI", "dificultad": "Baja", "minutos": 10, "xp": 50},
    {"titulo": "Deep Work: Resolver el problema más difícil del día", "materia": "Desafío Pro", "dificultad": "Alta", "minutos": 40, "xp": 160},
    {"titulo": "Repaso Express: Resumir 3 conceptos clave en voz alta", "materia": "Estudio Activo", "dificultad": "Baja", "minutos": 15, "xp": 60}
]


xp_total = 120
racha_dias = 3


def calcular_prioridad(dificultad, energia):
    if energia == "Alta":
        return {"Alta": 3, "Media": 2, "Baja": 1}.get(dificultad, 1)
    elif energia == "Baja":
        return {"Baja": 3, "Media": 2, "Alta": 1}.get(dificultad, 1)
    return {"Media": 3, "Alta": 2, "Baja": 1}.get(dificultad, 1)

def obtener_rango(xp):
    if xp < 250:
        return 1, "Explorador Digital", int((xp / 250) * 100)
    elif xp < 600:
        return 2, "Estratega del Tiempo", int(((xp - 250) / 350) * 100)
    elif xp < 1000:
        return 3, "Arquitecto Cyber-Pro", int(((xp - 600) / 400) * 100)
    return 4, "Leyenda del Enfoque", 100

@app.route('/', methods=['GET', 'POST'])
def index():
    energia = request.args.get('energia', 'Alta')

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        materia = request.form.get('materia', 'General').strip()
        dificultad = request.form.get('dificultad', 'Media')
        minutos = int(request.form.get('minutos', 25))
        energia = request.form.get('energia_usuario', 'Alta')

        xp_mapa = {"Alta": 150, "Media": 90, "Baja": 50}
        if titulo:
            nuevo_id = max([t["id"] for t in tareas], default=0) + 1
            tareas.append({
                "id": nuevo_id,
                "titulo": titulo,
                "materia": materia,
                "dificultad": dificultad,
                "minutos": minutos,
                "xp": xp_mapa.get(dificultad, 80)
            })
        return redirect(url_for('index', energia=energia))

    tareas_ordenadas = sorted(
        tareas,
        key=lambda t: calcular_prioridad(t["dificultad"], energia),
        reverse=True
    )


    total_minutos = sum(t["minutos"] for t in tareas_ordenadas)
    hora_fin = (datetime.now() + timedelta(minutes=total_minutos)).strftime("%H:%M")
    nivel, titulo_rango, progreso_nivel = obtener_rango(xp_total)


    mensajes = {
        "Alta": "🔥 ¡Energía al máximo! Primero conquistamos las misiones épicas (+150 XP).",
        "Media": "⚡ ¡Ritmo constante! Equilibramos avance rápido con victorias seguras.",
        "Baja": "🔋 ¡Modo inteligente! Empezamos por misiones rápidas para mantener la racha sin cansarte."
    }


    return render_template(
        'index.html',
        tareas=tareas_ordenadas,
        energia=energia,
        total_minutos=total_minutos,
        hora_fin=hora_fin,
        xp=xp_total,
        racha=racha_dias,
        nivel=nivel,
        rango=titulo_rango,
        progreso_nivel=progreso_nivel,
        mensaje=mensajes.get(energia, mensajes["Alta"])
    )

@app.route('/sorpresa')
def sorpresa():
    energia = request.args.get('energia', 'Alta')
    elegida = random.choice(misiones_sorpresa)
    nuevo_id = max([t["id"] for t in tareas], default=0) + 1
    tareas.append({
        "id": nuevo_id,
        "titulo": elegida["titulo"],
        "materia": elegida["materia"],
        "dificultad": elegida["dificultad"],
        "minutos": elegida["minutos"],
        "xp": elegida["xp"]
    })
    return redirect(url_for('index', energia=energia))

@app.route('/completar/<int:tarea_id>')
def completar(tarea_id):
    global tareas, xp_total
    energia = request.args.get('energia', 'Alta')
    for t in tareas:
        if t["id"] == tarea_id:
            xp_total += t.get("xp", 80)
            break
    tareas = [t for t in tareas if t["id"] != tarea_id]
    return redirect(url_for('index', energia=energia))

if __name__ == '__main__':
    app.run(debug=True)