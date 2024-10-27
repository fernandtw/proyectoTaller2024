from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.


# Categoría
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Nombre")
    active = models.BooleanField(default=True, verbose_name="Active")
    created = models.DateField(auto_now=True, verbose_name="Fecha de creacion")
    updated = models.DateField(auto_now=True, verbose_name="Fecha de modificacion")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]

    def __str__(self):
        return self.name


def user_avatar_upload_path(instance, filename):
    return f"avatars/{instance.usuario.username}/{filename}"


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_avatar_upload_path, null=True, blank=True, verbose_name="Avatar"
    )
    bio = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.usuario.username


# Autor


# Modelo


# Recetas post


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name="Titulo")
    ingredients = models.TextField(default="", verbose_name="Ingredientes")
    instructions = models.TextField(default="", verbose_name="Instrucciones")
    image = models.ImageField(
        upload_to="posts", null=True, blank=True, verbose_name="Imagen"
    )
    tabla = models.ImageField(
        upload_to="posts", null=True, blank=True, verbose_name="Tabla"
    )
    published = models.BooleanField(default=False, verbose_name="Publicado")

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Categoria"
    )

    created = models.DateTimeField(
        default=timezone.now, verbose_name="Fecha de creación"
    )
    update = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificación")

    class Meta:
        verbose_name = "Publicacion"
        verbose_name_plural = "Publicaciones"
        ordering = ["-created"]

    def __str__(self):
        return self.title
