from django.urls import path
from . import views
from .views import *


app_name = "noticias"

# urls de app noticias
urlpatterns = [
    path("", views.inicio, name= "inicio"),
     # url para el detalle de la noticia por pk
    path('detalle<int:pk>', views.Detalle_Noticias, name='detalle'),

    # url del formulario de contacto
    path('contacto', views.contacto, name="contacto"),

    # URL COMENTARIO
    path('comentario', views.Comentar_Noticia, name='comentar'),

    # comentarios
    path('<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('<int:pk>/edit/', views.Editcomentario.as_view(), name='comment_edit'),

    path('add_noticia', views.agregar_noticia, name='agregar_noticia'),
    path('<int:pk>/del_noticia', views.eliminar_noticia, name='eliminar_noticia'),
    path('<int:pk>/editar_noticia', views.editar_noticia, name='editar_noticia'),
    
]