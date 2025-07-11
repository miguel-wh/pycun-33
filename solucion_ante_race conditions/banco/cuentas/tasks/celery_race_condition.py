# cuentas/tasks/celery_race_condition.py

from decimal import Decimal
import time
import random
import threading
from celery import shared_task
from django.contrib.auth.models import User
from cuentas.models import Cuenta

lock = threading.Lock()

@shared_task
def actualizar_saldo_depositar_celery(username, cantidad):
    with lock:
        user = User.objects.get(username="miguelangel")
        cuenta = Cuenta.objects.get(usuario=user)

        time.sleep(random.uniform(0.005, 0.03))
        saldo_inicial = cuenta.saldo
        cantidad_decimal = Decimal(str(cantidad))
        cuenta.saldo += cantidad_decimal
        cuenta.save()
        return f"{username} depositó {cantidad_decimal} => saldo: {cuenta.saldo:.2f} (antes: {saldo_inicial:.2f})"

@shared_task
def actualizar_saldo_cargo_celery(cantidad):
    with lock:
        user = User.objects.get(username="miguelangel")
        cuenta = Cuenta.objects.get(usuario=user)

        time.sleep(random.uniform(0.005, 0.03))
        saldo_inicial = cuenta.saldo
        cantidad_decimal = Decimal(str(cantidad))
        cuenta.saldo -= cantidad_decimal
        cuenta.save()
        return f"miguelangel cargó {cantidad_decimal} => saldo: {cuenta.saldo:.2f} (antes: {saldo_inicial:.2f})"
