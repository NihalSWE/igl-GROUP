# Generated by Django 5.1.5 on 2025-02-01 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('igl', '0022_bod_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bod',
            name='position',
        ),
    ]
