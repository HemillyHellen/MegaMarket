from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms 
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# class UsuarioForm(UserCreationForm):
#     class Meta:
#         model = Usuario
#         fields = ("username", "email", "password", 'usu_tipo', 'usu_ger_id')