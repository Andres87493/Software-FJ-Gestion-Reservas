from modelos import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import SistemaSoftwareFJ
import logging

def ejecutar_simulaciones():
    sistema = SistemaSoftwareFJ()
    print("\n=== INICIANDO SIMULACIONES DEL SISTEMA SOFTWARE FJ ===\n")

    # Simulación 1: Registro válido de cliente
    c1 = sistema.registrar_cliente("C01", "Andrés Aponte", "andres@unad.edu.co")

    # Simulación 2: Registro inválido de cliente (correo sin @)
    sistema.registrar_cliente("C02", "Carlos Ruiz", "correo_invalido.com")

    # Simulación 3: Registro inválido de cliente (nombre muy corto)
    sistema.registrar_cliente("C03", "Lu", "lu@correo.com")

    # Simulación 4: Registro válido de servicios
    s1 = ReservaSala("S01", "Sala Juntas Norte", 50.0, capacidad=10)
    s2 = AlquilerEquipo("S02", "Servidor portátil Xeon", 120.0, gama="alta")
    s3 = AsesoriaEspecializada("S03", "Arquitectura Cloud", 90.0, especialidad="AWS")
    sistema.registrar_servicio(s1)
    sistema.registrar_servicio(s2)
    sistema.registrar_servicio(s3)

    # Simulación 5: Creación inválida de servicio (tarifa negativa)
    try:
        ReservaSala("S04", "Sala Defectuosa", -20.0, capacidad=5)
    except Exception as e:
        logging.error(f"Simulación 5 - Error capturado al crear servicio: {e}")

    # Simulación 6: Reserva exitosa de sala con descuento del 10%
    r1 = sistema.crear_y_confirmar_reserva("R01", c1, s1, duracion=3, descuento=0.10)

    # Simulación 7: Intento de reservar servicio NO disponible (s1 ya está ocupada)
    sistema.crear_y_confirmar_reserva("R02", c1, s1, duracion=2)

    # Simulación 8: Reserva inválida por duración fuera de rango (equipo > 30 días)
    sistema.crear_y_confirmar_reserva("R03", c1, s2, duracion=45)

    # Simulación 9: Encadenamiento de excepciones (descuento excesivo > 50% en asesoría)
    sistema.crear_y_confirmar_reserva("R04", c1, s3, duracion=2, descuento=0.75)

    # Simulación 10: Cancelación exitosa de reserva y posterior re-reserva válida
    if r1:
        r1.cancelar()
    sistema.crear_y_confirmar_reserva("R05", c1, s1, duracion=2, descuento=0.05)

    print("\n=== TODAS LAS SIMULACIONES FINALIZARON CON ÉXITO Y ESTABILIDAD ===")

if __name__ == "__main__":
    ejecutar_simulaciones()
