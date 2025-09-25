from django.contrib import admin
from .models import Usuario, TabelaProcessos, Processo, Auditoria

class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('processo', 'usuario', 'acao', 'data_evento', 'detalhes')
    list_filter = ('acao', 'usuario', 'data_evento')
    search_fields = ('processo__numero_processo', 'usuario__nome', 'detalhes')
    readonly_fields = ('processo', 'usuario', 'acao', 'data_evento', 'detalhes')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Usuario)
admin.site.register(TabelaProcessos)
admin.site.register(Processo)
admin.site.register(Auditoria, AuditoriaAdmin)
