# Generated by Django 4.2.1 on 2023-06-01 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0008_alter_dog_dogimageurl_observation_dogstance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='observation',
            old_name='sessionDurationsInMins',
            new_name='sessionDurationInMins',
        ),
    ]
