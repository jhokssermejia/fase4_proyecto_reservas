from abc import ABC, abstractmethod

# Clase base general
class EntidadBase(ABC):
    def __init__(self, identificador):
        self._id = identificador

    # -------------------------
    # Métodos con abstracción
    # -------------------------
    @abstractmethod
    def mostrar_detalle(self):
        pass


# -------------------------
# Clase abstracta Servicio
# -------------------------
class Servicio(EntidadBase):
    def __init__(self, identificador, nombre, costo_base):
        super().__init__(identificador)
        self._nombre = nombre
        self._costo_base = costo_base

    # GETTERS para acceder a las clases hijas
    @property
    def nombre(self):
        return self._nombre

    @property
    def costo_base(self):
        return self._costo_base

    # Ya NO recibe cantidad, porque NO usamos tiempo
    @abstractmethod
    def calcular_total(self):
        pass


# -------------------------
# CREACIÓN DE SERVICIOS 
# -------------------------

class ReservaSala(Servicio):
    def calcular_total(self):
        # Precio fijo
        return self.costo_base

    def mostrar_detalle(self):
        return f"Sala: {self.nombre}"


class AlquilerEquipo(Servicio):
    def calcular_total(self):
        # Precio fijo + IVA opcional
        return self.costo_base * 1.19

    def mostrar_detalle(self):
        return f"Equipo: {self.nombre}"


class Asesoria(Servicio):
    def calcular_total(self):
        # Precio fijo
        return self.costo_base

    def mostrar_detalle(self):
        return f"Asesoría: {self.nombre}"
