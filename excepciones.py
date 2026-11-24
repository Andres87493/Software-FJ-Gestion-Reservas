class ErrorSoftwareFJ(Exception):
    """Excepción base para el sistema de Software FJ."""
    pass

class DatosInvalidosError(ErrorSoftwareFJ):
    """Se lanza cuando los datos ingresados (nombre, correo, valores) no son válidos."""
    pass

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando el servicio solicitado está ocupado o inactivo."""
    pass

class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza al intentar confirmar, cancelar o procesar una reserva inválida."""
    pass

class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando ocurren errores matemáticos o parámetros inconsistentes en costos."""
    pass
