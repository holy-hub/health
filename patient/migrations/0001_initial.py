# Generated by Django 5.0.6 on 2024-07-04 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_rdv', models.DateTimeField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('accepte', 'ACCEPTÉ'), ('refuse', 'REFUSÉ'), ('annule', 'ANNULÉ'), ('en attente', 'EN ATTENTE')], default=('en attente', 'EN ATTENTE'), max_length=50)),
                ('medecin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointements_medecin', to='authentification.utilisateur', verbose_name='Medecin')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointements_patient', to='authentification.utilisateur', verbose_name='Patient')),
            ],
        ),
    ]
