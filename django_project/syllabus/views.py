from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from uuid import UUID

from .models import Silabo, Aporte, Contenido
from .forms import SilaboForm, AporteFormSet, ContenidoForm
from .report_pdf import Report


# Create your views here.
"""
Mixin para filtrar los syllabus que pertenecen al usuario de la sesión
"""
class DocenteSyllabusMixin:
    def get_queryset(self):
        return Silabo.objects.filter(
            docente=self.request.user.id
        ).distinct()

class DocenteTestMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.docente == self.request.user
"""
Vista para mostrar los syllabus en el tablero de seguimiento
"""
class HomePageView(LoginRequiredMixin, DocenteSyllabusMixin, ListView):
    model = Silabo
    context_object_name = 'silabos'
    template_name = 'home.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(estado='aprobado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for silabo in context['silabos']:
            total_contenidos = Contenido.objects.filter(syllabus=silabo).count()
            completados = Contenido.objects.filter(syllabus=silabo, completado=True).count()

            # Calcular el progreso, evitando división por 0
            progreso = int((completados / total_contenidos) * 100) if total_contenidos > 0 else 0
            silabo.progreso = progreso

        return context


class SilaboListView(LoginRequiredMixin, DocenteSyllabusMixin, ListView):
    model = Silabo
    context_object_name = 'silabos'
    template_name = 'syllabus/silabo_list.html'

@login_required
def registrar_silabo(request):
    if request.method == 'POST':
        form = SilaboForm(request.POST, user=request.user.id)
        formset = AporteFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    silabo = form.save(commit=False)
                    silabo.docente = request.user
                    silabo.save()

                    aportes = formset.save(commit=False)
                    for i, aporte in enumerate(aportes, start=1):
                        if not aporte.aporte:
                            aporte.aporte = i
                        aporte.syllabus = silabo
                        aporte.save()

                messages.success(request, 'Sílabo registrado exitosamente.')
                return redirect('silabo_list')

            except Exception as e:
                form.add_error(None, f"Error al registrar: {str(e)}")
        else:
            if not form.is_valid():
                messages.error(request, 'Por favor, corrija los errores en el formulario.')

            if not formset.is_valid():
                messages.error(request, 'Por favor, corrija los errores en los aportes.')

    else:
        form = SilaboForm(user=request.user.id)
        formset = AporteFormSet()

    return render(request, 'syllabus/silabo_new.html', {
        'form': form,
        'formset': formset,
    })


@login_required
def editar_silabo(request, pk):
    silabo = get_object_or_404(Silabo, pk=pk)

    if request.user != silabo.docente:
        return HttpResponse('403 Forbidden')
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


class SilaboDetailView(LoginRequiredMixin, DocenteTestMixin, DetailView):
    model = Silabo
    context_object_name = 'silabo'
    template_name = 'syllabus/silabo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        silabo = self.get_object()
        aportes = Aporte.objects.filter(syllabus=silabo)
        context['aportes'] = aportes
        return context


class ContenidoGet(DocenteTestMixin, DetailView):
    model = Silabo
    template_name = 'syllabus/contenido_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contenidos'] = self.object.contenido_syllabus.all().order_by('semana')
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


class ContenidoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contenido
    form_class = ContenidoForm
    template_name = 'syllabus/contenido_update.html'

    def get_success_url(self):
        syllabus_pk = self.object.syllabus.pk
        return reverse('contenido_list', kwargs={'pk': syllabus_pk})

    def test_func(self):
        obj = self.get_object()
        return obj.syllabus.docente == self.request.user


class ContenidoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Contenido
    template_name = 'syllabus/contenido_delete.html'

    def get_success_url(self):
        silabo = self.object.syllabus.pk
        return reverse('contenido_list', kwargs={'pk': silabo})

    def test_func(self):
        obj = self.get_object()
        return obj.syllabus.docente == self.request.user


class ContenidoListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Contenido
    context_object_name = 'contenidos'
    template_name = 'contenido/contenido_list_seguimiento.html'


    def get_queryset(self):
        silabo_id = self.kwargs.get('pk')
        silabo = get_object_or_404(Silabo, pk=silabo_id)
        # if self.request.user != silabo.docente:
        #     return None
        if silabo:
            return Contenido.objects.filter(syllabus=silabo).order_by('semana')

        return Contenido.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        silabo_id = self.kwargs.get('pk')
        context['silabo'] = get_object_or_404(Silabo, pk=silabo_id) if silabo_id else None
        return context

    def test_func(self):
        silabo_id = self.kwargs.get('pk')
        silabo = Silabo.objects.get(pk=silabo_id)
        return self.request.user == silabo.docente


@login_required
def registrar_completados(request, pk):
    silabo_id = get_object_or_404(Silabo, pk=pk)
    if request.method == 'POST':
        seleccionados = request.POST.getlist('completados')
        # Contenido.objects.all().update(completado=False)
        Contenido.objects.filter(id__in=seleccionados).update(completado=True)

        if seleccionados:
            primer_contenido = get_object_or_404(Contenido, id=seleccionados[0])
            silabo = primer_contenido.syllabus.pk
            return redirect('contenido_list_tracking', pk=silabo)

    return redirect('contenido_list_tracking', pk=silabo_id.id)

@login_required
def generar_pdf(request, pk):
    silabo = Silabo.objects.get(pk=pk)
    if request.user != silabo.docente:
        return HttpResponseForbidden('403 forbidden')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=reporte_{silabo.asignatura.codigo}.pdf'

    pre_requisitos = silabo.asignatura.pre_requisitos.all()
    nombres_pre_req = ' '
    for pre_req in pre_requisitos:
        nombres_pre_req += f'{pre_req.codigo} - {pre_req.nombre}' + '\n'

    co_requisitos = silabo.asignatura.co_requisitos.all()
    nombres_co_req = ' '
    for co_req in co_requisitos:
        nombres_co_req += f'{co_req.codigo} - {co_req.nombre}' + '\n'

    user = request.user
    aportes = silabo.aporte_syllabus.all()
    actividades = silabo.contenido_syllabus.all().order_by('semana')
    pdf = Report(silabo, nombres_pre_req, nombres_co_req, user, aportes, actividades)
    pdf.generar_pdf(response)

    return response
