from gestor_usuarios import GestorUsuarios
from servicios import ReservaSala
from reserva import Reserva
import datetime

# Función: Guardar fallos en un archivo físico.
def guardar_log(texto):
    with open("bitacora.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {texto}\n")

# Función: El ciclo de 10 pruebas que pide el Anexo 3.
def simulacion_obligatoria(gestor):
    print("\n--- Ejecutando 10 Pruebas Automáticas ---")
    guardar_log("Inicio de simulación de 10 operaciones.")
    docs = ["1010", "2020", "0000", "3030", "4040", "1234", "1010", "5555", "6666", "7777"]
    sala = ReservaSala("S1", "Sala de Espera Central", 40000)

    for i, d in enumerate(docs, 1):
        try:
            print(f"Prueba {i}: Cédula {d}")
            persona = gestor.buscar(d)
            if not persona:
                print("Cliente no existe. Creando uno...")
                persona = gestor.registrar("Test", "Prueba", d, "0", "N/A")
            
            res = Reserva(persona, sala, 1)
            print(res.procesar())
        except Exception as e:
            guardar_log(f"Fallo en prueba {i}: {e}")
            print(f"Error registrado en bitacora.txt")

def menu():
    db = GestorUsuarios()
    while True:
        print("\n--- SOFTWARE DE GESTION - MENÚ ---")
        print("1. NUEVO REGISTRO")
        print("2. SIMULACIÓN (10 OPERACIONES)")
        print("3. VER CLIENTES ")
        print("4. SALIR")
        
        op = input("OPCIÓN: ")
        
        if op == "1":
            print("\n--- INGRESO DE DATOS ---")
            try:
                # Captura y validación inmediata campo por campo
                n = input("NOMBRES: ")
                # Se exige que el campo tenga contenido y sea estrictamente alfabético
                if not n.replace(" ", "").isalpha():
                    raise ValueError("Los nombres solo deben contener letras, sin números ni caracteres especiales.")

                a = input("APELLIDOS: ")
                # Se exige que el campo tenga contenido y sea estrictamente alfabético
                if not a.replace(" ", "").isalpha():
                    raise ValueError("Los apellidos solo deben contener letras, sin números ni caracteres especiales.")

                d = input("DOCUMENTO: ")
                if not d.isdigit() or len(d) > 15:
                    raise ValueError("El documento debe ser numérico y tener máximo 15 dígitos.")

                t = input("TELÉFONO: ")
                if not t.isdigit() or len(t) != 10:
                    raise ValueError("El teléfono debe ser numérico y tener exactamente 10 dígitos.")

                dir = input("DIRECCIÓN: ")
                if not dir.strip():
                    raise ValueError("La dirección no puede estar vacía.")

                # Si pasa todas las validaciones inmediatas, se registra en memoria
                db.registrar(n, a, d, t, dir)
                print("Cliente registrado con éxito en el sistema.")

            except ValueError as e:
                # El error detiene el proceso de inmediato y vuelve al menú principal
                print(f"Fallo en el ingreso: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")
                
        elif op == "2":
            simulacion_obligatoria(db)
            
        elif op == "3":
            print("\n--- LISTA DE CLIENTES ---")
            for c in db._lista:
                print(f"[{c._documento_identidad}] {c._nombres} {c._apellidos} - Tel: {c._telefono}")
                
        elif op == "4":
            print("Cerrando sistema...")
            break

if __name__ == "__main__":
    menu()