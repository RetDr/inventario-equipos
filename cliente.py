import socket
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkFont
import threading

HOST = 'localhost'
PORT = 5000

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario de Equipos")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Estilos
        self.root.configure(bg="#f0f0f0")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores
        self.color_principal = "#2c3e50"
        self.color_secundario = "#3498db"
        self.color_exito = "#27ae60"
        self.color_error = "#e74c3c"
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.root, bg=self.color_principal, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        titulo = tk.Label(header, text="📦 Gestión de Inventario", 
                         font=("Arial", 18, "bold"), fg="white", bg=self.color_principal)
        titulo.pack(pady=10)
        
        # Frame principal con dos columnas
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Columna izquierda - Formulario
        left_frame = ttk.LabelFrame(main_frame, text="Operaciones", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        
        # Selector de acción
        ttk.Label(left_frame, text="Selecciona una acción:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        self.accion_var = tk.StringVar(value="registrar")
        acciones = [
            ("Registrar Equipo", "registrar"),
            ("Ver Inventario", "consultar"),
            ("Buscar Equipo", "buscar"),
            ("Actualizar Estado", "actualizar")
        ]
        
        for texto, valor in acciones:
            ttk.Radiobutton(left_frame, text=texto, variable=self.accion_var, 
                          value=valor, command=self.actualizar_formulario).pack(anchor=tk.W, pady=5)
        
        # Separador
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Frame para campos dinámicos
        self.campos_frame = ttk.Frame(left_frame)
        self.campos_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        botones_frame = ttk.Frame(left_frame)
        botones_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(botones_frame, text="Ejecutar", command=self.ejecutar_accion).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)
        
        # Columna derecha - Resultados
        right_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.resultado_text = scrolledtext.ScrolledText(right_frame, height=30, width=50, wrap=tk.WORD)
        self.resultado_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para colores
        self.resultado_text.tag_config("exito", foreground=self.color_exito)
        self.resultado_text.tag_config("error", foreground=self.color_error)
        self.resultado_text.tag_config("info", foreground=self.color_secundario)
        
        # Footer
        footer = tk.Frame(self.root, bg="#34495e", height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        estado = tk.Label(footer, text=f"Conectando a {HOST}:{PORT}", 
                         fg="white", bg="#34495e", font=("Arial", 9))
        estado.pack(pady=10)
        
        self.actualizar_formulario()
    
    def actualizar_formulario(self):
        # Limpiar frame de campos
        for widget in self.campos_frame.winfo_children():
            widget.destroy()
        
        self.campos = {}
        accion = self.accion_var.get()
        
        if accion == "registrar":
            campos = ["Código", "Nombre", "Tipo", "Estado"]
            for campo in campos:
                self.crear_campo(campo, self.campos_frame)
        
        elif accion == "buscar":
            self.crear_campo("Código", self.campos_frame)
        
        elif accion == "actualizar":
            self.crear_campo("Código", self.campos_frame)
            self.crear_campo("Nuevo Estado", self.campos_frame)
    
    def crear_campo(self, nombre, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text=f"{nombre}:", width=15).pack(side=tk.LEFT)
        
        if nombre == "Estado" or nombre == "Nuevo Estado":
            entry = ttk.Combobox(frame, values=["Disponible", "En uso", "En mantenimiento", "Dañado"], state="readonly")
        else:
            entry = ttk.Entry(frame)
        
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.campos[nombre] = entry
    
    def ejecutar_accion(self):
        accion = self.accion_var.get()
        
        try:
            if accion == "registrar":
                if not all(self.campos[k].get() for k in self.campos):
                    messagebox.showwarning("Advertencia", "Completa todos los campos")
                    return
                
                solicitud = {
                    "accion": "registrar",
                    "codigo": self.campos["Código"].get(),
                    "nombre": self.campos["Nombre"].get(),
                    "tipo": self.campos["Tipo"].get(),
                    "estado": self.campos["Estado"].get()
                }
            
            elif accion == "consultar":
                solicitud = {"accion": "consultar"}
            
            elif accion == "buscar":
                if not self.campos["Código"].get():
                    messagebox.showwarning("Advertencia", "Ingresa el código")
                    return
                
                solicitud = {"accion": "buscar", "codigo": self.campos["Código"].get()}
            
            elif accion == "actualizar":
                if not (self.campos["Código"].get() and self.campos["Nuevo Estado"].get()):
                    messagebox.showwarning("Advertencia", "Completa todos los campos")
                    return
                
                solicitud = {
                    "accion": "actualizar",
                    "codigo": self.campos["Código"].get(),
                    "estado": self.campos["Nuevo Estado"].get()
                }
            
            # Ejecutar en thread para no bloquear GUI
            thread = threading.Thread(target=self.enviar_solicitud, args=(solicitud,))
            thread.daemon = True
            thread.start()
        
        except Exception as e:
            self.mostrar_resultado(f"Error: {str(e)}", "error")
    
    def enviar_solicitud(self, solicitud):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((HOST, PORT))
                s.sendall(json.dumps(solicitud).encode())
                data = s.recv(4096)
                respuesta = json.loads(data.decode())
                
                self.procesar_respuesta(respuesta, solicitud["accion"])
        
        except socket.timeout:
            self.mostrar_resultado("Error: Conexión expirada", "error")
        except ConnectionRefusedError:
            self.mostrar_resultado(f"Error: No se pudo conectar a {HOST}:{PORT}", "error")
        except Exception as e:
            self.mostrar_resultado(f"Error: {str(e)}", "error")
    
    def procesar_respuesta(self, respuesta, accion):
        self.resultado_text.delete("1.0", tk.END)
        
        if accion == "consultar":
            equipos = respuesta.get("equipos", [])
            if equipos:
                self.mostrar_resultado("📋 INVENTARIO COMPLETO:\n", "info")
                for i, equipo in enumerate(equipos, 1):
                    texto = f"\n{i}. Código: {equipo.get('codigo')}\n"
                    texto += f"   Nombre: {equipo.get('nombre')}\n"
                    texto += f"   Tipo: {equipo.get('tipo')}\n"
                    texto += f"   Estado: {equipo.get('estado')}\n"
                    self.mostrar_resultado(texto, "info")
            else:
                self.mostrar_resultado("El inventario está vacío", "error")
        
        elif accion == "buscar":
            if respuesta.get("resultado") == "ok":
                equipo = respuesta.get("equipo", {})
                texto = f"✅ EQUIPO ENCONTRADO:\n\n"
                texto += f"Código: {equipo.get('codigo')}\n"
                texto += f"Nombre: {equipo.get('nombre')}\n"
                texto += f"Tipo: {equipo.get('tipo')}\n"
                texto += f"Estado: {equipo.get('estado')}\n"
                self.mostrar_resultado(texto, "exito")
            else:
                self.mostrar_resultado(f"❌ {respuesta.get('mensaje')}", "error")
        
        else:
            resultado = respuesta.get("resultado", "")
            mensaje = respuesta.get("mensaje", "")
            tag = "exito" if resultado == "ok" else "error"
            icono = "✅" if resultado == "ok" else "❌"
            self.mostrar_resultado(f"{icono} {mensaje}", tag)
    
    def mostrar_resultado(self, texto, tag):
        self.resultado_text.insert(tk.END, texto, tag)
        self.resultado_text.see(tk.END)
    
    def limpiar_campos(self):
        for entry in self.campos.values():
            entry.delete(0, tk.END) if isinstance(entry, ttk.Entry) else entry.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()
