from flask import Flask, request, jsonify, send_from_directory
import os

from algoritmos_pasos import (
    bfs_pasos, dfs_pasos, ucs_pasos,
    dls_pasos, iddfs_pasos, avara_pasos, a_estrella_pasos,
)

# Si también quieres usar tus algoritmos originales (para el menú de consola),
# puedes seguir importando algoritmos.py normalmente en main.py sin cambios.

app = Flask(__name__, static_folder=".")

# ─── Servir el frontend ───────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# ─── Listar archivos .txt disponibles ────────────────────────────────────────

@app.route("/api/grafos")
def listar_grafos():
    carpeta = request.args.get("carpeta", "grafos")
    if not os.path.isdir(carpeta):
        return jsonify({"archivos": [], "error": f"Carpeta '{carpeta}' no encontrada"})
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".txt")]
    return jsonify({"archivos": sorted(archivos)})


# ─── Parsear un .txt con el mismo formato que main.py ────────────────────────

def parsear_archivo(ruta: str):
    grafo: dict = {}
    heuristica: dict = {}
    inicio = None
    meta = None
    seccion = None

    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            if linea == "ESTADO_INICIAL":
                seccion = "inicio"
            elif linea == "ESTADO_FINAL":
                seccion = "meta"
            elif linea == "TRANSICIONES":
                seccion = "transiciones"
            elif linea == "HEURISTICAS":
                seccion = "heuristicas"
            else:
                if seccion == "inicio":
                    inicio = linea
                elif seccion == "meta":
                    meta = linea
                elif seccion == "transiciones":
                    partes = linea.split(",")
                    if len(partes) >= 3:
                        origen = partes[0].strip()
                        destino = partes[1].strip()
                        costo = float(partes[2].strip())
                        grafo.setdefault(origen, []).append((destino, costo))
                        grafo.setdefault(destino, [])
                elif seccion == "heuristicas":
                    partes = linea.split(",")
                    if len(partes) >= 2:
                        heuristica[partes[0].strip()] = float(partes[1].strip())

    return grafo, heuristica, inicio, meta


# ─── Endpoint principal: ejecutar búsqueda y devolver pasos ──────────────────

@app.route("/api/buscar", methods=["POST"])
def buscar():
    data = request.get_json()

    algoritmo = data.get("algoritmo", "bfs")
    fuente = data.get("fuente", "archivo")  # "archivo" | "manual"
    carpeta = data.get("carpeta", "grafos")
    limite_dls = int(data.get("limite_dls", 5))
    limite_iddfs = int(data.get("limite_iddfs", 15))

    # ── Cargar grafo ──────────────────────────────────────────────────────────
    if fuente == "archivo":
        nombre = data.get("archivo", "")
        ruta = os.path.join(carpeta, nombre)
        if not os.path.isfile(ruta):
            return jsonify({"error": f"Archivo no encontrado: {ruta}"}), 404
        try:
            grafo, heuristica, inicio, meta = parsear_archivo(ruta)
        except Exception as e:
            return jsonify({"error": f"Error al leer el archivo: {e}"}), 400

    else:  # fuente == "manual"
        grafo_raw = data.get("grafo", {})
        # grafo_raw viene como { "A": [["B", 1], ["C", 2]], ... }
        grafo = {k: [tuple(x) for x in v] for k, v in grafo_raw.items()}
        heuristica = data.get("heuristica", {})
        inicio = data.get("inicio", "")
        meta = data.get("meta", "")

    if not inicio or not meta:
        return jsonify({"error": "Falta inicio o meta"}), 400

    # ── Nodos para el visualizador ────────────────────────────────────────────
    nodos = list(grafo.keys())

    # ── Ejecutar algoritmo ────────────────────────────────────────────────────
    try:
        if algoritmo == "bfs":
            resultado = bfs_pasos(inicio, meta, grafo)
        elif algoritmo == "dfs":
            resultado = dfs_pasos(inicio, meta, grafo)
        elif algoritmo == "ucs":
            resultado = ucs_pasos(inicio, meta, grafo)
        elif algoritmo == "dls":
            resultado = dls_pasos(inicio, meta, grafo, limite_dls)
        elif algoritmo == "iddfs":
            resultado = iddfs_pasos(inicio, meta, grafo, limite_iddfs)
        elif algoritmo == "avara":
            resultado = avara_pasos(inicio, meta, grafo, heuristica)
        elif algoritmo == "astar":
            resultado = a_estrella_pasos(inicio, meta, grafo, heuristica)
        else:
            return jsonify({"error": f"Algoritmo desconocido: {algoritmo}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error en la búsqueda: {e}"}), 500

    resultado["nodos"] = nodos
    resultado["inicio"] = inicio
    resultado["meta"] = meta
    resultado["heuristica"] = heuristica

    return jsonify(resultado)


# ─── Arranque ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PIA — Visualizador de Búsqueda (FCFM)")
    print("  Luis Fernando Segobia Torres  2177528")
    print("  Angel Joseph Meraz Hernandez  2067151")
    print("=" * 60)
    print("\n  Abre tu navegador en:  http://localhost:5000\n")
    app.run(debug=True, port=5000)
