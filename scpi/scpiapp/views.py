from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Processo, Usuario
from datetime import datetime, date
from django.utils import timezone

def home(request):
    return render(request, 'base.html')

def processo(request):
    return render(request, 'processo.html')

def adicionar_processo(request):
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            nome = request.POST.get('nome')
            matricula = request.POST.get('matricula')
            numero_processo = request.POST.get('numero_processo')
            data_abertura = request.POST.get('data_abertura')
            data_retorno = request.POST.get('data_retorno')
            bolsa = request.POST.get('bolsa')
            status = request.POST.get('status')
            setor_origem = request.POST.get('setor_origem')
            assunto = request.POST.get('assunto')
            descricao = request.POST.get('descricao')
            
            # Validações básicas
            if not all([nome, matricula, numero_processo, data_abertura, status, setor_origem, assunto]):
                messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
                return render(request, 'processo.html')
            
            # Converter datas
            data_abertura = datetime.strptime(data_abertura, '%Y-%m-%d').date()
            data_retorno_obj = None
            if data_retorno:
                data_retorno_obj = datetime.strptime(data_retorno, '%Y-%m-%d').date()
            
            # Criar usuário temporário (em produção, usar o usuário logado)
            usuario_atual, created = Usuario.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@example.com',
                    'first_name': 'Admin',
                    'last_name': 'Sistema',
                    'tipo': Usuario.TiposUsuario.ADMIN,
                }
            )
            
            # Simular criação do processo (adaptado para a estrutura atual)
            processo_data = {
                'nome': nome,
                'matricula': matricula,
                'numero_processo': numero_processo,
                'data_abertura': data_abertura,
                'data_retorno': data_retorno_obj,
                'setor_origem': setor_origem,
                'assunto': assunto,
                'status': status,
                'descricao': descricao or '',
                'criado_por': usuario_atual,
            }
            
            # Por enquanto, vamos apenas simular o salvamento
            # Em produção, descomente a linha abaixo quando a estrutura do banco estiver correta:
            # processo = Processo.objects.create(**processo_data)
            
            messages.success(request, f'Processo {numero_processo} criado com sucesso!')
            return redirect('tabela')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar processo: {str(e)}')
            return render(request, 'processo.html')
    
    return render(request, 'processo.html')

def tabela(request):
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
    context = {
        'processos': processos_exemplo
    }
    return render(request, 'tabela.html', context)