from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import productos , ventas



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]

class productosForm(ModelForm): 
    class Meta:
        model = productos
        fields = '__all__'

class ventasForm(ModelForm): 
    class Meta:
        model = ventas
        fields = '__all__'



