# Generated by Django 5.0.1 on 2024-03-09 18:41

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0002_applicationrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Description'),
        ),
    ]
