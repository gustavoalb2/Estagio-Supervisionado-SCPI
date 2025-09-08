from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Processo, Usuario
from datetime import datetime, date
from django.utils import timezone

def home(request):
    return render(request, 'visualizarTabelas.html')

def processo(request):
    return render(request, 'processo.html')

def adicionarTabela(request):
    return render(request, 'adicionarTabela.html')

def editarProcesso(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    if request.method == 'POST':
        try:
            processo.numero = request.POST.get('numero_processo')
            processo.setor_origem = request.POST.get('setor_origem')
            data_abertura_str = request.POST.get('data_abertura')
            if data_abertura_str:
                processo.data_abertura = datetime.strptime(data_abertura_str, '%Y-%m-%d').date()
            processo.status = request.POST.get('status')
            processo.descricao = request.POST.get('descricao')
            
            processo.save()
            messages.success(request, f'Processo {processo.numero} atualizado com sucesso!')
            return redirect('tabela')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar processo: {str(e)}')
    
    context = {
        'processo': processo
    }
    return render(request, 'processo.html', context)

def deletaProcesso(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    if request.method == 'POST':
        try:
            numero_processo = processo.numero
            processo.delete()
            messages.success(request, f'Processo {numero_processo} deletado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao deletar processo: {str(e)}')
    return redirect('tabela')

def adicionarProcesso(request):
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            nome = request.POST.get('nome')
            matricula = request.POST.get('matricula')
            numero_processo = request.POST.get('numero_processo')
            data_abertura = request.POST.get('data_abertura')
            status = request.POST.get('status')
            setor_origem = request.POST.get('setor_origem')
            descricao = request.POST.get('descricao')
            
            # Validações básicas
            if not all([numero_processo, data_abertura, status, setor_origem]):
                messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
                return render(request, 'processo.html')
            
            # Converter data
            data_abertura_obj = datetime.strptime(data_abertura, '%Y-%m-%d').date()
            
            # Criar e salvar o processo
            novo_processo = Processo(
                numero=numero_processo,
                data_abertura=data_abertura_obj,
                status=status,
                setor_origem=setor_origem,
                descricao=descricao
            )
            novo_processo.save()
            
            messages.success(request, f'Processo {numero_processo} criado com sucesso!')
            return redirect('tabela')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar processo: {str(e)}')
            return render(request, 'processo.html')
    
    return render(request, 'processo.html')

def tabela(request):
<<<<<<< Updated upstream
    # Criar dados de exemplo diretamente para demonstração
    # Em um caso real, estes viriam do banco de dados
    processos_exemplo = [
        {
            'id': 1,
            'nome': 'João Silva',
            'matricula': 'MAT2025001',
            'numero_processo': 'PROC-2025001',
            'data_abertura': date(2025, 1, 15),
            'data_retorno': None,
            'setor_origem': 'Financeiro',
            'is_active': True,
            'status': 'em_andamento',
            'assunto': 'Solicitação de reembolso de despesas médicas',
        },
        {
            'id': 2,
            'nome': 'Maria Santos',
            'matricula': 'MAT2025002',
            'numero_processo': 'PROC-2025002',
            'data_abertura': date(2025, 2, 10),
            'data_retorno': date(2025, 2, 20),
            'setor_origem': 'RH',
            'is_active': True,
            'status': 'concluido',
            'assunto': 'Alteração de dados cadastrais',
        },
        {
            'id': 3,
            'nome': 'Pedro Oliveira',
            'matricula': 'MAT2025003',
            'numero_processo': 'PROC-2025003',
            'data_abertura': date(2025, 3, 5),
            'data_retorno': None,
            'setor_origem': 'TI',
            'is_active': False,
            'status': 'aberto',
            'assunto': 'Solicitação de acesso ao sistema',
        },
        {
            'id': 4,
            'nome': 'Ana Costa',
            'matricula': 'MAT2025004',
            'numero_processo': 'PROC-2025004',
            'data_abertura': date(2025, 4, 1),
            'data_retorno': None,
            'setor_origem': 'Operações',
            'is_active': True,
            'status': 'em_andamento',
            'assunto': 'Manutenção de equipamentos',
        },
        {
            'id': 5,
            'nome': 'Carlos Ferreira',
            'matricula': 'MAT2025005',
            'numero_processo': 'PROC-2025005',
            'data_abertura': date(2025, 5, 12),
            'data_retorno': date(2025, 5, 25),
            'setor_origem': 'Marketing',
            'is_active': True,
            'status': 'concluido',
            'assunto': 'Aprovação de campanha publicitária',
        },
        {
            'id': 5,
            'nome': 'Carlos Ferreira',
            'matricula': 'MAT2025005',
            'numero_processo': 'PROC-2025005',
            'data_abertura': date(2025, 5, 12),
            'data_retorno': date(2025, 5, 25),
            'setor_origem': 'Marketing',
            'is_active': True,
            'status': 'concluido',
            'assunto': 'Aprovação de campanha publicitária',
        },
        {
            'id': 5,
            'nome': 'Carlos Ferreira',
            'matricula': 'MAT2025005',
            'numero_processo': 'PROC-2025005',
            'data_abertura': date(2025, 5, 12),
            'data_retorno': date(2025, 5, 25),
            'setor_origem': 'Marketing',
            'is_active': True,
            'status': 'concluido',
            'assunto': 'Aprovação de campanha publicitária',
        },
        {
            'id': 5,
            'nome': 'Carlos Ferreira',
            'matricula': 'MAT2025005',
            'numero_processo': 'PROC-2025005',
            'data_abertura': date(2025, 5, 12),
            'data_retorno': date(2025, 5, 25),
            'setor_origem': 'Marketing',
            'is_active': True,
            'status': 'concluido',
            'assunto': 'Aprovação de campanha publicitária',
        },
        {
            'id': 5,
            'nome': 'Carlos Ferreira',
            'matricula': 'MAT2025005',
            'numero_processo': 'PROC-2025005',
            'data_abertura': date(2025, 5, 12),
            'data_retorno': date(2025, 5, 25),
            'setor_origem': 'Marketing',
            'is_active': True,
            'status': 'concluido',
            'assunto': 'Aprovação de campanha publicitária',
        },
        {
            'id': 5,
            'nome': 'Carlos Ferreira',
            'matricula': 'MAT2025005',
            'numero_processo': 'PROC-2025005',
            'data_abertura': date(2025, 5, 12),
            'data_retorno': date(2025, 5, 25),
            'setor_origem': 'Marketing',
            'is_active': True,
            'status': 'concluido',
            'assunto': 'Aprovação de campanha publicitária',
        },
    ]
    
    # Passar os dados para o template
=======
    processos = Processo.objects.all()
>>>>>>> Stashed changes
    context = {
        'processos': processos
    }
    return render(request, 'tabela.html', context)

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
