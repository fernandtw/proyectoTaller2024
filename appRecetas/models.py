from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario",  null=True, blank=True)
    title = models.CharField(max_length=250, verbose_name="Titulo")
    ingredients = models.TextField(default="", verbose_name="Ingredientes")
    instructions = models.TextField(default="", verbose_name="Instrucciones")
    image = models.ImageField(
        upload_to="posts", null=True, blank=True, verbose_name="Imagen"
    )
    tabla = models.ImageField(
        upload_to="posts", null=True, blank=True, verbose_name="Tabla"
    )
    category = models.CharField(max_length=40, choices=CATEGORIAS, default='otros')
    created = models.DateTimeField(
        default=timezone.now, verbose_name="Fecha de creación"
    )
    update = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificación")
    likes = models.ManyToManyField(User, related_name='app_recetas', verbose_name="Me Gusta")
    
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = "Publicacion"
        verbose_name_plural = "Publicaciones"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    
class Contacto(models.Model):
    OPCIONES_CONSULTAS = [
        ('general', 'Consulta General'),
        ('soporte', 'Soporte Técnico'),
        ('sugerencias', 'Sugerencias'),
        ('otros', 'Otros'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario",  null=True, blank=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    tipo_consulta = models.CharField(max_length=20, choices=OPCIONES_CONSULTAS, verbose_name="Tipo de Consulta")
    mensaje = models.TextField(verbose_name="Mensaje")
    avisos = models.BooleanField(default=False, verbose_name="Recibir Avisos")

    def __str__(self):
        return self.nombre


class Donaciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario",   null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField()
    metodoPago = models.CharField(max_length=45)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Ahora conectado con User directamente

    def __str__(self):
        return f"{self.monto} - {self.metodoPago}"






class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'{self.user.username} - {self.body[:20]}'
        return f'Comentario sin usuario - {self.body[:20]}' 