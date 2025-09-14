from django import forms
from .models import Processo, TabelaProcessos

class TabelaForm(forms.ModelForm):
    class Meta:
        model = TabelaProcessos
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Tabela'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição da Tabela'}),
        }

class ProcessoForm(forms.ModelForm):
    class Meta:
        model = Processo
        fields = [
            'nome', 'matricula', 'numero_processo', 'data_abertura', 'data_retorno', 
            'setor', 'bolsa', 'status', 'assunto', 'observacoes'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'id': 'nome'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'id': 'matricula'}),
            'numero_processo': forms.TextInput(attrs={'class': 'form-control', 'id': 'numero_processo'}),
            'data_abertura': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'data_abertura'}),
            'data_retorno': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'data_retorno'}),
            'setor': forms.Select(attrs={'class': 'form-select'}),
            'bolsa': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assunto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
