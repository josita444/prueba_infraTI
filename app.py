from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


tareas = [
    {
        "id": 1,
        "titulo": "Resolver guía de algoritmos y estructuras",
        "materia": "Programación",
        "dificultad": "Alta",
        "minutos": 50
    },
    {
        "id": 2,
        "titulo": "Repasar flujo de ramas main y develop en Git",
        "materia": "Infraestructura TI",
        "dificultad": "Media",
        "minutos": 25
    },
    {
        "id": 3,
        "titulo": "Ordenar apuntes y subir enlaces a GitHub",
        "materia": "Documentación",
        "dificultad": "Baja",
        "minutos": 15
    }
]


def calcular_prioridad(dificultad, minutos, energia):
    pesos = {"Alta": 3, "Media": 2, "Baja": 1}
    base = pesos.get(dificultad, 1) * 25
    if energia == "Alta" and dificultad == "Alta":
        base += 25
    elif energia == "Media" and dificultad == "Media":
        base += 20
    elif energia == "Baja" and dificultad == "Baja":
        base += 30
    return min(base + (minutos // 10), 100)


@app.route('/', methods=['GET', 'POST'])
def index():
    energia_actual = request.args.get('energia', 'Alta')


    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        materia = request.form.get('materia', 'General').strip()
        dificultad = request.form.get('dificultad', 'Media')
        minutos = int(request.form.get('minutos', 25))
        energia_actual = request.form.get('energia_usuario', 'Alta')


        if titulo:
            nuevo_id = max([t["id"] for t in tareas], default=0) + 1
            tareas.append({
                "id": nuevo_id,
                "titulo": titulo,
                "materia": materia,
                "dificultad": dificultad,
                "minutos": minutos
            })
        return redirect(url_for('index', energia=energia_actual))


    tareas_ordenadas = sorted(
        tareas,
        key=lambda t: calcular_prioridad(t["dificultad"], t["minutos"], energia_actual),
        reverse=True
    )


    total_minutos = sum(t["minutos"] for t in tareas_ordenadas)
    pomodoros = max(1, round(total_minutos / 25)) if total_minutos > 0 else 0
    descansos = max(0, (pomodoros - 1) * 5)
    hora_fin = (datetime.now() + timedelta(minutes=total_minutos + descansos)).strftime("%H:%M")


    consejos = {
        "Alta": "Estás al 100%. Atacaremos primero lo más difícil antes de que baje tu concentración.",
        "Media": "Ritmo equilibrado. Combinamos práctica constante con bloques de descanso corto.",
        "Baja": "Modo recuperación. Empezamos con tareas ligeras para ganar impulso sin agotarte."
    }


    return render_template(
        'index.html',
        tareas=tareas_ordenadas,
        energia=energia_actual,
        total_minutos=total_minutos,
        pomodoros=pomodoros,
        hora_fin=hora_fin,
        consejo=consejos.get(energia_actual, consejos["Alta"])
    )


@app.route('/eliminar/<int:tarea_id>')
def eliminar(tarea_id):
    global tareas
    energia_actual = request.args.get('energia', 'Alta')
    tareas = [t for t in tareas if t["id"] != tarea_id]
    return redirect(url_for('index', energia=energia_actual))


if __name__ == '__main__':
    app.run(debug=True)