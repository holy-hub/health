# Generated by Django 5.0.7 on 2024-07-19 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0012_utilisateur_is_medecin_utilisateur_is_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='sexe',
            field=models.CharField(choices=[('M', 'MASCULIN'), ('F', 'FEMININ'), ('BI', 'BISEXUEL'), ('N-G', 'NON-GENRE')], default='M', max_length=20),
        ),
    ]
