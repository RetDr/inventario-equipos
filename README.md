# Sistema de Inventario de Equipos

Sistema cliente-servidor para gestionar inventario de equipos con interfaz gráfica moderna.

## 🎯 Características

- Interfaz gráfica moderna con tkinter
- Arquitectura cliente-servidor con sockets
- Registro de equipos
- Consulta de inventario completo
- Búsqueda por código
- Actualización de estados
- Persistencia de datos en JSON
- Logs del servidor

## Requisitos

- Python 3.8 o superior
- tkinter (incluido con Python)

## Instalación

1. Clona el repositorio:

git remote add origin https://github.com/RetDr/inventario-equipos.git

cd inventario-equipos

## 💻 Uso

### Paso 1: Ejecutar el servidor

Abre una terminal y ejecuta:

python servidor.py

### Verás algo como:

==================================================
SERVIDOR DE INVENTARIO
Escuchando en: 0.0.0.0:5000
IP local: 192.168.18.3:5000
Para clientes en red: 192.168.18.3:5000
Para localhost: localhost:5000
OK: Servidor escuchando...

Anota tu **IP local** (ej: 192.168.18.3)

### Paso 2: Ejecutar el cliente

En **otra terminal**, ejecuta:

python cliente.py


Se abrirá la interfaz gráfica.

## 🌐 Uso en red local

Si quieres que **tus compañeros se conecten desde otras máquinas:**

1. **En tu PC (servidor):**
   - Asegúrate que el firewall permite conexiones en puerto 5000
   - Ejecuta `python servidor.py`
   - Anota tu IP local

2. **En las PCs de tus compañeros (clientes):**
   - Descargan o clonan el repositorio
   - Abren `cliente.py` y editan esta línea:

HOST = '192.168.18.3' # Cambian a la IP de tu servidor

- Guardan y ejecutan `python cliente.py`

## 🔧 Configurar Firewall en Windows

Si los clientes no pueden conectarse:

1. Abre **Firewall de Windows** → **Configuración avanzada**
2. Click en **Reglas de entrada** → **Nueva regla**
3. Selecciona **Puerto** → **Siguiente**
4. **TCP** → Puerto **5000** → **Siguiente**
5. **Permitir la conexión** → **Siguiente**
6. Aplica a **Dominio, Privada y Pública** → **Siguiente**
7. Nombre: `Inventario Equipos` → **Finalizar**

## 📁 Estructura del proyecto

inventario-equipos/
├── servidor.py # Servidor principal
├── cliente.py # Cliente con GUI
├── inventario.json # Base de datos (se crea automáticamente)
├── server.log # Log del servidor (se crea automáticamente)
├── README.md # Este archivo
├── requirements.txt # Dependencias del proyecto
└── .gitignore # Archivos ignorados por Git


## 🎓 Para estudiantes

Este proyecto es ideal para aprender:
- Programación con sockets
- Interfaces gráficas con tkinter
- Arquitectura cliente-servidor
- Gestión de JSON
- Threading en Python

## 👥 Autor

Desarrollado como proyecto académico del curso de Software II

## 📝 Licencia

MIT License - Usa libremente este código
