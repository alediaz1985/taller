# Generated by Django 5.1 on 2024-11-11 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
        ('mantenimiento', '0002_equipo_activo_historialequipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimiento',
            name='equipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.equipo'),
        ),
        migrations.RemoveField(
            model_name='historialequipo',
            name='equipo',
        ),
        migrations.DeleteModel(
            name='Equipo',
        ),
        migrations.DeleteModel(
            name='HistorialEquipo',
        ),
    ]
