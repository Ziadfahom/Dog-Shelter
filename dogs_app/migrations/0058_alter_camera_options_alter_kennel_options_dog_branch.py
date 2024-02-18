# Generated by Django 4.2.1 on 2024-02-15 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0057_camera_observes_observation_dogstance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='camera',
            options={'ordering': ['branch', 'camID']},
        ),
        migrations.AlterModelOptions(
            name='kennel',
            options={'ordering': ['branch', 'kennelNum']},
        ),
        migrations.AddField(
            model_name='dog',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dogs_app.branch', verbose_name='Branch'),
            preserve_default=False,
        ),
    ]
