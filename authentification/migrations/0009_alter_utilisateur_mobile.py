# Generated by Django 5.0.7 on 2024-07-18 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0008_alter_utilisateur_address_alter_utilisateur_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='mobile',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
