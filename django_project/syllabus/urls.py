from django.urls import path

from . import views
from .views import (
    HomePageView,
    SilaboListView,
    ContenidoNewView,
    SilaboDetailView,
    ContenidoUpdateView,
    ContenidoDeleteView,
    ContenidoListView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('syllabus/', SilaboListView.as_view(), name='silabo_list'),

    path('syllabus/new/', views.registrar_silabo, name='silabo_new'),
    path('syllabus/<int:pk>/', SilaboDetailView.as_view(), name='silabo_detail'),
    path('syllabus/<int:pk>/report', views.generar_pdf, name='generar_pdf'),
    path('syllabus/<int:pk>/edit/', views.editar_silabo, name='silabo_update'),
    path('syllabus/<int:pk>/contenido/new/', ContenidoNewView.as_view(), name='contenido_new'),
    path('syllabus/<int:pk>/contenido/', ContenidoNewView.as_view(), name='contenido_list'),
    path('syllabus/<int:pk>/contenido/edit/', ContenidoUpdateView.as_view(), name='contenido_update'),
    path('syllabus/<int:pk>/contenido/delete/', ContenidoDeleteView.as_view(), name='contenido_delete'),
    path('syllabus/seguimiento/<int:pk>/', ContenidoListView.as_view(), name='contenido_list_tracking'),
    path('syllabus/seguimiento/<int:pk>/registrar/contenido/', views.registrar_completados, name='guardar_completados'),
]
