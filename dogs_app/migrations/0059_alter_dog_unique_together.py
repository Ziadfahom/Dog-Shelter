# Generated by Django 4.2.1 on 2024-02-15 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0058_alter_camera_options_alter_kennel_options_dog_branch'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dog',
            unique_together={('chipNum', 'branch')},
        ),
    ]
