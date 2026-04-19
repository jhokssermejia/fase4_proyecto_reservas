# Función: Definir errores personalizados para el control del programa.
# Por qué está aquí: La guía exige manejar excepciones para que el sistema no muera ante un dato mal ingresado.

class ErrorDeNegocio(Exception):
    # Base para errores lógicos generales del sistema Software FJ.
    pass

class ErrorEnReserva(ErrorDeNegocio):
    # Se activa si falla la unión entre cliente y servicio.
    pass

# =================================================================
# EXCEPCIONES REQUERIDAS POR LA CLASE CLIENTE (Integración)
# =================================================================

class ErrorDeNombres(ErrorDeNegocio):
    # Se activa cuando el nombre ingresado está vacío o tiene números
    pass

class ErrorDeApellidos(ErrorDeNegocio):
    # Se activa si el apellido se deja en blanco
    pass

class ErrorDeDocumento(ErrorDeNegocio):
    # Se lanza si el documento de identidad contiene letras
    pass

class ErrorDeTelefono(ErrorDeNegocio):
    # Se lanza si el teléfono tiene caracteres no numéricos
    pass