# Generated by Django 5.0.7 on 2024-07-18 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0007_medecin_approuvermedecin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='address',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='mobile',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]
