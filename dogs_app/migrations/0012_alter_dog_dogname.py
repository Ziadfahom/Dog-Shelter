# Generated by Django 4.2.1 on 2023-06-10 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0011_alter_dog_ownerserialnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='dogName',
            field=models.CharField(default='Default', max_length=35),
            preserve_default=False,
        ),
    ]
