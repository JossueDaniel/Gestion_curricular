from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Asignatura(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100)
    eje_formacion = models.CharField(max_length=50)
    nivel_academico = models.PositiveIntegerField()
    creditos = models.PositiveIntegerField()
    total_horas = models.PositiveIntegerField()
    pre_requisitos = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='prerequisito',
    )
    co_requisitos = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='corequisito'
    )

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Docente(models.Model):
    asignatura = models.ForeignKey(
        Asignatura,
        related_name='relacion_asignatura',
        on_delete=models.CASCADE
    )
    docente = models.ForeignKey(
        'accounts.CustomUser',
        related_name='docente_asignatura',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
