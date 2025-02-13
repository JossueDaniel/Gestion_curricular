from django.db import models
from django.urls import reverse


# Create your models here.
class Silabo(models.Model):
    codigo = models.CharField(max_length=50, default='UNIB.E-CGC-FOR-05')
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    facultad = models.TextField()
    carrera = models.TextField()
    asignatura = models.ForeignKey(
        'asignaturas.Asignatura',
        related_name='syllabus_asignatura',
        on_delete=models.CASCADE
    )
    anio_academico = models.PositiveIntegerField()
    periodo_academico = models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    horario_clase = models.CharField(max_length=50)
    horas_tutorias = models.PositiveIntegerField(null=True, blank=True)
    horario_tutorias = models.CharField(max_length=50, null=True, blank=True)
    docente = models.ForeignKey(
        'accounts.CustomUser',
        related_name='syllabus_docente',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    caracterizacion_asignatura = models.TextField()
    objetivos = models.TextField()
    competencias_transversales = models.TextField()
    competencias_profesionales = models.TextField()
    metodologia = models.TextField()
    evaluacion = models.TextField()
    bibliografia = models.TextField()
    anexos = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Syllabus {self.asignatura}'

    def get_absolute_url(self):
        return reverse('silabo_detail', kwargs={'pk': self.pk})


class Contenido(models.Model):
    syllabus = models.ForeignKey(
        Silabo,
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
    observacion = models.TextField(null=True, blank=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f'Actividades Semana {self.semana} - {self.syllabus}'


class Aporte(models.Model):
    syllabus = models.ForeignKey(
        Silabo,
        related_name='aporte_syllabus',
        on_delete=models.CASCADE
    )
    aporte = models.PositiveIntegerField()
    actividades = models.PositiveIntegerField()
    examen = models.PositiveIntegerField()
    proyecto_final = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    def __str__(self):
        return f'Aporte {self.aporte}'
