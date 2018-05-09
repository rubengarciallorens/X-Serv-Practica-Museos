from django.db import models

# Create your models here.

class Post (models.Model):
    post_text = models.CharField(max_length=200)
    def __str__ (self):
        return self.post_text

class Museo (models.Model):
    ID = models.IntegerField ()
    nombre = models.TextField ()
    descripcion_entidad = models.TextField ()
    equipamiento = models.TextField ()
    transporte = models.TextField ()
    descripcion = models.TextField ()
    horario = models.TextField ()
    accesibilidad = models.IntegerField()
    url = models.TextField ()
    localizacion = models.TextField ()
    contacto = models.TextField ()
    tipo = models.TextField ()
    def __str__ (self):
        return self.nombre
