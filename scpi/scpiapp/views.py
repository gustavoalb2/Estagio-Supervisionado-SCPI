from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Processo, Usuario, TabelaProcessos
from .forms import ProcessoForm, TabelaForm
from datetime import datetime, date
from django.utils import timezone

def home(request):
    tabelas = TabelaProcessos.objects.all()
    context = {
        'tabelas': tabelas
    }
    return render(request, 'visualizarTabelas.html', context)

def processo(request):
    processos = TabelaProcessos.objects.all()
    return render(request, 'tabelaProcessos.html', {'processos': processos})

def adicionarTabela(request):
    if request.method == 'POST':
        try:
            nome_tabela = request.POST.get('titulo')
            descricao_tabela = request.POST.get('descricao')
            
            # Supondo que o usuário esteja logado. 
            # Em um cenário real, você teria um sistema de autenticação.
            # Por enquanto, vamos pegar o primeiro usuário ou criar um se não existir.
            usuario, created = Usuario.objects.get_or_create(
                id=1, 
                defaults={'nome': 'Usuário Padrão', 'email': 'padrao@example.com'}
            )

            if not nome_tabela:
                messages.error(request, 'O título da tabela é obrigatório.')
                return render(request, 'adicionarTabela.html')

            nova_tabela = TabelaProcessos(
                nome=nome_tabela,
                descricao=descricao_tabela,
                usuario=usuario
            )
            nova_tabela.save()
            
            messages.success(request, f'Tabela "{nome_tabela}" criada com sucesso!')
            return redirect('home') # Redireciona para a página inicial ou de visualização de tabelas

        except Exception as e:
            messages.error(request, f'Erro ao criar a tabela: {str(e)}')
            
    return render(request, 'adicionarTabela.html')

def editarProcesso(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    if request.method == 'POST':
        form = ProcessoForm(request.POST, instance=processo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Processo "{processo.numero_processo}" atualizado com sucesso!')
            if processo.tabela:
                return redirect('tabela_processos', tabela_id=processo.tabela.id)
            else:
                return redirect('visualizarTabelas')
        else:
            messages.error(request, 'Erro ao atualizar o processo. Verifique os dados informados.')
    else:
        form = ProcessoForm(instance=processo)

    context = {
        'form': form,
        'tabela': processo.tabela,
        'processo': processo  # Passa o objeto processo para o template
    }
    return render(request, 'processo_form.html', context)

def deletaProcesso(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    tabela_id = processo.tabela.id if processo.tabela else None

    if request.method == 'POST':
        try:
            numero_processo = processo.numero_processo
            processo.delete()
            messages.success(request, f'Processo {numero_processo} deletado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao deletar processo: {str(e)}')
    
    if tabela_id:
        return redirect('tabela_processos', tabela_id=tabela_id)
    else:
        return redirect('visualizarTabelas')

def adicionarProcesso(request, tabela_id=None):
    tabela = None
    if tabela_id:
        tabela = get_object_or_404(TabelaProcessos, pk=tabela_id)

    if request.method == 'POST':
        form = ProcessoForm(request.POST)
        if form.is_valid():
            processo = form.save(commit=False)
            if tabela:
                processo.tabela = tabela
            processo.save()
            messages.success(request, f'Processo "{processo.numero_processo}" adicionado com sucesso!')
            if tabela:
                return redirect('tabela_processos', tabela_id=tabela.id)
            else:
                return redirect('visualizarTabelas')
        else:
            messages.error(request, 'Erro ao adicionar o processo. Verifique os dados informados.')
    else:
        form = ProcessoForm()

    context = {
        'form': form,
        'tabela': tabela
    }
    return render(request, 'processo_form.html', context)

def tabela(request, tabela_id):
    tabela = get_object_or_404(TabelaProcessos, id=tabela_id)
    processos = Processo.objects.filter(tabela=tabela)

    # Contagem de processos por setor
    count_cic = processos.filter(setor='CIC').count()
    count_dpq = processos.filter(setor='DPQ').count()

    context = {
        'processos': processos,
        'tabela': tabela,
        'count_cic': count_cic,
        'count_dpq': count_dpq,
    }
    return render(request, 'tabelaProcessos.html', context)

def usuarios(request):
    # Exemplo: pegar o usuário logado (em produção)
    usuario = request.user if request.user.is_authenticated else None
    # Se não estiver autenticado, pode exibir um usuário de exemplo
    if not usuario or not hasattr(usuario, 'email'):
        usuario = Usuario(
            nome='Admin Sistema',
            email='admin@example.com',
            senha_hash='dummy',
            tipo=Usuario.TiposUsuario.ADMIN
        )
    context = {
        'usuario': usuario
    }
    return render(request, 'usuario.html', context)
