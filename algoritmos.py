import heapq
from collections import deque

def amplitud_bfs(inicio, meta, grafo):
    cola = deque([(inicio, [inicio])])
    visitados = set()
    while cola:
        actual, camino = cola.popleft()
        visitados.add(actual)
        if actual == meta:
            return camino
        if actual not in visitados:
            visitados.add(actual)
            for vecino in grafo[actual]:
                if vecino not in visitados:
                    cola.append((vecino, camino + [vecino]))
    return None
    
