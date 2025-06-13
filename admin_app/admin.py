from django.contrib import admin
from razorpay import Payment
from admin_app import models
from nm_app.models import Subscription

# Register your models here.


admin.site.register(models.Service)
admin.site.register(models.Category)
admin.site.register(models.editors)

from django.contrib import admin
from .models import SubscriptionPlan, NannySubscription

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')

@admin.register(NannySubscription)
class NannySubscriptionAdmin(admin.ModelAdmin):
    list_display = ('nanny', 'plan', 'start_date', 'end_date')  # Display fields
    list_filter = ('end_date',)  # Allows filtering by end date

# @admin.register(Subscription)
# class SubscriptionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'plan_name', 'start_date', 'end_date', 'is_active')
#     list_filter = ('is_active', 'start_date', 'end_date')
#     search_fields = ('user__username', 'plan_name')

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'plan_name', 'amount', 'razorpay_order_id', 'status', 'created_at')
#     list_filter = ('status',)
#     search_fields = ('user__username', 'plan_name', 'razorpay_order_id')