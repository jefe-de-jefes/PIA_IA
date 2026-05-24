import heapq
from collections import deque


def _costo_camino(camino, grafo):
    total = 0
    for i in range(len(camino) - 1):
        for vecino, peso in grafo.get(camino[i], []):
            if vecino == camino[i + 1]:
                total += peso
                break
    return total


def _imprimir_pasos(pasos, camino, grafo=None, mostrar_costo=False, etiqueta_costo='Nivel', mostrar_f=False, mostrar_saltos=False):
    if mostrar_saltos and mostrar_costo:
        col_header = f"{'Saltos':<8} {etiqueta_costo}"
    elif mostrar_costo:
        col_header = etiqueta_costo
    else:
        col_header = 'Saltos'

    print(f"\n  {'#':<5} {'Nodo expandido':<22} {'Hijos expandidos':<30} {col_header}")
    print(f"  {'-'*4} {'-'*21} {'-'*29} {'-'*16}")

    for i, paso in enumerate(pasos, 1):
        nodo      = paso[0]
        hijos     = paso[1]
        valor     = paso[2]
        es_meta   = paso[3]
        costo_r   = paso[4] if len(paso) > 4 else None
        f_val     = paso[5] if mostrar_f and len(paso) > 5 else None

        hijos_str = ', '.join(str(h) for h in hijos) if hijos else '—'
        marca     = '★' if es_meta else ' '

        if mostrar_saltos and mostrar_costo and costo_r is not None:
            extra = f"{int(valor):<8} {costo_r:.1f}"
        elif mostrar_costo:
            extra = f"{valor:.1f}"
            if f_val is not None:
                extra += f"  (f={f_val:.1f})"
        else:
            extra = str(int(valor))

        print(f"  {marca}{i:<4} {nodo:<22} {hijos_str:<30} {extra}")

    costo_final = _costo_camino(camino, grafo) if grafo else pasos[-1][2]
    saltos      = len(camino) - 1

    print(f"\n  Camino final : {' -> '.join(camino)}")
    print(f"  Costo total  : {costo_final:.1f}")
    if mostrar_saltos:
        print(f"  Saltos       : {saltos}")
    print()


def amplitud_bfs(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], verbose=False) -> list[str] | None:
    cola:deque[tuple[str, list[str]]] = deque([(inicio, [inicio])])
    visitados:set[str] = set([inicio])
    pasos = []

    while cola:
        actual, camino = cola.popleft()

        if actual == meta:
            costo_r = _costo_camino(camino, grafo)
            pasos.append((actual, [], len(camino) - 1, True, costo_r))
            if verbose:
                _imprimir_pasos(pasos, camino, grafo, mostrar_saltos=True, mostrar_costo=True)
            return camino

        hijos = []
        for vecino, _ in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
                hijos.append(vecino)
        costo_r = _costo_camino(camino, grafo)
        pasos.append((actual, hijos, len(camino) - 1, False, costo_r))

    return None


def costo_uniforme_ucs(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], verbose=False) -> tuple[list[str] | None, float]:
    heap:list[tuple[float, str, list[str]]] = [(0, inicio, [inicio])]
    visitados:dict[str, float] = {}
    pasos = []

    while heap:
        costo, actual, camino = heapq.heappop(heap)

        if actual == meta:
            pasos.append((actual, [], costo, True))
            if verbose:
                _imprimir_pasos(pasos, camino, mostrar_costo=True, etiqueta_costo='g(n)')
            return camino, costo

        if actual in visitados and visitados[actual] <= costo:
            continue
        visitados[actual] = costo

        hijos = []
        for vecino, peso in grafo.get(actual, []):
            nuevo_costo:float = costo + peso
            if vecino not in visitados or visitados[vecino] > nuevo_costo:
                heapq.heappush(heap, (nuevo_costo, vecino, camino + [vecino]))
                hijos.append(vecino)
        pasos.append((actual, hijos, costo, False))

    return None, float('inf')


