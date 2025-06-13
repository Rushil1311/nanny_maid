from django import forms
from nm_app import models


class serviceForm(forms.ModelForm):
    class Meta:
        model = models.services
        fields = "__all__"                                       #('name','email')
        exclude = ('user',)

class service_request_form(forms.ModelForm):
    class Meta:
        model = models.Service_form
        fields = "__all__"
        exclude = ['user']

class feedback(forms.ModelForm):
    class Meta:
        model = models.feedback
        fields = "__all__"

