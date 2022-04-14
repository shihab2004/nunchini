from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.models import fields_for_model
from customer.models import gender_choises
from root.models import City , chaldal_bottomMenu
class CreateUserForm(UserCreationForm):
    profile_photo = forms.ImageField(required=False,label='Profile Photo')
    gender = forms.CharField(widget=forms.Select(choices=gender_choises))
    Phone = forms.IntegerField(required=True)
    current_city = forms.ModelChoiceField(queryset=City.objects.all())

class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

