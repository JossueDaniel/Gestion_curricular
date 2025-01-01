from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView

from .models import Silabo, Aporte
from .forms import SilaboForm, AporteFormSet


# Create your views here.
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class SilaboListView(ListView):
    model = Silabo
    context_object_name = 'silabos'
    template_name = 'syllabus/silabo_list.html'


class SilaboCreateView(CreateView):
    model = Silabo
    template_name = 'syllabus/new.html'
    fields = '__all__'


class AporteCreateView(CreateView):
    model = Aporte
    template_name = 'syllabus/aporte_new.html'
    fields = '__all__'


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
