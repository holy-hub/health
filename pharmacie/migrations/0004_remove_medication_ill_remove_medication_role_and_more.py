# Generated by Django 5.0.7 on 2024-07-18 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacie', '0003_remove_maladie_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='ill',
        ),
        migrations.RemoveField(
            model_name='medication',
            name='role',
        ),
        migrations.AddField(
            model_name='medication',
            name='avantages',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='medication',
            name='inconvenients',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='pharmacie',
            name='medications',
            field=models.ManyToManyField(related_name='pharmacie', to='pharmacie.medication', verbose_name='Médicaments liés à la pharmacie'),
        ),
    ]
