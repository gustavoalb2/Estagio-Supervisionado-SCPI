from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Processo, Usuario, TabelaProcessos
from .forms import ProcessoForm, TabelaForm
from datetime import datetime, date
from django.utils import timezone

from django.db.models import Q
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from openpyxl import load_workbook, Workbook

def home(request):
    query = request.GET.get('q')
    if query:
        tabelas = TabelaProcessos.objects.filter(nome__icontains=query)
    else:
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
            return redirect('visualizarTabelas') # Redireciona para a página inicial ou de visualização de tabelas

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
    query = request.GET.get('q')
    
    # Parâmetros de ordenação
    sort_by = request.GET.get('sort', 'nome')  # Ordenação padrão por nome
    sort_direction = request.GET.get('direction', 'asc')  # Direção padrão ascendente
    
    if query:
        processos = Processo.objects.filter(
            Q(tabela=tabela) & 
            (Q(nome__icontains=query) | 
             Q(numero_processo__icontains=query) |
             Q(assunto__icontains=query))
        )
    else:
        processos = Processo.objects.filter(tabela=tabela)
    
    # Aplicar ordenação
    if sort_by == 'nome':
        if sort_direction == 'desc':
            processos = processos.order_by('-nome')
        else:
            processos = processos.order_by('nome')
    elif sort_by == 'data_abertura':
        if sort_direction == 'desc':
            processos = processos.order_by('-data_abertura')
        else:
            processos = processos.order_by('data_abertura')
    elif sort_by == 'data_retorno':
        if sort_direction == 'desc':
            processos = processos.order_by('-data_retorno')
        else:
            processos = processos.order_by('data_retorno')
    
    # Contagem de processos por setor
    count_cic = processos.filter(setor='CIC').count()
    count_dpq = processos.filter(setor='DPQ').count()

    context = {
        'processos': processos,
        'tabela': tabela,
        'count_cic': count_cic,
        'count_dpq': count_dpq,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
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

def editar_tabela(request, tabela_id):
    tabela = get_object_or_404(TabelaProcessos, id=tabela_id)
    if request.method == 'POST':
        form = TabelaForm(request.POST, instance=tabela)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tabela "{tabela.nome}" atualizada com sucesso!')
            return redirect('visualizarTabelas')
        else:
            messages.error(request, 'Erro ao atualizar a tabela. Verifique os dados informados.')
    else:
        form = TabelaForm(instance=tabela)

    context = {
        'form': form,
        'tabela': tabela
    }
    return render(request, 'editar_tabela.html', context)

def excluir_tabela(request, tabela_id):
    tabela = get_object_or_404(TabelaProcessos, id=tabela_id)
    if request.method == 'POST':
        try:
            nome_tabela = tabela.nome
            tabela.delete()
            messages.success(request, f'Tabela "{nome_tabela}" excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir a tabela: {str(e)}')
        return redirect('visualizarTabelas')
    
    context = {
        'tabela': tabela
    }
    return render(request, 'confirmar_exclusao_tabela.html', context)

def exportar_xlsx(request, tabela_id):
    tabela = get_object_or_404(TabelaProcessos, id=tabela_id)
    processos = Processo.objects.filter(tabela=tabela)
    
    # Criar um novo workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Processos"
    
    # Adicionar cabeçalhos (na ordem correta conforme o PDF de contexto)
    headers = ['Nome', 'Matrícula', 'Nº Processo', 'Data de Abertura', 'Data de Retorno', 'Setor', 'Bolsa', 'Status', 'Assunto', 'Observações']
    for col_num, header in enumerate(headers, 1):
        ws.cell(row=1, column=col_num, value=header)
    
    # Adicionar dados (na ordem correta)
    for row_num, processo in enumerate(processos, 2):
        ws.cell(row=row_num, column=1, value=processo.nome)
        ws.cell(row=row_num, column=2, value=processo.matricula)
        ws.cell(row=row_num, column=3, value=processo.numero_processo)
        ws.cell(row=row_num, column=4, value=processo.data_abertura)
        ws.cell(row=row_num, column=5, value=processo.data_retorno)
        ws.cell(row=row_num, column=6, value=processo.get_setor_display() if processo.setor else "")
        ws.cell(row=row_num, column=7, value=processo.get_bolsa_display() if processo.bolsa else "")
        ws.cell(row=row_num, column=8, value=processo.get_status_display() if processo.status else "")
        ws.cell(row=row_num, column=9, value=processo.assunto)
        ws.cell(row=row_num, column=10, value=processo.observacoes)
    
    # Ajustar largura das colunas
    for col_num in range(1, len(headers) + 1):
        col_letter = chr(64 + col_num)  # A, B, C, ...
        ws.column_dimensions[col_letter].width = 20
    
    # Criar a resposta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="processos_{tabela.nome}.xlsx"'
    
    # Salvar o workbook para a resposta
    wb.save(response)
    
    return response

def exportar_processos_xlsx(request, tabela_id):
    return exportar_xlsx(request, tabela_id)

def exportar_processos_csv(request, tabela_id):
    tabela = get_object_or_404(TabelaProcessos, id=tabela_id)
    processos = Processo.objects.filter(tabela=tabela)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="processos_{tabela.nome}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nome', 'Matrícula', 'Nº Processo', 'Data de Abertura', 'Data de Retorno', 'Setor', 'Bolsa', 'Status', 'Assunto', 'Observações'])
    
    for processo in processos:
        writer.writerow([
            processo.nome,
            processo.matricula,
            processo.numero_processo,
            processo.data_abertura,
            processo.data_retorno,
            processo.get_setor_display(),
            processo.get_bolsa_display(),
            processo.get_status_display(),
            processo.assunto,
            processo.observacoes
        ])
        
    return response

def exportar_processos_pdf(request, tabela_id):
    tabela = get_object_or_404(TabelaProcessos, id=tabela_id)
    processos = Processo.objects.filter(tabela=tabela)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="processos_{tabela.nome}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Processos da Tabela: {tabela.nome}")

    y = 700
    for processo in processos:
        p.drawString(100, y, f"Nome: {processo.nome}, Processo: {processo.numero_processo}, Status: {processo.get_status_display()}")
        y -= 20
        if y < 100:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    return response

