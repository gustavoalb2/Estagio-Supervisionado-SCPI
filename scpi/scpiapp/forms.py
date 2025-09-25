from django import forms
from .models import Processo, TabelaProcessos
from django.contrib.auth.models import User


class ProcessoForm(forms.ModelForm):
    class Meta:
        model = Processo
        fields = [
            'nome', 'matricula', 'numero_processo', 'data_abertura', 
            'data_retorno', 'setor', 'bolsa', 'status', 'assunto', 'observacoes'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo'
            }),
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a matrícula'
            }),
            'numero_processo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o número do processo'
            }),
            'data_abertura': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_retorno': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'setor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'bolsa': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assunto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite o assunto do processo'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite observações adicionais'
            })
        }
        labels = {
            'nome': 'Nome',
            'matricula': 'Matrícula',
            'numero_processo': 'Número do Processo',
            'data_abertura': 'Data de Abertura',
            'data_retorno': 'Data de Retorno',
            'setor': 'Setor',
            'bolsa': 'Bolsa',
            'status': 'Status',
            'assunto': 'Assunto',
            'observacoes': 'Observações'
        }


class TabelaForm(forms.ModelForm):
    class Meta:
        model = TabelaProcessos
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da tabela'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite uma descrição para a tabela'
            })
        }
        labels = {
            'nome': 'Nome da Tabela',
            'descricao': 'Descrição'
        }


class AlterarSenhaPropegForm(forms.Form):
    nova_senha = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a nova senha'
        }),
        min_length=8,
        help_text='A senha deve ter pelo menos 8 caracteres.'
    )
    confirmar_senha = forms.CharField(
        label='Confirmar Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get('nova_senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if nova_senha and confirmar_senha:
            if nova_senha != confirmar_senha:
                raise forms.ValidationError('As senhas não coincidem.')
        
        return cleaned_data