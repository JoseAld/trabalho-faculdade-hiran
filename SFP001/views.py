import json
from datetime import datetime
from django.db.models import Q
from wkhtmltopdf.views import PDFTemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlquote

from IBGE.models import Municipios
from controle.models import Controle
from core.utils.utils import mes_extenso
from core.views.basic_views import PermissaoMixin, BasicListView, BasicCreateView, BasicUpdateView, BasicDeleteView, \
    EntidadeMixin, BasicDetailView
from core.views.viewset import BaseModelViewSet
from entidades.models import Entidade
from recad import settings
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from usuario_entidade.models import UsuarioEntidade
from .forms import CursoFormSet, AfastamentosFormSet, DependenteFormSet, FormSearch, \
    PessoaForm
from .models import SFP001, Curso, sfp017, Dependentes, Fotos
from .serializers import SFP001Serializer, CursoSerializer, Sfp017Serializer, DependenteSerializer, FotoSerializer


# Create your views here.
class ListagemPessoa(LoginRequiredMixin, PermissaoMixin, BasicListView):
    model = SFP001
    template_name = 'pessoa/lista_pessoa.html'
    permission_required = 'SFP001.view_SFP001'
    paginate_by = 10
    queryset = SFP001.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ListagemPessoa, self).get_context_data(**kwargs)
        context['form'] = FormSearch(initial={'search': self.request.GET.get('search')})
        return context

    def get_parametros_get(self):
        self.kwargs = {}
        try:
            nome = self.request.GET.get('search', None)
            tipo = self.request.GET.get('tipo', None)
            if tipo == 'importado':
                self.kwargs['status'] = 'I'
            elif tipo == 'editado':
                self.kwargs['status'] = 'E'
            elif tipo == 'funcionario':
                self.kwargs['status'] = 'U'
            elif tipo == 'finalizado':
                self.kwargs['status'] = 'F'

            if nome:
                self.kwargs['nome__istartswith'] = nome
        except:
            pass

    def get_queryset(self, **kwargs):
        self.get_parametros_get()
        return super().get_queryset().filter(entidade=self.get_entidade(), **self.kwargs)


class RelatorioListaFuncionario(LoginRequiredMixin, PermissaoMixin, BasicListView):
    model = SFP001
    template_name = 'relatorios/lista_funcionarios.html'
    permission_required = 'SFP001.view_SFP001'
    paginate_by = 10
    context_object_name = 'servidores'
    queryset = SFP001.objects.all()

    def get_parametros_get(self):
        self.kwargs = {}
        try:
            nome = self.request.GET.get('nome', None)
            tipo = self.request.GET.get('tipo', None)
            if tipo == 'finalizados':
                self.kwargs['status'] = 'F'
            elif tipo == 'SNC':
                self.kwargs['status'] = ['E', 'I']

            if nome:
                self.kwargs['nome__icontains'] = nome
        except:
            pass

    def get_queryset(self):
        qs = super(RelatorioListaFuncionario, self).get_queryset()

        self.get_parametros_get()
        if "status" in self.kwargs:
            # return super().get_queryset().filter(entidade=self.get_entidade(), status__in=self.kwargs['status'])
            qs = qs.filter(entidade=self.get_entidade(), status__in=self.kwargs['status'])
        else:
            # return super().get_queryset().filter()
            qs = qs.filter(entidade=self.get_entidade(), **self.kwargs)

        data = self.request.GET
        search = data.get('search')

        if search:
            qs = qs.filter(
                Q(nome__icontains=search) |
                Q(matricula__icontains=search)
            )
        return qs


