# Generated by Django 5.1.5 on 2025-01-28 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igl', '0010_gallerybanner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog_images/')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
