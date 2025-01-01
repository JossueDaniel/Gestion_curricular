from django.db import models


# Create your models here.
class Contenido(models.Model):
    syllabus = models.ForeignKey(
        'syllabus.Silabo',
        related_name='contenido_syllabus',
        on_delete=models.CASCADE
    )
    semana = models.PositiveIntegerField()
    contenido = models.TextField()
    actividades_docente = models.TextField(null=True, blank=True)
    horas_docente = models.PositiveIntegerField(null=True, blank=True)
    actividades_practicas = models.TextField(null=True, blank=True)
    horas_practica = models.PositiveIntegerField(null=True, blank=True)
    actividades_autonomas = models.TextField(null=True, blank=True)
    horas_autonomas = models.PositiveIntegerField(null=True, blank=True)
    resultados = models.TextField()
    evidencias = models.TextField()

    def __str__(self):
        return f'Actividades Semana {self.semana} del syllabus {self.syllabus}'
