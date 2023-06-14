from imaplib import _Authenticator
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect, render
from django.http import Http404
from core.forms import CustomUserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import permission_required


# Create your views here.

def index(request):
    return render(request,'core/index.html')



def crearCuenta(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user =_Authenticator(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password2"])
            login(request, user)
            messages.success(request, "Usuario Creado")
            return redirect(to=index)
        data["form"] =formulario
    return render(request, 'registration/register.html', data) 