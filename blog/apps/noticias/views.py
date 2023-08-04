from django.shortcuts import render, HttpResponse, redirect
from .models import Noticia, Categoria, Contacto, Comentario

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  
from django.db.models import Q

from .forms import ContactoForm, NoticiaForm
# importamos reverse lazy para los comentarios
from django.urls import reverse_lazy


# decorador para ver las noticias solamente como usuario logueado
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View


# def inicio(request):
#     contexto = {}
#     queryset = request.GET.get("buscar") 
#     if queryset:
#         n = Noticia.objects.filter(
#             Q(titulo__icontains = queryset) |
#             Q(cuerpo__icontains = queryset) |
#             Q(categoria_noticia__nombre = queryset)
#         ).distinct().order_by('-fecha')[:5]
#         contexto['noticias'] = n

#         return render(request, 'noticias/inicio.html',contexto)
#     else:
#         id_categoria = request.GET.get('id', None)
#         if id_categoria:
#             n = Noticia.objects.filter(categoria_noticia=id_categoria).order_by('-fecha')[:5]
#         else:
#             n = Noticia.objects.all().order_by('-fecha')[:5]  # una lista
#         contexto['noticias'] = n
#         cat = Categoria.objects.all().order_by('nombre')[:5]
#         contexto['categorias'] = cat
#         return render(request, 'noticias/inicio.html', contexto)

    


# @login_required
def Detalle_Noticias(request, pk):
    contexto = {}
    n = Noticia.objects.get(pk=pk)
    contexto['noticia'] = n
    c = Comentario.objects.filter(noticia=n)
    contexto['comentarios'] = c
    return render(request, 'noticias/detalle.html', contexto)



# ClaseName.objects.all()[0:2]              select * from noticias
# ClaseName.objects.get(pk = 1)        select * from noticias where id = 1
# ClaseName.objects.filter(categoria)  select * from noticias where categoria = deportes


def contacto(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
           ContactoForm(data=request.POST).save()

    return render(request, 'contacto/formulario.html', data)


@login_required
def Comentar_Noticia(request):
    comentario = request.POST.get('comentario', None)
    user = request.user
    noti = request.POST.get('id_noticia', None)
    noticia = Noticia.objects.get(pk=noti)
    coment = Comentario.objects.create(
        usuario=user, noticia=noticia, texto=comentario)
    return redirect(reverse_lazy('noticias:detalle', kwargs={"pk": noti}))


# creando las clases que me permiten modificar y elimiar los comentarios
class Editcomentario(View):
    def get(self, request, pk):
        comment = Comentario.objects.get(pk=pk) # extraemos el objeto de comentarios con igual pk
        return render(request, 'noticias/edit.html', {'comment': comment})

    def post(self, request, pk):
        comment = Comentario.objects.get(pk=pk)
        nuevo_contenido = request.POST.get('texto')
        comment.texto = nuevo_contenido
        comment.save()
        noticia = comment.noticia      # buscamos de que noticia es el comentario, para usarlo para redireccionarme a la misma despues de editarla
        return redirect('noticias:detalle', pk=noticia.pk)



class CommentDeleteView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk) # comprobamos si el usuaro que va a borrarlo es el mismo que quien creó el comentario, para mandarlo al html de delete
        if comment.usuario == request.user:
            return render(request, 'noticias/delete.html', {'comment': comment})
        else:
            noticia = comment.noticia  # sinó lo redireccionamos de nuevo
            return redirect('noticias:detalle', pk=noticia.pk) 

    def post(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk)
        if comment.usuario == request.user: # si el usuario es el que creó el comentario este se borra
            comment.delete()
        noticia = comment.noticia
        return redirect('noticias:detalle', pk=noticia.pk)  

@login_required
def agregar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('noticias:inicio')
    else:
        form = NoticiaForm()

    return render(request, 'noticias/formulario.html', {'form': form})
  
def eliminar_noticia(request, pk):
    noticia = Noticia.objects.get(pk =pk)
    noticia = get_object_or_404(Noticia, pk=pk)
    contexto = {'noticia': noticia}
    if request.method == 'POST':
        noticia.delete()
        return redirect('noticias:inicio')
    return render(request, 'noticias/deletenoticia.html', contexto)

def editar_noticia(request, pk):
    # obtengo la noticia y si no existe tira error
    noticia = get_object_or_404(Noticia, pk=pk)
    # si se aprieta el boton de guardar cambios manda la info a travez de POST
    if request.method == 'POST':
        # inicializamos el formulario con el parametro instance, que es un parametro que se necesita para actualizar una instancia de la BD
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('noticias:detalle', pk=noticia.pk) 

    else:
        form = NoticiaForm(instance=noticia)

        return render(request, 'noticias/editnoticia.html',{'form': form, 'noticia': noticia})




def inicio(request):
    contexto = {}
    queryset_buscar = request.GET.get("buscar") 
    queryset_fecha = request.GET.get('fecha')
    queryset_orden = request.GET.get('orden')
    queryset_categoria = request.GET.get('id')


    if queryset_categoria:
        n = Noticia.objects.filter(categoria_noticia=queryset_categoria)
        noticias = n
        contexto['noticias']= noticias
        cat = Categoria.objects.filter(id=queryset_categoria)
        contexto['categorias']= cat
        return render(request, 'noticias/inicio.html',contexto)

    elif queryset_buscar:
        noticias = Noticia.objects.filter(
        Q(titulo__icontains = queryset_buscar) |
        Q(cuerpo__icontains = queryset_buscar) |            
        Q(categoria_noticia__nombre = queryset_buscar)
        ).distinct()
        contexto['noticias']= noticias
        return render(request, 'noticias/inicio.html',contexto)
        
    elif queryset_fecha == 'asc':
        noticias = Noticia.objects.order_by('fecha')
        contexto['noticias']= noticias
        return render(request, 'noticias/inicio.html',contexto)
    
    elif queryset_fecha == 'des':
        noticias = Noticia.objects.order_by('-fecha')
        contexto['noticias']= noticias
        return render(request, 'noticias/inicio.html',contexto)
    
    elif queryset_orden == 'asc':
        noticias = Noticia.objects.order_by('titulo')
        contexto['noticias']= noticias
        return render(request, 'noticias/inicio.html',contexto)
    
    elif queryset_orden == 'des':
        noticias = Noticia.objects.order_by('-titulo')
        contexto['noticias']= noticias
        return render(request, 'noticias/inicio.html',contexto)

    else:
        noticias = Noticia.objects.all()
        contexto['noticias']= noticias
        cat = Categoria.objects.all()
        contexto['categorias'] = cat
        return render(request, 'noticias/inicio.html',contexto)
