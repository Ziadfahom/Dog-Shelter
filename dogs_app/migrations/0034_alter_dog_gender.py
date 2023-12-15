# Generated by Django 4.2.1 on 2023-10-03 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0033_alter_dog_gender_alter_dogstance_doglocation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1),
            preserve_default=False,
        ),
    ]
