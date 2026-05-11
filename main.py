import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

# Intentar importar módulos de lógica
try:
    from gestor_usuarios import GestorUsuarios
    from reserva import Reserva
    from servicios import ReservaSala, AlquilerEquipo, Asesoria
    from logger import guardar_log
    from excepciones import ErrorDeNegocio
except ImportError as e:
    print(f"Error de dependencias: {e}")

db = GestorUsuarios()

# --- CONFIGURACIÓN DE ESTILO ---
COLOR_BG = "#1e1e1e"
COLOR_CARD = "#2d2d2d"
COLOR_TEXT = "#e0e0e0"
COLOR_ACCENT = "#3a7ebf"
COLOR_ENTRY = "#3d3d3d"
COLOR_CONSOLE = "#121212"
COLOR_SUCCESS = "#81c784"

# -------------------------
# LÓGICA DE INTERFAZ
# -------------------------

def registrar_cliente():
    try:
        n, a, d = e_n.get().strip(), e_a.get().strip(), e_d.get().strip()
        t, direccion = e_t.get().strip(), e_dir.get().strip()

        if not all([n, a, d, t, direccion]):
            raise ErrorDeNegocio("Todos los campos son obligatorios.")
        
        db.registrar(n, a, d, t, direccion)
        messagebox.showinfo("Éxito", f"Cliente {n} registrado.")
        limpiar_campos()
    except ErrorDeNegocio as e:
        messagebox.showwarning("Atención", str(e))
    except Exception as e:
        guardar_log(f"Error: {e}")
        messagebox.showerror("Error", "Fallo interno en el registro.")

def limpiar_campos():
    for e in [e_n, e_a, e_d, e_t, e_dir]: e.delete(0, tk.END)

def ver_clientes():
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, f"{'DOC':<12} | {'NOMBRE COMPLETO':<25} | {'TELÉFONO':<12}\n")
    salida.insert(tk.END, "-" * 60 + "\n")
    for c in db.obtener_todos():
        nombre = f"{c.nombres} {c.apellidos}"
        salida.insert(tk.END, f"{c.documento_identidad:<12} | {nombre[:25]:<25} | {c.telefono:<12}\n")

def crear_servicio():
    tipo = combo_servicio.get()
    if tipo == "Sala": return ReservaSala("S1", "Sala Central", 40000)
    if tipo == "Equipo": return AlquilerEquipo("E1", "Video Beam", 60000)
    return Asesoria("A1", "Asesoría Técnica", 80000)

# -------------------------
# SIMULADOR MEJORADO (10 Registros Ordenados)
# -------------------------

def simulacion():
    salida.delete("1.0", tk.END)
    guardar_log("Iniciando simulador robusto.")
    
    try:
        servicio_base = crear_servicio()
        # Lista de 10 documentos para la simulación
        docs_simulacion = [
            "1010", "2020", "3030", "ABC_ERR", "4040", 
            "5050", "6060", "7070", "8080", "9090"
        ]

        header = f"{'N°':<4} | {'ESTADO':<10} | {'DETALLES DE LA OPERACIÓN':<45}\n"
        salida.insert(tk.END, header)
        salida.insert(tk.END, "=" * 70 + "\n\n")

        for i, doc in enumerate(docs_simulacion, 1):
            try:
                # Intentar proceso de negocio
                persona = db.buscar(doc)
                if not persona:
                    # Si no existe, lo registramos automáticamente (Simulación de flujo)
                    if not doc.isalnum(): raise ErrorDeNegocio("Formato inválido")
                    persona = db.registrar(f"User{i}", "Simulado", doc, "000-000", "Sede Central")

                res = Reserva(persona, servicio_base)
                info = res.procesar()
                
                # Formato de salida exitosa
                salida.insert(tk.END, f"{i:02d}   | OK         | Doc:{doc} -> {info}\n")

            except ErrorDeNegocio as e:
                salida.insert(tk.END, f"{i:02d}   | RECHAZADO  | Doc:{doc} -> Error: {e}\n")
            except Exception as e:
                salida.insert(tk.END, f"{i:02d}   | CRÍTICO    | Doc:{doc} -> Error inesperado\n")
            
            # Espaciado entre registros para mejor visibilidad
            salida.insert(tk.END, "-" * 70 + "\n")

        salida.insert(tk.END, f"\n[SISTEMA]: Simulación completada. Revise el archivo log para detalles técnicos.")
        guardar_log("Simulación finalizada exitosamente.")

    except Exception as e:
        messagebox.showerror("Error de Simulación", f"No se pudo iniciar el proceso: {e}")

# -------------------------
# CONSTRUCCIÓN DE LA GUI
# -------------------------

root = tk.Tk()
root.title("Sistema de Reservas - Software FJ")
root.geometry("800x750")
root.configure(bg=COLOR_BG)
root.columnconfigure(1, weight=1)

# Estilos ttk
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground=COLOR_ENTRY, background=COLOR_BG, foreground="white")

# Labels y Entries con Grid
fields = [("Nombres:", 0), ("Apellidos:", 1), ("Documento:", 2), ("Teléfono:", 3), ("Dirección:", 4)]
entries = []

for text, row in fields:
    tk.Label(root, text=text, bg=COLOR_BG, fg=COLOR_TEXT, font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="e", padx=20, pady=8)
    en = tk.Entry(root, bg=COLOR_ENTRY, fg="white", insertbackground="white", width=45, relief="flat")
    en.grid(row=row, column=1, sticky="w", padx=20)
    entries.append(en)

e_n, e_a, e_d, e_t, e_dir = entries

tk.Label(root, text="Servicio:", bg=COLOR_BG, fg=COLOR_TEXT, font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="e", padx=20, pady=8)
combo_servicio = ttk.Combobox(root, values=["Sala", "Equipo", "Asesoría"], state="readonly", width=42)
combo_servicio.grid(row=5, column=1, sticky="w", padx=20)
combo_servicio.current(0)

# Botonera
frame_btns = tk.Frame(root, bg=COLOR_BG)
frame_btns.grid(row=6, column=0, columnspan=2, pady=25)

btn_style = {"font": ("Arial", 9, "bold"), "fg": "white", "width": 18, "relief": "flat", "cursor": "hand2"}

tk.Button(frame_btns, text="Registrar", bg="#2e7d32", command=registrar_cliente, **btn_style).pack(side="left", padx=5)
tk.Button(frame_btns, text="Listar", bg=COLOR_ACCENT, command=ver_clientes, **btn_style).pack(side="left", padx=5)
tk.Button(frame_btns, text="Simular (10)", bg="#ef6c00", command=simulacion, **btn_style).pack(side="left", padx=5)
tk.Button(frame_btns, text="Salir", bg="#c62828", command=root.destroy, **btn_style).pack(side="left", padx=5)

# Pantalla de resultados
salida = ScrolledText(root, bg=COLOR_CONSOLE, fg=COLOR_SUCCESS, font=("Consolas", 10), width=90, height=18, relief="flat")
salida.grid(row=7, column=0, columnspan=2, padx=25, pady=10)

root.mainloop()