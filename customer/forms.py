from django.db.models import fields

from django import forms
from .models import Profile
from Product.models import report_choise , Order
from django.core.validators import RegexValidator

class gender_from(forms.ModelForm):
    class Meta:
        fields = ["gender"]
        model  = Profile

class order_report_form(forms.Form):
    orderId = forms.IntegerField(min_value=1)
    report = forms.ChoiceField(choices=report_choise)

class order_star_submit(forms.Form):
    orderId = forms.IntegerField(min_value=1)
    rating = forms.IntegerField(validators=[RegexValidator(regex=r'^[1-5]$')])

class profile_update_form(forms.Form):
    profile_photo = forms.ImageField()