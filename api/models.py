from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    blocked = models.BooleanField(default=False)
    block_reason = models.TextField(blank=True, null=True, max_length=255)
    groups = models.ManyToManyField("auth.Group", related_name="usuarios")
    color = models.CharField(max_length=10, default="bg-red-400")
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="usuarios"
    )

    def __str__(self):
        return self.username


class Moderador(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    reason = models.TextField()
    active = models.BooleanField(default=True)


class Tema(models.Model):
    name = models.CharField(max_length=100)


class Sala(models.Model):
    theme = models.ForeignKey(Tema, on_delete=models.CASCADE)
    moderator = models.ForeignKey(Moderador, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RoomUser(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    room = models.ForeignKey(Sala, on_delete=models.CASCADE)
