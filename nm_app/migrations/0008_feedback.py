# Generated by Django 5.1.5 on 2025-03-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nm_app', '0007_servicerequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('feedback', models.TextField()),
            ],
        ),
    ]
