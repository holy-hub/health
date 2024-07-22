# Generated by Django 5.0.7 on 2024-07-18 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0011_remove_utilisateur_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='is_medecin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='is_patient',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='is_pharmacien',
            field=models.BooleanField(default=False),
        ),
    ]