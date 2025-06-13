from django.db import models
# from django.contrib.auth.models import User
from nm_app.models import User
from datetime import timedelta, datetime
# Create your models here.


class Service(models.Model):
 name = models.CharField(max_length=255)
 description = models.TextField(blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    Image = models.ImageField(upload_to='cat_image/')

class editors(models.Model):
    YN = models.CharField(max_length=255)
    em = models.EmailField()
    pas = models.TextField()
    ad = models.CharField(max_length=255)
    ct = models.TextField()
    zipc = models.IntegerField()

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_year', 'Half-Year'),
        ('full_year', 'Full-Year'),
    ]

    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()  # e.g., 30 for Monthly, 90 for Quarterly
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def get_price_in_paise(self):
        return int(self.price * 100)


class NannySubscription(models.Model):
    nanny = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if datetime.now() > self.end_date:
            self.is_active = False
        super().save(*args, **kwargs)

    def is_active(self):
        return datetime.now() <= self.end_date
