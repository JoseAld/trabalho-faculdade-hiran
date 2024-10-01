from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Entre com o seu e-mail',}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Entre com sua senha'}))

    error_messages = {
        'invalid_login': (
            "Usuário ou senha incorretos."
        ),
        'inactive': ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(request=None, *args, **kwargs)
        self.fields['username'].required = False

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            usuario = Usuario.objects.get(email=email)
        except:
            usuario = None
            raise self.get_invalid_login_error()

        if usuario is not None and password:
            self.user_cache = authenticate(self.request, username=usuario.username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
            'groups': forms.SelectMultiple(attrs={'data-toggle': 'select2',
                                                  'class': 'form-control select2-multiple',
                                                  'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
        }

    """ Função para associar um usuario ao setor da entidade """
    # def __init__(self, *args, **kwargs):
    #     self.entidade = None
    #     if kwargs.get('entidade', None):
    #         self.entidade = kwargs.pop('entidade')
    #     super(UsuarioForm, self).__init__(*args, **kwargs)
    #     self.fields['cdsetor'] = ModelChoiceField(queryset=SFP006.objects.all(), empty_label="", widget=forms.SelectMultiple(attrs={'data-toggle': 'select2',
    #                                               'class': 'form-control select2-multiple form-control-sm',
    #                                               'required': True}))

    def clean(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']

        if not self.instance.id:
            if Usuario.objects.filter(email=email).exists():
                raise forms.ValidationError("E-mail já cadastrado")
            if Usuario.objects.filter(username=username).exists():
                raise forms.ValidationError("Usuário já cadastrado")
        else:
            if Usuario.objects.filter(email=email).exclude(pk=self.instance.id).exists():
                raise forms.ValidationError("E-mail já cadastrado")
            if Usuario.objects.filter(username=username).exclude(pk=self.instance.id).exists():
                raise forms.ValidationError("Usuário já cadastrado")
