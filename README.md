# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para la **Fase 4 - Componente Práctico (Prácticas Simuladas)** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Autor
* **Andrés Sebastián Aponte Mahecha** (Grupo 644)

## Arquitectura del Sistema (POO y Manejo de Excepciones)
El sistema está implementado en Python sin uso de bases de datos (persistencia en memoria mediante estructuras de listas y objetos):
* `excepciones.py`: Jerarquía de excepciones personalizadas (`ErrorSoftwareFJ`, `DatosInvalidosError`, `ServicioNoDisponibleError`, `ReservaInvalidaError`, `CalculoInconsistenteError`).
* `modelos.py`: Clases abstractas (`EntidadBase`, `Servicio`), encapsulación con validaciones (`Cliente`) y polimorfismo en tres servicios especializados (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`).
* `gestor.py`: Gestión de reservas y control robusto mediante bloques `try/except`, `try/except/else`, `try/except/finally`, encadenamiento de excepciones (`raise ... from e`) y registro en `software_fj.log` mediante `logging`.
* `main.py`: Ejecución secuencial de 10 simulaciones completas (casos válidos e inválidos) demostrando estabilidad ante errores.

## Ejecución
```bash
python main.py
