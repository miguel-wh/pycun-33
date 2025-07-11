### LOCK
import asyncio
from decimal import Decimal
import time
import random
import threading
from django.http import JsonResponse
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from cuentas.models import Cuenta

# Lock global para sincronizar acceso
cuenta_lock = threading.Lock()

@sync_to_async
def obtener_cuenta(usuario):
    return Cuenta.objects.get(usuario=usuario)

@sync_to_async
def actualizar_saldo_depositar_lock(cuenta_id, cantidad, quien):
    with cuenta_lock:
        cuenta = Cuenta.objects.get(id=cuenta_id)
        time.sleep(random.uniform(0.005, 0.03))
        saldo_inicial = cuenta.saldo
        cantidad_decimal = Decimal(str(cantidad))
        cuenta.saldo += cantidad_decimal
        cuenta.save()
        return f"[LOCK] {quien} depositó {cantidad_decimal} => saldo: {cuenta.saldo:.2f} (antes: {saldo_inicial:.2f})"

@sync_to_async
def actualizar_saldo_cargo_lock(cuenta_id, cantidad):
    with cuenta_lock:
        cuenta = Cuenta.objects.get(id=cuenta_id)
        time.sleep(random.uniform(0.005, 0.03))
        saldo_inicial = cuenta.saldo
        cantidad_decimal = Decimal(str(cantidad))
        cuenta.saldo -= cantidad_decimal
        cuenta.save()
        return f"[LOCK] miguelangel cargó {cantidad_decimal} => saldo: {cuenta.saldo:.2f} (antes: {saldo_inicial:.2f})"

# Vista async para depósitos con lock
async def vista_depositar_lock(request):
    username = request.GET.get("username", "anonimo")
    cantidad = float(request.GET.get("cantidad", 0))

    user_miguel = await sync_to_async(User.objects.get)(username="miguelangel")
    cuenta = await obtener_cuenta(user_miguel)

    resultado = await actualizar_saldo_depositar_lock(cuenta.id, cantidad, username)

    return JsonResponse({"transaccion": resultado})

# Vista async para cargos con lock
async def vista_cargar_lock(request):
    cantidad = float(request.GET.get("cantidad", 0))

    user_miguel = await sync_to_async(User.objects.get)(username="miguelangel")
    cuenta = await obtener_cuenta(user_miguel)

    resultado = await actualizar_saldo_cargo_lock(cuenta.id, cantidad)

    return JsonResponse({"transaccion": resultado})