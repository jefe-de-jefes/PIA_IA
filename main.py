from algoritmos import *
import os
 
def cargar_desde_archivo(ruta:str) -> tuple[
    dict[str, list[tuple[str, float]]],
    dict[str, float],
    str | None,
    str | None
]:
    grafo:dict[str, list[tuple[str, float]]] = {}
    heuristica:dict[str, float] = {}
    inicio:str | None = None
    meta:str | None = None
    seccion:str | None = None
    
    with open("grafos/" + ruta, 'r') as f:
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
                    partes:list[str] = linea.split(',')
                    origen, destino, costo = partes[0], partes[1], float(partes[2])
                    grafo.setdefault(origen, []).append((destino, costo))
                    grafo.setdefault(destino, [])
                elif seccion == 'heuristicas':
                    partes = linea.split(',')
                    heuristica[partes[0]] = float(partes[1])
                    
    return grafo, heuristica, inicio, meta
 
def capturar_en_linea() -> tuple[dict[str, list[tuple[str, float]]], dict[str, float], str, str]:
    while(True):
        inicio:str = input("Estado inicial: ").strip()
        if inicio == "":
            print("Debe ingresar un estado inicial")
        else:
            break
    while(True):
        meta:str = input("Estado final: ").strip()
        if meta == "":
            print("Debe ingresar un estado final")
        else:
            break
    
    grafo:dict[str, list[tuple[str, float]]]  = {}
    heuristica:dict[str, float] = {}
    
    print("\nIngresa las transiciones en formato: origen,destino,costo")
    print("(Escribe 'fin' para terminar)")
    while True:
        linea:str = input("Transición: ").strip()
        if linea.lower() == 'fin':
            break
        try:
            origen, destino, costo = linea.split(',')
            grafo.setdefault(origen.strip(), []).append((destino.strip(), float(costo)))
            grafo.setdefault(destino.strip(), [])
        except ValueError:
            print("  Formato invalido. Usa: origen,destino,costo")
            
    print("\nIngresa las heuristicas en formato: nodo,valor")
    print("(Escribe 'fin' para terminar)")
    while True:
        linea:str = input("Heuristica: ").strip()
        if linea.lower() == 'fin':
            break
        try:
            nodo, valor = linea.split(',')
            heuristica[nodo.strip()] = float(valor)
        except ValueError:
            print("  Formato inválido. Usa: nodo,valor")
 
    print("\nValidando heuristicas...")
    for nodo in heuristica:
        _, costo_real = costo_uniforme_ucs(nodo, meta, grafo)
        if costo_real == float('inf'):
            print(f"  El nodo {nodo} no deberia tener heuristica.")
            heuristica[nodo] = 0
            continue
        while heuristica[nodo] > costo_real or heuristica[nodo] < 0:
            print(f"  Heuristica inválida en nodo {nodo}")
            print(f"  Valor ingresado: {heuristica[nodo]}")
            print(f"  Costo minimo real a meta: {costo_real}")
            try:
                nuevo = float(input(f"  Ingresa un nuevo valor para {nodo} (<= {costo_real} y >= 0): "))
                heuristica[nodo] = nuevo
            except ValueError:
                print("  Valor inválido.")
    return grafo, heuristica, inicio, meta
 
 
def imprimir_encabezado(nombre: str) -> None:
    print(f"\n{'='*65}")
    print(f"  Algoritmo : {nombre}")
    print(f"{'='*65}")

def imprimir_resumen(camino:list[str], costo:float=None, limite:int=None, saltos:int=None):
    print("-" * 65)
    print(f"  Resultado : {' -> '.join(camino)}")
    if costo is not None:
        print(f"  Costo total : {costo:.1f}")
    if saltos is not None:
        print(f"  Saltos      : {saltos}")
    if limite is not None:
        print(f"  Límite      : {limite}")
    print("=" * 65)
 
def configurar_grafo():
    print("\n¿Cómo deseas ingresar el espacio de estados?")
    opcion_fuente = '0'
    while opcion_fuente not in ('1', '2'):
        print("  1. Desde archivo de texto")
        print("  2. Captura en linea")
        opcion_fuente = input("Opción: ").strip()
 
        if opcion_fuente == '1':
            while True:
                ruta = input("Nombre del archivo o \"fin\" para volver: \n").strip() or 'grafo.txt'
                if ruta.lower() == 'fin':
                    opcion_fuente = '0'
                    break
                try:
                    grafo, heuristica, inicio, meta = cargar_desde_archivo(ruta)
                    print(f"\n  Grafo cargado: inicio={inicio}, meta={meta}")
                    return grafo, heuristica, inicio, meta 
                except FileNotFoundError:
                    print(f"  Error: no se encontró el archivo '{ruta}'")
        elif opcion_fuente == '2':
            return capturar_en_linea()
        else:
            print("Esa opción no existe, por favor elige 1 o 2.\n")

