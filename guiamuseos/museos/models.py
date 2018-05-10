from django.db import models

# Create your models here.

class Post (models.Model):
    post_text = models.TextField (default = "DEFAULT_VALUE")
    def __str__ (self):
        return self.post_text

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
