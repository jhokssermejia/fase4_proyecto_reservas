from excepciones import (
    ErrorDeNombres,
    ErrorDeApellidos,
    ErrorDeDocumento,
    ErrorDeTelefono
)

class Cliente:
    def __init__(self, nombres, apellidos, documento_identidad, telefono, direccion):

        # -------------------------
        # VALIDACIÓN DE NOMBRES
        # -------------------------
        nombre_limpio = nombres.strip()
        if not nombre_limpio:
            raise ErrorDeNombres("El nombre no puede estar vacío")

        for palabra in nombre_limpio.split():
            if not palabra.isalpha():
                raise ErrorDeNombres("El nombre solo debe contener letras")

        # -------------------------
        # VALIDACIÓN DE APELLIDOS
        # -------------------------
        apellidos_limpios = apellidos.strip()
        if not apellidos_limpios:
            raise ErrorDeApellidos("El apellido no puede estar vacío")

        for palabra in apellidos_limpios.split():
            if not palabra.isalpha():
                raise ErrorDeApellidos("El apellido solo debe contener letras")

        # -------------------------
        # VALIDACIÓN DE DOCUMENTO
        # -------------------------
        if not documento_identidad.isdigit():
            raise ErrorDeDocumento("El documento debe contener solo números")

        # -------------------------
        # VALIDACIÓN DE TELÉFONO
        # -------------------------
        if not telefono.isdigit():
            raise ErrorDeTelefono("El teléfono debe contener solo números")

        # -------------------------
        # ENCAPSULAMIENTO
        # -------------------------
        self.__nombres = nombre_limpio
        self.__apellidos = apellidos_limpios
        self.__documento_identidad = documento_identidad
        self.__telefono = telefono
        self.__direccion = direccion

    # -------------------------
    # GETTERS solo lectura
    # -------------------------
    @property
    def nombres(self):
        return self.__nombres

    @property
    def apellidos(self):
        return self.__apellidos

    @property
    def documento_identidad(self):
        return self.__documento_identidad

    @property
    def telefono(self):
        return self.__telefono

    @property
    def direccion(self):
        return self.__direccion
