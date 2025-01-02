from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from .models import Silabo, Aporte
from .forms import SilaboForm, AporteFormSet, ContenidoForm


# Create your views here.
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class SilaboListView(LoginRequiredMixin, ListView):
    model = Silabo
    context_object_name = 'silabos'
    template_name = 'syllabus/silabo_list.html'


def registrar_silabo(request):
    if request.method == 'POST':
        form = SilaboForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    silabo = form.save()
                    formset = AporteFormSet(request.POST, instance=silabo)

                    if formset.is_valid():
                        aportes = formset.save(commit=False)

                        for i, aporte in enumerate(aportes, start=1):
                            if not aporte.aporte:
                                aporte.aporte = i
                            aporte.syllabus = silabo
                            aporte.save()

                        return redirect('silabo_list')
                    else:
                        print(formset.errors)
            except Exception as e:
                form.add_error(None, f"Error al registrar: {str(e)}")
        else:
            formset = AporteFormSet(request.POST)
    else:
        form = SilaboForm()
        formset = AporteFormSet()

    return render(request, 'syllabus/silabo_new.html', {
        'form': form,
        'formset': formset,
    })


class SilaboDetailView(DetailView):
    model = Silabo
    context_object_name = 'silabo'
    template_name = 'syllabus/silabo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContenidoForm()
        context['contenidos'] = self.object.contenido_syllabus.all()
        return context
