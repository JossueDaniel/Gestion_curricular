# Generated by Django 5.1.4 on 2024-12-22 01:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syllabus', '0003_rename_competencias_silabo_competencias_transversales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contenido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semana', models.PositiveIntegerField()),
                ('contenido', models.TextField()),
                ('actividades_docente', models.TextField(blank=True, null=True)),
                ('horas_docente', models.PositiveIntegerField(blank=True, null=True)),
                ('actividades_practicas', models.TextField(blank=True, null=True)),
                ('horas_practica', models.PositiveIntegerField(blank=True, null=True)),
                ('actividades_autonomas', models.TextField(blank=True, null=True)),
                ('horas_autonomas', models.PositiveIntegerField(blank=True, null=True)),
                ('resultados', models.TextField()),
                ('evidencias', models.TextField()),
                ('syllabus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contenido_syllabus', to='syllabus.silabo')),
            ],
        ),
    ]
