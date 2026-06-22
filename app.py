from flask import Flask, render_template

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
if __name__ == "__main__":
    app.run(debug=True)