from algoritmos import *

def cargar_desde_archivo(ruta):
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
                    grafo.setdefault(destino, [])
                elif seccion == 'heuristicas':
                    partes = linea.split(',')
                    heuristica[partes[0]] = float(partes[1])
                    
    return grafo, heuristica, inicio, meta

#Escribir tu propio grafo
def capturar_en_linea():
    while(True):
        inicio = input("Estado inicial: ").strip()
        if inicio == "":
            print("Debe ingresar un estado inicial")
        else:
            break
    while(True):
        meta = input("Estado final: ").strip()
        if meta == "":
            print("Debe ingresar un estado final")
        else:
            break
    
    grafo = {}
    heuristica = {}
    
    #cuanto cuesta pasar al siguiente nodo
    
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
        
            
    #Debes especificar cuanto falta entre el nodo actual hasta el final, D debe ser 0 porque ya llegaste
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
    #Validar heurísticas usando UCS
    print("\nValidando heurísticas...")
    
    for nodo in heuristica:
        _, costo_real = costo_uniforme_ucs(nodo, meta, grafo)

        if costo_real == float('inf'):
            print(f"  El nodo {nodo} no debería tener heurística.")
            heuristica[nodo] = 0
            continue
        
        while heuristica[nodo] > costo_real or heuristica[nodo] < 0:
            print(f"  Heurística inválida en nodo {nodo}")
            print(f"  Valor ingresado: {heuristica[nodo]}")
            print(f"  Costo mínimo real a meta: {costo_real}")
            
            try:
                nuevo = float(input(f"  Ingresa un nuevo valor para {nodo} (<= {costo_real} y >= 0): "))
                heuristica[nodo] = nuevo
            except ValueError:
                print("  Valor inválido.")
    return grafo, heuristica, inicio, meta

def mostrar_resultado(nombre, camino, costo=None, limite=None):
    print(f"\n{'='*70}")
    print(f"  Algoritmo: {nombre}")
    print(f"{'='*70}")
    if camino:
        print(f"  Camino encontrado: {' -> '.join(camino)}")
        if costo is not None:
            print(f"  Costo total:       {costo}")
        if limite is not None:
            print(f"  Límite usado:      {limite}")
    else:
        print("  No se encontró un camino.")
    print(f"{'='*70}\n")

#Menu pricipal
def menu():
    print("\n" + "="*70)
    print("   PIA - ALGORITMOS DE BÚSQUEDA  (Inteligencia Artificail FCFM)")
    print("   Luis Fernando Segobia Torres \t2177528")
    print("   Angel Joseph Meraz Hernandez \t2067151")
    print("="*70)
    
    #Eleccion del grafico
    print("\n¿Cómo deseas ingresar el espacio de estados?")
    opcion_fuente = '0'
    while(opcion_fuente != '1' and opcion_fuente != '2'):        
        print("  1. Desde archivo de texto (grafo.txt)")
        print("  2. Captura en línea")
        opcion_fuente = input("Opción: ").strip()
         
        if opcion_fuente == '1':
            while(True):
                ruta = input("Ruta del archivo [sugerencia: grafo.txt] o escribe \"fin\" si quieres cambiar de opcion: \n").strip() or 'grafo.txt'
                if (ruta.lower() == 'fin'):
                    opcion_fuente = '0'
                    break
                if (ruta.lower() != 'fin'):
                    try:
                        grafo, heuristica, inicio, meta = cargar_desde_archivo(ruta)
                        print(f"\n  Grafo cargado: inicio={inicio}, meta={meta}")
                        break
                    except FileNotFoundError:
                        print(f"  Error: no se encontró el archivo '{ruta}'")
        elif opcion_fuente == '2':
            grafo, heuristica, inicio, meta = capturar_en_linea()
        else:
            print(f"Esa opcion no existe, por favor escoje 1 o 2.\n")
    
    #Menu de algoritmo de busqueda
    print("\nSelecciona el algoritmo de búsqueda:")
    print("  1. Búsqueda por Amplitud (BFS)")
    print("  2. Búsqueda por Costo Uniforme (UCS)")
    print("  3. Búsqueda por Profundidad (DFS)")
    print("  4. Búsqueda por Profundidad Limitada (DLS)")
    print("  5. Búsqueda por Profundidad Iterativa (IDDFS)")
    print("  6. Búsqueda Avara (Greedy)")
    print("  7. Búsqueda A*")
    print("  0. Ejecutar TODOS")
    opcion = -1
    while(opcion not in [str(i) for i in range(8)]):
        opcion = input("Opción: ").strip()
        if opcion not in [str(i) for i in range(8)]:
            print("Opción no válida.\n")
 
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
        camino, profundidad_real = profundidad_limitada_dls(inicio, meta, grafo, limite)
        mostrar_resultado("Búsqueda por Profundidad Limitada (DLS)", camino, limite=profundidad_real)
        
    if opcion == '5' or opcion == '0':
        camino, limite_usado = profundidad_iterativa_iddfs(inicio, meta, grafo)
        mostrar_resultado("Búsqueda por Profundidad Iterativa (IDDFS)", camino, limite=limite_usado)
 
    if opcion == '6' or opcion == '0':
        camino = busqueda_avara(inicio, meta, grafo, heuristica)
        mostrar_resultado("Búsqueda Avara (Greedy)", camino)
        
    if opcion == '7' or opcion == '0':
        camino, costo = busqueda_a_estrella(inicio, meta, grafo, heuristica)
        mostrar_resultado("Búsqueda A*", camino, costo=costo)

        
# Llamada al menu y saber si se repite o no
if __name__ == '__main__':
    while True:
        menu()
        otra = 'e'
        while(otra != 's' and otra != 'n'):
            otra = input("¿Ejecutar otra búsqueda? (s/n): ").strip().lower()
            if(otra != 's' and otra != 'n'):
                print("Ingrese una opcion correcta")
        if otra == 'n':
            print("\n¡Hasta luego!\n")
            break
