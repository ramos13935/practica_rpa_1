class Persona:
    def __init__(self, nombre, telefono, poblacion, habitaciones, precio_max):
        self.nombre = nombre
        self.telefono = telefono
        self.poblacion = poblacion
        self.habitaciones = habitaciones
        self.precio_max = precio_max
    #
    # @property
    # def nombre(self):
    #     return self._nombre
    # @nombre.setter
    # def nombre(self, nombre):
    #     self._nombre = nombre
    #
    # @property
    # def telefono(self):
    #     return self._telefono
    #
    # @telefono.setter
    # def telefono(self, telefono):
    #     self._telefono = telefono
    #
    # @property
    # def poblacion(self):
    #     return self._poblacion
    # @poblacion.setter
    # def poblacion(self, poblacion):
    #     self._poblacion = poblacion
    #
    #
    # @property
    # def habitaciones(self):
    #     return self._habitaciones
    # @habitaciones.setter
    # def habitaciones(self, habitaciones):
    #     self._habitaciones = habitaciones
    #
    # @property
    # def precio_max(self):
    #     return self._precio_max
    #
    # @precio_max.setter
    # def precio_max(self, precio_max):
    #     self._precio_max = precio_max

    def __str__(self):
        return f"Nombre : {self._nombre}, Teléfono: {self._telefono} Población: {self._poblacion} Habitaciones: {self._habitaciones} Precio máximo: {self._precio_max}"