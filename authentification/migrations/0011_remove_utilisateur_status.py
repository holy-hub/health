# Generated by Django 5.0.6 on 2024-07-18 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0010_alter_pharmacien_pharmacie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='status',
        ),
    ]