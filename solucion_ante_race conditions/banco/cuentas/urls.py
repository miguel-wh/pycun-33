from django.urls import path
from cuentas.views import home, race_conditions, lock, celery_race_condition, atomic_transactions

urlpatterns = [
    path('', home.index),
    path('saldo/', home.vista_saldo),
    path('reset/', home.vista_reset_saldo),

    # Ejemplo 1: con condicion de carrera
    path('depositar/', race_conditions.vista_depositar),
    path('cargar/', race_conditions.vista_cargar),

    # Ejemplo 2: condicion de carrera resuelto con threading.Lock
    path('depositar_lock/', lock.vista_depositar_lock),
    path('cargar_lock/', lock.vista_cargar_lock),

    # Ejemplo 3: condicion de carrera con celery (no sirve lock)
    path("celery/depositar/", celery_race_condition.vista_depositar_celery, name="vista_depositar_celery"),
    path("celery/cargar/", celery_race_condition.vista_cargar_celery, name="vista_cargar_celery"),

    # Ejemplo 4: condicion de carrera con celery resuelto con transaction.atomic
    path("atomic/depositar/", atomic_transactions.vista_depositar_atomic, name="vista_depositar_atomic"),
    path("atomic/cargar/", atomic_transactions.vista_cargar_atomic, name="vista_cargar_atomic"),
]
