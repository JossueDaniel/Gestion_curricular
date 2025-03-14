# Generated by Django 5.1.4 on 2024-12-21 21:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asignaturas', '0003_alter_asignatura_co_requisitos_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Silabo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(default='UNIB.E-CGC-FOR-05', max_length=50)),
                ('fecha_actualizacion', models.DateField(auto_now=True)),
                ('facultad', models.CharField(max_length=100)),
                ('carrera', models.CharField(max_length=100)),
                ('anio_academico', models.PositiveIntegerField()),
                ('periodo_academico', models.CharField(max_length=10)),
                ('fecha_inicio', models.DateField()),
                ('fecha_finalizacion', models.DateField()),
                ('horario_clase', models.CharField(max_length=50)),
                ('horas_tutorias', models.PositiveIntegerField()),
                ('horario_tutorias', models.CharField(max_length=50)),
                ('caracterizacion_asignatura', models.TextField()),
                ('objetivos', models.TextField()),
                ('competencias', models.TextField()),
                ('competencias_profesionales', models.TextField()),
                ('metodologia', models.TextField()),
                ('evaluacion', models.TextField()),
                ('bibliografia', models.TextField()),
                ('anexos', models.TextField(blank=True, null=True)),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syllabus_asignatura', to='asignaturas.asignatura')),
                ('docente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='syllabus_docente', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
