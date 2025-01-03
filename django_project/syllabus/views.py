from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.urls import reverse

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


class ContenidoGet(DetailView):
    model = Silabo
    template_name = 'syllabus/contenido_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contenidos'] = self.object.contenido_syllabus.all()
        context['form'] = ContenidoForm()
        return context


class ContenidoPost(SingleObjectMixin, FormView):
    model = Silabo
    form_class = ContenidoForm
    template_name = 'syllabus/contenido_new.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        contenido = form.save(commit=False)
        contenido.syllabus = self.object
        contenido.save()
        return super().form_valid(form)

    def get_success_url(self):
        silabo = self.get_object()
        return reverse('contneido_new', kwargs={'pk': silabo.pk})

class ContenidoNewView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = ContenidoGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ContenidoPost.as_view()
        return view(request, *args, **kwargs)


class SilaboDetailView(LoginRequiredMixin, DetailView):
    model = Silabo
    context_object_name = 'silabo'
    template_name = 'syllabus/silabo_detail.html'
