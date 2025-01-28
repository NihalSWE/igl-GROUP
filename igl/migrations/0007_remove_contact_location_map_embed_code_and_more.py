# Generated by Django 5.1.5 on 2025-01-28 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igl', '0006_contact_location_contact_schedule_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact_location',
            name='map_embed_code',
        ),
        migrations.AddField(
            model_name='contact_location',
            name='map_url',
            field=models.URLField(blank=True, help_text='Google Maps link for the location. Paste the link from Google Maps.', null=True),
        ),
    ]
