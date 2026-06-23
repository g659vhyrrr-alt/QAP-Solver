from flask import Flask, jsonify, render_template, request

from algorithms.busqueda_local import busqueda_local
from algorithms.construccion_aleatorizada import construccion_aleatorizada
from algorithms.mayores_flujos import mayores_flujos
from algorithms.pares_swap import pares_swap

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/heuristicos")
def heuristicos():
    return render_template("heuristicos.html")


@app.route("/matrices-mayores-flujos")
def matrices_mayores_flujos():
    return render_template("matrices_mayores_flujos.html")


@app.route("/matrices-aleatorizada")
def matrices_aleatorizada():
    return render_template("matrices_aleatorizada.html")

@app.route("/cargar")
def cargar():
    return render_template("cargar.html")

@app.route("/ejemplo")
def ejemplo():
    return render_template("ejemplo.html")


@app.route("/solucion-inicial")
def solucion_inicial():
    return render_template("solucion_inicial.html")


@app.route("/mejora")
def mejora():
    return render_template("mejora.html")


@app.route("/resultados")
def resultados():
    return render_template("resultados.html")


@app.route("/api/solucion-inicial", methods=["POST"])
def api_solucion_inicial():
    datos = request.get_json(silent=True) or {}

    metodo = datos.get("metodo")
    flujo = datos.get("flujo")
    distancia = datos.get("distancia")
    iteraciones = datos.get("iteraciones", 10)

    if metodo not in ("mayores_flujos", "aleatorizada"):
        return jsonify({"error": "Metodo de construccion no valido."}), 400

    if flujo is None or distancia is None:
        return jsonify({"error": "Debes enviar matriz de flujo y distancia."}), 400

    try:
        if metodo == "mayores_flujos":
            resultado = mayores_flujos(flujo, distancia)
        else:
            resultado = construccion_aleatorizada(
                flujo,
                distancia,
                iteraciones=int(iteraciones),
            )

        return jsonify(resultado)

    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400


@app.route("/api/mejora", methods=["POST"])
def api_mejora():
    datos = request.get_json(silent=True) or {}

    metodo = datos.get("metodo")
    flujo = datos.get("flujo")
    distancia = datos.get("distancia")
    asignacion_inicial = datos.get("asignacion_inicial")
    max_iteraciones = datos.get("max_iteraciones")

    if metodo not in ("swap", "busqueda_local"):
        return jsonify({"error": "Metodo de mejora no valido."}), 400

    if flujo is None or distancia is None or asignacion_inicial is None:
        return jsonify(
            {
                "error": (
                    "Debes enviar matriz de flujo, matriz de distancia "
                    "y asignacion inicial."
                )
            }
        ), 400

    try:
        if metodo == "swap":
            resultado = pares_swap(flujo, distancia, asignacion_inicial)
        else:
            if max_iteraciones is None:
                resultado = busqueda_local(flujo, distancia, asignacion_inicial)
            else:
                resultado = busqueda_local(
                    flujo,
                    distancia,
                    asignacion_inicial,
                    max_iteraciones=int(max_iteraciones),
                )

        return jsonify(resultado)

    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
