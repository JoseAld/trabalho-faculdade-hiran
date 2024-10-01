from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from CFG_VINC.models import CFG_VINC
from IBGE.models import Municipios, Uf
from SFP005.models import SFP005
from SFP006.models import SFP006
from core.utils.utils import base64_to_image
from entidades.models import Entidade
from .models import SFP001, sfp017, Dependentes, Fotos
from .models import Curso
from controle.models import Controle
from datetime import datetime


class PessoaForm(forms.ModelForm):
    foto_uri = forms.CharField(label='foto_uri', required=False)
    foto = forms.ImageField(label='foto', required=False)

    class Meta:
        model = SFP001
        fields = ['entidade', 'matricula', 'matricfun', 'nome', 'sistema', 'hortrab', 'funcao',
                  'funcao2', 'cargo_acumulo', 'cdsecreta', 'cdsetor', 'cpf', 'certmilit', 'numcons', 'nomepai',
                  'nomemae',
                  'nacionalid', 'naturaliza', 'estcivil', 'sexo', 'raca', 'tpsanguineo', 'dtnasc', 'dtadmissao',
                  'dtadmissao2', 'obs', 'grinstr', 'cep',
                  'cidade', 'uf', 'tplogradouro',
                  'endereco', 'endnum', 'ufnasc', 'cidnasc', 'bairro',
                  'identidade', 'orgaoident', 'ufident', 'dtident', 'titeleitor', 'zona', 'secao', 'banco', 'agencia',
                  'dvagencia', 'tipoconta', 'conta', 'dvconta', 'fone', 'fone2', 'email', 'dtconcurso', 'classific',
                  'dtconcurs2', 'classific2', 'dtposse', 'contrato', 'dtopcao', 'horbase', 'cnh', 'cnhcat', 'dtcnh',
                  'cnhorgao', 'cnhdtexp',
                  'ufcnh', 'dtprimcnh',
                  'numcartprof', 'seriecartprof', 'ufcartprof', 'pispasep', 'dtpispasep', 'ncertcasamento',
                  'sus_numcart', 'sus_dtemissao', 'categoria_situacao',
                  'ncertnascimento', 'naverbdivorcio', 'jacotribregime', 'dataregimeprev', 'lotacao_acumulo',
                  'data_ingresso_acumulo', 'jornada_acumulo', 'carga_horaria_acumulo', 'esfera_acumulo',
                  'regime_juridico_acumulo', 'defic_vis', 'defic_ment', 'defic_fis', 'defic_aud', 'defic_intlec',
                  'cota_def_hab_reab', 'reabilitado', 'tipo_defic_fis', 'tipo_defic_vis', 'tipo_defic_ment',
                  'dtlaudodeficiente', 'efetivo_fuc_gratif', 'efetivo_sec_municp', 'efetivo_org_inst',
                  'efetivo_lic_venc', 'nomeados_estg_prob', 'dt_efetivo_vencimento', 'dt_efetivo_venci_fim',
                  'dt_nomeados_prob_fim', 'dt_nomeados_probatorio', 'regcons', 'tp_cat_siop', 'cat_siop',
                  'cdsecretaorigem',
                  'cdsetororigem', 'qualifcadastral', 'parentesco_instpensao', 'inativacao_sagres_pe',
                  'siap_mot_cont_temp',
                  'siap_tipo_cont_temp', 'siap_veic_publicacao', 'siap_motivo_contratacao', 'estrangeiro', 'paisorigem',
                  'cartbrasil', 'dtbrasil', 'casadocombr', 'filhocombr', 'estado_estrangeiro', 'cidade_estrangeiro',
                  'rnenum', 'rneorgao', 'rnedataemi', 'dtchegadaestran', 'tmpresidestrang', 'condingestrang',
                  ]
        widgets = {
            'entidade': forms.HiddenInput(),
            'foto': forms.FileInput(attrs={'class': 'img-fluid', 'alt': 'Imagem responsiva'}),
            'matricula': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'matricfun': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'nome': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'sistema': forms.Select(attrs={'data-toggle': 'select2',
                                           'class': 'form-control'}),
            'hortrab': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'funcao': forms.Select(attrs={'data-toggle': 'select2',
                                          'class': 'form-control'}),
            'funcao2': forms.Select(attrs={'data-toggle': 'select2',
                                           'class': 'form-control'}),
            'cargo_acumulo': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'lotacao_acumulo': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'data_ingresso_acumulo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'jornada_acumulo': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'carga_horaria_acumulo': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            'esfera_acumulo': forms.Select(attrs={'data-toggle': 'select2',
                                                  'class': 'form-control select2-multiple formulario_input'}),
            'regime_juridico_acumulo': forms.Select(attrs={'data-toggle': 'select2',
                                                           'class': 'form-control select2-multiple formulario_input'}),
            'cdsecreta': forms.Select(attrs={'data-toggle': 'select2',
                                             'class': 'form-control select2 formulario_input'}),
            'cdsetor': forms.Select(attrs={'data-toggle': 'select2',
                                           'class': 'form-control select2 formulario_input'}),
            'cdsecretaorigem': forms.Select(attrs={'data-toggle': 'select2',
                                                   'class': 'form-control select2 formulario_input'}),
            'cdsetororigem': forms.Select(attrs={'data-toggle': 'select2',
                                                 'class': 'form-control select2 formulario_input'}),
            'nomepai': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'nomemae': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dtnasc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cidnasc': forms.Select(attrs={'data-toggle': 'select2',
                                           'class': 'form-control'}),
            'ufnasc': forms.Select(attrs={'data-toggle': 'select2',
                                          'class': 'form-control'}),
            'endereco': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'endnum': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.Select(attrs={'data-toggle': 'select2',
                                          'class': 'form-control'}),
            'bairro': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'uf': forms.Select(attrs={'data-toggle': 'select2',
                                      'class': 'form-control'}),
            'fone': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'data-toggle': 'select2',
                                        'class': 'form-control'}),
            'tpsanguineo': forms.Select(attrs={'data-toggle': 'select2',
                                               'class': 'form-control'}),
            'raca': forms.Select(attrs={'data-toggle': 'select2',
                                        'class': 'form-control select2-multiple'}),
            'grinstr': forms.Select(attrs={'data-toggle': 'select2',
                                           'class': 'form-control'}),
            'estcivil': forms.Select(attrs={'data-toggle': 'select2',
                                            'class': 'form-control'}),
            'dtadmissao': forms.DateInput(attrs={'class': 'form-control ', 'type': 'date'}),
            'dtadmissao2': forms.DateInput(attrs={'class': 'form-control ', 'type': 'date'}),
            'dtopcao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'identidade': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'orgaoident': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'ufident': forms.Select(attrs={'data-toggle': 'select2',
                                           'class': 'form-control'}),
            'dtident': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'cpf-mask': "000.000.000-00"}),
            'ctps_digital': forms.Select(attrs={'data-toggle': 'select2', 'class': 'form-control'}),
            'numcartprof': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'seriecartprof': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'ufcartprof': forms.Select(attrs={'data-toggle': 'select2',
                                              'class': 'form-control',
                                              'data-mask': "DD/MM/YYYY"}),
            'pispasep': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'titeleitor': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'zona': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'secao': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'cnh': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'cnhcat': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dtcnh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cnhorgao': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'cnhdtexp': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ufcnh': forms.Select(attrs={'data-toggle': 'select2',
                                         'class': 'form-control'}),
            'dtprimcnh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ncertcasamento': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'ncertnascimento': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'naverbdivorcio': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'jacotribregime': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'dataregimeprev': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sus_numcart': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'sus_dtemissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'banco': forms.Select(attrs={'data-toggle': 'select2',
                                         'class': 'form-control'}),
            'agencia': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dvagencia': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'tipoconta': forms.Select(attrs={'data-toggle': 'select2',
                                             'class': 'form-control'}),
            'conta': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dvconta': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'horbase': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),

            'obs': forms.Textarea(attrs={'class': 'form-control formulario_input', 'rows': '5'}),
            'nacionalid': forms.Select(attrs={'data-toggle': 'select2',
                                              'class': 'form-control'}),
            'naturaliza': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dtconcurso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'classific': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dtconcurs2': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'classific2': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dtposse': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contrato': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),

            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),

            'fone2': forms.TextInput(attrs={'class': 'form-control'}),

            'certmilit': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),

            'dtpispasep': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'regcons': forms.Select(attrs={'data-toggle': 'select2',
                                           'class': 'form-control'}),
            'numcons': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),

            'efetivo_fuc_gratif': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'efetivo_sec_municp': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'efetivo_org_inst': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'efetivo_lic_venc': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'nomeados_estg_prob': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'dt_efetivo_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dt_efetivo_venci_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dt_nomeados_probatorio': forms.DateInput(attrs={'class': 'form-control ', 'type': 'date'}),
            'dt_nomeados_prob_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'defic_fis': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'defic_vis': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'defic_ment': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'defic_aud': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'defic_intlec': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'cota_def_hab_reab': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'reabilitado': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'tipo_defic_fis': forms.Select(attrs={'data-toggle': 'select2',
                                                  'class': 'form-control'}),
            'tipo_defic_vis': forms.Select(attrs={'data-toggle': 'select2',
                                                  'class': 'form-control'}),
            'tipo_defic_ment': forms.Select(attrs={'data-toggle': 'select2',
                                                   'class': 'form-control'}),

            'cat_siop': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'tp_cat_siop': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'categoria_situacao': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),

            'inativacao_sagres_pe': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'parentesco_instpensao': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dtlaudodeficiente': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tplogradouro': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),

            'siap_mot_cont_temp': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'siap_tipo_cont_temp': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'siap_veic_publicacao': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'siap_motivo_contratacao': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'estrangeiro': forms.Select(attrs={'data-toggle': 'select2',
                                        'class': 'form-control'}),
            'paisorigem': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'cartbrasil': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dtbrasil': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'casadocombr': forms.Select(attrs={'data-toggle': 'select2',
                                        'class': 'form-control'}),
            'filhocombr': forms.Select(attrs={'data-toggle': 'select2',
                                        'class': 'form-control'}),
            'estado_estrangeiro': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'cidade_estrangeiro': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'rnenum': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'rneorgao': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'rnedataemi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dtchegadaestran': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tmpresidestrang': forms.Select(attrs={'data-toggle': 'select2',
                                               'class': 'form-control'}),
            'condingestrang': forms.Select(attrs={'data-toggle': 'select2',
                                                   'class': 'form-control'}),



        }

    def __init__(self, *args, **kwargs):
        self.entidade = None
        if kwargs.get('entidade', None):
            self.entidade = kwargs.pop('entidade')
        super(PessoaForm, self).__init__(*args, **kwargs)

        if self.data:
            entidade = Entidade.objects.get(pk=self.entidade)
            self.fields['cidade'].queryset = Municipios.objects.filter(uf__uf=entidade.estado)
            self.fields['cidnasc'].queryset = Municipios.objects.filter(uf__uf=entidade.estado)
            self.fields['cdsecreta'].queryset = SFP006.objects.filter(entidade__id=self.entidade)
            self.fields['cdsetor'].queryset = SFP006.objects.filter(entidade__id=self.entidade)
            self.fields['sistema'].queryset = CFG_VINC.objects.filter(entidade__id=self.entidade)
            self.fields['funcao'].queryset = SFP005.objects.filter(entidade__id=self.entidade)
            self.fields['funcao2'].queryset = SFP005.objects.filter(entidade__id=self.entidade)
            self.fields['cdsecretaorigem'].queryset = SFP006.objects.filter(entidade__id=self.entidade)
            self.fields['cdsetororigem'].queryset = SFP006.objects.filter(entidade__id=self.entidade)
        else:
            cidade = "" if self.instance.uf == None else self.instance.uf
            cidnasc = "" if self.instance.ufnasc == None else self.instance.ufnasc
            cdsecreta = -1 if self.instance.cdsecreta == None else self.instance.cdsecreta.pk
            cdsetor = -1 if self.instance.cdsetor == None else self.instance.cdsetor.pk
            sistema = -1 if self.instance.sistema == None else self.instance.sistema.pk
            funcao = -1 if self.instance.funcao == None else self.instance.funcao.pk
            funcao2 = -1 if self.instance.funcao2 == None else self.instance.funcao2.pk
            cdsecretaorigem = -1 if self.instance.cdsecretaorigem == None else self.instance.cdsecretaorigem.pk
            cdsetororigem = -1 if self.instance.cdsetororigem == None else self.instance.cdsetororigem.pk

            #self.fields['cidade'].queryset = Municipios.objects.filter(uf=cidade)
            #self.fields['cidnasc'].queryset = Municipios.objects.filter(uf=cidnasc)
            self.fields['cdsecreta'].queryset = SFP006.objects.filter(pk=cdsecreta)
            self.fields['cdsetor'].queryset = SFP006.objects.filter(pk=cdsetor)
            self.fields['sistema'].queryset = CFG_VINC.objects.filter(pk=sistema)
            self.fields['funcao'].queryset = SFP005.objects.filter(pk=funcao)
            self.fields['funcao2'].queryset = SFP005.objects.filter(pk=funcao2)
            self.fields['cdsecretaorigem'].queryset = SFP006.objects.filter(pk=cdsecretaorigem)
            self.fields['cdsetororigem'].queryset = SFP006.objects.filter(pk=cdsetororigem)

            if self.instance.pk:
                for ft in Fotos.objects.filter(pessoa_id=self.instance.pk):
                    self.fields['foto'].widget.attrs['base64_string'] = base64_to_image

    def clean(self):
        dados = self.cleaned_data
        dados = super(PessoaForm, self).clean()
        cdsecreta = self.cleaned_data['cdsecreta']
        cdsecretaorigem = self.cleaned_data['cdsecretaorigem']
        cdsetor = self.cleaned_data['cdsetor']
        foto = self.cleaned_data['foto']
        cdsetororigem = self.cleaned_data['cdsetororigem']
        cidnasc = self.cleaned_data.get('cidnasc')
        cidade = self.cleaned_data.get('cidade')

        erros = []

        # if not cdsecreta:  # Verifica se 'cdsecreta' não está presente
        #     erros.append(ValidationError({'cdsecreta': "Campo de preenchimento obrigatório."}))
        #     self.add_error('cdsecreta', 'Campo de preenchimento obrigatório.')
        #     self.fields['cdsecreta'].widget.attrs['class'] += ' parsley-error'
        #
        # if not cdsecretaorigem:  # Verifica se 'cdsecretaorigem' não está presente
        #     erros.append(ValidationError({'cdsecretaorigem': "Campo de preenchimento obrigatório."}))
        #     self.add_error('cdsecretaorigem', 'Campo de preenchimento obrigatório.')
        #     self.fields['cdsecretaorigem'].widget.attrs['class'] += ' parsley-error'
        #
        # if not cdsetor:  # Verifica se 'cdsetor' não está presente
        #     erros.append(ValidationError({'cdsetor': "Campo de preenchimento obrigatório."}))
        #     self.add_error('cdsetor', 'Campo de preenchimento obrigatório.')
        #     self.fields['cdsetor'].widget.attrs['class'] += ' parsley-error'
        #
        # if not cdsetor:  # Verifica se 'cdsetororigem' não está presente
        #     erros.append(ValidationError({'cdsetororigem': "Campo de preenchimento obrigatório."}))
        #     self.add_error('cdsetororigem', 'Campo de preenchimento obrigatório.')
        #     self.fields['cdsetororigem'].widget.attrs['class'] += ' parsley-error'

        print(foto)
        for c in Controle.objects.filter(entidade_id=self.entidade, obrigatorio=True):
            try:
                if dados[f'{c.campo.lower()}'] is None:
                    erros.append(ValidationError( {f'{c.campo.lower()}': "Campo de preenchimento obrigatório."}))


                    self.add_error('{}'.format(c.campo).lower(), 'Campo de preenchimento obrigatório.')
                    self.fields[f'{c.campo.lower()}'].widget.attrs['class'] += ' parsley-error'
            except:
                pass


            # if cdsecreta != cdsecretaorigem:
            #     erros.append(ValidationError(
            #         "A Secretaria escolhida não possui relação com a Secretaria de Origem ou não existe, por favor tente novamente!"))
            # if cdsetor and cdsetor.cdsecreta != cdsetororigem.cdsecreta:
            #     erros.append(ValidationError(
            #         "O Setor escolhido não possui relação com o Setor de Origem ou não existe, por favor tente novamente!"))
        print(foto)
        return dados


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = [
            'nivel', 'nomecurso', 'instituicao', 'dtiniciocurso', 'dtfimcurso', 'carghora', 'anobase', 'anobase',
            'obscurso',
        ]
        widgets = {
            'anobase': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'nivel': forms.Select(
                attrs={'data-toggle': 'select2', 'class': 'form-control select2 formulario_input', }),
            'nomecurso': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'instituicao': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'carghora': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'dtiniciocurso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dtfimcurso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'obscurso': forms.Textarea(attrs={'class': 'form-control formulario_input', 'rows': '2',
                                              'style': 'text-transform:uppercase;'}),
        }


