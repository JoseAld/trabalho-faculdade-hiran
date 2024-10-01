from django import forms

from entidades.models import Entidade
from .models import UsuarioEntidade


class UsuarioEntidadeForm(forms.ModelForm):
    class Meta:
        model = UsuarioEntidade
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.entidade = kwargs.pop('entidades')
        self.usuario = kwargs.pop('usuario')
        super(UsuarioEntidadeForm, self).__init__(*args, **kwargs)

    def clean(self):
        setor = self.cleaned_data['cdsetor']

        if UsuarioEntidade.objects.filter(usuario=self.usuario, entidade=self.entidade, cdsetor=setor):
            raise forms.ValidationError('Usuário já cadastrado no setor!')
