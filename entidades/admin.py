import os
import re
from datetime import datetime
from threading import Thread
from zipfile import ZipFile
from django.contrib import admin
import json
from django.core.checks import messages
from django.apps import apps
from django.http import HttpResponse
from CFG_VINC.models import CFG_VINC
from SFP001.models import Curso, SFP001, Dependentes, sfp017
from SFP005.models import SFP005, SFPDXX25
from SFP006.models import SFP006
from SFPD9924.models import SFPD9924
from controle.models import Controle
from recad.settings import BASE_DIR
from .models import Entidade
from django.db import transaction
from recad.settings import MEDIA_ROOT


class ThreadImportacao(Thread):

    def __init__(self, entidade):
        Thread.__init__(self)
        self.entidade = entidade

    def run(self):

        caminho_arqv = BASE_DIR + self.entidade.arqv_importacao.url
        print(caminho_arqv)

        # inicia o save point
        # sid = transaction.savepoint()
        regex = r'[0-9]+'
        numeros = re.findall(regex, caminho_arqv)

        cnpjPontuado = numeros[0]
        print(cnpjPontuado)
        # try:
        entidade = Entidade.objects.get(cnpj=cnpjPontuado)
        # except Exception as e:
        #     print(e)

        with ZipFile(caminho_arqv, 'r') as zip_ref:
            if not os.path.exists(MEDIA_ROOT + "/" + cnpjPontuado):
                os.makedirs(MEDIA_ROOT + "/" + cnpjPontuado)
            zip_ref.extractall(MEDIA_ROOT + "/" + cnpjPontuado)

        if os.path.isfile(MEDIA_ROOT + "/" + cnpjPontuado + '/funcao.json'):
            print(
                "\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\nImportando Funcoes\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-")
            dadosFuncoes = json.load(open(MEDIA_ROOT + "/" + cnpjPontuado + '/funcao.json'))
            for funcao in dadosFuncoes['funcao']:
                funcaoFiltrada = {}
                funcaoFiltrada['entidade'] = entidade
                for item in funcao.items():
                    if item[0] in 'codigo cargo2':
                        if item[1] != "" and item[1] is not None and item[1] != "          " and item[1] != " ":
                            funcaoFiltrada[item[0]] = item[1]
                try:
                    criou, obj = SFPDXX25.objects.update_or_create(codigo=funcaoFiltrada['codigo'],
                                                                   entidade=funcaoFiltrada['entidade'],
                                                                   defaults=funcaoFiltrada)
                except Exception as e:
                    print("\nERRO NA IMPORTAÇÃO DE FUNÇÕES: \n"+ str(e))
            try:
                os.remove(MEDIA_ROOT + "/" + cnpjPontuado + '/funcao.json')
                print('\nFunções importadas!')
            except:
                pass

        if os.path.isfile(MEDIA_ROOT + "/" + cnpjPontuado + '/cargos.json'):
            print(
                "\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\nImportando Cargos\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-")
            dadosCargos = json.load(open(MEDIA_ROOT + "/" + cnpjPontuado + '/cargos.json'))
            for cargo in dadosCargos['cargos']:
                cargosfiltrado = {}
                for item in cargo.items():
                    if item[0] in 'codigo cargo':
                        if item[1] != "" and item[1] is not None and item[1] != "          " and item[1] != " ":
                            cargosfiltrado[item[0]] = item[1]
                cargosfiltrado['entidade'] = entidade

                try:
                    SFP005.objects.update_or_create(codigo=str("0" + cargosfiltrado['codigo']),
                                                    entidade=cargosfiltrado['entidade'],
                                                    defaults=cargosfiltrado)
                except Exception as e:
                    print("\nERRO NA IMPORTAÇÃO DE CARGOS: \n"+ str(e))
            try:
                os.remove(MEDIA_ROOT + "/" + cnpjPontuado + '/cargos.json')
                print('\nCargos importados!')
            except:
                pass


        if os.path.isfile(MEDIA_ROOT + "/" + cnpjPontuado + '/lotacoes.json'):
            print(
                "\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\nImportando Lotações\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-")
            dadosLotacao = json.load(open(MEDIA_ROOT + "/" + cnpjPontuado + '/lotacoes.json'))
            for lotacao in dadosLotacao['lotacoes']:
                lotacaofiltrado = {}
                for item in lotacao.items():
                    if item[0] in 'cdsecreta cdsetor cddepart descricao':
                        if item[1] != "" and item[1] is not None:
                            lotacaofiltrado[item[0]] = item[1]
                lotacaofiltrado['entidade'] = entidade
                try:
                    SFP006.objects.update_or_create(cdsecreta=str(lotacaofiltrado['cdsecreta']),
                                                    cdsetor=lotacaofiltrado['cdsetor'],
                                                    entidade=lotacaofiltrado['entidade'],
                                                    defaults=lotacaofiltrado)
                except Exception as e:
                    print("\nERRO NA IMPORTAÇÃO DE LOTAÇÃO: \n"+ str(e))
            try:
                os.remove(MEDIA_ROOT + "/" + cnpjPontuado + '/lotacoes.json')
                print("\nLotações importadas!")
            except:
                pass

        if os.path.isfile(MEDIA_ROOT + "/" + cnpjPontuado + '/undTrab.json'):
            print(
                "\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\nImportando Unidades de Trabalho\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-")
            dadosUnidTrab = json.load(open(MEDIA_ROOT + "/" + cnpjPontuado + '/undTrab.json'))
            for unidTrab in dadosUnidTrab['undTrab']:
                unidTrabFiltrada = {}
                for item in unidTrab.items():
                    if item[0] in 'codigo escola obs cdsecreta':
                        if item[1] != "" and item[1] is not None:
                            unidTrabFiltrada[item[0]] = item[1]
                unidTrabFiltrada['entidade'] = entidade

                try:
                    SFPD9924.objects.update_or_create(codigo=unidTrabFiltrada['codigo'],
                                                      entidade=unidTrabFiltrada['entidade'],
                                                      defaults=unidTrabFiltrada)
                    # Como Todd Howard uma vez disse: "It just works"
                except Exception as e:
                    print("\nERRO NA IMPORTAÇÃO DE UNIDADE DE TRABALHO: \n"+ str(e))
            try:
                os.remove(MEDIA_ROOT + "/" + cnpjPontuado + '/undTrab.json')
                print('\nUnidades de trabalho importadas!')
            except:
                pass

        if os.path.isfile(MEDIA_ROOT + "/" + cnpjPontuado + '/vinculos.json'):
            print(
                "\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\nImportando Vínculo\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-")
            dadosVinculos = json.load(open(MEDIA_ROOT + "/" + cnpjPontuado + '/vinculos.json'))
            for vinculo in dadosVinculos['vinculos']:
                vinculoFiltrados = {}

                for item in vinculo.items():
                    if item[0] in 'id_vinculo nm_vinculo tribunal cdsecreta':
                        if item[1] != "" and item[1] is not None and item[1] != '  ':
                            vinculoFiltrados[item[0]] = item[1]
                vinculoFiltrados['entidade'] = entidade

                try:
                    CFG_VINC.objects.update_or_create(id_vinculo=vinculoFiltrados['id_vinculo'],
                                                      entidade=vinculoFiltrados['entidade'],
                                                      defaults=vinculoFiltrados)
                except Exception as e:
                    print("\nERRO NA IMPORTAÇÃO DE VINCULO: \n"+ str(e))
            try:
                os.remove(MEDIA_ROOT + "/" + cnpjPontuado + '/vinculos.json')
                print('\nVínculos importados!')
            except:
                pass

        if os.path.isfile(MEDIA_ROOT + "/" + cnpjPontuado + '/pessoa.json'):
            print(
                "\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\nImportando Pessoas\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-")
            dadosPessoa = json.load(open(MEDIA_ROOT + "/" + cnpjPontuado + '/pessoa.json'))
            for pessoa in dadosPessoa['pessoa']:
                pessoaFiltrado = {}
                for item in pessoa.items():
                    if getattr(SFP001, item[0], None):
                        if item[0] != "" and item[0] is not None and item[0] != '  ':
                            if item[1] != "" and item[1] is not None and item[1] != '  ':
                                pessoaFiltrado[item[0]] = item[1]
                                if 'Date' in str(SFP001._meta.get_field(item[0]).get_internal_type()):
                                    try:
                                        dt = datetime.strptime(item[1], '%d/%m/%Y')
                                        pessoaFiltrado[item[0]] = dt
                                    except:
                                        print('Erro ao converter data!')
                pessoaFiltrado['entidade'] = entidade
                pessoaFiltrado['status'] = 'I'

                try:
                    pessoaFiltrado['uf'] = get_chave(chave='uf',
                                                     valor=pessoaFiltrado['uf'],
                                                     valor1=None,
                                                     entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('uf')
                    except:
                        pass
                try:
                    pessoaFiltrado['sistema'] = get_chave(chave='sistema',
                                                          valor=pessoaFiltrado['sistema'],
                                                          valor1=None,
                                                          entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('sistema')
                    except:
                        pass

                try:
                    pessoaFiltrado['cdsecreta'] = get_chave(chave='cdsecreta',
                                                          valor=pessoaFiltrado['cdsecreta'],
                                                          valor1=None,
                                                          entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('cdsecreta')
                    except:
                        pass

                try:
                    pessoaFiltrado['cdsetor'] = get_chave(chave='cdsetor',
                                                          valor=pessoaFiltrado['cdsecreta'].cdsecreta,
                                                          valor1=pessoaFiltrado['cdsetor'],
                                                          entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('cdsetor')
                    except:
                        pass

                try:
                    pessoaFiltrado['cdsecretaorigem'] = get_chave(chave='cdsecretaorigem',
                                                          valor=pessoaFiltrado['cdsecretaorigem'],
                                                          valor1=None,
                                                          entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('cdsecretaorigem')
                    except:
                        pass

                try:
                    pessoaFiltrado['cdsetororigem'] = get_chave(chave='cdsetororigem',
                                                                valor=pessoaFiltrado['cdsecretaorigem'].cdsecreta,
                                                                valor1=pessoaFiltrado['cdsetororigem'],
                                                                entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('cdsetororigem')
                    except:
                        pass

                try:
                    pessoaFiltrado['funcao'] = get_chave(chave='funcao',
                                                         valor=pessoaFiltrado['funcao'],
                                                         valor1=None,
                                                         entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('funcao')
                    except:
                        pass

                try:
                    pessoaFiltrado['funcao2'] = get_chave(chave='funcao2',
                                                          valor=pessoaFiltrado['funcao2'],
                                                          valor1=None,
                                                          entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('funcao2')
                    except:
                        pass

                try:
                    pessoaFiltrado['banco'] = get_chave(chave='banco',
                                                        valor=pessoaFiltrado['banco'],
                                                        valor1=None,
                                                        entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('banco')
                    except:
                        pass

                try:
                    pessoaFiltrado['tipoconta'] = get_chave(chave='tipoconta',
                                                            valor=pessoaFiltrado['banco'].codbanco,
                                                            valor1=pessoaFiltrado['tipoconta'],
                                                            entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('tipoconta')
                    except:
                        pass
                try:
                    pessoaFiltrado['ufident'] = get_chave(chave='ufident',
                                                          valor=pessoaFiltrado['ufident'],
                                                          valor1=None,
                                                          entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('ufident')
                    except:
                        pass
                try:
                    pessoaFiltrado['ufcartprof'] = get_chave(chave='ufcartprof',
                                                             valor=pessoaFiltrado['ufcartprof'],
                                                             valor1=None,
                                                             entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('ufcartprof')
                    except:
                        pass

                try:
                    pessoaFiltrado['ufnasc'] = get_chave(chave='ufnasc',
                                                         valor=pessoaFiltrado['ufnasc'],
                                                         valor1=None,
                                                         entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('ufnasc')
                    except:
                        pass
                try:
                    pessoaFiltrado['cidade'] = get_chave(chave='cidade',
                                                         valor=pessoaFiltrado['cidade'],
                                                         valor1=None,
                                                         entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('cidade')
                    except:
                        pass
                try:
                    pessoaFiltrado['cidnasc'] = get_chave(chave='cidnasc',
                                                          valor=pessoaFiltrado['cidnasc'],
                                                          valor1=None,
                                                          entidade=entidade)
                except:
                    try:
                        pessoaFiltrado.pop('cidnasc')
                    except:
                        pass

                try:
                    obj, criou = SFP001.objects.update_or_create(matricula=pessoaFiltrado['matricula'],
                                                                 cpf=pessoaFiltrado['cpf'],
                                                                 entidade=pessoaFiltrado['entidade'],
                                                                 defaults=pessoaFiltrado)
                except Exception as e:
                    print(pessoaFiltrado['nome'])
                    print(pessoaFiltrado['matricula'])
                    print("\nERRO NA IMPORTAÇÃO DE PESSOA: \n"+ str(e))
            try:
                os.remove(MEDIA_ROOT + "/" + cnpjPontuado + '/pessoa.json')
                print('\nPessoas importadas!')
            except:
                pass

        if os.path.isfile(MEDIA_ROOT + "/" + cnpjPontuado + '/depend.json'):
            print(
                "\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\nImportando Dependentes\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-")
            dadosDepen = json.load(open(MEDIA_ROOT + "/" + cnpjPontuado + '/depend.json'))
            for pessoa in dadosDepen['depend']:
                depenFiltrado = {}
                for item in pessoa.items():
                    if item[0] in 'matricula nomedep dependsocial cpf_dependente sexo nascdep parent identdepend sus_numcartdep sus_dtemissaodep depir depsf incap_fisica':
                        if item[1] != "" and item[1] is not None and item[1] != '  ':
                            depenFiltrado[item[0]] = item[1]
                            if 'Date' in str(Dependentes._meta.get_field(item[0]).get_internal_type()):
                                try:
                                    dt = datetime.strptime(item[1], '%d/%m/%Y')
                                    depenFiltrado[item[0]] = dt
                                except:
                                    print('Erro ao converter data!')
                depenFiltrado['entidade'] = entidade
                depenFiltrado['matricula'] = get_chave(chave='matricula',
                                                        valor=depenFiltrado['matricula'],
                                                        valor1=None,
                                                        entidade=entidade)
                if depenFiltrado['matricula'] is None:
                    continue
                depenFiltrado['depir'] = depenFiltrado['depir'] == 'T'
                depenFiltrado['depsf'] = depenFiltrado['depsf'] == 'T'
                try:
                    depenFiltrado['incap_fisica'] = depenFiltrado['incap_fisica'] == 'S'
                except:
                    try:
                        depenFiltrado.pop('incap_fisica')
                    except:
                        pass

                try:
                    obj, criou = Dependentes.objects.update_or_create(matricula=depenFiltrado['matricula'],
                                                         nomedep=depenFiltrado['nomedep'],
                                                         entidade=depenFiltrado['entidade'],
                                                         defaults=depenFiltrado)
                except Exception as e:
                    print(depenFiltrado['nomedep'])
                    print(depenFiltrado['matricula'])
                    print("\nERRO NA IMPORTAÇÃO DE DEPENDENTE: \n"+ str(e))
            try:
                os.remove(MEDIA_ROOT + "/" + cnpjPontuado + '/depend.json')
                print('\nDependentes importadas!')
            except:
                pass

        if os.path.isfile(MEDIA_ROOT + "/" + cnpjPontuado + '/afastamentos.json'):
            print(
                "\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\nImportando Afastamentos\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-")
            dadosAfast = json.load(open(MEDIA_ROOT + "/" + cnpjPontuado + '/afastamentos.json'))
            for pessoa in dadosAfast['afastamentos']:
                afastFiltrado = {}
                for item in pessoa.items():
                    if item[0] in 'anobase matricula codfol dtinicioafst dtfimafst obsafst':
                        if item[1] != "" and item[1] is not None and item[1] != '  ':
                            afastFiltrado[item[0]] = item[1]
                            if 'Date' in str(sfp017._meta.get_field(item[0]).get_internal_type()):
                                try:
                                    dt = datetime.strptime(item[1], '%d/%m/%Y')
                                    afastFiltrado[item[0]] = dt
                                except:
                                    print('Erro ao converter data!')
                afastFiltrado['entidade'] = entidade
                afastFiltrado['matricula'] = get_chave(chave='matricula',
                                                        valor=afastFiltrado['matricula'],
                                                        valor1=None,
                                                        entidade=entidade)
                if afastFiltrado['matricula'] is None:
                    continue

                try:
                    obj, criou = sfp017.objects.update_or_create(matricula=afastFiltrado['matricula'],
                                                                 dtinicioafst=afastFiltrado['dtinicioafst'],
                                                                 entidade=afastFiltrado['entidade'],
                                                                 defaults=afastFiltrado)
                except Exception as e:
                    print(afastFiltrado['matricula'])
                    print("\nERRO NA IMPORTAÇÃO DE AFASTAMENTO: \n"+ str(e))
            try:
                os.remove(MEDIA_ROOT + "/" + cnpjPontuado + '/afastamentos.json')
                print('\nAfastamentos importadas!')
            except:
                pass

        if os.path.isfile(MEDIA_ROOT + "/" + cnpjPontuado + '/cursos.json'):
            print(
                "\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\nImportando Cursos\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-")
            dadosCursos = json.load(open(MEDIA_ROOT + "/" + cnpjPontuado + '/cursos.json'))
            for pessoa in dadosCursos['depend']:
                cursosFiltrado = {}
                for item in pessoa.items():
                    if item[0] in 'anobase matricula codfol dtinicioafst dtfimafst obsafst':
                        if item[1] != "" and item[1] is not None and item[1] != '  ':
                            cursosFiltrado[item[0]] = item[1]
                            if 'Date' in str(Curso._meta.get_field(item[0]).get_internal_type()):
                                try:
                                    dt = datetime.strptime(item[1], '%d/%m/%Y')
                                    cursosFiltrado[item[0]] = dt
                                except:
                                    print('Erro ao converter data!')
                cursosFiltrado['entidade'] = entidade
                cursosFiltrado['matricula'] = get_chave(chave='matricula',
                                                        valor=cursosFiltrado['matricula'],
                                                        valor1=None,
                                                        entidade=entidade)

                try:
                    obj, criou = Curso.objects.update_or_create(matricula=cursosFiltrado['matricula'],
                                                                nivel=cursosFiltrado['nivel'],
                                                                entidade=cursosFiltrado['entidade'],
                                                                defaults=cursosFiltrado)
                except Exception as e:
                    print(cursosFiltrado['matricula'])
                    print("\nERRO NA IMPORTAÇÃO DE CURSO: \n"+ str(e))
            try:
                os.remove(MEDIA_ROOT + "/" + cnpjPontuado + '/cursos.json')
                print('\ncursos importadas!')
            except:
                pass

def get_chave(chave, valor, valor1=None, entidade=None):
    appName = None
    modelName = None
    fields = {}
    if chave == 'sistema':
        appName = 'CFG_VINC'
        modelName = 'CFG_VINC'
        fields['id_vinculo'] = valor
        fields['entidade__id'] = entidade.id

    if chave == 'cdsecreta':
        appName = 'SFP006'
        modelName = 'SFP006'
        fields['cdsecreta'] = valor
        fields['cdsetor'] = '000'
        fields['entidade__id'] = entidade.id

    if chave == 'cdsetor':
        appName = 'SFP006'
        modelName = 'SFP006'
        fields['cdsecreta'] = valor
        fields['cdsetor'] = valor1
        fields['entidade__id'] = entidade.id

    if chave == 'cdsecretaorigem':
        appName = 'SFP006'
        modelName = 'SFP006'
        fields['cdsecreta'] = valor
        fields['cdsetor'] = '000'
        fields['entidade__id'] = entidade.id

    if chave == 'cdsetororigem':
        appName = 'SFP006'
        modelName = 'SFP006'
        fields['cdsecreta'] = valor
        fields['cdsetor'] = valor1
        fields['entidade__id'] = entidade.id

    if chave == 'funcao':
        appName = 'SFP005'
        modelName = 'SFP005'
        fields['codigo'] = valor
        fields['entidade__id'] = entidade.id

    if chave == 'funcao2':
        appName = 'SFP005'
        modelName = 'SFP005'
        fields['codigo'] = valor
        fields['entidade__id'] = entidade.id

    if chave in 'cidnasc cidade':
        appName = 'IBGE'
        modelName = 'Municipios'
        fields['municipio'] = valor

    if chave in 'uf ufident ufcartprof ufcnh ufnasc':
        appName = 'IBGE'
        modelName = 'Uf'
        fields['uf'] = valor

    if chave == 'banco':
        appName = 'banco'
        modelName = 'Bancos'
        fields['codbanco'] = valor

    if chave == 'tipoconta':
        appName = 'banco'
        modelName = 'TipoConta'
        fields['tipoconta'] = valor1
        fields['codbanco__codbanco'] = valor

    if chave == 'matricula':
        appName = 'SFP001'
        modelName = 'SFP001'
        fields['matricula'] = valor
        if entidade:
            fields['entidade__id'] = entidade.id

    if chave == 'curso':
        appName = 'SFP001'
        modelName = 'Cursos'
        fields['matricula'] = valor

    try:
        model = apps.get_model(appName, modelName, True)
        return model.objects.filter(**fields)[0]
    except Exception as e:
        print(e)
        # if valor1:
        #     return valor1
        # else:
        #     if valor:
        #         return valor
        #     else:
        #         return None


def importacao(modeladmin, request, queryset):
    for obj in queryset:
        try:
            ThreadImportacao(obj).start()
        except Exception as e:
            modeladmin.message_user(request, "Error ao encontrar arquivo", level=messages.WARNING)
            print(str(e))
            return None

    modeladmin.message_user(request, "Importação realizada com sucesso")


importacao.short_description = "Realizar importação de dados"


def importacaoControle(modeladmin, request, queryset):
    for obj in queryset:
        try:
            with open('core/fixtures/controle.json') as json_file:
                arquivo = json.load(json_file)
                for objeto in arquivo:
                    new_dict = objeto['fields']
                    del new_dict['entidade']
                    c = Controle(entidade=obj, **new_dict)
                    c.save()
                print(objeto)
        except Exception as e:
            modeladmin.message_user(request, "Error ao encontrar arquivo", level=messages.WARNING)
            print(str(e))
            return None

    modeladmin.message_user(request, "Controle importado com sucesso")


importacaoControle.short_description = "Realizar importação de controle"


def exportacao(modeladmin, request, queryset):
    for obj in queryset:
        cnp = obj.cnpj.replace('.', '').replace('/', '').replace('-', '')
        filename = f"RECAD_{cnp}.json"
        new_dict = dict()
        dados = dict()
        pessoas = []
        for pessoa in obj.sfp001_set.all():
            p = dict()
            field_names = [field.name for field in pessoa._meta.fields]
            for field in field_names:
                p[field] = str(getattr(pessoa, field))
            pessoas.append(p)
        dependentes = []
        for dependente in Dependentes.objects.filter(matricula__entidade=obj).distinct():
            d = dict()
            field_names = [field.name for field in dependente._meta.fields]
            for field in field_names:
                d[field] = str(getattr(dependente, field))
            dependentes.append(d)
        dados['cnpj'] = cnp
        dados['razao'] = obj.razao
        dados['pessoas'] = pessoas
        dados['dependentes'] = dependentes
        new_dict['dados'] = dados
        content = json.dumps(new_dict)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response


exportacao.short_description = "Realizar exportação de dados"


class EntidadeAdmin(admin.ModelAdmin):
    list_display = ('razao', 'codigo_entidade', 'cnpj')
    search_fields = ('razao',)
    ordering = ['razao']
    actions = [importacao, exportacao, importacaoControle]


admin.site.register(Entidade, EntidadeAdmin)
