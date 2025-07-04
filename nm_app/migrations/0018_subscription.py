# Generated by Django 5.1.5 on 2025-03-27 16:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nm_app', '0017_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(choices=[('3_months', '3 Months Subscription'), ('6_months', '6 Months Subscription'), ('1_year', '1 Year Subscription')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(default='Active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nm_app.payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
