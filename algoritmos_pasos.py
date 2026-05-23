import heapq
from collections import deque

# ─────────────────────────────────────────────────────────────────────────────
# Módulo de trazado de pasos para el visualizador
# Cada función devuelve una lista de "pasos" (dicts) que describen qué nodo
# se expandió, qué hijos generó, el costo acumulado, la frontera, etc.
# Tu algoritmos.py original NO se modifica.
# ─────────────────────────────────────────────────────────────────────────────

def _aristas(grafo: dict) -> list[dict]:
    """Construye lista de aristas únicas para el visualizador."""
    vistas = set()
    aristas = []
    for origen, vecinos in grafo.items():
        for destino, costo in vecinos:
            clave = (origen, destino)
            if clave not in vistas:
                vistas.add(clave)
                aristas.append({"from": origen, "to": destino, "cost": costo})
    return aristas


def bfs_pasos(inicio: str, meta: str, grafo: dict) -> dict:
    cola = deque([(inicio, [inicio], 0)])
    visitados = set([inicio])
    frontera = [inicio]
    pasos = []

    while cola:
        actual, camino, g = cola.popleft()
        frontera = [n for n in frontera if n != actual]

        hijos_generados = []
        costos_hijos = {}
        for vecino, costo in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                nuevo_g = g + costo
                cola.append((vecino, camino + [vecino], nuevo_g))
                frontera.append(vecino)
                hijos_generados.append(vecino)
                costos_hijos[vecino] = nuevo_g

        pasos.append({
            "nodo": actual,
            "hijos": hijos_generados,
            "costos_hijos": costos_hijos,
            "camino_actual": list(camino),
            "visitados": list(visitados),
            "frontera": list(frontera),
            "g": g,
            "es_meta": actual == meta,
        })

        if actual == meta:
            break

    return {"pasos": pasos, "aristas": _aristas(grafo)}


def dfs_pasos(inicio: str, meta: str, grafo: dict) -> dict:
    pila = [(inicio, [inicio], 0)]
    visitados = set()
    pasos = []

    while pila:
        actual, camino, g = pila.pop()
        if actual in visitados:
            continue
        visitados.add(actual)

        hijos_generados = []
        costos_hijos = {}
        for vecino, costo in reversed(grafo.get(actual, [])):
            if vecino not in visitados:
                nuevo_g = g + costo
                pila.append((vecino, camino + [vecino], nuevo_g))
                hijos_generados.append(vecino)
                costos_hijos[vecino] = nuevo_g

        frontera = [item[0] for item in reversed(pila)]

        pasos.append({
            "nodo": actual,
            "hijos": hijos_generados,
            "costos_hijos": costos_hijos,
            "camino_actual": list(camino),
            "visitados": list(visitados),
            "frontera": frontera,
            "g": g,
            "es_meta": actual == meta,
        })

        if actual == meta:
            break

    return {"pasos": pasos, "aristas": _aristas(grafo)}


def ucs_pasos(inicio: str, meta: str, grafo: dict) -> dict:
    heap = [(0, inicio, [inicio])]
    visitados = {}
    pasos = []

    while heap:
        costo, actual, camino = heapq.heappop(heap)

        if actual in visitados and visitados[actual] <= costo:
            continue
        visitados[actual] = costo

        hijos_generados = []
        costos_hijos = {}
        for vecino, peso in grafo.get(actual, []):
            nuevo_costo = costo + peso
            if vecino not in visitados or visitados[vecino] > nuevo_costo:
                heapq.heappush(heap, (nuevo_costo, vecino, camino + [vecino]))
                hijos_generados.append(vecino)
                costos_hijos[vecino] = nuevo_costo

        frontera = sorted(set(item[1] for item in heap), key=lambda n: next(i[0] for i in heap if i[1] == n))

        pasos.append({
            "nodo": actual,
            "hijos": hijos_generados,
            "costos_hijos": costos_hijos,
            "camino_actual": list(camino),
            "visitados": list(visitados.keys()),
            "frontera": frontera,
            "g": costo,
            "es_meta": actual == meta,
        })

        if actual == meta:
            break

    return {"pasos": pasos, "aristas": _aristas(grafo)}


