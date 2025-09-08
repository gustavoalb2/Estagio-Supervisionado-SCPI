from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='visualizarTabelas'),
    path('tabela/', views.tabela, name='tabela'),
    path('tabela/adicionarTabela', views.adicionarTabela, name='adicionarTabela'),
    path('processo/', views.processo, name='processo'),
    path('processo/adicionar/', views.adicionarProcesso, name='adicionar_processo'),
    path('processo/editar/<int:processo_id>/', views.editarProcesso, name='editar_processo'),
    path('processo/deletar/<int:processo_id>/', views.deletaProcesso, name='deletar_processo'),
    path('usuario/', views.usuarios, name='usuarios'),
]