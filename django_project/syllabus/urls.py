from django.urls import path

from . import views
from .views import HomePageView, SilaboListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('syllabus/', SilaboListView.as_view(), name='silabo_list'),
    path('syllabus/new/', views.registrar_silabo, name='silabo_new'),
]
