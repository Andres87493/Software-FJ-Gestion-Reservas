from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError, ServicioNoDisponibleError, CalculoInconsistenteError

class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad del sistema."""
    def __init__(self, id_entidad: str):
        if not id_entidad or not id_entidad.strip():
            raise DatosInvalidosError("El ID de la entidad no puede estar vacío.")
        self._id = id_entidad.strip()

    @property
    def id(self):
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        pass


class Cliente(EntidadBase):
    """Representa un cliente con encapsulación y validaciones estrictas."""
    def __init__(self, id_cliente: str, nombre: str, correo: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatosInvalidosError(f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise DatosInvalidosError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip()

    def obtener_resumen(self) -> str:
        return f"Cliente [{self._id}]: {self._nombre} ({self._correo})"


class Servicio(EntidadBase, ABC):
    """Clase abstracta base para los servicios de Software FJ."""
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor a cero.")
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Método polimórfico y sobrecargado mediante parámetros opcionales."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion: int):
        pass


class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        self.capacidad = capacidad

    def validar_parametros(self, duracion: int):
        if duracion < 1 or duracion > 12:
            raise DatosInvalidosError("La reserva de sala debe ser entre 1 y 12 horas.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(duracion)
        subtotal = (self._tarifa_base * duracion) * (1 - descuento)
        return round(subtotal * (1 + impuesto), 2)

    def obtener_resumen(self) -> str:
        return f"Sala [{self._id}]: {self._nombre} (Capacidad: {self.capacidad} pers. | ${self._tarifa_base}/h)"


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, gama: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_dia, disponible)
        self.gama = gama

    def validar_parametros(self, duracion: int):
        if duracion < 1 or duracion > 30:
            raise DatosInvalidosError("El alquiler de equipos debe ser entre 1 y 30 días.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(duracion)
        recargo_seguro = 15.0 if self.gama.lower() == "alta" else 5.0
        subtotal = ((self._tarifa_base * duracion) + recargo_seguro) * (1 - descuento)
        return round(subtotal * (1 + impuesto), 2)

    def obtener_resumen(self) -> str:
        return f"Equipo [{self._id}]: {self._nombre} (Gama {self.gama} | ${self._tarifa_base}/día)"


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_sesion: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_sesion, disponible)
        self.especialidad = especialidad

    def validar_parametros(self, duracion: int):
        if duracion < 1:
            raise DatosInvalidosError("La asesoría requiere al menos 1 sesión.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(duracion)
        if descuento > 0.50:
            raise CalculoInconsistenteError("El descuento en asesorías no puede superar el 50%.")
        subtotal = (self._tarifa_base * duracion) * (1 - descuento)
        return round(subtotal * (1 + impuesto), 2)

    def obtener_resumen(self) -> str:
        return f"Asesoría [{self._id}]: {self._nombre} ({self.especialidad} | ${self._tarifa_base}/sesión)"