def profundidad_dfs(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], verbose=False) -> list[str] | None:
    pila:list[tuple[str, list[str]]] = [(inicio, [inicio])]
    visitados:set[str] = set()
    pasos = []

    while pila:
        actual, camino = pila.pop()

        if actual in visitados:
            continue
        visitados.add(actual)

        if actual == meta:
            costo_r = _costo_camino(camino, grafo)
            pasos.append((actual, [], len(camino) - 1, True, costo_r))
            if verbose:
                _imprimir_pasos(pasos, camino, grafo, mostrar_saltos=True, mostrar_costo=True)
            return camino

        hijos = []
        for vecino, _ in reversed(grafo.get(actual, [])):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))
                hijos.append(vecino)
        costo_r = _costo_camino(camino, grafo)
        pasos.append((actual, hijos, len(camino) - 1, False, costo_r))

    return None


def profundidad_limitada_dls(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], limite:int, verbose=False) -> tuple[list[str] | None, int | None]:
    pasos = []

    def dfs(nodo:str, profundidad:int, camino:list[str]):
        if nodo == meta:
            costo_r = _costo_camino(camino, grafo)
            pasos.append((nodo, [], profundidad, True, costo_r))
            return camino, profundidad

        if profundidad == limite:
            pasos.append((nodo, ['[límite]'], profundidad, False, 0))
            return None

        hijos = [v for v, _ in grafo.get(nodo, []) if v not in camino]
        costo_r = _costo_camino(camino, grafo)
        pasos.append((nodo, hijos, profundidad, False, costo_r))

        for vecino, _ in grafo.get(nodo, []):
            if vecino not in camino:
                resultado = dfs(vecino, profundidad + 1, camino + [vecino])
                if resultado:
                    return resultado
        return None

    resultado = dfs(inicio, 0, [inicio])
    if verbose and resultado:
        _imprimir_pasos(pasos, resultado[0], grafo, mostrar_saltos=True, mostrar_costo=True, etiqueta_costo='Prof.')
    if resultado:
        return resultado
    return None, None


def profundidad_iterativa_iddfs(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], limite_max=50, verbose=False) -> tuple[list[str] | None, int]:
    for limite in range(limite_max + 1):
        if verbose:
            print(f"  [IDDFS] Probando limite = {limite}...")
        resultado, _ = profundidad_limitada_dls(inicio, meta, grafo, limite)
        if resultado is not None:
            if verbose:
                profundidad_limitada_dls(inicio, meta, grafo, limite, verbose=True)
            return resultado, limite
    return None, -1


def busqueda_avara(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], heuristica:dict[str, float], verbose=False) -> list[str] | None:
    heap:list[tuple[float, str, list[str]]] = [(heuristica.get(inicio, 0), inicio, [inicio])]
    visitados:set[str] = set()
    pasos = []

    while heap:
        h, actual, camino = heapq.heappop(heap)

        if actual in visitados:
            continue
        visitados.add(actual)

        if actual == meta:
            costo_r = _costo_camino(camino, grafo)
            pasos.append((actual, [], h, True, costo_r))
            if verbose:
                _imprimir_pasos(pasos, camino, grafo, mostrar_costo=True, etiqueta_costo='h(n)')
            return camino

        hijos = []
        for vecino, _ in grafo.get(actual, []):
            if vecino not in visitados:
                h_vecino = heuristica.get(vecino, 0)
                heapq.heappush(heap, (h_vecino, vecino, camino + [vecino]))
                hijos.append(vecino)
        costo_r = _costo_camino(camino, grafo)
        pasos.append((actual, hijos, h, False, costo_r))

    return None


def busqueda_a_estrella(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], heuristica:dict[str, float], verbose=False):
    heap:list[tuple[float, float, str, list[str]]] = [(heuristica.get(inicio, 0), 0, inicio, [inicio])]
    costo_min:dict[str, float] = {inicio: 0}
    pasos = []

    while heap:
        f, g, actual, camino = heapq.heappop(heap)

        if actual == meta:
            pasos.append((actual, [], g, True, g, f))
            if verbose:
                _imprimir_pasos(pasos, camino, mostrar_costo=True, etiqueta_costo='g(n)', mostrar_f=True)
            return camino, g

        if g > costo_min.get(actual, float('inf')):
            continue

        hijos = []
        for vecino, peso in grafo.get(actual, []):
            nuevo_g = g + peso
            if nuevo_g < costo_min.get(vecino, float('inf')):
                costo_min[vecino] = nuevo_g
                nuevo_f = nuevo_g + heuristica.get(vecino, 0)
                heapq.heappush(heap, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
                hijos.append(vecino)
        pasos.append((actual, hijos, g, False, g, f))

    return None, float('inf')
