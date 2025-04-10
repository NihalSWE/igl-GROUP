# Generated by Django 5.1.5 on 2025-02-03 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igl', '0035_alter_reasontochooseus_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeIntro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image1', models.ImageField(upload_to='home_intro/')),
                ('image2', models.ImageField(upload_to='home_intro/')),
                ('progress1_title', models.CharField(max_length=255)),
                ('progress1_value', models.IntegerField()),
                ('progress2_title', models.CharField(max_length=255)),
                ('progress2_value', models.IntegerField()),
            ],
        ),
    ]
