from django.contrib import admin
from .models import Museo
from .models import Comentario
from .models import Seleccion
# Register your models here.

admin.site.register(Museo)
admin.site.register(Comentario)
admin.site.register(Seleccion)
