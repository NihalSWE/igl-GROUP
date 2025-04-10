# Generated by Django 5.1.5 on 2025-02-10 10:35

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('igl', '0045_felna_tech_igl_host_igl_web_student_visa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='felna_tech',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='igl_host',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='igl_web',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='student_visa',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=5000),
        ),
    ]
