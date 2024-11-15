from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Post, CATEGORIAS
from usuarios.models import Perfil
from django.http import HttpResponseRedirect
from django.urls import reverse
from .decorators import check_user_blocked
from .forms import PostForm, ContactoForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404



############################
def is_admin(user):
    return user.is_staff


#############################


# Vista de inicio (home)
def home(request):
    # Obtener todas las recetas
    recetas = Post.objects.all().order_by('-created')

    # Obtener las tres recetas con más "me gusta" llamando a la función
    top_posts = get_top_posts()

    return render(request, 'index.html', {
        'recetas': recetas,
        'top_posts': top_posts,
    })

# Vista de recetas
@check_user_blocked
def recetas(request):
    recetas = Post.objects.all()  # Transforma datos a una lista
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(recetas, 5)
        recetas = paginator.page(page)

    except:
        raise Http404

    data = {"entity": recetas,
            'paginator': paginator}
    return render(request, "pages/recetas/lista_recetas.html", data)


@user_passes_test(is_admin)
def agregar_receta(request):
    if request.method == "POST":
        formulario = PostForm(data=request.POST, files=request.FILES)  # Crea una instancia del formulario
        if formulario.is_valid():
            formulario.save()
            return redirect('recetas:listar_recetas')  # Cambia esto a la URL que desees después de guardar
    else:
        formulario = PostForm()

    return render(request, "pages/Admin/agregar.html", {
        "form": formulario,
    })




@user_passes_test(is_admin)
def listar_recetas(request):
    recetas = Post.objects.all()  # Asegúrate de usar la clase Post correctamente
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(recetas, 5)
        recetas = paginator.page(page)

    except:
        raise Http404
         


    data = {
        "entity": recetas,  # Cambia 'Post' por 'recetas' para que sea más descriptivo
        'paginator': paginator
    }
    return render(request, "pages/Admin/listar.html", data)


@user_passes_test(is_admin)
def modificar_receta(request, id):

    receta = get_object_or_404(Post, id=id)

    data = {"form": PostForm(instance=receta)}

    if request.method == "POST":
        formulario = PostForm(data=request.POST, instance=receta, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="recetas:listar_recetas")
        data["form"] = formulario

    return render(request, "pages/Admin/modificar.html", data)


@user_passes_test(is_admin)
def eliminar_receta(request, id):
    receta = get_object_or_404(Post, id=id)
    receta.delete()
    return redirect(to="recetas:listar_recetas")

#Administracion usuarios
@user_passes_test(is_admin)
def gestionar_usuarios(request):
    perfiles = Perfil.objects.filter(usuario__is_staff=False)
    return render(request, 'pages/Admin/gestionar_usuarios.html', {'perfiles': perfiles})

@user_passes_test(is_admin)
def bloquear_usuario(request, usuario_id):
    perfil = Perfil.objects.get(usuario_id=usuario_id)
    perfil.is_blocked = not perfil.is_blocked
    perfil.save()
    return redirect('recetas:gestionar_usuarios')


# Detalle receta

@check_user_blocked
def receta_detalle(request, receta_id):
    receta = get_object_or_404(Post, id=receta_id)
    ingredientes = receta.ingredients.split("\n")
    instrucciones = receta.instructions.split("\n")
    comments = receta.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = receta  # Asignar la receta al comentario
            comment.user = request.user  # Asignar el usuario autenticado
            comment.save()
            return redirect('recetas:receta_detalle', receta_id=receta.id)
    else:
        form = CommentForm()

    return render(request, 'pages/recetas/receta_detalle.html', {
        'receta': receta,
        'ingredientes': ingredientes,
        'instrucciones': instrucciones,
        'comments': comments,
        'form': form,
    })
    
def busqueda_funcional(request):
    searched = request.GET.get('busquedaFuncional', '')
    category = request.GET.get('categoria', '')
    resultados_list = Post.objects.all()

    if searched:
        resultados_list = resultados_list.filter(title__icontains=searched)

    if category:
        resultados_list = resultados_list.filter(category=category)

    paginator = Paginator(resultados_list, 2)
    page_number = request.GET.get('page')
    resultados = paginator.get_page(page_number)

    context = {
        'searched': searched,
        'resultados': resultados,
        'categorias': CATEGORIAS,
        'categoria_seleccionada': category,
    }

    return render(request, 'pages/post/busqueda.html', context)
    
#Recetas mas populares


def get_top_posts(limit=3):
    """Obtiene las recetas más populares, ordenadas por likes y fecha de creación."""
    return Post.objects.annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count', '-created')[:limit]
    
    
#Ayuda
@check_user_blocked
def contacto(request):
    if request.method == "POST":
        formulario = ContactoForm(data=request.POST)
        
        if formulario.is_valid():
            # Obtener los datos del formulario
            nombre = formulario.cleaned_data['nombre']
            correo = formulario.cleaned_data['correo']
            mensaje = formulario.cleaned_data['mensaje']
            tipo_consulta = formulario.cleaned_data['tipo_consulta']

            # Enviar correo
            template = render_to_string('pages/ayudaUsuario/email_template.html', {
                'nombre': nombre,
                'correo': correo,
                'mensaje': mensaje
            })
            email_message = EmailMessage(
                subject=tipo_consulta,
                body=template,
                from_email=correo,
                to=['rukasabor@gmail.com']
            )

            try:
                email_message.send()
                messages.success(request, "Tu mensaje ha sido enviado exitosamente.")
                return redirect('recetas:contacto')  # Ajusta la URL según sea necesario
            except Exception as e:
                messages.error(request, "Hubo un error al enviar el correo. Intenta de nuevo más tarde.")
                print(f"Error al enviar el correo: {e}")
        else:
            # Solo se muestra un mensaje de error si el formulario no es válido
            messages.error(request, "Por favor, corrige los errores en el formulario.")
            print(formulario.errors)
    else:
        formulario = ContactoForm()  # Crear un nuevo formulario si no es un POST

    return render(request, "pages/ayudaUsuario/contacto.html", {'form': formulario})


#Likes en un post

@login_required
@check_user_blocked
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('recetas:receta_detalle', post.id) 

@check_user_blocked
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Obtiene todos los comentarios relacionados con el post

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # No lo guardamos aún
            comment.post = post  # Asignamos el post al comentario
            comment.save()  # Ahora sí, guardamos el comentario
            return redirect('post_detail', post_id=post.id)  # Redirigimos a la misma página

    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'form': form, 'comments': comments})