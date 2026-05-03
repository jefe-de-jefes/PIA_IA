import heapq
from collections import deque
 
# 1. BÚSQUEDA POR AMPLITUD (BFS)
def amplitud_bfs(inicio, meta, grafo):
    """
    Explora nodo a nodo en capas (nivel por nivel).
    Usa una cola FIFO. Garantiza el camino con menos
    pasos (no necesariamente el de menor costo).
    """
    cola = deque([(inicio, [inicio])])
    visitados = set([inicio])
 
    while cola:
        actual, camino = cola.popleft()
 
        if actual == meta:
            return camino
 
        for vecino, _ in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
 
    return None  # No se encontró camino
 
 
def costo_uniforme_ucs(inicio, meta, grafo):
    """
    Expande siempre el nodo con menor costo acumulado g(n).
    Usa una cola de prioridad (min-heap).
    Garantiza el camino de menor costo total.
    """
    # heap: (costo_acumulado, nodo_actual, camino)
    heap = [(0, inicio, [inicio])]
    visitados = {}  # nodo -> menor costo conocido
 
    while heap:
        costo, actual, camino = heapq.heappop(heap)
 
        if actual == meta:
            return camino, costo
 
        # Si ya visitamos este nodo con menor costo, lo saltamos
        if actual in visitados and visitados[actual] <= costo:
            continue
        visitados[actual] = costo
 
        for vecino, peso in grafo.get(actual, []):
            nuevo_costo = costo + peso
            if vecino not in visitados or visitados[vecino] > nuevo_costo:
                heapq.heappush(heap, (nuevo_costo, vecino, camino + [vecino]))
 
    return None, float('inf')  # No se encontró camino
 
 
def profundidad_dfs(inicio, meta, grafo):
    """
    Explora tan profundo como sea posible antes de retroceder.
    Usa una pila (stack). NO garantiza el camino óptimo.
    Puede no terminar en grafos con ciclos si no se controlan visitados.
    """
    pila = [(inicio, [inicio])]
    visitados = set()
 
    while pila:
        actual, camino = pila.pop()  # LIFO
 
        if actual in visitados:
            continue
        visitados.add(actual)
 
        if actual == meta:
            return camino
 
        # Se agregan en orden inverso para expandir en orden natural
        for vecino, _ in reversed(grafo.get(actual, [])):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))
 
    return None  # No se encontró camino
 
 
# ─────────────────────────────────────────────
# 4. BÚSQUEDA POR PROFUNDIDAD LIMITADA (DLS)
# ─────────────────────────────────────────────
def profundidad_limitada_dls(inicio, meta, grafo, limite):
    """
    DFS con un límite máximo de profundidad.
    Evita explorar más allá del nivel 'limite'.
    Retorna el camino o None si no encuentra solución dentro del límite.
    """
    def _dls_recursivo(nodo, meta, grafo, limite, camino, visitados):
        if nodo == meta:
            return camino
 
        if limite == 0:
            return None  # Límite alcanzado, no se puede seguir
 
        visitados.add(nodo)
        for vecino, _ in grafo.get(nodo, []):
            if vecino not in visitados:
                resultado = _dls_recursivo(
                    vecino, meta, grafo, limite - 1,
                    camino + [vecino], visitados
                )
                if resultado is not None:
                    return resultado
        visitados.discard(nodo)  # Backtracking: permite revisar desde otra rama
        return None
 
    return _dls_recursivo(inicio, meta, grafo, limite, [inicio], set())
 
 
# ─────────────────────────────────────────────
# 5. BÚSQUEDA POR PROFUNDIDAD ITERATIVA (IDDFS)
# ─────────────────────────────────────────────
def profundidad_iterativa_iddfs(inicio, meta, grafo, limite_max=50):
    """
    Llama repetidamente a DLS incrementando el límite desde 0.
    Combina la completitud de BFS con el bajo uso de memoria de DFS.
    Garantiza encontrar la solución con menos pasos.
    """
    for limite in range(limite_max + 1):
        resultado = profundidad_limitada_dls(inicio, meta, grafo, limite)
        if resultado is not None:
            return resultado, limite  # Retorna camino y el límite donde lo encontró
 
    return None, -1  # No se encontró dentro del límite máximo
 
 
# ─────────────────────────────────────────────
# 6. BÚSQUEDA AVARA (GREEDY BEST-FIRST)
# ─────────────────────────────────────────────
def busqueda_avara(inicio, meta, grafo, heuristica):
    """
    Expande siempre el nodo con menor valor heurístico h(n).
    h(n) = estimación de la distancia al objetivo.
    No garantiza el camino óptimo, pero suele ser rápida.
    """
    # heap: (h(n), nodo_actual, camino)
    heap = [(heuristica.get(inicio, 0), inicio, [inicio])]
    visitados = set()
 
    while heap:
        h, actual, camino = heapq.heappop(heap)
 
        if actual in visitados:
            continue
        visitados.add(actual)
 
        if actual == meta:
            return camino
 
        for vecino, _ in grafo.get(actual, []):
            if vecino not in visitados:
                h_vecino = heuristica.get(vecino, 0)
                heapq.heappush(heap, (h_vecino, vecino, camino + [vecino]))
 
    return None  # No se encontró camino
 
 
# ─────────────────────────────────────────────
# 7. BÚSQUEDA A*
# ─────────────────────────────────────────────
def busqueda_a_estrella(inicio, meta, grafo, heuristica):
    """
    Combina el costo acumulado g(n) y la heurística h(n).
    Prioriza por f(n) = g(n) + h(n).
    Garantiza el camino óptimo si h(n) es admisible (nunca sobreestima).
    """
    # heap: (f(n), g(n), nodo_actual, camino)
    heap = [(heuristica.get(inicio, 0), 0, inicio, [inicio])]
    # costo_min: menor g(n) conocido para cada nodo
    costo_min = {inicio: 0}
 
    while heap:
        f, g, actual, camino = heapq.heappop(heap)
 
        if actual == meta:
            return camino, g  # Retorna camino y costo total
 
        # Si encontramos una ruta más barata antes, descartamos esta
        if g > costo_min.get(actual, float('inf')):
            continue
 
        for vecino, peso in grafo.get(actual, []):
            nuevo_g = g + peso
            if nuevo_g < costo_min.get(vecino, float('inf')):
                costo_min[vecino] = nuevo_g
                nuevo_f = nuevo_g + heuristica.get(vecino, 0)
                heapq.heappush(heap, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
 
    return None, float('inf')  # No se encontró camino
 