class NovoPessoa(LoginRequiredMixin, PermissaoMixin, BasicCreateView):
    model = SFP001
    form_class = PessoaForm
    template_name = 'pessoa/cadastro_pessoa.html'
    success_url = reverse_lazy('SFP001:listagem_pessoa')
    permission_required = 'SFP001.add_SFP001'

    def get_context_data(self, **kwargs):
        context = super(BasicCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = PessoaForm(self.request.POST, instance=self.object, entidade=self.get_entidade().id)
            context['was_validated'] = "was-validated"
            context['formset'] = CursoFormSet(self.request.POST, instance=self.object)
            context['formsetafast'] = AfastamentosFormSet(self.request.POST, instance=self.object)
            context['formsetdepen'] = DependenteFormSet(self.request.POST, instance=self.object)
        else:
            context['form'] = PessoaForm()
            context['formset'] = CursoFormSet()
            context['formsetafast'] = AfastamentosFormSet()
            context['formsetdepen'] = DependenteFormSet()
        context['cursos'] = []
        entidades_usuario = UsuarioEntidade.objects.filter(usuario=self.request.user).count()
        context['entidades_usuario'] = entidades_usuario
        context['entidade'] = self.get_entidade()
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(BasicCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['entidade'] = self.get_entidade().id

        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao gravar formulário.')
        return super().form_invalid(form)

    def _set_status(self):
        for c in Controle.objects.filter(entidade_id=self.get_entidade(), obrigatorio=True):
                return 'E'
        return 'F'
    def form_valid(self, form):
        if form.is_valid():
            print(form.cleaned_data)
            import base64
            foto_uri = form.data["foto_uri"]
            print(form.data["foto_uri"])


            form.instance.entidade = self.get_entidade()
            form.instance.status = self._set_status()
            self.object = form.save()
            salva_foto_pessoa(foto_uri, self.object, form)
            formset = CursoFormSet(self.request.POST, instance=self.object)
            formsetafast = AfastamentosFormSet(self.request.POST, instance=self.object)
            formsetdepen = DependenteFormSet(self.request.POST, instance=self.object)

            # Qualificação Profissional
            if formset.is_valid():
                for fsa in formset.forms:
                    fsa.instance.pessoa = self.object
                    fsa.instance.entidade = self.get_entidade()
                formset.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))

            # Afastamentos
            if formsetafast.is_valid():
                for fsaf in formsetafast.forms:
                    fsaf.instance.pessoa = self.object
                    fsaf.instance.entidade = self.get_entidade()
                formsetafast.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))

            # Dependentes
            if formsetdepen.is_valid():
                for fsad in formsetdepen.forms:
                    fsad.instance.pessoa = self.object
                    fsad.instance.entidade = self.get_entidade()
                formsetdepen.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))

            form.save()
            messages.success(self.request, str('Formulário salvo com sucesso.'))
            return redirect('SFP001:listagem_pessoa')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ConfirmarPessoa(LoginRequiredMixin, PermissaoMixin, BasicDetailView):
    model = SFP001
    form_class = PessoaForm
    template_name = 'pessoa/confirma_pessoa.html'
    success_url = reverse_lazy('SFP001:listagem_pessoa')
    permission_required = 'SFP001.add_SFP001'

    def _ret_campo(self, campo):
        if campo in 'sexo raca tpsanguineo grinstr estcivil nacionalid regcons':
            return getattr(self.object, f'get_{str(campo).lower()}_display')
        elif campo == 'sistema':
            return getattr(self.object, f'get_{str(campo).lower()}_display')
        else:
            return getattr(self.object, f'{str(campo).lower()}')

    def get_context_data(self, **kwargs):
        context = super(ConfirmarPessoa, self).get_context_data(**kwargs)
        jsn_object = json.loads(self.get_object().registro)
        pessoa = self.object  # Supondo que self.object é a pessoa editada
        registros = []
        base64_string = ""
        if pessoa.fotos.exists():
            foto_obj = pessoa.fotos.first()
            base64_string = foto_obj.foto  # Extract the base64 string from the foto field
        for cnt in Controle.objects.all().order_by('id'):
            if hasattr(self.object, f'{str(cnt.campo).lower()}'):
                vlr = self._ret_campo(cnt.campo)
                vlrold = jsn_object.get(f'{str(cnt.campo).lower()}')
                if vlr != vlrold:
                    reg={}
                    reg['descricao'] = cnt.descricao
                    # Formata a data original (vlrold) antes de adicioná-la ao dicionário
                    if isinstance(vlrold, str) and (
                            vlrold.count('-') == 2 or vlrold.count(':') == 2):  # Verifica formato de data ou hora
                        try:
                            # Attempt to parse with both date and time formats
                            date_obj = datetime.strptime(vlrold, "%Y-%m-%d %H:%M:%S")  # Verifica data com hora
                            if date_obj:
                                # Check if the time component is 00:00:00
                                if date_obj.hour == 0 and date_obj.minute == 0 and date_obj.second == 0:
                                    vlrold_formatted = date_obj.strftime("%d/%m/%Y")  # Remove o componente Tempo 00:00:00
                                else:
                                    vlrold_formatted = date_obj.strftime("%d/%m/%Y %H:%M:%S")
                            else:
                                date_obj = datetime.strptime(vlrold, "%Y-%m-%d")  # # Verifica apenas data
                                if date_obj:
                                    vlrold_formatted = date_obj.strftime("%d/%m/%Y")
                        except ValueError:  # Cuida de possiveis erros
                            vlrold_formatted = vlrold  # Mantem o formato original caso dê erro
                    else:
                        vlrold_formatted = vlrold  # Mantém valores que não sejam data/hora como estão
                    reg['valor'] = vlr
                    reg['valor_anterior'] = vlrold_formatted
                    registros.append(reg)
            vlr = None
            vlrold = None
        context['registro'] = registros
        context['base64_string'] = base64_string
        del jsn_object
        return context



