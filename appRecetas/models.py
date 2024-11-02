from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Contacto(models.Model):
    OPCIONES_CONSULTAS = [
        ('general', 'Consulta General'),
        ('soporte', 'Soporte Técnico'),
        ('sugerencias', 'Sugerencias'),
        ('otros', 'Otros'),
    ]

    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    tipo_consulta = models.CharField(max_length=20, choices=OPCIONES_CONSULTAS, verbose_name="Tipo de Consulta")
    mensaje = models.TextField(verbose_name="Mensaje")
    avisos = models.BooleanField(default=False, verbose_name="Recibir Avisos")

    def __str__(self):
        return self.nombre



# Recetas post

CATEGORIAS = [
    ('aperitivo', 'Aperitivo'),
    ('principal', 'Plato Principal'),
    ('postre', 'Postre'),
    ('bebida', 'Bebida'),
    ('pan', 'Pan y Bollería'),
    ('sopa', 'Sopa y Guiso'),
    ('ensalada', 'Ensalada'),
    ('mariscos', 'Mariscos'),
    ('carnes', 'Carnes'),
        ('vegetariano', 'Vegetariano'),
    ('otros', 'Otros'),
]
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
    category = models.CharField(max_length=40, choices=CATEGORIAS, default='otros')
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

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Anomimo")
    body = models.TextField(default="")
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '%s -%s' % (self.post.title, self.name)
