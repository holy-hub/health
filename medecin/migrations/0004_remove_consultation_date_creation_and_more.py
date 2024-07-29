# Generated by Django 5.0.7 on 2024-07-29 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0014_medecin_verifiermedecin_and_more'),
        ('medecin', '0003_rename_nom_deces_hospitalisation_cause_deces_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='date_creation',
        ),
        migrations.RemoveField(
            model_name='consultation',
            name='patient',
        ),
        migrations.AlterField(
            model_name='advice',
            name='image',
            field=models.FileField(max_length=255, upload_to='img/conseils/'),
        ),
        migrations.AlterField(
            model_name='carnetsante',
            name='patient',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='patient_carnet', to='authentification.patient', unique=True, verbose_name='Carnet_patient'),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='date_consultation',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='date_modification',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='medecin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultation_medecin', to='authentification.medecin'),
        ),
    ]
