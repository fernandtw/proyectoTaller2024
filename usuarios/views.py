from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from .models import Perfil
from .forms import CustomUserCreationForm, EditarPerfilForm


# Vista de cierre de sesión
def exit(request):
    logout(request)
    return redirect("recetas:home")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("recetas:home")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def perfil(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        # Crear un perfil por defecto si deseas
        perfil = Perfil.objects.create(usuario=request.user)

    # Precargar datos relacionados si es necesario
    perfil = Perfil.objects.select_related('usuario').get(usuario=request.user)

    return render(
        request,
        "pages/usuario/perfil.html",
        {
            "perfil": perfil,
            "email": request.user.email,
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
            return redirect("usuarios:perfil")
    else:
        form = EditarPerfilForm(instance=perfil)

    return render(request, "pages/usuario/editar_perfil.html", {"form": form})

# Create your views here.
