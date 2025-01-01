from django import forms

from .models import Asignatura

class AsignaturaAdminForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['pre_requisitos'].queryset = Asignatura.objects.exclude(pk=self.instance.pk)
            self.fields['co_requisitos'].queryset = Asignatura.objects.exclude(pk=self.instance.pk)
