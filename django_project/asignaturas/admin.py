from django.contrib import admin

from .models import Asignatura, Docente
from .forms import AsignaturaAdminForm

# Register your models here.
class DocenteInLine(admin.TabularInline):
    model = Docente
    extra = 0

class AsignaturaAdmin(admin.ModelAdmin):
    form = AsignaturaAdminForm
    list_display = ['codigo', 'nombre']
    filter_horizontal = ('pre_requisitos', 'co_requisitos')
    inlines = [DocenteInLine]

admin.site.register(Asignatura, AsignaturaAdmin)
