from django.contrib.sites import requests
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.apps import apps

def reorden(modelo_nombre: str, numero: int):
    """
    Incrementa el campo 'orden' de todos los objetos del modelo dado (por nombre)
    que tengan orden >= numero.
    """
    Modelo = apps.get_model('Issue_Tracker', modelo_nombre)

    try:
        objeto = Modelo.objects.get(orden=numero)
        reorden(modelo_nombre, numero + 1)
        objeto.orden = numero + 1
        objeto.save()
    except ObjectDoesNotExist:
        print(f"no existe el objeto con orden {numero}. Fin recursividad reorden")
