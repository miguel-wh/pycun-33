# PyCUN 33

## 💡 Introducción

Este proyecto demuestra cómo ocurren **condiciones de carrera (race conditions)** en una aplicación Django al simular operaciones concurrentes sobre el saldo de una cuenta bancaria (depósitos y cargos).

Una condición de carrera sucede cuando múltiples operaciones acceden y modifican el mismo recurso (en este caso, el saldo) al mismo tiempo, produciendo resultados inconsistentes.

Aquí mostramos cómo abordar este problema utilizando distintos mecanismos de sincronización:

- `threading.Lock`: útil para proteger operaciones dentro de un mismo proceso.
- Celery + `threading.Lock`: se demuestra que **no es suficiente**, ya que los locks no funcionan entre procesos.
- `transaction.atomic` con `select_for_update`: una solución robusta a nivel de base de datos que garantiza consistencia, incluso con múltiples procesos o workers.
