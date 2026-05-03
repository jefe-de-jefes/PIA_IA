
from algoritmos import *

# CARGA DEL GRAFO
def cargar_desde_archivo(ruta):
    """
    Lee el espacio de estados desde un archivo de texto con el formato:
        ESTADO_INICIAL
        A
        ESTADO_FINAL
        E
        TRANSICIONES
        A,B,1
        ...
        HEURISTICAS
        A,7
        ...
    """
    grafo = {}
    heuristica = {}
    inicio = None
    meta = None
    seccion = None
 
    with open(ruta, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            if linea == 'ESTADO_INICIAL':
                seccion = 'inicio'
            elif linea == 'ESTADO_FINAL':
                seccion = 'meta'
            elif linea == 'TRANSICIONES':
                seccion = 'transiciones'
            elif linea == 'HEURISTICAS':
                seccion = 'heuristicas'
            else:
                if seccion == 'inicio':
                    inicio = linea
                elif seccion == 'meta':
                    meta = linea
                elif seccion == 'transiciones':
                    partes = linea.split(',')
                    origen, destino, costo = partes[0], partes[1], float(partes[2])
                    grafo.setdefault(origen, []).append((destino, costo))
                    # Aseguramos que los nodos destino también existen en el grafo
                    grafo.setdefault(destino, [])
                elif seccion == 'heuristicas':
                    partes = linea.split(',')
                    heuristica[partes[0]] = float(partes[1])
 
    return grafo, heuristica, inicio, meta
 
 
def capturar_en_linea():
    """
    Permite al usuario definir el grafo directamente desde la consola.
    """
    inicio = input("Estado inicial: ").strip()
    meta = input("Estado final: ").strip()
 
    grafo = {}
    heuristica = {}
 
    print("\nIngresa las transiciones en formato: origen,destino,costo")
    print("(Escribe 'fin' para terminar)")
    while True:
        linea = input("Transición: ").strip()
        if linea.lower() == 'fin':
            break
        try:
            origen, destino, costo = linea.split(',')
            grafo.setdefault(origen.strip(), []).append((destino.strip(), float(costo)))
            grafo.setdefault(destino.strip(), [])
        except ValueError:
            print("  Formato inválido. Usa: origen,destino,costo")
 
    print("\nIngresa las heurísticas en formato: nodo,valor")
    print("(Escribe 'fin' para terminar)")
    while True:
        linea = input("Heurística: ").strip()
        if linea.lower() == 'fin':
            break
        try:
            nodo, valor = linea.split(',')
            heuristica[nodo.strip()] = float(valor)
        except ValueError:
            print("  Formato inválido. Usa: nodo,valor")
 
    return grafo, heuristica, inicio, meta
 
 
# ─────────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────────
 
def mostrar_resultado(nombre, camino, costo=None, limite=None):
    print(f"\n{'='*45}")
    print(f"  Algoritmo: {nombre}")
    print(f"{'='*45}")
    if camino:
        print(f"  Camino encontrado: {' -> '.join(camino)}")
        if costo is not None:
            print(f"  Costo total:       {costo}")
        if limite is not None:
            print(f"  Límite usado:      {limite}")
    else:
        print("  No se encontró un camino.")
    print(f"{'='*45}\n")
 
 
def menu():
    print("\n" + "="*45)
    print("   PIA - ALGORITMOS DE BÚSQUEDA  (IA FCFM)")
    print("="*45)
 
    # ── Fuente del grafo ──
    print("\n¿Cómo deseas ingresar el espacio de estados?")
    print("  1. Desde archivo de texto (grafo.txt)")
    print("  2. Captura en línea")
    opcion_fuente = input("Opción: ").strip()
 
    if opcion_fuente == '1':
        ruta = input("Ruta del archivo [grafo.txt]: ").strip() or 'grafo.txt'
        try:
            grafo, heuristica, inicio, meta = cargar_desde_archivo(ruta)
            print(f"\n  Grafo cargado: inicio={inicio}, meta={meta}")
        except FileNotFoundError:
            print(f"  Error: no se encontró el archivo '{ruta}'")
            return
    else:
        grafo, heuristica, inicio, meta = capturar_en_linea()
 
    # ── Selección de algoritmo ──
    print("\nSelecciona el algoritmo de búsqueda:")
    print("  1. Búsqueda por Amplitud (BFS)")
    print("  2. Búsqueda por Costo Uniforme (UCS)")
    print("  3. Búsqueda por Profundidad (DFS)")
    print("  4. Búsqueda por Profundidad Limitada (DLS)")
    print("  5. Búsqueda por Profundidad Iterativa (IDDFS)")
    print("  6. Búsqueda Avara (Greedy)")
    print("  7. Búsqueda A*")
    print("  0. Ejecutar TODOS")
    opcion = input("Opción: ").strip()
 
    if opcion == '1' or opcion == '0':
        camino = amplitud_bfs(inicio, meta, grafo)
        mostrar_resultado("Búsqueda por Amplitud (BFS)", camino)
 
    if opcion == '2' or opcion == '0':
        camino, costo = costo_uniforme_ucs(inicio, meta, grafo)
        mostrar_resultado("Búsqueda por Costo Uniforme (UCS)", camino, costo=costo)
 
    if opcion == '3' or opcion == '0':
        camino = profundidad_dfs(inicio, meta, grafo)
        mostrar_resultado("Búsqueda por Profundidad (DFS)", camino)
 
    if opcion == '4' or opcion == '0':
        try:
            limite = int(input("Límite de profundidad para DLS: "))
        except ValueError:
            limite = 10
        camino = profundidad_limitada_dls(inicio, meta, grafo, limite)
        mostrar_resultado("Búsqueda por Profundidad Limitada (DLS)", camino, limite=limite)
 
    if opcion == '5' or opcion == '0':
        camino, limite_usado = profundidad_iterativa_iddfs(inicio, meta, grafo)
        mostrar_resultado("Búsqueda por Profundidad Iterativa (IDDFS)", camino, limite=limite_usado)
 
    if opcion == '6' or opcion == '0':
        camino = busqueda_avara(inicio, meta, grafo, heuristica)
        mostrar_resultado("Búsqueda Avara (Greedy)", camino)
 
    if opcion == '7' or opcion == '0':
        camino, costo = busqueda_a_estrella(inicio, meta, grafo, heuristica)
        mostrar_resultado("Búsqueda A*", camino, costo=costo)
 
    if opcion not in [str(i) for i in range(8)]:
        print("Opción no válida.")
 
 
# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────
 
if __name__ == '__main__':
    while True:
        menu()
        otra = input("¿Ejecutar otra búsqueda? (s/n): ").strip().lower()
        if otra != 's':
            print("\n¡Hasta luego!\n")
            break
