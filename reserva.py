from excepciones import ErrorEnReserva

# Función: Unir al cliente con el servicio solicitado.
# Por qué está aquí: La guía pide una clase que gestione el estado y proceso de la reserva.
class Reserva:
    def __init__(self, cliente, servicio, tiempo):
        # Usamos la clase Cliente que hizo el otro integrante.
        self._cliente = cliente
        self._servicio = servicio
        self._tiempo = tiempo
        self._estado = "Creada"

    def procesar(self):
        # Ejecuta la lógica del negocio con manejo de errores.
        try:
            if not self._cliente or not self._servicio:
                raise ErrorEnReserva("Datos incompletos.")
            
            pago = self._servicio.calcular_total(self._tiempo)
            self._estado = "Confirmada"
            return f"Reserva de {self._cliente._nombres} lista. Pago: ${pago}"
        except Exception as e:
            self._estado = "Fallida"
            # Relanzamos el error para que el log lo registre.
            raise ErrorEnReserva(f"No se pudo procesar: {e}")