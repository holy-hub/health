# Generated by Django 5.0.7 on 2024-07-19 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_appointement_reminder_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointement',
            name='motif',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='appointement',
            name='status',
            field=models.CharField(choices=[('accepte', 'ACCEPTÉ'), ('refuse', 'REFUSÉ'), ('annule', 'ANNULÉ'), ('en attente', 'EN ATTENTE')], default='EN ATTENTE', max_length=50),
        ),
    ]
