# Generated by Django 5.1.4 on 2024-12-23 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syllabus', '0005_silabo_fecha_creacion_aporte'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='observacion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
