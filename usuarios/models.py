from django.db import models
from django.contrib.auth.models import User


def user_avatar_upload_path(instance, filename):
    return f"avatars/{instance.usuario.username}/{filename}"

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_avatar_upload_path, null=True, blank=True, verbose_name="Avatar"
    )
    bio = models.CharField(max_length=250, blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username

# Create your models here.

