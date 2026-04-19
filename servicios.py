from abc import ABC, abstractmethod

# Función: Base para cualquier objeto del sistema.
# Por qué está aquí: Requisito del Anexo 3 sobre "Entidades generales".
class EntidadBase(ABC):
    def __init__(self, identificador):
        self._id = identificador

    @abstractmethod
    def mostrar_detalle(self):
        # Cada objeto debe saber describirse a sí mismo.
        pass

# Función: Molde para los servicios que ofrece la empresa.
# Por qué está aquí: Clase abstracta obligatoria según la guía.
class Servicio(EntidadBase):
    def __init__(self, identificador, nombre, costo_base):
        super().__init__(identificador)
        self._nombre = nombre
        self._costo_base = costo_base

    @abstractmethod
    def calcular_total(self, cantidad, extra=0):
        # Polimorfismo: cada hijo calcula el costo a su manera.
        pass

# Función: Primer servicio especializado.
class ReservaSala(Servicio):
    def calcular_total(self, horas, descuento=0):
        # Cobra por tiempo y permite restar un descuento opcional.
        return (self._costo_base * horas) - descuento

    def mostrar_detalle(self):
        return f"Sala de Espera: {self._nombre}"

# Función: Segundo servicio especializado.
class AlquilerEquipo(Servicio):
    def calcular_total(self, dias, impuesto=0.19):
        # Suma el impuesto de ley al costo por días.
        return (self._costo_base * dias) * (1 + impuesto)

    def mostrar_detalle(self):
        return f"Equipo: {self._nombre}"

# Función: Tercer servicio especializado.
class Asesoria(Servicio):
    def calcular_total(self, horas, virtual=False):
        # Aplica rebaja si no es presencial.
        ajuste = 0.8 if virtual else 1.0
        return (self._costo_base * horas) * ajuste

    def mostrar_detalle(self):
        return f"Asesoría: {self._nombre}"