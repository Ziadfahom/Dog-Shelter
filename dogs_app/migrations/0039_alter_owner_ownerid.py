# Generated by Django 4.2.1 on 2023-12-17 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0038_alter_dog_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='ownerID',
            field=models.CharField(blank=True, max_length=9, null=True, unique=True),
        ),
    ]
