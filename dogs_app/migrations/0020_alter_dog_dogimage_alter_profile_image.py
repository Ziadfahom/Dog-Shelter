# Generated by Django 4.2.1 on 2023-06-30 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0019_alter_dog_dogimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='dogImage',
            field=models.ImageField(blank=True, default='dog_pictures/default_dog.jpg', null=True, upload_to='dog_pictures'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pictures/default.jpg', upload_to='profile_pictures'),
        ),
    ]
