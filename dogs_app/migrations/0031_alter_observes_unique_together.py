# Generated by Django 4.2.1 on 2023-09-16 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0030_observes_sessiondate'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='observes',
            unique_together={('dog', 'camera', 'sessionDate')},
        ),
    ]
