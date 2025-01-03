from django import forms
from django.forms import modelformset_factory, inlineformset_factory

from .models import Silabo, Aporte, Contenido


class SilaboForm(forms.ModelForm):
    class Meta:
        model = Silabo
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-input rounded-md',
                'required': 'required'
            }),
            'facultad': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3
            }),
            'carrera': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3
            }),
            'asignatura': forms.Select(attrs={
                'class': 'form-select rounded-md'
            }),
            'anio_academico': forms.NumberInput(attrs={
                'class': 'form-input rounded-md'
            }),
            'periodo_academico': forms.TextInput(attrs={
                'class': 'form-input rounded-md'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-input rounded-md',
                'type': 'date'
            }),
            'fecha_finalizacion': forms.DateInput(attrs={
                'class': 'form-input rounded-md',
                'type': 'date'
            }),
            'horario_clase': forms.TextInput(attrs={
                'class': 'form-input rounded-md'
            }),
            'horas_tutorias': forms.NumberInput(attrs={
                'class': 'form-input rounded-md'
            }),
            'horario_tutorias': forms.TextInput(attrs={
                'class': 'form-input rounded-md'
            }),
            'docente': forms.Select(attrs={
                'class': 'form-select rounded-md'
            }),
            'caracterizacion_asignatura': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3
            }),
            'objetivos': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3
            }),
            'competencias_transversales': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3
            }),
            'competencias_profesionales': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3
            }),
            'metodologia': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3
            }),
            'evaluacion': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3
            }),
            'bibliografia': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3
            }),
            'anexos': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3,
            }),
        }


class AporteForm(forms.ModelForm):
    class Meta:
        model = Aporte
        fields = ['actividades', 'examen', 'proyecto_final', 'total']
        widgets = {
            'actividades': forms.NumberInput(attrs={
                'class': 'form-input rounded-md w-16',
                'required': 'required'
            }),
            'examen': forms.NumberInput(attrs={
                'class': 'form-input rounded-md w-16',
                'required': 'required'
            }),
            'proyecto_final': forms.NumberInput(attrs={
                'class': 'form-input rounded-md w-16',
                'required': 'required'
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-input rounded-md w-16 p-2',
                'required': 'required'
            })
        }


AporteFormSet = inlineformset_factory(
    Silabo,
    Aporte,
    form=AporteForm,
    extra=3,
    max_num=3,
    validate_min=False,
    can_delete=False
)


class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = '__all__'
        exclude = ['syllabus']
        widgets = {
            'semana': forms.NumberInput(attrs={
                'class': 'form-input rounded-md w-16'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3,
            }),
            'actividades_docente': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3,
            }),
            'horas_docente': forms.NumberInput(attrs={
                'class': 'form-input rounded-md w-10',
            }),
            'actividades_practicas': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3,
            }),
            'horas_practica': forms.NumberInput(attrs={
                'class': 'form-input rounded-md w-10',
            }),
            'actividades_autonomas': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3,
            }),
            'horas_autonomas': forms.NumberInput(attrs={
                'class': 'form-input rounded-md w-10',
            }),
            'resultados': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3,
            }),
            'evidencias': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3,
            }),
            'observacion': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md',
                'rows': 3,
            }),
        }
