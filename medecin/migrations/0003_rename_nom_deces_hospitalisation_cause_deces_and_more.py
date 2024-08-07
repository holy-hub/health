# Generated by Django 5.0.7 on 2024-07-17 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0007_medecin_approuvermedecin_and_more'),
        ('medecin', '0002_remove_carnetsante_frequence_cardiaque_and_more'),
        ('pharmacie', '0003_remove_maladie_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospitalisation',
            old_name='nom_deces',
            new_name='cause_deces',
        ),
        migrations.AddField(
            model_name='facture',
            name='patient',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='authentification.patient', verbose_name='Facture du patient'),
        ),
        migrations.AddField(
            model_name='hospitalisation',
            name='title',
            field=models.CharField(default='Facture', max_length=50),
        ),
        migrations.AddField(
            model_name='prescription',
            name='consultation',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='consultation_medecin', to='medecin.consultation', verbose_name='consultation du Medecin'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='medications',
            field=models.ManyToManyField(default=None, to='pharmacie.medication', verbose_name='medicaments de prescription'),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='tension_arterielle',
            field=models.CharField(default=0, max_length=20),
        ),
    ]
