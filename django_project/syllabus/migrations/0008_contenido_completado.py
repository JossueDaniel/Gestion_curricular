# Generated by Django 5.1.4 on 2025-02-13 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syllabus', '0007_alter_silabo_periodo_academico'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='completado',
            field=models.BooleanField(default=False),
        ),
    ]
