# Generated by Django 5.1.5 on 2025-02-02 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igl', '0029_blogbanner'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Who We Are', max_length=255)),
                ('description', models.TextField()),
            ],
        ),
    ]
