from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Silabo, Aporte, Contenido
from .forms import SilaboForm, AporteFormSet, ContenidoForm


# Create your views here.
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class SilaboListView(LoginRequiredMixin, ListView):
    model = Silabo
    context_object_name = 'silabos'
    template_name = 'syllabus/silabo_list.html'

@login_required
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

@login_required
def editar_silabo(request, pk):
    silabo = get_object_or_404(Silabo, pk=pk)

    if request.method == 'POST':
        form = SilaboForm(request.POST, instance=silabo)
        # formset = AporteFormSet(request.POST, instance=silabo)

        if form.is_valid():
            silabo = form.save()
            # for form in formset:
            #     if form.cleaned_data():
            #         aporte = form.save(commit=False)
            #         aporte.syllabus = silabo
            #         aporte_id = form.cleaned_data.get('id')
            #         print('Apiorte id: ', aporte_id)
            #         if aporte_id:
            #             aporte.id = aporte_id
            #         aporte.save()
            form.save()

            return redirect('silabo_detail', pk=pk)
        else:
            print("Form errors:", form.errors)
            # print("Formset errors:", formset.errors)
    else:
        form = SilaboForm(instance=silabo)
        # formset = AporteFormSet(instance=silabo)


    return render(request, 'syllabus/silabo_update.html', {
        'form': form,
        'silabo': silabo,
        # 'formset': formset
    })


class SilaboDetailView(LoginRequiredMixin, DetailView):
    model = Silabo
    context_object_name = 'silabo'
    template_name = 'syllabus/silabo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        silabo = self.get_object()
        aportes = Aporte.objects.filter(syllabus=silabo)
        context['aportes'] = aportes
        return context


class ContenidoGet(DetailView):
    model = Silabo
    template_name = 'syllabus/contenido_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contenidos'] = self.object.contenido_syllabus.all()
        context['form'] = ContenidoForm()
        return context


class ContenidoPost(SingleObjectMixin, FormView):
    model = Silabo
    form_class = ContenidoForm
    template_name = 'syllabus/contenido_list.html'

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
        return reverse('contenido_list', kwargs={'pk': silabo.pk})


class ContenidoNewView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = ContenidoGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ContenidoPost.as_view()
        return view(request, *args, **kwargs)


class ContenidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Contenido
    form_class = ContenidoForm
    template_name = 'syllabus/contenido_update.html'

    def get_success_url(self):
        syllabus_pk = self.object.syllabus.pk
        return reverse('contenido_list', kwargs={'pk': syllabus_pk})


class ContenidoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contenido
    template_name = 'syllabus/contenido_delete.html'

    def get_success_url(self):
        silabo = self.object.syllabus.pk
        return reverse('contenido_list', kwargs={'pk': silabo})
