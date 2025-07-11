from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Cuenta(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)