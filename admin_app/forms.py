from django import forms
from admin_app import models


class Service(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = "__all__"                                       #('name','email')
        exclude = ('user',)
        
class Category_form(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = "__all__"
