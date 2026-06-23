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


def calcular_flujos_acumulados(flujo):
    flujos_acumulados = []

    for i in range(len(flujo)):
        suma = 0

        for j in range(len(flujo)):
            if i != j:
                suma = suma + flujo[i][j]

        flujos_acumulados.append(suma)

    return flujos_acumulados


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


def mayores_flujos(flujo, distancia):
    validar_matrices(flujo, distancia)

    n = len(flujo)
    asignacion = [-1] * n
    flujos_acumulados = calcular_flujos_acumulados(flujo)

    mayor_flujo = max(flujos_acumulados)
    maquina_semilla = flujos_acumulados.index(mayor_flujo)

    asignacion[maquina_semilla] = 0
    pasos = []

    while -1 in asignacion:
        ubicadas = []
        restantes = []

        for maquina in range(n):
            if asignacion[maquina] != -1:
                ubicadas.append(maquina)
            else:
                restantes.append(maquina)

        interacciones = []

        for maquina in restantes:
            suma_interaccion = 0

            for maquina_ubicada in ubicadas:
                suma_interaccion = suma_interaccion + flujo[maquina][maquina_ubicada]

            interacciones.append(
                {
                    "maquina": maquina,
                    "suma": suma_interaccion,
                }
            )

        mayor_interaccion = -1
        siguiente_maquina = -1

        for interaccion in interacciones:
            if interaccion["suma"] > mayor_interaccion:
                mayor_interaccion = interaccion["suma"]
                siguiente_maquina = interaccion["maquina"]

        ubicaciones_vacias = []

        for ubicacion in range(n):
            if ubicacion not in asignacion:
                ubicaciones_vacias.append(ubicacion)

        costos = []

        for ubicacion_prueba in ubicaciones_vacias:
            costo_incremental = 0
            productos = []

            for maquina_ubicada in ubicadas:
                ubicacion_asignada = asignacion[maquina_ubicada]
                producto = (
                    flujo[siguiente_maquina][maquina_ubicada]
                    * distancia[ubicacion_prueba][ubicacion_asignada]
                )

                productos.append(producto)
                costo_incremental = costo_incremental + producto

            costos.append(
                {
                    "ubicacion": ubicacion_prueba,
                    "costo": costo_incremental,
                    "productos": productos,
                }
            )

        menor_costo = costos[0]["costo"]
        mejor_ubicacion = costos[0]["ubicacion"]

        for costo in costos:
            if costo["costo"] < menor_costo:
                menor_costo = costo["costo"]
                mejor_ubicacion = costo["ubicacion"]

        asignacion_antes = asignacion.copy()
        asignacion[siguiente_maquina] = mejor_ubicacion

        pasos.append(
            {
                "ubicadas_antes": ubicadas,
                "restantes_antes": restantes,
                "interacciones": interacciones,
                "maquina_elegida": siguiente_maquina,
                "mayor_interaccion": mayor_interaccion,
                "ubicaciones_vacias": ubicaciones_vacias,
                "costos": costos,
                "mejor_ubicacion": mejor_ubicacion,
                "menor_costo": menor_costo,
                "asignacion_antes": asignacion_antes,
                "asignacion_despues": asignacion.copy(),
            }
        )

    costo_total = calcular_costo(flujo, distancia, asignacion)

    return {
        "metodo": "mayores_flujos",
        "asignacion": asignacion,
        "costo_total": costo_total,
        "flujos_acumulados": flujos_acumulados,
        "maquina_semilla": maquina_semilla,
        "mayor_flujo": mayor_flujo,
        "pasos": pasos,
    }
