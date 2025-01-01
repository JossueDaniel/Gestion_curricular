from django.urls import path

from .views import AsignaturasListView, AsignaturaDetailView

urlpatterns = [
    path('', AsignaturasListView.as_view(), name='asignaturas_list'),
    path('<str:pk>/', AsignaturaDetailView.as_view(), name='asignatura_detail'),
]
