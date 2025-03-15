# Generated by Django 5.1.5 on 2025-03-13 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igl', '0059_weserve'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact_schedule',
            name='button_link',
        ),
        migrations.AddField(
            model_name='contact_schedule',
            name='phone_number',
            field=models.CharField(blank=True, help_text='Contact phone number.', max_length=20, null=True),
        ),
    ]
