from django.db import models
import django.contrib.auth.models as modelsAuth
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
    contacto = models.TextField (default = "DEFAULT_VALUE")
    tipo = models.TextField (default = "DEFAULT_VALUE")
    def __str__ (self):
        return self.nombre

class Comentario (models.Model):
    museo = models.ForeignKey (Museo)
    comentario = models.TextField(default = "DEFAULT_VALUE")
    
class Seleccion (models.Model):
    museos_fav = models.ManyToManyField(Museo)
    propietario = models.OneToOneField(modelsAuth.User)

