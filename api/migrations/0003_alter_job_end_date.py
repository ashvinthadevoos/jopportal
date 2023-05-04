# Generated by Django 4.1.4 on 2023-05-04 06:19

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_candidateprofile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='end_date',
            field=models.DateField(verbose_name=django.core.validators.MinValueValidator(datetime.date.today)),
        ),
    ]