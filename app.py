from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Tareas iniciales precargadas para demostrar el funcionamiento al iniciar
tareas = [
    {
        "id": 1,
        "titulo": "Resolver guía de algoritmos y estructuras",
        "materia": "Programación",
        "dificultad": "Alta",
        "minutos": 50,
        "puntaje_prioridad": 95
    },
    {
        "id": 2,
        "titulo": "Repasar flujo de ramas main y develop en Git",
        "materia": "Infraestructura TI",
        "dificultad": "Media",
        "minutos": 25,
        "puntaje_prioridad": 70
    }
]

def calcular_prioridad(dificultad, minutos, energia):
    pesos = {"Alta": 3, "Media": 2, "Baja": 1}
    base = pesos.get(dificultad, 1) * 25
    if energia == "Alta" and dificultad == "Alta":
        base += 20
    elif energia == "Baja" and dificultad == "Baja":
        base += 25
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
            prioridad = calcular_prioridad(dificultad, minutos, energia_actual)
            tareas.append({
                "id": nuevo_id,
                "titulo": titulo,
                "materia": materia,
                "dificultad": dificultad,
                "minutos": minutos,
                "puntaje_prioridad": prioridad
            })
        return redirect(url_for('index', energia=energia_actual))

    tareas_ordenadas = sorted(
        tareas,
        key=lambda t: calcular_prioridad(t["dificultad"], t["minutos"], energia_actual),
        reverse=True
    )

    total_minutos = sum(t["minutos"] for t in tareas_ordenadas)
    pomodoros = round(total_minutos / 25, 1)

    return render_template(
        'index.html',
        tareas=tareas_ordenadas,
        energia=energia_actual,
        total_minutos=total_minutos,
        pomodoros=pomodoros
    )

@app.route('/eliminar/<int:tarea_id>')
def eliminar(tarea_id):
    global tareas
    tareas = [t for t in tareas if t["id"] != tarea_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)