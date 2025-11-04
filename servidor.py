# -*- coding: utf-8 -*-
import socket
import threading
import json
import os
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000
FILE = 'inventario.json'
LOG_FILE = 'server.log'

if not os.path.exists(FILE):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def log(mensaje):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mensaje}")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {mensaje}\n")

def cargar_inventario():
    with open(FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_inventario(inventario):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(inventario, f, indent=2, ensure_ascii=False)

def procesar_solicitud(data):
    try:
        req = json.loads(data)
        inventario = cargar_inventario()
        accion = req.get("accion")
        
        if accion == "registrar":
            if any(equipo["codigo"] == req["codigo"] for equipo in inventario):
                return json.dumps({"resultado": "error", "mensaje": "El codigo ya existe"})
            equipo = {
                "codigo": req["codigo"],
                "nombre": req["nombre"],
                "tipo": req.get("tipo", ""),
                "estado": req["estado"]
            }
            inventario.append(equipo)
            guardar_inventario(inventario)
            log(f"REGISTRAR: {req['codigo']} - {req['nombre']}")
            return json.dumps({"resultado": "ok", "mensaje": "Equipo registrado correctamente"})
        
        elif accion == "consultar":
            log(f"CONSULTAR: {len(inventario)} equipos")
            return json.dumps({"resultado": "ok", "equipos": inventario})
        
        elif accion == "buscar":
            equipo = next((e for e in inventario if e["codigo"] == req["codigo"]), None)
            if not equipo:
                log(f"BUSCAR: No encontrado - {req['codigo']}")
                return json.dumps({"resultado": "error", "mensaje": "Equipo no encontrado"})
            log(f"BUSCAR: Encontrado - {req['codigo']}")
            return json.dumps({"resultado": "ok", "equipo": equipo})
        
        elif accion == "actualizar":
            for equipo in inventario:
                if equipo["codigo"] == req["codigo"]:
                    equipo["estado"] = req["estado"]
                    guardar_inventario(inventario)
                    log(f"ACTUALIZAR: {req['codigo']} -> {req['estado']}")
                    return json.dumps({"resultado": "ok", "mensaje": "Estado actualizado"})
            log(f"ACTUALIZAR: No encontrado - {req['codigo']}")
            return json.dumps({"resultado": "error", "mensaje": "Equipo no encontrado"})
        
        else:
            return json.dumps({"resultado": "error", "mensaje": "Accion invalida"})
    except json.JSONDecodeError:
        return json.dumps({"resultado": "error", "mensaje": "JSON invalido"})
    except Exception as e:
        return json.dumps({"resultado": "error", "mensaje": f"Error: {str(e)}"})

def manejar_cliente(conn, addr):
    log(f"CONEXION: {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            respuesta = procesar_solicitud(data.decode())
            conn.sendall(respuesta.encode())
    except Exception as e:
        log(f"ERROR: {addr} - {str(e)}")
    finally:
        conn.close()
        log(f"DESCONEXION: {addr}")

def obtener_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == "__main__":
    ip_local = obtener_ip_local()
    print(f"\n{'='*50}")
    print(f"SERVIDOR DE INVENTARIO")
    print(f"{'='*50}")
    print(f"Escuchando en: 0.0.0.0:{PORT}")
    print(f"IP local: {ip_local}:{PORT}")
    print(f"Para clientes en red: {ip_local}:{PORT}")
    print(f"Para localhost: localhost:{PORT}")
    print(f"{'='*50}\n")
    
    log(f"Iniciando servidor en puerto {PORT}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"OK: Servidor escuchando...\n")
        try:
            while True:
                conn, addr = s.accept()
                threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            log("Servidor detenido por usuario")
            print("\nSTOP: Servidor detenido")
