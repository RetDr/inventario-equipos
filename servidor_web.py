from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
FILE = 'inventario.json'

# Inicializa el inventario si no existe
if not os.path.exists(FILE):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def cargar_inventario():
    with open(FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_inventario(inventario):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(inventario, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/registrar', methods=['POST'])
def registrar():
    try:
        data = request.json
        inventario = cargar_inventario()

        # Validación: evita duplicados por código
        if any(e["codigo"] == data["codigo"] for e in inventario):
            return jsonify({"resultado": "error", "mensaje": "El codigo ya existe"}), 400

        equipo = {
            "codigo": data["codigo"],
            "nombre": data["nombre"],
            "tipo": data.get("tipo", ""),
            "estado": data["estado"]
        }
        inventario.append(equipo)
        guardar_inventario(inventario)
        return jsonify({"resultado": "ok", "mensaje": "Equipo registrado correctamente"})
    except Exception as e:
        return jsonify({"resultado": "error", "mensaje": f"Error: {str(e)}"}), 500

@app.route('/api/consultar', methods=['GET'])
def consultar():
    try:
        inventario = cargar_inventario()
        return jsonify({"resultado": "ok", "equipos": inventario})
    except Exception as e:
        return jsonify({"resultado": "error", "mensaje": f"Error: {str(e)}"}), 500

@app.route('/api/buscar/<codigo>', methods=['GET'])
def buscar(codigo):
    try:
        inventario = cargar_inventario()
        equipo = next((e for e in inventario if e["codigo"] == codigo), None)
        if not equipo:
            return jsonify({"resultado": "error", "mensaje": "Equipo no encontrado"}), 404
        return jsonify({"resultado": "ok", "equipo": equipo})
    except Exception as e:
        return jsonify({"resultado": "error", "mensaje": f"Error: {str(e)}"}), 500

@app.route('/api/actualizar', methods=['PUT'])
def actualizar():
    try:
        data = request.json
        inventario = cargar_inventario()

        for equipo in inventario:
            if equipo["codigo"] == data["codigo"]:
                equipo["estado"] = data["estado"]
                guardar_inventario(inventario)
                return jsonify({"resultado": "ok", "mensaje": "Estado actualizado"})
        return jsonify({"resultado": "error", "mensaje": "Equipo no encontrado"}), 404
    except Exception as e:
        return jsonify({"resultado": "error", "mensaje": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
