from traceback import format_tb
from django.contrib import admin
from django.urls import reverse

from nm_app.models import Subscription

# Register your models here.
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_name', 'amount', 'payment_link', 'status', 'created_at')

    def payment_link(self, obj):
        url = reverse('subscription_list')
        return format_tb('<a href="{}" target="_blank">View Subscriptions</a>', url)

    payment_link.short_description = "Subscriptions Page"

admin.site.register(Subscription, SubscriptionAdmin)