def dls_pasos(inicio: str, meta: str, grafo: dict, limite: int) -> dict:
    pasos = []

    def dfs(nodo: str, profundidad: int, camino: list):
        hijos_validos = [v for v, _ in grafo.get(nodo, []) if v not in camino]
        es_corte = profundidad == limite and nodo != meta

        pasos.append({
            "nodo": nodo,
            "hijos": hijos_validos if not es_corte else [],
            "costos_hijos": {},
            "camino_actual": list(camino),
            "visitados": list(camino),
            "frontera": hijos_validos,
            "g": profundidad,
            "depth": profundidad,
            "limite": limite,
            "es_meta": nodo == meta,
            "corte": es_corte,
        })

        if nodo == meta:
            return True
        if es_corte:
            return False

        for vecino, _ in grafo.get(nodo, []):
            if vecino not in camino:
                if dfs(vecino, profundidad + 1, camino + [vecino]):
                    return True
        return False

    dfs(inicio, 0, [inicio])
    return {"pasos": pasos, "aristas": _aristas(grafo)}


def iddfs_pasos(inicio: str, meta: str, grafo: dict, limite_max: int = 15) -> dict:
    todos_pasos = []
    aristas = _aristas(grafo)

    for limite in range(limite_max + 1):
        pasos_iter = []

        def dfs(nodo: str, profundidad: int, camino: list):
            hijos_validos = [v for v, _ in grafo.get(nodo, []) if v not in camino]
            es_corte = profundidad == limite and nodo != meta

            pasos_iter.append({
                "nodo": nodo,
                "hijos": hijos_validos if not es_corte else [],
                "costos_hijos": {},
                "camino_actual": list(camino),
                "visitados": list(camino),
                "frontera": hijos_validos,
                "g": profundidad,
                "depth": profundidad,
                "limite": limite,
                "iddfs_iter": limite,
                "es_meta": nodo == meta,
                "corte": es_corte,
            })

            if nodo == meta:
                return True
            if es_corte:
                return False
            for vecino, _ in grafo.get(nodo, []):
                if vecino not in camino:
                    if dfs(vecino, profundidad + 1, camino + [vecino]):
                        return True
            return False

        encontrado = dfs(inicio, 0, [inicio])
        todos_pasos.extend(pasos_iter)

        if encontrado:
            break
        else:
            todos_pasos.append({
                "separador": True,
                "iddfs_iter": limite,
                "mensaje": f"Límite {limite} agotado — aumentando a {limite + 1}",
            })

    return {"pasos": todos_pasos, "aristas": aristas}


def avara_pasos(inicio: str, meta: str, grafo: dict, heuristica: dict) -> dict:
    heap = [(heuristica.get(inicio, 0), inicio, [inicio])]
    visitados = set()
    pasos = []

    while heap:
        h, actual, camino = heapq.heappop(heap)
        if actual in visitados:
            continue
        visitados.add(actual)

        hijos_generados = []
        costos_hijos = {}
        for vecino, _ in grafo.get(actual, []):
            if vecino not in visitados:
                h_vecino = heuristica.get(vecino, 0)
                heapq.heappush(heap, (h_vecino, vecino, camino + [vecino]))
                hijos_generados.append(vecino)
                costos_hijos[vecino] = h_vecino

        frontera = [item[1] for item in sorted(heap, key=lambda x: x[0])]

        pasos.append({
            "nodo": actual,
            "hijos": hijos_generados,
            "costos_hijos": costos_hijos,
            "camino_actual": list(camino),
            "visitados": list(visitados),
            "frontera": frontera,
            "g": h,
            "h": h,
            "es_meta": actual == meta,
        })

        if actual == meta:
            break

    return {"pasos": pasos, "aristas": _aristas(grafo)}


def a_estrella_pasos(inicio: str, meta: str, grafo: dict, heuristica: dict) -> dict:
    heap = [(heuristica.get(inicio, 0), 0, inicio, [inicio])]
    costo_min = {inicio: 0}
    visitados = set()
    pasos = []

    while heap:
        f, g, actual, camino = heapq.heappop(heap)

        if actual in visitados:
            continue
        if g > costo_min.get(actual, float('inf')):
            continue
        visitados.add(actual)

        hijos_generados = []
        costos_hijos = {}
        for vecino, peso in grafo.get(actual, []):
            nuevo_g = g + peso
            if nuevo_g < costo_min.get(vecino, float('inf')):
                costo_min[vecino] = nuevo_g
                nuevo_f = nuevo_g + heuristica.get(vecino, 0)
                heapq.heappush(heap, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
                hijos_generados.append(vecino)
                costos_hijos[vecino] = nuevo_g

        frontera = [item[2] for item in sorted(heap, key=lambda x: x[0])]

        pasos.append({
            "nodo": actual,
            "hijos": hijos_generados,
            "costos_hijos": costos_hijos,
            "camino_actual": list(camino),
            "visitados": list(visitados),
            "frontera": frontera,
            "g": g,
            "f": round(f, 4),
            "h": heuristica.get(actual, 0),
            "es_meta": actual == meta,
        })

        if actual == meta:
            break

    return {"pasos": pasos, "aristas": _aristas(grafo)}
