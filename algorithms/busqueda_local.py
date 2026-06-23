from algorithms.pares_swap import (
    calcular_costo,
    elegir_mejor_intercambio,
    evaluar_intercambios,
    validar_datos,
)


def busqueda_local(flujo, distancia, asignacion_inicial, max_iteraciones=None):
    validar_datos(flujo, distancia, asignacion_inicial)

    if max_iteraciones is not None and max_iteraciones < 1:
        raise ValueError("El numero maximo de iteraciones debe ser mayor o igual a 1.")

    asignacion_actual = asignacion_inicial.copy()
    costo_inicial = calcular_costo(flujo, distancia, asignacion_actual)
    costo_actual = costo_inicial

    evaluaciones_totales = []
    mejoras_aceptadas = []
    historial = []
    mejor_global = None

    ronda = 0
    seguir = True

    while seguir:
        if max_iteraciones is not None and ronda >= max_iteraciones:
            break

        ronda = ronda + 1

        evaluaciones = evaluar_intercambios(
            flujo,
            distancia,
            asignacion_actual,
            costo_actual,
            ronda,
        )

        mejor_vecino = elegir_mejor_intercambio(evaluaciones)
        evaluaciones_totales.extend(evaluaciones)

        historial.append(
            {
                "ronda": ronda,
                "asignacion_base": asignacion_actual.copy(),
                "costo_base": costo_actual,
                "mejor_vecino": mejor_vecino,
            }
        )

        if mejor_global is None or mejor_vecino["delta"] < mejor_global["delta"]:
            mejor_global = mejor_vecino

        if mejor_vecino["delta"] < 0:
            asignacion_actual = mejor_vecino["asignacion"].copy()
            costo_actual = mejor_vecino["costo"]
            mejoras_aceptadas.append(mejor_vecino)
        else:
            seguir = False

    porcentaje_mejora = 0

    if costo_inicial > 0:
        porcentaje_mejora = ((costo_inicial - costo_actual) / costo_inicial) * 100

    if max_iteraciones is not None and ronda >= max_iteraciones and seguir:
        criterio_parada = "max_iteraciones"
    else:
        criterio_parada = "sin_mejora"

    return {
        "metodo": "busqueda_local",
        "vecindario": "intercambio_pares",
        "criterio": "mejor_mejora",
        "criterio_parada": criterio_parada,
        "costo_inicial": costo_inicial,
        "asignacion_inicial": asignacion_inicial,
        "asignacion_final": asignacion_actual,
        "costo_final": costo_actual,
        "porcentaje_mejora": porcentaje_mejora,
        "aplicado": len(mejoras_aceptadas) > 0,
        "mejor": mejor_global,
        "mejoras_aceptadas": mejoras_aceptadas,
        "evaluaciones": evaluaciones_totales,
        "historial": historial,
        "rondas": ronda,
    }
