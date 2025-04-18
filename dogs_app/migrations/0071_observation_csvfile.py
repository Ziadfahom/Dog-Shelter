# Generated by Django 4.2.1 on 2024-03-09 23:37

from django.db import migrations, models
import dogs_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs_app', '0070_branch_branchcity_alter_branch_branchaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='csvFile',
            field=models.FileField(blank=True, null=True, upload_to='csv_files', validators=[dogs_app.models.validate_csv_file_extension], verbose_name='CSV File'),
        ),
    ]
