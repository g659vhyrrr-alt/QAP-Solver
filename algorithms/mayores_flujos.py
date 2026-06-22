def mayores_flujos(flujo, distancia):

    n = len(flujo)

    asignacion = [-1] * n

    flujos_acumulados = []

    for i in range(n):

        suma = 0

        for j in range(n):
            suma = suma + flujo[i][j]

        flujos_acumulados.append(suma)

    mayor = max(flujos_acumulados)

    instalacion_semilla = flujos_acumulados.index(mayor)

    asignacion[instalacion_semilla] = 0

    return asignacion