# Función: Definir errores personalizados para el control del programa.
# Por qué está aquí: La guía exige manejar excepciones para que el sistema no muera ante un dato mal ingresado.

class ErrorDeNegocio(Exception):
    """Error base para la lógica de negocio."""
    pass


class ErrorEnReserva(ErrorDeNegocio):
    """Errores relacionados con el proceso de reservas."""
    pass


class ErrorDeNombres(ErrorDeNegocio):
    """Errores en los nombres del cliente."""
    pass


class ErrorDeApellidos(ErrorDeNegocio):
    """Errores en los apellidos del cliente."""
    pass


class ErrorDeDocumento(ErrorDeNegocio):
    """Errores relacionados con el documento de identidad."""
    pass


class ErrorDeTelefono(ErrorDeNegocio):
    """Errores relacionados con el teléfono."""
    pass

