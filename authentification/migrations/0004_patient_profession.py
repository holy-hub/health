# Generated by Django 5.0.7 on 2024-07-13 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0003_alter_patient_assurance_medicale_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='profession',
            field=models.CharField(default='survivant', max_length=50, verbose_name='Profession du Patient'),
        ),
    ]