class AtualizarPessoa(LoginRequiredMixin, PermissaoMixin, BasicUpdateView):
    model = SFP001
    form_class = PessoaForm
    template_name = 'pessoa/cadastro_pessoa.html'
    success_url = reverse_lazy('SFP001:listagem_pessoa')
    permission_required = 'SFP001.add_SFP001'

    def get_context_data(self, **kwargs):
        context = super(BasicUpdateView, self).get_context_data(**kwargs)
        pessoa = self.object  # Supondo que self.object é a pessoa editada

        if pessoa.fotos.exists():
            foto_obj = pessoa.fotos.first()
            base64_string = foto_obj.foto  # Extract the base64 string from the foto field
        else:
            base64_string = None  # Handle the case where no photo exists

        if self.request.POST:
            context['was_validated'] = "was-validated"
        context['formset'] = CursoFormSet(instance=self.object)
        entidades = UsuarioEntidade.objects.filter(usuario=self.get_usuario()).values_list('entidade', flat=True)
        context['entidades_usuario'] = Entidade.objects.filter(pk__in=entidades).count()
        context['formsetafast'] = AfastamentosFormSet(instance=self.object)
        context['formsetdepen'] = DependenteFormSet(instance=self.object)
        context['entidade'] = self.get_entidade()
        context['base64_string'] = base64_string
        return context


    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(BasicUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['entidade'] = self.get_entidade().id
        if self.object.status is None or self.object.status == 'I':
            self.object.status = 'E'
            self.object.save()
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar formulário.')
        return super().form_invalid(form)

    def _set_status(self):
        for c in Controle.objects.filter(entidade_id=self.get_entidade(), obrigatorio=True):
            if getattr(self.object, '{}'.format(c.campo).lower()) is None:
                return 'E'
        return 'F'

    def form_valid(self, form,):
        if form.is_valid():
            import base64
            foto_uri = form.data["foto_uri"]
            salva_foto_pessoa(foto_uri, self.object, form)
            print(form.data["foto_uri"])



            form.instance.entidade = self.get_entidade()
            form.instance.status = self._set_status()
            self.object = form.save(commit=False)
            formset = CursoFormSet(self.request.POST, instance=self.object)
            formsetafast = AfastamentosFormSet(self.request.POST, instance=self.object)
            formsetdepen = DependenteFormSet(self.request.POST, instance=self.object)

            # Qualificação Profissional
            if formset.is_valid():
                for fsa in formset.forms:
                    fsa.instance.pessoa = self.object
                    fsa.instance.entidade = self.get_entidade()
                formset.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))

            # Afastamentos
            if formsetafast.is_valid():
                for fsaf in formsetafast.forms:
                    fsaf.instance.pessoa = self.object
                    fsaf.instance.entidade = self.get_entidade()
                formsetafast.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))

            # Dependentes
            if formsetdepen.is_valid():
                for fsad in formsetdepen.forms:
                    fsad.instance.pessoa = self.object
                    # fsad.instance.entidade = self.get_entidade()
                formsetdepen.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))

            pessoa = form.save()
            messages.info(self.request, str('Formulário editado com sucesso.'))
            return redirect('SFP001:listagem_pessoa')
        else:
            return self.render_to_response(self.get_context_data(form=form))


    #mudar depois para base64
