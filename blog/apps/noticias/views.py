from django.shortcuts import render, HttpResponse, redirect
from .models import Noticia, Categoria, Contacto, Comentario
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  

from .forms import ContactoForm, NoticiaForm
# importamos reverse lazy para los comentarios
from django.urls import reverse_lazy

from django.db.models import Q 

# decorador para ver las noticias solamente como usuario logueado
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View


# uso de decorador para verificar logeo de usuario y poder ver noticia
# @login_required
def inicio(request):
    contexto = {}
    queryset_search = request.GET.get("buscar")
    id_categoria = request.GET.get('id')
    fecha_param = request.GET.get('fecha')
    orden_param = request.GET.get('orden')

    # 1. Start with all news.
    base_noticias_qs = Noticia.objects.all()

    # 2. Apply search filter if 'buscar' parameter is present.
    if queryset_search:
        base_noticias_qs = base_noticias_qs.filter(
            Q(titulo__icontains=queryset_search) |
            Q(cuerpo__icontains=queryset_search) |
            Q(categoria_noticia__nombre__icontains=queryset_search)
        ).distinct()

    # 3. Apply category filter if 'id' parameter is present.
    # This 'if' (not 'elif') ensures it chains with the search filter if both are there.
    if id_categoria:
        base_noticias_qs = base_noticias_qs.filter(categoria_noticia=id_categoria)

    # 4. Apply a default ordering. This is the fallback if no 'fecha' or 'orden'
    # parameters are provided in the URL, or if 'filtrar_noticia' doesn't apply a new order.
    base_noticias_qs = base_noticias_qs.order_by('-fecha')

    # 5. Pass the already filtered (by search/category) queryset to 'filtrar_noticia'
    # for further ordering based on 'fecha_param' or 'orden_param'.
    final_noticias_qs = filtrar_noticia(base_noticias_qs, fecha_param, orden_param)

    contexto['noticias'] = final_noticias_qs
    contexto['categorias'] = Categoria.objects.all()

    return render(request, 'noticias/inicio.html', contexto)

def filtrar_noticia(noticias_queryset, fecha_param, orden_param):
    # This function should ONLY modify the 'noticias_queryset' that's passed to it.
    # It must NOT start a new query with Noticia.objects.all().

    # Prioritize ordering by title if 'orden_param' is provided.
    # If both 'fecha_param' and 'orden_param' are present, 'orden_param' will take precedence.
    if orden_param == 'asc':
        noticias_queryset = noticias_queryset.order_by('titulo')
    elif orden_param == 'des':
        noticias_queryset = noticias_queryset.order_by('-titulo')
    # If 'orden_param' was NOT provided, then check for 'fecha_param'.
    elif fecha_param == 'asc':
        noticias_queryset = noticias_queryset.order_by('fecha')
    elif fecha_param == 'des':
        noticias_queryset = noticias_queryset.order_by('-fecha')

    return noticias_queryset # Return the modified (ordered) queryset
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
        noticia = comment.noticia 
        return render(request, 'noticias/edit.html', {'comment': comment, 'noticia': noticia})

    def post(self, request, pk):
        comment = Comentario.objects.get(pk=pk)
        nuevo_contenido = request.POST.get('texto')
        comment.texto = nuevo_contenido
        comment.save()
        noticia = comment.noticia      # buscamos de que noticia es el comentario para sarlo para redireccionarme a la misma despues de editarla
        return redirect('noticias:detalle', pk=noticia.pk)



class CommentDeleteView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk) # comprobamos si el usuaro que va a borrarlo es el mismo que quien creó el comentario, para mandarlo al html de delete
        noticia = comment.noticia
        if comment.usuario == request.user:
            return render(request, 'noticias/delete.html', {'comment': comment, 'noticia': noticia})
        else:
            noticia = comment.noticia  # sinó lo redireccionamos de nuevo
            return redirect('noticias:detalle', pk=noticia.pk) 

    def post(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk)
        if comment.usuario == request.user: # si el usuario es el que creó el comentario este se borra
            if request.method == 'POST':
                comment.delete()
        noticia = comment.noticia
        return redirect('noticias:detalle', pk=noticia.pk)  

# agregar, eliminar, editar y filtrar noticias
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