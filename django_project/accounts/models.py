import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    roles = [
        ('admin', 'Administrador'),
        ('full_time', 'Docente Tiempo Completo'),
        ('part_time', 'Docente Tiempo Parcial'),
        ('guest', 'Docente Invitado')
    ]
    formacion = models.TextField(null=True, blank=True)
    rol_academico = models.CharField(
        max_length=50,
        choices=roles,
        verbose_name='Rol Académico de Docente'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
