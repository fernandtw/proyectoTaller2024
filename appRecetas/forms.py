from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Perfil


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "ingredients",
            "instructions",
            "image",
            "tabla",
            "published",
            "category",
        ]
        widgets = {
            "ingredients": forms.Textarea(attrs={"rows": 4}),
            "instructions": forms.Textarea(attrs={"rows": 4}),
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["bio", "avatar"]


class EditarPerfilForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, required=True
    )  # Campo para editar el nombre de usuario
    email = forms.EmailField(required=True)  # Campo para editar el correo

    class Meta:
        model = Perfil
        fields = [
            "bio",
            "avatar",
            "username",
            "email",
        ]  # Añadimos username y email a los campos

    # Sobrescribir el método init para inicializar los campos de User
    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        user = kwargs.get(
            "instance"
        ).usuario  # Obtener el usuario relacionado con el perfil
        self.fields["username"].initial = user.username
        self.fields["email"].initial = user.email

    # Validar la unicidad del nombre de usuario
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if (
            User.objects.filter(username=username)
            .exclude(pk=self.instance.usuario.pk)
            .exists()
        ):
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    # Validar la unicidad del correo electrónico
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            User.objects.filter(email=email)
            .exclude(pk=self.instance.usuario.pk)
            .exists()
        ):
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email
