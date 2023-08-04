from django import forms
from .models import Contacto, Noticia


class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = "__all__"


class NoticiaForm(forms.ModelForm):

    class Meta:
        model= Noticia
        fields = "__all__"