def importar_processos(request, tabela_id):
    if request.method == 'POST':
        tabela = get_object_or_404(TabelaProcessos, id=tabela_id)
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            messages.error(request, "Nenhum arquivo foi enviado.")
            return redirect('tabela_processos', tabela_id=tabela.id)

        try:
            workbook = load_workbook(excel_file)
            sheet = workbook.active
            
            processos_importados = 0
            processos_ignorados = 0
            
            # Determinar cabeçalhos e suas posições
            headers = None
            for row in sheet.iter_rows(min_row=1, max_row=1, values_only=True):
                headers = row
                break
            
            # Definir índices padrão (baseados na ordem da planilha do contexto)
            nome_idx = 0
            matricula_idx = 1
            numero_processo_idx = 2
            data_abertura_idx = 3
            data_retorno_idx = 4
            setor_idx = 5
            bolsa_idx = 6
            status_idx = 7
            assunto_idx = 8
            observacoes_idx = 9
            
            # Se os cabeçalhos existirem, ajustar os índices
            if headers:
                # Mapear cabeçalhos para índices (caso a ordem da planilha seja diferente)
                header_map = {h.lower().strip() if h else "": i for i, h in enumerate(headers)}
                
                # Atualizar índices com base nos cabeçalhos encontrados
                nome_idx = header_map.get("nome", 0)
                matricula_idx = header_map.get("matrícula", 1)
                numero_processo_idx = header_map.get("nº processo", 2)
                data_abertura_idx = header_map.get("data de abertura", 3)
                data_retorno_idx = header_map.get("data de retorno", 4)
                setor_idx = header_map.get("setor", 5)
                bolsa_idx = header_map.get("bolsa", 6)
                status_idx = header_map.get("status", 7)
                assunto_idx = header_map.get("assunto", 8)
                observacoes_idx = header_map.get("observações", 9)
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Verificar se a linha tem dados suficientes
                if not row or len(row) < 1 or not row[nome_idx]:  # Verificar se pelo menos o nome existe
                    continue  # Pular linhas vazias ou sem nome
                
                # Extrair valores de forma segura com valores padrão para campos faltantes
                nome = row[nome_idx] if len(row) > nome_idx and row[nome_idx] else ""
                matricula = row[matricula_idx] if len(row) > matricula_idx and row[matricula_idx] else None
                numero_processo = row[numero_processo_idx] if len(row) > numero_processo_idx and row[numero_processo_idx] else None
                data_abertura = row[data_abertura_idx] if len(row) > data_abertura_idx and row[data_abertura_idx] else None
                data_retorno = row[data_retorno_idx] if len(row) > data_retorno_idx and row[data_retorno_idx] else None
                setor = row[setor_idx] if len(row) > setor_idx and row[setor_idx] else None
                bolsa = row[bolsa_idx] if len(row) > bolsa_idx and row[bolsa_idx] else None
                status = row[status_idx] if len(row) > status_idx and row[status_idx] else None
                assunto = row[assunto_idx] if len(row) > assunto_idx and row[assunto_idx] else None
                observacoes = row[observacoes_idx] if len(row) > observacoes_idx and row[observacoes_idx] else None
                
                # Verificar se já existe um processo com o mesmo número
                if numero_processo and Processo.objects.filter(numero_processo=numero_processo).exists():
                    processos_ignorados += 1
                    continue
                
                # Criar o processo com os valores extraídos na ordem correta
                try:
                    # Verificar se os valores de Setor e Bolsa correspondem às opções permitidas
                    # Ajuste para Setor
                    setor_value = None
                    if setor:
                        setor_upper = str(setor).upper()
                        if setor_upper == 'CIC' or setor_upper == 'COORDENAÇÃO DE INICIAÇÃO CIENTÍFICA':
                            setor_value = 'CIC'
                        elif setor_upper == 'DPQ' or setor_upper == 'DEPARTAMENTO DE PESQUISA':
                            setor_value = 'DPQ'
                    
                    # Ajuste para Bolsa
                    bolsa_value = None
                    if bolsa:
                        bolsa_upper = str(bolsa).upper()
                        if bolsa_upper == 'SIM' or bolsa_upper == 'S' or bolsa_upper == 'TRUE' or bolsa_upper == '1':
                            bolsa_value = 'Sim'
                        elif bolsa_upper == 'NÃO' or bolsa_upper == 'NAO' or bolsa_upper == 'N' or bolsa_upper == 'FALSE' or bolsa_upper == '0':
                            bolsa_value = 'Não'
                    
                    # Ajuste para Status
                    status_value = None
                    if status:
                        status_upper = str(status).upper()
                        if 'CONCLU' in status_upper or status_upper == 'FINALIZADO':
                            status_value = 'concluido'
                        elif 'ANDAMENTO' in status_upper or 'EM PROCESSO' in status_upper or 'ABERTO' in status_upper:
                            status_value = 'em_andamento'
                    
                    Processo.objects.create(
                        tabela=tabela,
                        nome=nome,
                        matricula=matricula,
                        numero_processo=numero_processo,
                        data_abertura=data_abertura,
                        data_retorno=data_retorno,
                        setor=setor_value,
                        bolsa=bolsa_value,
                        status=status_value,
                        assunto=assunto,
                        observacoes=observacoes
                    )
                    processos_importados += 1
                except Exception as inner_e:
                    # Log detalhado do erro específico desta linha
                    processos_ignorados += 1
                    continue
            
            if processos_importados > 0:
                mensagem = f"Processos importados com sucesso! ({processos_importados} importados"
                if processos_ignorados > 0:
                    mensagem += f", {processos_ignorados} ignorados por duplicação ou erro)"
                else:
                    mensagem += ")"
                messages.success(request, mensagem)
            else:
                if processos_ignorados > 0:
                    messages.warning(request, f"Nenhum processo importado. {processos_ignorados} processos foram ignorados por duplicação ou erro.")
                else:
                    messages.warning(request, "Nenhum processo válido encontrado no arquivo.")
        except Exception as e:
            messages.error(request, f"Erro ao importar o arquivo: {e}")

    return redirect('tabela_processos', tabela_id=tabela_id)
