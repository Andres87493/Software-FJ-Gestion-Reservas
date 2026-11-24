import logging
from modelos import Cliente, Servicio
from excepciones import (
    ErrorSoftwareFJ,
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
)

# Configuración del sistema de Logs (archivo + consola)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("software_fj.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio._nombre}' no está disponible.")
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"
        self.total = 0.0

    def confirmar(self, descuento: float = 0.0, impuesto: float = 0.19):
        if self.estado != "PENDIENTE":
            raise ReservaInvalidaError(f"No se puede confirmar la reserva {self.id_reserva} en estado {self.estado}.")
        try:
            self.total = self.servicio.calcular_costo(self.duracion, descuento, impuesto)
        except Exception as e:
            # Encadenamiento de excepciones obligatorio en rúbrica
            raise CalculoInconsistenteError(f"Fallo al liquidar reserva {self.id_reserva}") from e
        else:
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False
            logging.info(f"Reserva {self.id_reserva} CONFIRMADA para {self.cliente.nombre}. Total: ${self.total}")
        finally:
            logging.info(f"Auditoría de intento de confirmación finalizada para {self.id_reserva}.")

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.id_reserva} ya se encuentra cancelada.")
        self.estado = "CANCELADA"
        self.servicio.disponible = True
        logging.warning(f"Reserva {self.id_reserva} CANCELADA. Servicio liberado.")


class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str):
        try:
            nuevo = Cliente(id_cliente, nombre, correo)
        except DatosInvalidosError as e:
            logging.error(f"Error registrando cliente [{id_cliente}]: {e}")
            return None
        else:
            self.clientes.append(nuevo)
            logging.info(f"Cliente registrado exitosamente: {nuevo.obtener_resumen()}")
            return nuevo

    def registrar_servicio(self, servicio: Servicio):
        self.servicios.append(servicio)
        logging.info(f"Servicio agregado al catálogo: {servicio.obtener_resumen()}")

    def crear_y_confirmar_reserva(self, id_res: str, cliente: Cliente, servicio: Servicio, duracion: int, descuento: float = 0.0):
        try:
            if cliente is None or servicio is None:
                raise ReservaInvalidaError("Cliente o servicio nulo en la solicitud de reserva.")
            reserva = Reserva(id_res, cliente, servicio, duracion)
            reserva.confirmar(descuento=descuento)
            self.reservas.append(reserva)
            return reserva
        except ErrorSoftwareFJ as e:
            logging.error(f"Fallo controlado en operación [{id_res}]: {e} | Causa: {e.__cause__}")
            return None
        except Exception as e:
            logging.critical(f"Error inesperado capturado en [{id_res}]: {e}")
            return None
        finally:
            logging.info(f"--- Fin de transacción {id_res} ---")
