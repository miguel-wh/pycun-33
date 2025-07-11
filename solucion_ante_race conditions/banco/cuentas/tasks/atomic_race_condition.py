from decimal import Decimal
import time
import random
from celery import shared_task
from django.db import transaction
from django.contrib.auth.models import User
from cuentas.models import Cuenta

@shared_task
def actualizar_saldo_depositar_atomic(username, cantidad):
    time.sleep(random.uniform(0.005, 0.03))
    cantidad_decimal = Decimal(str(cantidad))

    with transaction.atomic():
        user = User.objects.get(username="miguelangel")
        cuenta = Cuenta.objects.select_for_update().get(usuario=user) # Bloquea la fila  en la base de datos hasta que termine la transaccion.
        saldo_inicial = cuenta.saldo
        cuenta.saldo += cantidad_decimal
        cuenta.save()
        return f"{username} deposito {cantidad_decimal} => saldo: {cuenta.saldo:.2f} (antes: {saldo_inicial:.2f})"

@shared_task
def actualizar_saldo_cargo_atomic(cantidad):
    time.sleep(random.uniform(0.005, 0.03))
    cantidad_decimal = Decimal(str(cantidad))

    with transaction.atomic():
        user = User.objects.get(username="miguelangel")
        cuenta = Cuenta.objects.select_for_update().get(usuario=user)
        saldo_inicial = cuenta.saldo
        cuenta.saldo -= cantidad_decimal
        cuenta.save()
        return f"miguelangel cargo {cantidad_decimal} => saldo: {cuenta.saldo:.2f} (antes: {saldo_inicial:.2f})"
