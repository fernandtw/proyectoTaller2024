from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Post
from .forms import PostForm, ContactoForm



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
    return render(request, "pages/recetas/receta_detalle.html",  context)

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


#Ayuda

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