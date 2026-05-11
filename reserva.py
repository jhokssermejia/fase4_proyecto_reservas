from excepciones import ErrorEnReserva
from logger import guardar_log

# -------------------------
# CREAMOS LA CLASE RESERVA 
# -------------------------
class Reserva:

    def __init__(self, cliente, servicio):
        self._cliente = cliente       # DATOS QUE NO SE PUEDEN MODIFICAR 
        self._servicio = servicio
        self._estado = "Creada"

    # -------------------------
    # FUNCIÓN PROCESAR EN CASO DE NO INGRESAR LOS DATOS CORRECTAMENTE 
    # -------------------------
    def procesar(self):
        try:
            if not self._cliente or not self._servicio:
                raise ErrorEnReserva("Datos incompletos para la reserva")

            # Ya NO se usa tiempo, solo precio fijo
            total = self._servicio.calcular_total()

        except Exception as e:
            self._estado = "Fallida"
            guardar_log(f"Error en reserva: {e}")
            raise ErrorEnReserva(f"No se pudo procesar la reserva: {e}")

        else:
            self._estado = "Confirmada"
            return (
                f"Reserva confirmada.\n"
                f"Cliente: {self._cliente.nombres} {self._cliente.apellidos}\n"
                f"Documento: {self._cliente.documento_identidad}\n"
                f"Teléfono: {self._cliente.telefono}\n"
                f"Dirección: {self._cliente.direccion}\n"
                f"Servicio: {self._servicio.mostrar_detalle()}\n"
                f"Pago total: ${total:.2f}"
            )

        finally:
            guardar_log("Proceso de reserva finalizado")
