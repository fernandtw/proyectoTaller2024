from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, Perfil
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, PostForm, EditarPerfilForm
from django.contrib.auth.forms import AuthenticationForm


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
@login_required
def recetas(request):
    recetas = Post.objects.all()  # Transforma datos a una lista
    data = {"recetas": recetas}
    return render(request, "pages/recetas/lista_recetas.html", data)


# Vista de cierre de sesión
def exit(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@user_passes_test(is_admin)
def agregar_receta(request):

    data = {"form": PostForm()}

    if request.method == "POST":
        formulario = PostForm(
            data=request.POST, files=request.FILES
        )  # Crea una instancia del formulario
        if formulario.is_valid():
            formulario.save()
        else:
            # Si el formulario no es válido, lo volvemos a enviar con los errores
            data = {
                "form": formulario,
                "mensaje": "Hubo un error al guardar la receta.",
            }
    else:
        formulario = PostForm()
        data = {"form": formulario}

    return render(request, "pages/Admin/agregar.html", data)


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
            return redirect(to="listar_recetas")
        data["form"] = formulario

    return render(request, "pages/Admin/modificar.html", data)


@user_passes_test(is_admin)
def eliminar_receta(request, id):
    receta = get_object_or_404(Post, id=id)
    receta.delete()
    return redirect(to="listar_recetas")


# Detalle receta


def receta_detalle(request, receta_id):
    receta = get_object_or_404(Post, id=receta_id)
    ingredientes = receta.ingredients.split(
        "\n"
    )  # Convertir los ingredientes en una lista
    instrucciones = receta.instructions.split(
        "\n"
    )  # Convertir las instrucciones en una lista

    context = {
        "receta": receta,
        "ingredientes": ingredientes,
        "instrucciones": instrucciones,
    }
    return render(request, "pages/recetas/receta_detalle.html", context)


@login_required
def perfil(request):
    perfil = request.user.perfil
    return render(
        request,
        "pages/usuario/perfil.html",
        {
            "perfil": perfil,
            "email": request.user.email,  # Asegúrate de incluir el correo electrónico
        },
    )


@login_required
def editar_perfil(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)

    if request.method == "POST":
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            # Actualizar nombre de usuario y correo electrónico en el modelo User
            request.user.username = form.cleaned_data["username"]
            request.user.email = form.cleaned_data["email"]
            request.user.save()

            # Guardar cambios en el perfil
            form.save()
            return redirect("perfil")
    else:
        form = EditarPerfilForm(instance=perfil)

    return render(request, "pages/usuario/editar_perfil.html", {"form": form})


# Busqueda


def busqueda_funcional(request):
    if request.method == "POST":
        searched = request.POST.get("busquedaFuncional")
        resultados = Post.objects.filter(title__contains=searched)
        return render(
            request,
            "pages/post/busqueda.html",
            {
                "searched": searched,
                "resultados": resultados,
            },
        )
    else:
        return render(request, "pages/post/busqueda.html", {})
