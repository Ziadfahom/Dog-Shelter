# Generated by Django 4.2.1 on 2024-06-22 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0076_dog_city_dog_colorgroup_dog_dogimage2_dog_dogimage3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='dogImage2',
            field=models.ImageField(blank=True, null=True, upload_to='dog_pictures'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='dogImage3',
            field=models.ImageField(blank=True, null=True, upload_to='dog_pictures'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='dogImage4',
            field=models.ImageField(blank=True, null=True, upload_to='dog_pictures'),
        ),
    ]
