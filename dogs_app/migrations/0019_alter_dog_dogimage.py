# Generated by Django 4.2.1 on 2023-06-28 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0018_remove_dog_dogimageurl_dog_dogimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='dogImage',
            field=models.ImageField(blank=True, default='/dog_pictures/default_dog.jpg', null=True, upload_to='dog_pictures'),
        ),
    ]
