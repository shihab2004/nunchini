from django import forms

class discount_code_form(forms.Form):
    code = forms.CharField()