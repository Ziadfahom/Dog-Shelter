# Generated by Django 4.2.1 on 2023-12-12 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0035_alter_owner_phonenum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('', '-')], max_length=1),
        ),
    ]
