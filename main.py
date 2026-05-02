import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime

# Asegúrate de tener estos módulos en el mismo directorio
from gestor_usuarios import GestorUsuarios
from servicios import ReservaSala
from reserva import Reserva

# Función externa para guardar log físico
def guardar_log(texto):
    with open("bitacora.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {texto}\n")

class GestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Software de Gestión")
        self.root.geometry("700x550")
        self.root.configure(bg="black")
        
        # Inicializar gestor
        self.db = GestorUsuarios()

        # Estilos compartidos
        self.estilo_btn = {"bg": "#333333", "fg": "white", "font": ("Arial", 11, "bold"), "relief": tk.FLAT, "width": 25}
        self.estilo_lbl = {"bg": "black", "fg": "white", "font": ("Arial", 12)}

        self._crear_interfaz()

    def _crear_interfaz(self):
        # --- Frame Superior (Botones) ---
        frame_botones = tk.Frame(self.root, bg="black")
        frame_botones.pack(pady=20)

        # Título
        lbl_titulo = tk.Label(frame_botones, text="--- MENÚ PRINCIPAL ---", font=("Arial", 14, "bold"), bg="black", fg="#00FF00")
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Botones
        btn_nuevo = tk.Button(frame_botones, text="1. NUEVO REGISTRO", command=self.ventana_nuevo_registro, **self.estilo_btn)
        btn_nuevo.grid(row=1, column=0, padx=10, pady=5)

        btn_simulacion = tk.Button(frame_botones, text="2. SIMULACIÓN (10 OP)", command=self.ejecutar_simulacion, **self.estilo_btn)
        btn_simulacion.grid(row=1, column=1, padx=10, pady=5)

        btn_ver = tk.Button(frame_botones, text="3. VER CLIENTES", command=self.ver_clientes, **self.estilo_btn)
        btn_ver.grid(row=2, column=0, padx=10, pady=5)

        btn_salir = tk.Button(frame_botones, text="4. SALIR", command=self.root.quit, bg="#770000", fg="white", font=("Arial", 11, "bold"), relief=tk.FLAT, width=25)
        btn_salir.grid(row=2, column=1, padx=10, pady=5)

        # --- Frame Inferior (Consola de salida) ---
        frame_consola = tk.Frame(self.root, bg="black")
        frame_consola.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        lbl_consola = tk.Label(frame_consola, text="Salida del Sistema:", **self.estilo_lbl)
        lbl_consola.pack(anchor=tk.W)

        self.txt_consola = scrolledtext.ScrolledText(frame_consola, bg="#111111", fg="#00FF00", font=("Consolas", 10))
        self.txt_consola.pack(fill=tk.BOTH, expand=True)
        self.escribir_consola("Sistema iniciado correctamente. Esperando instrucciones...")

    def escribir_consola(self, texto):
        """Añade texto a la caja de salida gráfica."""
        self.txt_consola.insert(tk.END, f"{texto}\n")
        self.txt_consola.see(tk.END)  # Autoscroll hacia abajo

    def ventana_nuevo_registro(self):
        """Abre una sub-ventana para capturar los datos del cliente."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo Registro")
        ventana.geometry("350x350")
        ventana.configure(bg="black")
        ventana.grab_set() # Foco a esta ventana

        tk.Label(ventana, text="--- INGRESO DE DATOS ---", **self.estilo_lbl).pack(pady=10)

        # Diccionario para guardar los widgets Entry
        entradas = {}
        campos = ["NOMBRES", "APELLIDOS", "DOCUMENTO", "TELÉFONO", "DIRECCIÓN"]

        for campo in campos:
            frame_campo = tk.Frame(ventana, bg="black")
            frame_campo.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame_campo, text=f"{campo}:", width=12, anchor=tk.W, **self.estilo_lbl).pack(side=tk.LEFT)
            entry = tk.Entry(frame_campo, bg="#333333", fg="white", insertbackground="white")
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            entradas[campo] = entry

        def procesar_registro():
            n = entradas["NOMBRES"].get()
            a = entradas["APELLIDOS"].get()
            d = entradas["DOCUMENTO"].get()
            t = entradas["TELÉFONO"].get()
            dir_val = entradas["DIRECCIÓN"].get()

            try:
                # Validaciones originales
                if not n.replace(" ", "").isalpha():
                    raise ValueError("Los nombres solo deben contener letras.")
                if not a.replace(" ", "").isalpha():
                    raise ValueError("Los apellidos solo deben contener letras.")
                if not d.isdigit() or len(d) > 15:
                    raise ValueError("El documento debe ser numérico y máximo 15 dígitos.")
                if not t.isdigit() or len(t) != 10:
                    raise ValueError("El teléfono debe tener exactamente 10 dígitos.")
                if not dir_val.strip():
                    raise ValueError("La dirección no puede estar vacía.")

                # Registro exitoso
                self.db.registrar(n, a, d, t, dir_val)
                messagebox.showinfo("Éxito", "Cliente registrado con éxito en el sistema.", parent=ventana)
                self.escribir_consola(f"Nuevo cliente registrado: {d} - {n} {a}")
                ventana.destroy()

            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e), parent=ventana)
                self.escribir_consola(f"Intento de registro fallido: {e}")
            except Exception as e:
                messagebox.showerror("Error Inesperado", str(e), parent=ventana)

        btn_guardar = tk.Button(ventana, text="GUARDAR CLIENTE", command=procesar_registro, bg="#006600", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT)
        btn_guardar.pack(pady=20)

    def ejecutar_simulacion(self):
        """Ejecuta las 10 pruebas y muestra la salida en la consola virtual."""
        self.escribir_consola("\n--- Ejecutando 10 Pruebas Automáticas ---")
        guardar_log("Inicio de simulación de 10 operaciones.")
        
        docs = ["1010", "2020", "0000", "3030", "4040", "1234", "1010", "5555", "6666", "7777"]
        sala = ReservaSala("S1", "Sala de Espera Central", 40000)

        for i, d in enumerate(docs, 1):
            try:
                self.escribir_consola(f"Prueba {i}: Cédula {d}")
                persona = self.db.buscar(d)
                
                if not persona:
                    self.escribir_consola("-> Cliente no existe. Creando uno...")
                    persona = self.db.registrar("Test", "Prueba", d, "0000000000", "N/A")
                
                res = Reserva(persona, sala, 1)
                # Asumiendo que res.procesar() devuelve un string con el resultado
                self.escribir_consola(f"-> {res.procesar()}")
                
            except Exception as e:
                guardar_log(f"Fallo en prueba {i}: {e}")
                self.escribir_consola(f"-> ERROR en prueba {i}. Registrado en bitacora.txt")

    def ver_clientes(self):
        """Lista los clientes registrados en la consola virtual."""
        self.escribir_consola("\n--- LISTA DE CLIENTES ---")
        if not self.db._lista:
            self.escribir_consola("No hay clientes registrados aún.")
            return

        for c in self.db._lista:
            self.escribir_consola(f"[{c._documento_identidad}] {c._nombres} {c._apellidos} - Tel: {c._telefono}")

if __name__ == "__main__":
    # Creamos la ventana principal de Tkinter y la pasamos a nuestra clase
    root = tk.Tk()
    app = GestionApp(root)
    root.mainloop()