def ejecutar_menu_algoritmos(grafo, heuristica, inicio, meta):
    print("\nSelecciona el algoritmo de busqueda:")
    print("  1. Busqueda por Amplitud       (BFS)")
    print("  2. Busqueda por Costo Uniforme (UCS)")
    print("  3. Busqueda por Profundidad    (DFS)")
    print("  4. Busqueda por Prof. Limitada (DLS)")
    print("  5. Busqueda por Prof. Iterativa(IDDFS)")
    print("  6. Busqueda Avara           (Greedy)")
    print("  7. Busqueda A*")
    print("  0. Ejecutar TODOS")
    
    opcion = '-1'
    while opcion not in [str(i) for i in range(8)]:
        opcion = input("Opción: ").strip()
        if opcion not in [str(i) for i in range(8)]:
            print("Opción no válida.\n")
 
    limite_dls = 10
    if opcion == '4' or opcion == '0':
        try:
            limite_dls = int(input("\nLimite de profundidad para DLS (Enter para 10): "))
        except ValueError:
            limite_dls = 10
 
    if opcion == '1' or opcion == '0':
        imprimir_encabezado("Busqueda por amplitud (BFS)")
        camino, pasos = amplitud_bfs(inicio, meta, grafo)
        if pasos:
            imprimir_pasos(pasos, camino, grafo, mostrar_saltos=True, mostrar_costo=True, etiqueta_costo='Costo g(n)')
        else:
            print("No se expandio ningun nodo")
        if camino:
            imprimir_resumen(camino, costo=costo_camino(camino, grafo), saltos=len(camino)-1)
        else:
            print("No se encontró un camino.")

    if opcion == '2' or opcion == '0':
        imprimir_encabezado("Busqueda por costo uniforme (UCS)")
        camino, costo, pasos = costo_uniforme_ucs(inicio, meta, grafo)
        if pasos:
            imprimir_pasos(pasos, camino, mostrar_costo=True, etiqueta_costo='g(n)')
        else:
            print("No se expandio ningun nodo")
        if camino:
            imprimir_resumen(camino, costo=costo)
        else:
            print("No se encontró un camino.")

    if opcion == '3' or opcion == '0':
        imprimir_encabezado("Busqueda por Profundidad (DFS)")
        camino, pasos = profundidad_dfs(inicio, meta, grafo)
        if pasos:
            imprimir_pasos(pasos, camino, grafo, mostrar_saltos=True, mostrar_costo=True)
        else:
            print("No se expandio ningun nodo")
        if camino:
            imprimir_resumen(camino, costo=costo_camino(camino, grafo), saltos=len(camino)-1)
        else:
            print("No se encontró un camino.")

    if opcion == '4' or opcion == '0':
        imprimir_encabezado("Busqueda por Profundidad limitada (DLS)")
        camino, profundidad_real, pasos = profundidad_limitada_dls(inicio, meta, grafo, limite_dls)
        if pasos:
            imprimir_pasos(pasos, camino, grafo, mostrar_saltos=True, mostrar_costo=True, etiqueta_costo='Prof.')
        else:
            print("No se expandio ningun nodo")
        if camino:
            imprimir_resumen(camino, costo=costo_camino(camino, grafo), saltos=len(camino)-1, limite=profundidad_real)
        else:
            print("No se encontró un camino.")

    if opcion == '5' or opcion == '0':
        imprimir_encabezado("Busqueda por profundidad iterativa (IDDFS)")
        camino, limite_usado, pasos = profundidad_iterativa_iddfs(inicio, meta, grafo)
        if pasos:
            imprimir_pasos(pasos, camino, grafo, mostrar_saltos=True, mostrar_costo=True, etiqueta_costo='Prof.')
        else:
            print("No se expandio ningun nodo")
        if camino:
            imprimir_resumen(camino, costo=costo_camino(camino, grafo), saltos=len(camino)-1, limite=limite_usado)
        else:
            print("No se encontró un camino.")


    if opcion == '6' or opcion == '0':
        imprimir_encabezado("Busqueda Avara (Greedy)")
        camino, pasos = busqueda_avara(inicio, meta, grafo, heuristica)
        if pasos:
            imprimir_pasos(pasos, camino, grafo, mostrar_costo=True, etiqueta_costo='h(n)')
        else:
            print("No se expandio ningun nodo")
        if camino:
            costo_greedy = costo_camino(camino, grafo)
            imprimir_resumen(camino, costo=costo_greedy)
        else:
            print("No se encontró un camino.")


    if opcion == '7' or opcion == '0':
        imprimir_encabezado("Busqueda A*")
        camino, costo, pasos = busqueda_a_estrella(inicio, meta, grafo, heuristica)
        if pasos:
            imprimir_pasos(pasos, camino, mostrar_costo=True, etiqueta_costo='g(n)', mostrar_f=True)
        else:
            print("No se expandio ningun nodo")
        if camino:
            imprimir_resumen(camino, costo=costo)
        else:
            print("No se encontró un camino.")

 
if __name__ == '__main__':
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*65)
        print("   PIA - ALGORITMOS DE BUSQUEDA  (Inteligencia Artificial FCFM)")
        print("   Luis Fernando Segobia Torres      2177528")
        print("   Angel Joseph Meraz Hernandez      2067151")
        print("="*65)
        
        grafo, heuristica, inicio, meta = configurar_grafo()
        
        while True: 
            
            ejecutar_menu_algoritmos(grafo, heuristica, inicio, meta)
            
            otra = ''
            while otra not in ('1', '2', '3'):
                print("\n¿Qué deseas hacer ahora?")
                print("  1.- Probar otro algoritmo")
                print("  2.- Cargar otro grafo")
                print("  3.- Salir del programa")
                otra = input("Opcion: ").strip()
            
            if otra == '1':
                continue 
            elif otra == '2':
                break 
            elif otra == '3':
                print("\n¡Hasta luego!\n")
                exit()
