# Generated by Django 4.2.1 on 2024-02-11 22:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0053_alter_kennel_unique_together_remove_kennel_branch_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kennel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kennelNum', models.PositiveSmallIntegerField(verbose_name='Kennel Number')),
                ('kennelImage', models.ImageField(blank=True, default='kennel_pictures/default_kennel.jpg', null=True, upload_to='kennel_pictures', verbose_name='Kennel Image')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogs_app.branch', verbose_name='Branch')),
            ],
            options={
                'ordering': ['kennelNum', 'branch'],
                'unique_together': {('kennelNum', 'branch')},
            },
        ),
        migrations.CreateModel(
            name='DogPlacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entranceDate', models.DateField(default=django.utils.timezone.now, verbose_name='Entrance Date')),
                ('expirationDate', models.DateField(blank=True, null=True, verbose_name='Expiration Date')),
                ('placementReason', models.CharField(blank=True, max_length=75, null=True, verbose_name='Placement Reason')),
                ('dog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dogs_app.dog', verbose_name='Dog')),
                ('kennel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dogs_app.kennel', verbose_name='Kennel')),
            ],
            options={
                'ordering': ['-entranceDate'],
                'unique_together': {('dog', 'kennel', 'entranceDate')},
            },
        ),
    ]