def salva_foto_pessoa(datauri, pessoa, form):
    import base64

    image_webcam = datauri
    foto = None
    if image_webcam:
        from urllib import request
        with request.urlopen(image_webcam) as response:
            data = response.read()
        foto = base64.b64encode(data).decode('utf-8')
    elif form.files.get('foto'):  # Verificar se a foto foi enviada no formulário
        foto_file = form.files['foto']  # Obter o arquivo da foto
        foto_data = foto_file.read()  # Ler o conteúdo do arquivo
        foto = base64.b64encode(foto_data).decode('utf-8')  # Converter para base64

    if foto:
        # Cria um novo objeto Fotos
        nova_foto = Fotos(pessoa=pessoa, foto=foto)
        nova_foto.save()



class DeletePessoa(LoginRequiredMixin, PermissaoMixin, BasicDeleteView):
    model = SFP001
    success_url = reverse_lazy('SFP001:listagem_pessoa')
    permission_required = 'SFP001.delete_SFP001'

    def dispatch(self, request, *args, **kwargs):
        pessoa = self.get_object()
        pessoa.delete()
        return HttpResponseRedirect(reverse_lazy("SFP001:listagem_pessoa"))


class ImprimirRelatorioPDF(LoginRequiredMixin, PermissaoMixin, EntidadeMixin, PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'pessoa/imprimir_pessoa.html'
    permission_required = 'SFP001.delete_SFP001'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entidade = self.get_entidade()
        servidores = SFP001.objects.filter(entidade=entidade)
        dados = self.request.GET
        tipoRelatorio = dados.get("radioTipoRelatorio", None)
        servidores_get = dados.get("servidores", None)
        if tipoRelatorio == '1':
            self.template_name = 'pessoa/imprimir_pessoa.html'
            titulo = "RECADASTRAMENTO SERVIDOR PÚBLICO MUNICIPAL"
            self.filename = 'Relatorio - Ficha Pessoal.pdf'
        elif tipoRelatorio == '2':
            self.template_name = 'relatorios/imprimir_relatoriolistafuncionario.html'
            titulo = "LISTAGEM DE FUNCIONÁRIOS"
            self.filename = 'Relatorio - Listagem de Funcionarios.pdf'
        elif tipoRelatorio == '3':
            self.template_name = 'relatorios/imprimir_relatoriolistaservidores.html'
            titulo = "LISTAGEM DE SERVIDORES"
            self.filename = 'Relatorio - Listagem de Servidores.pdf'
        elif tipoRelatorio == '4':
            self.template_name = 'relatorios/imprimir_ficharecadastramento.html'
            titulo = "DADOS DO RECADASTRAMENTO"
            self.filename = 'Relatorio de Recadastramento Detalhado.pdf'
        if servidores_get and servidores_get != 'all':
            servidores_get = servidores_get.replace('[', '').replace(']', '').replace('"', '')
            servidores_id = servidores_get.split(',')
            servidores = servidores.filter(id__in=servidores_id)
        context['servidores'] = servidores
        context['entidade'] = entidade
        context['titulo'] = titulo
        context['ano'] = datetime.today().year
        context['mes'] = datetime.today().month
        context['dia'] = datetime.today().day
        self.show_content_in_browser = True
        context['link_static'] = settings.LINK_STATIC
        context['url'] = settings.LINK_URL

        return context


class ImprimirDeclaracaoPDF(LoginRequiredMixin, PermissaoMixin, EntidadeMixin, PDFTemplateView):
    filename = 'my_declaracao_pdf.pdf'
    template_name = 'pessoa/imprimir_pessoa.html'
    permission_required = 'SFP001.view_SFP001'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entidade = self.get_entidade()
        servidores = SFP001.objects.filter(entidade=entidade)
        dados = self.request.GET
        tipoDeclaracao = dados.get("selectTipoDeclaracao", None)
        servidores_get = dados.get("servidores", None)
        if tipoDeclaracao == '1':
            self.template_name = 'declaracoes/imprimir_declaracaoacumulocargos.html'
            titulo = "DECLARAÇÃO DE ACUMULAÇÃO DE CARGOS"
            self.filename = 'Declaracao de acumulcao de cargos.pdf'
        elif tipoDeclaracao == '2':
            self.template_name = 'declaracoes/imprimir_declaracaonaoacumuladodecargo.html'
            titulo = "DECLARAÇÃO DE NÃO ACUMULAÇÃO DE CARGOS"
            self.filename = 'Declaracao de nao acumulcao de cargos.pdf'
        elif tipoDeclaracao == '3':
            self.template_name = 'declaracoes/imprimir_declaracaoestadocivil.html'
            titulo = "DECLARAÇÃO DE VIDA, ESTADO CIVIL E RESIDÊNCIA"
            self.filename = 'Declaracao de vida, estado civil e residencia.pdf'
        elif tipoDeclaracao == '4':
            self.template_name = 'declaracoes/imprimir_declaracaodocumentocontratacao.html'
            titulo = "PROTOCOLO DE RECEBIMENTO DE DOCUMENTO"
            self.filename = 'Declaracao de documentos de contrataçao.pdf'
        elif tipoDeclaracao == '5':
            self.template_name = 'declaracoes/imprimir_declaracaouniaoestavel.html'
            titulo = 'DECLARAÇÃO DE ESTADO CIVIL E UNIÃO ESTÁVEL'
            self.filename = 'Declaracao de estado civil e uniao estavel.pdf'
        elif tipoDeclaracao == '6':
            self.template_name = 'declaracoes/imprimir_declaracaopossuobens.html'
            titulo = 'DECLARAÇÃO DE BENS'
            self.filename = 'Declaracao de bens.pdf'
        elif tipoDeclaracao == '7':
            self.template_name = 'declaracoes/imprimir_declaracaonaopossuobens.html'
            titulo = 'DECLARAÇÃO NEGATIVA DE BENS'
            self.filename = 'Declaracao negativa de bens.pdf'
        elif tipoDeclaracao == '8':
            self.template_name = 'declaracoes/imprimir_declaracaoparentesco.html'
            titulo = 'DECLARAÇÃO DE PARENTESCO'
            self.filename = 'Declaracao de parentesco.pdf'
        if servidores_get and servidores_get != 'all':
            servidores_get = servidores_get.replace('[', '').replace(']', '').replace('"', '')
            servidores_id = servidores_get.split(',')
            servidores = servidores.filter(id__in=servidores_id)
        context['servidores'] = servidores
        today = datetime.today()
        dia = today.day
        mes = mes_extenso(today.month)
        ano = today.year
        datahoje = f'{dia} de {mes} de {ano}'

        context['datadehoje'] = datahoje
        context['entidade'] = entidade
        context['titulo'] = titulo
        self.show_content_in_browser = True
        context['link_static'] = settings.LINK_STATIC
        context['url'] = settings.LINK_URL

        return context


class SFP001ViewSet(BaseModelViewSet):
    queryset = SFP001.objects.all()
    serializer_class = SFP001Serializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('entidade', 'sistema', 'cdsecreta', 'cdsetor', 'matricula')
    search_fields = ('nome', 'matricula', )


class FotoViewSet(BaseModelViewSet):
    queryset = Fotos.objects.all()
    serializer_class = FotoSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('pessoa', 'pessoa__matricula',)
    search_fields = ('pessoa__matricula', )


class CursoViewSet(BaseModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('entidade', 'matricula')
    search_fields = ('nomecurso', 'matricula', )


class Sfp017ViewSet(BaseModelViewSet):
    queryset = sfp017.objects.all()
    serializer_class = Sfp017Serializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('entidade', 'matricula')
    search_fields = ('matricula', )


class DependenteViewSet(BaseModelViewSet):
    queryset = Dependentes.objects.all()
    serializer_class = DependenteSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('entidade', 'matricula')
    search_fields = ('matricula', 'nomedep', )
