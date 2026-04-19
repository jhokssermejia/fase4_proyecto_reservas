from cliente import Cliente

# Función: Manejar la lista de clientes en la RAM.
# Por qué está aquí: Para no usar bases de datos, guardamos todo en listas mientras el programa corre.
class GestorUsuarios:
    def __init__(self):
        self._lista = []
        self._precargar()

    def _precargar(self):
        # Metemos datos reales de tus colegas para dar seriedad al proyecto.
        try:
            self._lista.append(Cliente("John Hermes", "Alvarez Roman", "1010", "300000", "Anserma"))
            self._lista.append(Cliente("Leonardo", "Alvarez", "2020", "310000", "Anserma"))
            self._lista.append(Cliente("Cesar", "Giraldo", "3030", "320000", "Anserma"))
            self._lista.append(Cliente("Jenny", "Aricapa", "4040", "330000", "Anserma"))
        except:
            pass # Si falla la clase Cliente externa, el sistema sigue.

    def buscar(self, cedula):
        for c in self._lista:
            if c._documento_identidad == cedula:
                return c
        return None

    def registrar(self, n, a, d, t, dir):
        nuevo = Cliente(n, a, d, t, dir)
        self._lista.append(nuevo)
        return nuevo