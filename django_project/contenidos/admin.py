from django.contrib import admin

from .models import Contenido


# Register your models here.
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ['semana', 'contenido', 'resultados', 'resultados']


admin.site.register(Contenido, ContenidoAdmin)
