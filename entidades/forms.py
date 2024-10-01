from django import forms

from core.utils.utils import validar_cnpj, validar_cep
from .models import Entidade


class EntidadeForm(forms.ModelForm):
    class Meta:
        model = Entidade
        fields = ['codigo_entidade', 'cnpj', 'razao', 'fone', 'fax', 'email', 'cep', 'logradouro', 'log_numero',
                  'complemento', 'complemento', 'bairro', 'estado', 'cidade', 'brasao']
        widgets = {
            'codigo_entidade': forms.TextInput(
                attrs={'class': 'form-control formulario_input', 'maxlength': '6', 'minlength': '6'}),
            'cnpj': forms.TextInput(
                attrs={'class': 'form-control formulario_input',}),
            'razao': forms.TextInput(attrs={'class': 'form-control formulario_input'}),
            'fone': forms.TextInput(attrs={'class': 'form-control formulario_input',}),
            'fax': forms.TextInput(attrs={'class': 'form-control formulario_input', }),
            'email': forms.EmailInput(attrs={'class': 'form-control formulario_input', 'type': 'email'}),
            'cep': forms.TextInput(attrs={'class': 'form-control formulario_input',}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control formulario_input'}),
            'log_numero': forms.TextInput(attrs={'class': 'form-control formulario_input'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control formulario_input'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control formulario_input'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control formulario_input'}),
            'estado': forms.TextInput(attrs={'class': 'form-control formulario_input'}),
            'brasao': forms.FileInput(attrs={'class': 'dropify', 'data-max-file-size': '1M'}),
        }


    def clean_cnpj(self):

        cnpj = self.cleaned_data['cnpj']
        if cnpj:
            try:
                cli = Entidade.objects.get(cnpj=cnpj)
                if cli.id != self.instance.id:
                    self.add_error('cnpj', 'Esté CNPJ já está informado.')
            except Entidade.DoesNotExist:
                pass
            if validar_cnpj(cnpj) == False:
                self.add_error('cnpj', 'CNPJ %s inválido.' % cnpj)
        return cnpj
