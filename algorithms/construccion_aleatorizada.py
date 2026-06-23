import random


def validar_matrices(flujo, distancia):
    if not flujo or not distancia:
        raise ValueError("Las matrices de flujo y distancia no pueden estar vacias.")

    if len(flujo) != len(distancia):
        raise ValueError("Las matrices de flujo y distancia deben tener el mismo tamano.")

    n = len(flujo)

    for nombre, matriz in (("flujo", flujo), ("distancia", distancia)):
        if len(matriz) != n:
            raise ValueError(f"La matriz de {nombre} debe ser cuadrada.")

        for fila in matriz:
            if len(fila) != n:
                raise ValueError(f"La matriz de {nombre} debe ser cuadrada.")

            for valor in fila:
                if not isinstance(valor, (int, float)):
                    raise ValueError(
                        f"La matriz de {nombre} solo debe contener numeros."
                    )


def calcular_costo(flujo, distancia, asignacion):
    maquina_por_ubicacion = []

    for ubicacion in range(len(asignacion)):
        maquina_por_ubicacion.append(asignacion.index(ubicacion))

    costo_total = 0

    for ubicacion_i in range(len(maquina_por_ubicacion)):
        for ubicacion_j in range(ubicacion_i + 1, len(maquina_por_ubicacion)):
            maquina_i = maquina_por_ubicacion[ubicacion_i]
            maquina_j = maquina_por_ubicacion[ubicacion_j]

            costo_total = (
                costo_total
                + flujo[maquina_i][maquina_j] * distancia[ubicacion_i][ubicacion_j]
            )

    return costo_total


def generar_asignacion_aleatoria(n, generador):
    ubicaciones_disponibles = list(range(n))
    asignacion = [-1] * n
    pasos = []

    for maquina in range(n):
        disponibles_antes = ubicaciones_disponibles.copy()
        indice_aleatorio = generador.randint(0, len(ubicaciones_disponibles) - 1)
        ubicacion_elegida = ubicaciones_disponibles[indice_aleatorio]

        asignacion[maquina] = ubicacion_elegida
        ubicaciones_disponibles.pop(indice_aleatorio)

        pasos.append(
            {
                "maquina": maquina,
                "ubicacion": ubicacion_elegida,
                "disponibles_antes": disponibles_antes,
                "disponibles_despues": ubicaciones_disponibles.copy(),
                "indice_aleatorio": indice_aleatorio,
            }
        )

    return asignacion, pasos


def construccion_aleatorizada(flujo, distancia, iteraciones=10, semilla=None):
    validar_matrices(flujo, distancia)

    if iteraciones < 1:
        raise ValueError("El numero de iteraciones debe ser mayor o igual a 1.")

    n = len(flujo)
    generador = random.Random(semilla)
    historial = []
    mejor_resultado = None

    for iteracion in range(1, iteraciones + 1):
        asignacion, pasos = generar_asignacion_aleatoria(n, generador)
        costo_total = calcular_costo(flujo, distancia, asignacion)

        resultado_iteracion = {
            "iteracion": iteracion,
            "asignacion": asignacion,
            "costo_total": costo_total,
            "pasos": pasos,
        }

        historial.append(resultado_iteracion)

        if mejor_resultado is None or costo_total < mejor_resultado["costo_total"]:
            mejor_resultado = resultado_iteracion

    return {
        "metodo": "construccion_aleatorizada",
        "iteraciones": iteraciones,
        "mejor_iteracion": mejor_resultado["iteracion"],
        "asignacion": mejor_resultado["asignacion"],
        "costo_total": mejor_resultado["costo_total"],
        "pasos": mejor_resultado["pasos"],
        "historial": historial,
    }
