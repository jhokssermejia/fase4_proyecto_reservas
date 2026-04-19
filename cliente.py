# importacion de excepciones a nuestras clases 
from excepciones import ErrorDeNombres
from excepciones import ErrorDeApellidos
from excepciones import ErrorDeDocumento
from excepciones import ErrorDeTelefono 
class Cliente:
    def __init__(self, nombres, apellidos, documento_identidad, telefono, direccion):

        # quita los espacios
        nombre_limpio = nombres.strip()

        # 2 verifica que hallan datos
        if not nombre_limpio:
            raise ErrorDeNombres("El nombre no puede estar vacío")

        # separa las palabras
        palabras = nombre_limpio.split()

        # Recorre las palabra
        for palabra in palabras:

            # revisa que las palabras sea solo texto 
            if not palabra.isalpha():
                raise ErrorDeNombres("El nombre solo debe contener letras")

        # Validación de apellidos
        if not apellidos.strip():
            raise ErrorDeApellidos("no puedes dejar el cuadro sin el apellido.")

        # Validación de documento
        if not documento_identidad.isdigit():
            raise ErrorDeDocumento("El documento debe contener solo números.")

        # Validación de teléfono
        if not telefono.isdigit():
            raise ErrorDeTelefono("Para el telefono debe contener solo números")

        # Encapsulación
        self._nombres = nombres
        self._apellidos = apellidos
        self._documento_identidad = documento_identidad
        self._telefono = telefono
        self._direccion = direccion
