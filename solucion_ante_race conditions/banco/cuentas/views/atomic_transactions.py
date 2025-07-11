
from decimal import Decimal
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import transaction
from cuentas.models import Cuenta
from cuentas.tasks.atomic_race_condition import (
    actualizar_saldo_depositar_atomic,
    actualizar_saldo_cargo_atomic,
)

def vista_depositar_atomic(request):
    username = request.GET.get("username", "anonimo")
    cantidad = float(request.GET.get("cantidad", 0))

    actualizar_saldo_depositar_atomic.delay(username, cantidad)

    return JsonResponse({"mensaje": f"Deposito de {cantidad} por {username} enviado a Celery (transaccion)"})

def vista_cargar_atomic(request):
    cantidad = float(request.GET.get("cantidad", 0))

    actualizar_saldo_cargo_atomic.delay(cantidad)

    return JsonResponse({"mensaje": f"Cargo de {cantidad} enviado a Celery (transaccion)"})
