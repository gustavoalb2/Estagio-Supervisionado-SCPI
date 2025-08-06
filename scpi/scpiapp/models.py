# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    class TiposUsuario(models.TextChoices):
        ADMIN = 'admin', _('Administrador')
        COMUM = 'comum', _('Usuário Comum')
    
    tipo = models.CharField(
        max_length=10,
        choices=TiposUsuario.choices,
        default=TiposUsuario.COMUM
    )
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def is_admin(self):
        return self.tipo == self.TiposUsuario.ADMIN
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class Processo(models.Model):
    class StatusProcesso(models.TextChoices):
        ABERTO = 'aberto', _('Aberto')
        EM_ANDAMENTO = 'em_andamento', _('Em Andamento')
        CONCLUIDO = 'concluido', _('Concluído')
    
    numero = models.CharField(max_length=50, unique=True)
    setor_origem = models.CharField(max_length=100)
    data_abertura = models.DateField()
    status = models.CharField(
        max_length=15,
        choices=StatusProcesso.choices,
        default=StatusProcesso.ABERTO
    )
    descricao = models.TextField(blank=True)
    criado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='processos_criados'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def atualizar_status(self, novo_status):
        self.status = novo_status
        self.save()
        # Disparar notificação será implementado nos signals
        return True
    
    def __str__(self):
        return f"Processo #{self.numero} - {self.get_status_display()}"

class Notificacao(models.Model):
    processo = models.ForeignKey(
        Processo,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    mensagem = models.CharField(max_length=255)
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def marcar_como_lida(self):
        self.lida = True
        self.save()
        return True
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-data_criacao']

class Relatorio(models.Model):
    class TiposRelatorio(models.TextChoices):
        PDF = 'pdf', _('PDF')
        EXCEL = 'excel', _('Excel')
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='relatorios'
    )
    tipo = models.CharField(
        max_length=10,
        choices=TiposRelatorio.choices
    )
    parametros_filtro = models.JSONField()
    data_geracao = models.DateTimeField(auto_now_add=True)
    
    def gerar_arquivo(self):
        # Lógica de geração será implementada em signals/services
        return f"relatorio_{self.id}.{self.tipo}"
    
    class Meta:
        verbose_name = 'Relatório'
        verbose_name_plural = 'Relatórios'

class Auditoria(models.Model):
    class AcoesAuditoria(models.TextChoices):
        CRIAR = 'criar', _('Criar')
        ATUALIZAR = 'atualizar', _('Atualizar')
        EXCLUIR = 'excluir', _('Excluir')
    
    processo = models.ForeignKey(
        Processo,
        on_delete=models.CASCADE,
        related_name='auditorias'
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='acoes_auditadas'
    )
    acao = models.CharField(
        max_length=15,
        choices=AcoesAuditoria.choices
    )
    detalhes = models.TextField()
    data_evento = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Auditoria'
        verbose_name_plural = 'Auditorias'
        ordering = ['-data_evento']