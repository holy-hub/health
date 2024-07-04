# Generated by Django 5.0.6 on 2024-07-04 19:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentification', '0001_initial'),
        ('pharmacie', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(verbose_name='description de la Spécialité')),
            ],
        ),
        migrations.CreateModel(
            name='Advice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Titre du conseil')),
                ('content', models.TextField(verbose_name='Contenu du conseil')),
                ('image', models.FileField(max_length=255, upload_to='image/conseils/')),
                ('is_publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ill', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pharmacie.maladie', verbose_name='Maladie choisie pour le conseil')),
                ('medecin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Medecin originaire de cette enregistrement')),
            ],
        ),
        migrations.CreateModel(
            name='Consigne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posologie', models.CharField(choices=[('comprimé 0.5', 'Moitié de comprimé par jour'), ('comprimé 1', '1 comprimé par jour'), ('comprimé 2', '2 comprimés par jour'), ('comprimé 3', '3 comprimés par jour'), ('sirop 1', '1 cuillerée par jour'), ('sirop 2', '2 cuillerées par jour'), ('sirop 3', '3 cuillerées par jour'), ('poudre 1', '1 sachet par jour'), ('poudre 2', '2 sachets par jour'), ('poudre 3', '3 sachets par jour')], max_length=50, null=True)),
                ('medication', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pharmacie.medication', verbose_name='Les medicaments prescrits')),
            ],
        ),
        migrations.CreateModel(
            name='Hopital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=50, unique=True)),
                ('localisation', models.URLField(max_length=255)),
                ('medecins', models.ManyToManyField(related_name='hopitaux', to='authentification.utilisateur', verbose_name="Medecin de l'hôpital")),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('temperature', models.PositiveSmallIntegerField(default=37)),
                ('observation', models.TextField(verbose_name='Observations du medecin')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('consigne', models.ManyToManyField(to='medecin.consigne', verbose_name='Les medications et leur posologie a suivre')),
                ('medecin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_medecin', to='authentification.utilisateur', verbose_name='Medecin de consultation')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_patient', to='authentification.utilisateur', verbose_name='Patient de consultation')),
            ],
        ),
        migrations.CreateModel(
            name='SubSpeciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(verbose_name='description de la Spécialité')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medecin.speciality', verbose_name='Specialite de cette sous spécialité')),
            ],
        ),
    ]
