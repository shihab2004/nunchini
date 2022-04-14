from django import forms
from .models import Corporate_Customer

class Corporate_Customer_form(forms.ModelForm):
    class Meta:
        model = Corporate_Customer
        fields = "__all__"