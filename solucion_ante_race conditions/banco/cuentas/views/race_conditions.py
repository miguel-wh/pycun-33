from decimal import Decimal
import time
import random
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from asgiref.sync import sync_to_async
from cuentas.models import Cuenta


@sync_to_async
def obtener_cuenta(usuario):
    return Cuenta.objects.get(usuario=usuario)

# Funcion de depositos en la cuenta
@sync_to_async
def actualizar_saldo_depositar(cuenta_id, cantidad, quien):
    cuenta = Cuenta.objects.get(id=cuenta_id)
    time.sleep(random.uniform(0.005, 0.03))  # Simular procesamiento
    saldo_inicial = cuenta.saldo
    cantidad_decimal = Decimal(str(cantidad))
    cuenta.saldo += cantidad_decimal
    cuenta.save()
    return f"{quien} depositó {cantidad_decimal} => saldo: {cuenta.saldo:.2f} (antes: {saldo_inicial:.2f})"

# funcion de cagos en la cuenta
@sync_to_async
def actualizar_saldo_cargo(cuenta_id, cantidad):
    cuenta = Cuenta.objects.get(id=cuenta_id)
    time.sleep(random.uniform(0.005, 0.03))
    saldo_inicial = cuenta.saldo
    cantidad_decimal = Decimal(str(cantidad))
    cuenta.saldo -= cantidad_decimal
    cuenta.save()
    return f"miguelangel cargó {cantidad_decimal} => saldo: {cuenta.saldo:.2f} (antes: {saldo_inicial:.2f})"

# Vista async para realizar ingresos (depositos)
async def vista_depositar(request):
    username = request.GET.get("username", "anonimo")
    cantidad = float(request.GET.get("cantidad", 0))

    user_miguel = await sync_to_async(User.objects.get)(username="miguelangel")
    cuenta = await obtener_cuenta(user_miguel)

    resultado = await actualizar_saldo_depositar(cuenta.id, cantidad, username)

    return JsonResponse({"transaccion": resultado})

# Vista async para realizar cargos (gastos)
async def vista_cargar(request):
    cantidad = float(request.GET.get("cantidad", 0))

    user_miguel = await sync_to_async(User.objects.get)(username="miguelangel")
    cuenta = await obtener_cuenta(user_miguel)

    resultado = await actualizar_saldo_cargo(cuenta.id, cantidad)

    return JsonResponse({"transaccion": resultado})