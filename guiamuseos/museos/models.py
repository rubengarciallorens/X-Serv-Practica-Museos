from django.db import models

# Create your models here.

class Post (models.Model):
    post_text = models.CharField(max_length=200)
    def __str__ (self):
        return self.post_text

class Museo (models.Model):
    museo.nombre = models.TextField ()
    museo.direccion = models.TextField ()
    museo.url = models.TextField ()
