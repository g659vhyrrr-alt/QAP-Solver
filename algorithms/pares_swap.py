def validar_datos(flujo, distancia, asignacion):
    if not flujo or not distancia:
        raise ValueError("Las matrices de flujo y distancia no pueden estar vacias.")

    if len(flujo) != len(distancia):
        raise ValueError("Las matrices de flujo y distancia deben tener el mismo tamano.")

    n = len(flujo)

    if len(asignacion) != n:
        raise ValueError("La asignacion inicial debe tener el mismo tamano que las matrices.")

    if sorted(asignacion) != list(range(n)):
        raise ValueError("La asignacion inicial debe ser una permutacion valida.")

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


def evaluar_intercambios(flujo, distancia, asignacion_base, costo_base, ronda):
    evaluaciones = []

    for maquina_i in range(len(asignacion_base)):
        for maquina_j in range(maquina_i + 1, len(asignacion_base)):
            asignacion_prueba = asignacion_base.copy()

            ubicacion_i = asignacion_prueba[maquina_i]
            ubicacion_j = asignacion_prueba[maquina_j]

            asignacion_prueba[maquina_i] = ubicacion_j
            asignacion_prueba[maquina_j] = ubicacion_i

            costo_prueba = calcular_costo(flujo, distancia, asignacion_prueba)
            delta = costo_prueba - costo_base

            evaluaciones.append(
                {
                    "ronda": ronda,
                    "maquina_i": maquina_i,
                    "maquina_j": maquina_j,
                    "ubicacion_i": ubicacion_i,
                    "ubicacion_j": ubicacion_j,
                    "asignacion": asignacion_prueba,
                    "costo": costo_prueba,
                    "delta": delta,
                }
            )

    return evaluaciones


def elegir_mejor_intercambio(evaluaciones):
    mejor = evaluaciones[0]

    for evaluacion in evaluaciones:
        if evaluacion["delta"] < mejor["delta"]:
            mejor = evaluacion

    return mejor


def pares_swap(flujo, distancia, asignacion_inicial):
    validar_datos(flujo, distancia, asignacion_inicial)

    asignacion_actual = asignacion_inicial.copy()
    costo_inicial = calcular_costo(flujo, distancia, asignacion_actual)
    costo_actual = costo_inicial
    evaluaciones_totales = []
    mejoras_aceptadas = []
    mejor_global = None
    ronda = 0
    seguir = True

    while seguir:
        ronda = ronda + 1
        evaluaciones = evaluar_intercambios(
            flujo,
            distancia,
            asignacion_actual,
            costo_actual,
            ronda,
        )
        mejor_ronda = elegir_mejor_intercambio(evaluaciones)

        evaluaciones_totales.extend(evaluaciones)

        if mejor_global is None or mejor_ronda["delta"] < mejor_global["delta"]:
            mejor_global = mejor_ronda

        if mejor_ronda["delta"] < 0:
            asignacion_actual = mejor_ronda["asignacion"].copy()
            costo_actual = mejor_ronda["costo"]
            mejoras_aceptadas.append(mejor_ronda)
        else:
            seguir = False

    porcentaje_mejora = 0

    if costo_inicial > 0:
        porcentaje_mejora = ((costo_inicial - costo_actual) / costo_inicial) * 100

    return {
        "metodo": "swap",
        "criterio": "mejor_mejora",
        "costo_inicial": costo_inicial,
        "asignacion_inicial": asignacion_inicial,
        "asignacion_final": asignacion_actual,
        "costo_final": costo_actual,
        "porcentaje_mejora": porcentaje_mejora,
        "aplicado": len(mejoras_aceptadas) > 0,
        "mejor": mejor_global,
        "mejoras_aceptadas": mejoras_aceptadas,
        "evaluaciones": evaluaciones_totales,
        "rondas": ronda,
    }
