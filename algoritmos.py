import heapq
from collections import deque

def amplitud_bfs(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]]) ->list[str] | None:
    cola:deque[tuple[str, list[str]]] = deque([(inicio, [inicio])])
    visitados:set[str] = set([inicio])
    
    while cola:
        actual, camino = cola.popleft()
        
        if actual == meta:
            return camino
        
        for vecino, _ in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
                
    return None

def costo_uniforme_ucs(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]]) -> tuple[list[str] | None, float]:
    heap:list[tuple[float, str, list[str]]] = [(0, inicio, [inicio])]
    visitados:list[tuple[float, str, list[str]]] = {}
    
    while heap:
        costo, actual, camino = heapq.heappop(heap)
        
        if actual == meta:
            return camino, costo
        
        if actual in visitados and visitados[actual] <= costo:
            continue
        visitados[actual] = costo
        
        for vecino, peso in grafo.get(actual, []):
            nuevo_costo:float = costo + peso
            if vecino not in visitados or visitados[vecino] > nuevo_costo:
                heapq.heappush(heap, (nuevo_costo, vecino, camino + [vecino]))
                
    return None, float('inf')

def profundidad_dfs(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]])-> list[str] | None:
    pila:list[tuple[str, list[str]]] = [(inicio, [inicio])]
    visitados:set[str] = set()
    
    while pila:
        actual, camino = pila.pop()
        
        if actual in visitados:
            continue
        visitados.add(actual)
        
        if actual == meta:
            return camino
        
        #Se agregan en orden inverso para expandir en orden natural
        for vecino, _ in reversed(grafo.get(actual, [])):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))
                
    return None

def profundidad_limitada_dls(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], limite:int)-> tuple[list[str] | None, int | None]:
    def dfs(nodo:str, profundidad:int, camino:list[str]):
        if nodo == meta:
            return camino, profundidad
        
        if profundidad == limite:
            return None
        
        for vecino, _ in grafo.get(nodo, []):
            if vecino not in camino:  #evita ciclos
                resultado:tuple[list[str], int] | None = dfs(vecino, profundidad + 1, camino + [vecino])
                if resultado:
                    return resultado
        return None
    resultado:tuple[list[str], int] | None = dfs(inicio, 0, [inicio])
    if resultado:
        return resultado  #camino, profundidad_real
    return None, None

def profundidad_iterativa_iddfs(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], limite_max=50) -> tuple[list[str] | None, int]:
    for limite in range(limite_max + 1):
        resultado, _ = profundidad_limitada_dls(inicio, meta, grafo, limite)
        if resultado is not None:
            return resultado, limite  #Retorna camino y el límite donde lo encontro
        
    return None, -1

def busqueda_avara(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], heuristica:dict[str, float])-> list[str] | None:
    heap:list[tuple[float, str, list[str]]] = [(heuristica.get(inicio, 0), inicio, [inicio])]
    visitados:set[str] = set()
    
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
                
    return None

def busqueda_a_estrella(inicio:str, meta:str, grafo:dict[str, list[tuple[str, float]]], heuristica:dict[str, float]):
    heap:list[tuple[float, float, str, list[str]]] = [(heuristica.get(inicio, 0), 0, inicio, [inicio])]
    # costo_min: menor g(n) conocido para cada nodo
    costo_min:dict[str, float] = {inicio: 0}
    
    while heap:
        f, g, actual, camino = heapq.heappop(heap)
        
        if actual == meta:
            return camino, g  #Retorna camino y costo total
        
        #Si encontramos una ruta más barata antes, descartamos esta
        if g > costo_min.get(actual, float('inf')):
            continue
        
        for vecino, peso in grafo.get(actual, []):
            nuevo_g = g + peso
            if nuevo_g < costo_min.get(vecino, float('inf')):
                costo_min[vecino] = nuevo_g
                nuevo_f = nuevo_g + heuristica.get(vecino, 0)
                heapq.heappush(heap, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
                
    return None, float('inf')
