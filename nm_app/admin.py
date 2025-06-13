from django.contrib import admin
from nm_app import models

# Register your models here.
admin.site.register(models.services)
admin.site.register(models.User)
admin.site.register(models.Service_form)    
admin.site.register(models.ServiceResponse)    
admin.site.register(models.feedback)
admin.site.register(models.Payment)


@admin.register(models.NannyReview)
class NannyReviewAdmin(admin.ModelAdmin):
    list_display = ('nanny', 'reviewer', 'rating', 'created_at')
    search_fields = ('nanny__username', 'reviewer__username')
    list_filter = ('rating', 'created_at')