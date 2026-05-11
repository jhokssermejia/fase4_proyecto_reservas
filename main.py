import tkinter as tk                                                 # libreria de tkinter 
from tkinter import messagebox                                    
from tkinter.scrolledtext import ScrolledText                     
from tkinter import ttk

from gestor_usuarios import GestorUsuarios                            # importando diferente py para la ejecucion
from reserva import Reserva
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from logger import guardar_log
from excepciones import ErrorDeNegocio

db = GestorUsuarios()

# -------------------------
# FUNCIÓN: REGISTRAR CLIENTE
# -------------------------

def registrar_cliente():
    try:
        n = e_n.get().strip()
        a = e_a.get().strip()
        d = e_d.get().strip()
        t = e_t.get().strip()
        dir = e_dir.get().strip()

        db.registrar(n, a, d, t, dir)
        messagebox.showinfo("Éxito", "Cliente registrado correctamente")

        e_n.delete(0, tk.END)
        e_a.delete(0, tk.END)
        e_d.delete(0, tk.END)
        e_t.delete(0, tk.END)
        e_dir.delete(0, tk.END)

    except ErrorDeNegocio as e:
        messagebox.showerror("Error de datos", str(e))
    except Exception as e:
        messagebox.showerror("Error inesperado", str(e))


# -------------------------
# FUNCIÓN: VER CLIENTES
# -------------------------
def ver_clientes():
    salida.delete("1.0", tk.END)

    # Obtener el servicio seleccionado actualmente
    try:
        servicio = crear_servicio_desde_seleccion()
        detalle_servicio = servicio.mostrar_detalle()
    except:
        detalle_servicio = "Sin servicio seleccionado"

    # Mostrar clientes y servicio seleccionado
    for c in db.obtener_todos():
        salida.insert(
            tk.END,
            f"{c.documento_identidad} - {c.nombres} {c.apellidos} - "
            f"Tel: {c.telefono} - Dir: {c.direccion} - "
            f"Servicio: {detalle_servicio}\n"
        )

# -------------------------
# FUNCIÓN DE SERVICIOS
# -------------------------

def crear_servicio_desde_seleccion():
    tipo = combo_servicio.get()
    if tipo == "Sala":
        return ReservaSala("S1", "Sala Central", 40000)
    elif tipo == "Equipo":
        return AlquilerEquipo("E1", "Video Beam", 60000)
    elif tipo == "Asesoría":
        return Asesoria("A1", "Asesoría Técnica", 80000)
    else:
        raise ValueError("Tipo de servicio no válido")

# -------------------------
# FUNCIÓN: SIMULACIÓN
# -------------------------

def simulacion():
    salida.delete("1.0", tk.END)
    guardar_log("Inicio de simulación de 10 operaciones.")

    try:
        servicio_base = crear_servicio_desde_seleccion()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el servicio: {e}")
        return

    docs = ["1010", "2020", "0000", "3030", "4040",
            "1234", "1010", "5555", "6666", "7777"]

    for i, d in enumerate(docs, 1):
        try:
            salida.insert(tk.END, f"Prueba {i}: Cédula {d}\n")
            persona = db.buscar(d)

            if not persona:
                salida.insert(tk.END, "Cliente no existe. Creando uno automático...\n")
                persona = db.registrar("Auto", "Generado", d, "3000000000", "N/A")

            # Crear un servicio nuevo basado en la selección
            if isinstance(servicio_base, ReservaSala):
                servicio = ReservaSala("S1", servicio_base._nombre, servicio_base._costo_base)
            elif isinstance(servicio_base, AlquilerEquipo):
                servicio = AlquilerEquipo("E1", servicio_base._nombre, servicio_base._costo_base)
            else:
                servicio = Asesoria("A1", servicio_base._nombre, servicio_base._costo_base)

            # Reserva SIN tiempo
            res = Reserva(persona, servicio)
            resultado = res.procesar()

            salida.insert(
                tk.END,
                f"{resultado}\n"
                f"----------------------------------------\n\n"
            )

        except Exception as e:
            guardar_log(f"Fallo en prueba {i}: {e}")
            salida.insert(tk.END, f"Error en prueba {i}: {e}\n\n")

    guardar_log("Fin de simulación de 10 operaciones.")

# -------------------------
# VENTANA PRINCIPAL
# -------------------------

root = tk.Tk()
root.title("Sistema de Reservas")
root.geometry("700x650")

# -------------------------
# CAMPOS DE REGISTRO
# -----------------------

tk.Label(root, text="Nombres:").pack()
e_n = tk.Entry(root, width=40); e_n.pack()

tk.Label(root, text="Apellidos:").pack()
e_a = tk.Entry(root, width=40); e_a.pack()

tk.Label(root, text="Documento:").pack()
e_d = tk.Entry(root, width=40); e_d.pack()

tk.Label(root, text="Teléfono:").pack()
e_t = tk.Entry(root, width=40); e_t.pack()

tk.Label(root, text="Dirección:").pack()
e_dir = tk.Entry(root, width=40); e_dir.pack()

tk.Label(root, text="Tipo de servicio:").pack(pady=(10, 0))
combo_servicio = ttk.Combobox(root, values=["Sala", "Equipo", "Asesoría"], state="readonly", width=30)
combo_servicio.pack()
combo_servicio.current(0)

# -------------------------
# BOTONES
# -------------------------

tk.Button(root, text="Registrar Cliente", width=25, command=registrar_cliente).pack(pady=10)
tk.Button(root, text="Ver Clientes", width=25, command=ver_clientes).pack(pady=10)
tk.Button(root, text="Simulación (10 operaciones)", width=25, command=simulacion).pack(pady=10)
tk.Button(root, text="Salir", width=25, command=root.destroy).pack(pady=10)

# -------------------------
# CUADRO DE SALIDA
# -------------------------

salida = ScrolledText(root, wrap=tk.WORD, width=80, height=15)
salida.pack(pady=10)

root.mainloop()
