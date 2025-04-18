# Generated by Django 4.2.1 on 2023-06-01 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0003_alter_observes_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('treatmentID', models.AutoField(primary_key=True, serialize=False)),
                ('treatmentName', models.CharField(max_length=50)),
                ('treatmentDate', models.DateField(blank=True, null=True)),
                ('treatedBy', models.CharField(max_length=50)),
                ('comments', models.CharField(blank=True, max_length=250, null=True)),
                ('dogID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dogs_app.dog')),
            ],
        ),
        migrations.CreateModel(
            name='EntranceExamination',
            fields=[
                ('examinationID', models.AutoField(primary_key=True, serialize=False)),
                ('examinationDate', models.DateField(auto_now_add=True)),
                ('examinedBy', models.CharField(max_length=50)),
                ('results', models.CharField(blank=True, max_length=100, null=True)),
                ('dogWeight', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('dogTemperature', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('dogPulse', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('comments', models.CharField(blank=True, max_length=200, null=True)),
                ('dogID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dogs_app.dog')),
            ],
        ),
    ]
