from django.db import models
import django.contrib.auth.models as modelsAuth
from django.utils import timezone
# Create your models here.


class Museo (models.Model):
    identidad = models.TextField (default = "DEFAULT_VALUE")
    nombre = models.TextField (default = "DEFAULT_VALUE")
    descripcion_entidad = models.TextField (default = "DEFAULT_VALUE")
    equipamiento = models.TextField (default = "DEFAULT_VALUE")
    transporte = models.TextField (default = "DEFAULT_VALUE")
    descripcion = models.TextField (default = "DEFAULT_VALUE")
    horario = models.TextField (default = "DEFAULT_VALUE")
    accesibilidad = models.TextField(default = "DEFAULT_VALUE")
    url = models.TextField (default = "DEFAULT_VALUE")
    localizacion = models.TextField (default = "DEFAULT_VALUE")
    telefono = models.TextField (default = "DEFAULT_VALUE")
    fax = models.TextField (default = "No proporcionado")
    email = models.TextField (default = "No proporcionado")
    tipo = models.TextField (default = "No proporcionado")
    num_comentarios = models.IntegerField (default=0)
    def __str__ (self):
        return self.nombre

class Comentario (models.Model):
    museo = models.ForeignKey (Museo)
    texto = models.TextField(default = "DEFAULT_VALUE")
    def __str__ (self):
        return self.texto

class Museo_añadido (models.Model):
    museo = models.ForeignKey(Museo)
    añadido = models.DateTimeField(default=timezone.now)

class Seleccion (models.Model):
    museos_fav = models.ManyToManyField(Museo_añadido)
    propietario = models.OneToOneField(modelsAuth.User)
    nombre = models.TextField(default = "DEFAULT_VALUE")
