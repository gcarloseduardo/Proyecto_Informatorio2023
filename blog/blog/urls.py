"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include                
from . import views

# URLS PARA LOGIN
from django.contrib.auth import views as auth
from django.conf.urls.static import static

from django.urls import reverse_lazy 
from django.conf import settings

# URL PRINCIPAL
urlpatterns = [
    path('admin/', admin.site.urls),
    # path para la view
    path("", views.home, name="home"),
    # path para nosotros
    path("nosotros/", views.nosotros, name="nosotros"),

    # ---------URL APP NOTICIAS------------------
    path("noticias/", include('apps.noticias.urls')),

    # # -----------URL LOGIN----------
    # path("usuarios/login",views.login, name="login")
    # path("login/", auth.LoginView.as_view(template_name= "usuarios/login.html"), name="login"),
    # path("logout/", auth.LoginView.as_view(), name= "logout"),
     # LOGIN
    # path('usuarios/login', views.login, name='login')
    path('login/', auth.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    # ultimo error de la clase solucionado
    # path('logout/', auth.LoginView.as_view(), name='logout'),
    # cambiar   LoginView por LogoutView
    path('logout/',auth.LogoutView.as_view() , name='logout'),


    # registro
    path("usuarios/", include("apps.usuarios.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #carga las imagenes de blog/media que son imagenes que se guardan en la BD
