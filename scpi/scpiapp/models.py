from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    class TiposUsuario(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        COMUM = 'comum', 'Usuário Comum'

    nome = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True, null=True)
    senha_hash = models.CharField(max_length=255, null=True)
    tipo = models.CharField(max_length=10, choices=TiposUsuario.choices, default=TiposUsuario.COMUM, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class TabelaProcessos(models.Model):
    nome = models.CharField(max_length=255, null=True)
    descricao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tabelas')
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class Processo(models.Model):
    class StatusProcesso(models.TextChoices):
        EM_ANDAMENTO = 'em_andamento', 'Em Andamento'
        CONCLUIDO = 'concluido', 'Concluído'

    class BolsaOpcoes(models.TextChoices):
        SIM = 'Sim', 'Sim'
        NAO = 'Não', 'Não'

    class SetorOpcoes(models.TextChoices):
        CIC = 'CIC', 'CIC'
        DPQ = 'DPQ', 'DPQ'

    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50, blank=True, null=True)
    numero_processo = models.CharField(max_length=50, unique=True, null=True)
    data_abertura = models.DateField(null=True, blank=True)
    data_retorno = models.DateField(null=True, blank=True)
    setor = models.CharField(max_length=100, choices=SetorOpcoes.choices, null=True, blank=True)
    bolsa = models.CharField(max_length=3, choices=BolsaOpcoes.choices, null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusProcesso.choices, null=True, blank=True)
    assunto = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    tabela = models.ForeignKey(TabelaProcessos, on_delete=models.CASCADE, related_name='processos', null=True, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Processo #{self.numero_processo} - {self.nome}"

class Relatorio(models.Model):
    class TiposRelatorio(models.TextChoices):
        PDF = 'PDF', 'PDF'
        EXCEL = 'Excel', 'Excel'

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='relatorios', null=True)
    tipo = models.CharField(max_length=10, choices=TiposRelatorio.choices, null=True)
    parametros_filtro = models.JSONField(null=True)
    data_geracao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Relatório {self.id} - {self.tipo}"


class Auditoria(models.Model):
    class AcoesAuditoria(models.TextChoices):
        CRIAR = 'CRIAR', 'Criar'
        ATUALIZAR = 'ATUALIZAR', 'Atualizar'
        EXCLUIR = 'EXCLUIR', 'Excluir'

    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='auditorias', null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='acoes_auditadas', null=True)
    acao = models.CharField(max_length=15, choices=AcoesAuditoria.choices, null=True)
    detalhes = models.TextField(null=True)
    data_evento = models.DateTimeField(default=timezone.now)