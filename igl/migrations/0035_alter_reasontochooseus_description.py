# Generated by Django 5.1.5 on 2025-02-03 09:03

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('igl', '0034_reasontochooseus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reasontochooseus',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=500),
        ),
    ]
