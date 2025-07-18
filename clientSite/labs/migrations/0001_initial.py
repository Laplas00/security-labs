# Generated by Django 5.1.2 on 2025-06-27 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LabModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_name', models.CharField(max_length=128)),
                ('container_name', models.CharField(max_length=64)),
                ('tier', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='easy', max_length=8)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(max_length=64)),
                ('full_description', models.TextField(blank=True)),
            ],
        ),
    ]
