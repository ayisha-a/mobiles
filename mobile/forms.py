from django.forms import forms,ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CheckOutForm(forms.ModelForm):
   class Meta:
        model = Order
        fields = ["ordered_by", "shipping_address",
                  "mobile", "email"]

class UserRegistartionForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.TextInput(attrs={'class': 'form-control'}),
            "password1": forms.TextInput(attrs={'class': 'form-control'}),
            "password2": forms.TextInput(attrs={'class': 'form-control'}),

        }

