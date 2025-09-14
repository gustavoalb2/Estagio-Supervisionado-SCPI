from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='visualizarTabelas'),
    path('tabela/<int:tabela_id>/', views.tabela, name='tabela_processos'),
    path('adicionarTabela/', views.adicionarTabela, name='adicionarTabela'),
    path('adicionarProcesso/', views.adicionarProcesso, name='adicionar_processo'),
    path('processo/', views.processo, name='processo'),
    path('tabela/<int:tabela_id>/adicionar_processo/', views.adicionarProcesso, name='adicionar_processo_tabela'),
    path('processo/editar/<int:processo_id>/', views.editarProcesso, name='editar_processo'),
    path('processo/deletar/<int:processo_id>/', views.deletaProcesso, name='deletar_processo'),
    path('usuario/', views.usuarios, name='usuarios'),
]