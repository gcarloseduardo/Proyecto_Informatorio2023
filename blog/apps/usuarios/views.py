from django.shortcuts import render

# Create your views here.
# importts
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistroForm


class Registro(CreateView):
    # forms django
    form_class = RegistroForm
    success_url = reverse_lazy('login')
    template_name = 'usuarios/registro.html'

 
