# Generated by Django 4.2.1 on 2024-03-08 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0064_observation_isdog_observation_ishuman_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dogstance',
            name='dogLocation',
            field=models.CharField(blank=True, choices=[('FLOOR', 'On Floor'), ('BENCH', 'On Bench'), ('ONBARS', 'On Bars'), ('ONBED', 'On Bed'), ('WALLTOWALL', 'From Wall to Wall'), ('ELSE', 'Else')], max_length=10, null=True, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='isDog',
            field=models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], default=None, max_length=1, null=True, verbose_name='With Dog'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='isHuman',
            field=models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], default=None, max_length=1, null=True, verbose_name='With Human'),
        ),
    ]
