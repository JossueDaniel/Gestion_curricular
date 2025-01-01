from django.contrib import admin

from .models import Silabo, Contenido, Aporte

# Register your models here.
class ContenidoInLine(admin.StackedInline):
    model = Contenido
    extra = 0

class ContenidoAdmin(admin.ModelAdmin):
    list_display = ['semana', 'contenido', 'resultados', 'resultados']

class AporteInLine(admin.TabularInline):
    model = Aporte
    max_num = 3

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['asignatura', 'facultad', 'carrera', 'fecha_actualizacion', 'fecha_creacion']
    inlines = [AporteInLine, ContenidoInLine]


admin.site.register(Contenido, ContenidoAdmin)
admin.site.register(Silabo, SyllabusAdmin)
admin.site.register(Aporte)
