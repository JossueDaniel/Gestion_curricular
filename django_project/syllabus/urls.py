from django.urls import path

from . import views
from .views import (
    HomePageView,
    SilaboListView,
    ContenidoNewView,
    SilaboDetailView,
    ContenidoListView,
    ContenidoUpdateView,
    ContenidoDeleteView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('syllabus/', SilaboListView.as_view(), name='silabo_list'),
    path('syllabus/new/', views.registrar_silabo, name='silabo_new'),
    path('syllabus/<int:pk>/edit/', views.editar_silabo, name='silabo_update'),
    path('syllabus/<int:pk>/contenido/new/', ContenidoNewView.as_view(), name='contenido_new'),
    path('syllabus/<int:pk>/', SilaboDetailView.as_view(), name='silabo_detail'),
    path('syllabus/<int:pk>/contenido/', ContenidoListView.as_view(), name='contenido_list'),
    path('syllabus/<int:pk>/contenido/edit/', ContenidoUpdateView.as_view(), name='contenido_update'),
    path('syllabus/<int:pk>/contenido/delete/', ContenidoDeleteView.as_view(), name='contenido_delete'),
]
