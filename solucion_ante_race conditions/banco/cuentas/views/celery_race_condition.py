from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from cuentas.models import Cuenta
from cuentas.tasks.celery_race_condition import actualizar_saldo_depositar_celery, actualizar_saldo_cargo_celery

# Vista para lanzar un depósito usando Celery
def vista_depositar_celery(request):
    username = request.GET.get("username", "anonimo")
    cantidad = request.GET.get("cantidad", "0")
    actualizar_saldo_depositar_celery.delay(username, cantidad)
    return JsonResponse({"mensaje": f"Tarea enviada: {username} depositará {cantidad}"})

# Vista para lanzar un cargo usando Celery
def vista_cargar_celery(request):
    cantidad = request.GET.get("cantidad", "0")
    actualizar_saldo_cargo_celery.delay(cantidad)
    return JsonResponse({"mensaje": f"Tarea enviada: miguelangel cargará {cantidad}"})