CursoFormSet = inlineformset_factory(SFP001, Curso, form=CursoForm, fk_name='matricula', extra=1, can_delete=True)


class AfastamentosForm(forms.ModelForm):
    class Meta:
        model = sfp017
        fields = [
            'anobase', 'codfol', 'dtinicioafst', 'dtfimafst', 'obsafst',
        ]
        widgets = {
            'anobase': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'codfol': forms.Select(
                attrs={'data-toggle': 'select2', 'class': 'form-control select2 formulario_input'}),
            'dtinicioafst': forms.DateInput(attrs={'class': 'form-control ', 'type': 'date'}),
            'dtfimafst': forms.DateInput(attrs={'class': 'form-control ', 'type': 'date'}),
            'obsafst': forms.Textarea(attrs={'class': 'form-control formulario_input', 'rows': '2',
                                             'style': 'text-transform:uppercase;'}),
        }

    def __init__(self, *args, **kwargs):
        super(AfastamentosForm, self).__init__(*args, **kwargs)


AfastamentosFormSet = inlineformset_factory(SFP001, sfp017, form=AfastamentosForm, fk_name='matricula', extra=1,
                                            can_delete=True)


class DependentesForm(forms.ModelForm):
    class Meta:
        model = Dependentes
        fields = [
            'id', 'nomedep', 'cpf_dependente', 'sexo', 'dependsocial', 'nascdep', 'parent', 'identdepend',
            'sus_numcartdep',
            'sus_dtemissaodep', 'depir', 'depsf', 'incap_fisica'
        ]
        widgets = {
            'nomedep': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'cpf_dependente': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'dependsocial': forms.Select(
                attrs={'data-toggle': 'select2', 'class': 'form-control select2-multiple'}),
            'sexo': forms.Select(
                attrs={'data-toggle': 'select2', 'class': 'form-control select2-multiple'}),
            'nascdep': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'parent': forms.Select(
                attrs={'data-toggle': 'select2', 'class': 'form-control select2-multiple'}),
            'identdepend': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'sus_numcartdep': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'sus_dtemissaodep': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'depir': forms.CheckboxInput(attrs={'class': 'checkbox checkbox-success checkbox-circle'}),
            'depsf': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
            'incap_fisica': forms.CheckboxInput(attrs={'class': 'col-form-label'}),
        }


DependenteFormSet = inlineformset_factory(SFP001, Dependentes, form=DependentesForm, fk_name='matricula', extra=1, can_delete=True)

class FormSearch(forms.Form):
    search = forms.CharField(max_length=60, required=False ,widget=forms.TextInput(attrs={'class': 'form-control search-input',
                                                                    'type': 'search', 'placeholder': 'Localizar aqui...',
                                                                    'autocomplete': 'off'}))