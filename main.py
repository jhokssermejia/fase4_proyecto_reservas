import tkinter as tk
from tkinter import messagebox, scrolledtext
import logging

# Asegúrate de tener estos módulos en el mismo directorio
from gestor_usuarios import GestorUsuarios
from servicios import ReservaSala
from reserva import Reserva

# Configuración del sistema de logging (Reemplaza a guardar_log manual)
logging.basicConfig(
    filename="bitacora.txt",
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class GestionApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Software de Gestión")
        self.root.geometry("700x550")
        self.root.configure(bg="black")
        
        # Inicializar gestor
        self.db = GestorUsuarios()

        # Estilos compartidos (Diccionarios para reutilización)
        self.estilo_btn = {
            "bg": "#333333", "fg": "white", 
            "font": ("Arial", 11, "bold"), 
            "relief": tk.FLAT, "width": 25
        }
        self.estilo_lbl = {"bg": "black", "fg": "white", "font": ("Arial", 12)}

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        # --- Frame Superior (Botones) ---
        frame_botones = tk.Frame(self.root, bg="black")
        frame_botones.pack(pady=20)

        # Título
        lbl_titulo = tk.Label(
            frame_botones, text="--- MENÚ PRINCIPAL ---", 
            font=("Arial", 14, "bold"), bg="black", fg="#00FF00"
        )
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Botones
        btn_nuevo = tk.Button(frame_botones, text="1. NUEVO REGISTRO", command=self.ventana_nuevo_registro, **self.estilo_btn)
        btn_nuevo.grid(row=1, column=0, padx=10, pady=5)

        btn_simulacion = tk.Button(frame_botones, text="2. SIMULACIÓN (10 OP)", command=self.ejecutar_simulacion, **self.estilo_btn)
        btn_simulacion.grid(row=1, column=1, padx=10, pady=5)

        btn_ver = tk.Button(frame_botones, text="3. VER CLIENTES", command=self.ver_clientes, **self.estilo_btn)
        btn_ver.grid(row=2, column=0, padx=10, pady=5)

        btn_salir = tk.Button(
            frame_botones, text="4. SALIR", command=self.root.quit, 
            bg="#770000", fg="white", font=("Arial", 11, "bold"), 
            relief=tk.FLAT, width=25
        )
        btn_salir.grid(row=2, column=1, padx=10, pady=5)

        # --- Frame Inferior (Consola de salida) ---
        frame_consola = tk.Frame(self.root, bg="black")
        frame_consola.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        lbl_consola = tk.Label(frame_consola, text="Salida del Sistema:", **self.estilo_lbl)
        lbl_consola.pack(anchor=tk.W)

        self.txt_consola = scrolledtext.ScrolledText(frame_consola, bg="#111111", fg="#00FF00", font=("Consolas", 10))
        self.txt_consola.pack(fill=tk.BOTH, expand=True)
        self.escribir_consola("Sistema iniciado correctamente. Esperando instrucciones...")

    def escribir_consola(self, texto: str) -> None:
        """Añade texto a la caja de salida gráfica."""
        self.txt_consola.insert(tk.END, f"{texto}\n")
        self.txt_consola.see(tk.END)  # Autoscroll hacia abajo

    def ventana_nuevo_registro(self) -> None:
        """Abre una sub-ventana para capturar los datos del cliente."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo Registro")
        ventana.geometry("380x380") # Ligeramente más ancha para mejor ajuste del grid
        ventana.configure(bg="black")
        ventana.grab_set() # Foco a esta ventana

        tk.Label(ventana, text="--- INGRESO DE DATOS ---", **self.estilo_lbl).pack(pady=10)

        # Frame contenedor para el formulario usando grid
        frame_form = tk.Frame(ventana, bg="black")
        frame_form.pack(padx=20, pady=5, fill=tk.X)

        entradas = {}
        campos = ["NOMBRES", "APELLIDOS", "DOCUMENTO", "TELÉFONO", "DIRECCIÓN"]

        for i, campo in enumerate(campos):
            tk.Label(frame_form, text=f"{campo}:", width=12, anchor=tk.W, **self.estilo_lbl).grid(row=i, column=0, pady=8, sticky="w")
            entry = tk.Entry(frame_form, bg="#333333", fg="white", insertbackground="white", font=("Arial", 10))
            entry.grid(row=i, column=1, pady=8, sticky="ew")
            entradas[campo] = entry
            
        frame_form.columnconfigure(1, weight=1) # Permite que los Entry se expandan

        def procesar_registro() -> None:
            nombres = entradas["NOMBRES"].get()
            apellidos = entradas["APELLIDOS"].get()
            documento = entradas["DOCUMENTO"].get()
            telefono = entradas["TELÉFONO"].get()
            direccion = entradas["DIRECCIÓN"].get()

            try:
                # Validaciones
                if not nombres.replace(" ", "").isalpha():
                    raise ValueError("Los nombres solo deben contener letras.")
                if not apellidos.replace(" ", "").isalpha():
                    raise ValueError("Los apellidos solo deben contener letras.")
                if not documento.isdigit() or len(documento) > 15:
                    raise ValueError("El documento debe ser numérico y máximo 15 dígitos.")
                if not telefono.isdigit() or len(telefono) != 10:
                    raise ValueError("El teléfono debe tener exactamente 10 dígitos.")
                if not direccion.strip():
                    raise ValueError("La dirección no puede estar vacía.")

                # Registro exitoso
                self.db.registrar(nombres, apellidos, documento, telefono, direccion)
                messagebox.showinfo("Éxito", "Cliente registrado con éxito en el sistema.", parent=ventana)
                self.escribir_consola(f"Nuevo cliente registrado: {documento} - {nombres} {apellidos}")
                logging.info(f"Cliente registrado exitosamente: {documento}")
                ventana.destroy()

            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e), parent=ventana)
                self.escribir_consola(f"Intento de registro fallido: {e}")
                logging.warning(f"Error de validación en registro: {e}")
            except Exception as e:
                messagebox.showerror("Error Inesperado", str(e), parent=ventana)
                logging.error(f"Error inesperado en registro: {e}", exc_info=True)

        btn_guardar = tk.Button(
            ventana, text="GUARDAR CLIENTE", command=procesar_registro, 
            bg="#006600", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT
        )
        btn_guardar.pack(pady=20)

    def ejecutar_simulacion(self) -> None:
        """Ejecuta las 10 pruebas y muestra la salida en la consola virtual."""
        self.escribir_consola("\n--- Ejecutando 10 Pruebas Automáticas ---")
        logging.info("Inicio de simulación de 10 operaciones.")
        
        docs = ["1010", "2020", "0000", "3030", "4040", "1234", "1010", "5555", "6666", "7777"]
        sala = ReservaSala("S1", "Sala de Espera Central", 40000)

        for i, doc in enumerate(docs, 1):
            try:
                self.escribir_consola(f"Prueba {i}: Cédula {doc}")
                persona = self.db.buscar(doc)
                
                if not persona:
                    self.escribir_consola("-> Cliente no existe. Creando uno...")
                    persona = self.db.registrar("Test", "Prueba", doc, "0000000000", "N/A")
                
                res = Reserva(persona, sala, 1)
                self.escribir_consola(f"-> {res.procesar()}")
                
            except Exception as e:
                logging.error(f"Fallo en prueba {i} con doc {doc}: {e}")
                self.escribir_consola(f"-> ERROR en prueba {i}. Registrado en bitacora.txt")

    def ver_clientes(self) -> None:
        """Lista los clientes registrados en la consola virtual."""
        self.escribir_consola("\n--- LISTA DE CLIENTES ---")
        
        # Nota: Acceder a variables protegidas como _lista o _documento_identidad 
        # va en contra de los principios de encapsulamiento estricto.
        # Sería ideal implementar getters en GestorUsuarios y Cliente (ej: self.db.obtener_clientes())
        if not self.db._lista:
            self.escribir_consola("No hay clientes registrados aún.")
            return

        for cliente in self.db._lista:
            self.escribir_consola(f"[{cliente._documento_identidad}] {cliente._nombres} {cliente._apellidos} - Tel: {cliente._telefono}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionApp(root)
    root.mainloop()