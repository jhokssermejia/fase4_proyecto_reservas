from cliente import Cliente
from excepciones import ErrorDeDocumento, ErrorDeNegocio
from logger import guardar_log

class GestorUsuarios:

    # -------------------------
    # Precarga de datos iniciales
    # -------------------------

    def __init__(self):
        self._lista = []
        self._precargar()


    def _precargar(self):
        datos = [
            ("John", "Alvarez", "1010", "3000000000", "Anserma"),
            ("Leonardo", "Alvarez", "2020", "3100000000", "Anserma"),
            ("Cesar", "Giraldo", "3030", "3200000000", "Anserma"),
            ("Jenny", "Aricapa", "4040", "3300000000", "Anserma")
        ]
        for d in datos:
            try:
                self._lista.append(Cliente(*d))
            except Exception as e:
                guardar_log(f"Error precarga cliente {d[2]}: {e}")
    
    # Buscar cliente por cédula

    def buscar(self, cedula):
        return next((c for c in self._lista if c.documento_identidad == cedula), None)

    def obtener_todos(self):
        return list(self._lista)
    
     # Validar duplicado

    def registrar(self, n, a, d, t, dir):
        try:
            if self.buscar(d):
                raise ErrorDeDocumento(f"El documento {d} ya está registrado")

            cliente = Cliente(n, a, d, t, dir)


            # errores de registros 

        except ErrorDeNegocio as e:
            guardar_log(f"Error registrando cliente {d}: {e}")
            raise ErrorDeDocumento(f"No se pudo registrar el cliente: {e}")

        except Exception as e:
            guardar_log(f"Error inesperado registrando {d}: {e}")
            raise ErrorDeDocumento("Error inesperado al registrar cliente")

        else:
            self._lista.append(cliente)
            guardar_log(f"Cliente registrado correctamente: {d}")
            return cliente

        finally:
            guardar_log("Fin de intento de registro")
