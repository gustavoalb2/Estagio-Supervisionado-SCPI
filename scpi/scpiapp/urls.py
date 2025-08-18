from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='inicio'),
    path('tabela/', views.tabela, name='tabela'),
    path('processo/', views.processo, name='processo'),
    path('processo/adicionar/', views.adicionar_processo, name='adicionar_processo'),
]