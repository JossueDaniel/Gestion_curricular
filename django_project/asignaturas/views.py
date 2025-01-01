from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Asignatura, Docente

# Create your views here.
class DocenteAsignaturaMixin:
    def get_queryset(self):
        return Asignatura.objects.filter(
            relacion_asignatura__docente__id=self.request.user.id
        ).distinct()

class AsignaturasListView(LoginRequiredMixin, DocenteAsignaturaMixin, ListView):
    model = Asignatura
    context_object_name = 'asignaturas_list'
    template_name = 'asignaturas/asignatura_list.html'


class AsignaturaDetailView(LoginRequiredMixin, DetailView):
    model = Asignatura
    context_object_name = 'asignatura'
    template_name = 'asignaturas/asignatura_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pre_requsitos'] = self.object.pre_requisitos.all()
        context['co_requsitos'] = self.object.co_requisitos.all()
        pre_requisitos = self.object.pre_requisitos.all()
        co_requisitos = self.object.co_requisitos.all()
        context['pre_requisitos'] = pre_requisitos
        context['co_requisitos'] = co_requisitos
        return context
