from cuentas.models import Cuenta
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
def index(request):
    return render(request, "index.html")

def vista_saldo(request):
    user = User.objects.get(username="miguelangel")
    cuenta = Cuenta.objects.get(usuario=user)
    return JsonResponse({"saldo": float(cuenta.saldo)})

def vista_reset_saldo(request):
    user, _ = User.objects.get_or_create(username="miguelangel")
    cuenta, _ = Cuenta.objects.get_or_create(usuario=user)
    cuenta.saldo = 1000
    cuenta.save()
    return JsonResponse({"mensaje": "Saldo reseteado", "saldo": float(cuenta.saldo)})