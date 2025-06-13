from celery import shared_task
from django.utils import timezone
from .models import Subscription

@shared_task
def check_subscription_expirations():
    today = timezone.now()
    expired_subscriptions = Subscription.objects.filter(is_active=True, end_date__lt=today)

    for subscription in expired_subscriptions:
        subscription.is_active = False
        subscription.save()
