from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Post
from usuarios.models import Perfil
from django.http import HttpResponseRedirect
from django.urls import reverse
from .decorators import check_user_blocked
from .forms import PostForm, ContactoForm, CommentForm



############################
def is_admin(user):
    return user.is_staff


#############################


# Vista de inicio (home)
def home(request):
    recetas = Post.objects.all()  # Transforma datos a una lista
    data = {"recetas": recetas}
    return render(request, "index.html", data)


# Vista de recetas
@check_user_blocked
def recetas(request):
    recetas = Post.objects.all()  # Transforma datos a una lista
    data = {"recetas": recetas}
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
    data = {
        "recetas": recetas  # Cambia 'Post' por 'recetas' para que sea más descriptivo
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
    
@check_user_blocked
def busqueda_funcional(request):
    searched = request.GET.get('searched')
    
    if searched:
        resultados = Receta.objects.filter(nombre__icontains=searched)  # Ajusta el filtro según tu modelo

        # Paginación
        paginator = Paginator(resultados, 5)  # Muestra 10 resultados por página
        page = request.GET.get('page')
        try:
            resultados = paginator.page(page)
        except PageNotAnInteger:
            # Si la página no es un entero, muestra la primera página
            resultados = paginator.page(1)
        except EmptyPage:
            # Si la página está fuera de rango, muestra la última página
            resultados = paginator.page(paginator.num_pages)

        return render(request, 'busqueda.html', {'resultados': resultados, 'searched': searched})
    else:
        return render(request, 'busqueda.html', {'mensaje': 'Ingresa un término de búsqueda'})


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