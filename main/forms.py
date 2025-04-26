# forms.py
from django import forms
from .models import Register

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['name', 'email', 'age', 'phone_num', 'education_level']
