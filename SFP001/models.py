import json

from django.db import models
from SFP001.choices import CH_SEXO, CH_GRAU_INSTRUCAO, CH_ESTCIVIL, CH_TRUE_FALSE, CH_SIM_NAO, CH_ESFERA, \
    CH_REGIME, CH_NIVEL_INSTRUCAO, CH_CODFOL, CH_RACA, CH_TIPO_SANGUINEO, CH_TIPO_DEF_FISICA, CH_TIPO_DEF_VISUAL, \
    CH_TIPO_DEF_MENTAL, CH_NACIONALIDADE, CH_CONSELHOS, CH_STATUS, CH_PARENTESCO, CH_TIPOS_DOCS, CH_TEMPO_RESIDENCIA,CH_CONDICAO_ESTRANGEIRO


class RelatoriosCadastro(models.Model):
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE)
    data = models.DateField(null=True, blank=True)
    qtde_importado = models.IntegerField()
    qtde_editado = models.IntegerField()
    qtde_finalizado = models.IntegerField()

    def __str__(self):
        return '{} - {}'.format(self.entidade, self.data)

    class Meta:
        db_table = 'relatorioscadastro'


class Curso(models.Model):
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE)
    matricula = models.ForeignKey('SFP001.SFP001', related_name='matricula_curso', on_delete=models.CASCADE)
    nivel = models.CharField(max_length=2, choices=CH_NIVEL_INSTRUCAO, null=True, blank=True)
    nomecurso = models.CharField(max_length=60, null=True, blank=True)
    anobase = models.IntegerField(null=True, blank=True)
    instituicao = models.CharField(max_length=60, null=True, blank=True)
    carghora = models.CharField(max_length=5, null=True, blank=True)
    dtiniciocurso = models.DateField(null=True, blank=True)
    dtfimcurso = models.DateField(null=True, blank=True)
    obscurso = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.pessoa)

    class Meta:
        db_table = 'curso'


class sfp017(models.Model):
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE)
    anobase = models.IntegerField(null=True, blank=True)
    matricula = models.ForeignKey('SFP001.SFP001', related_name='matricula_afast', on_delete=models.CASCADE)
    codfol = models.CharField(max_length=2, choices=CH_CODFOL, null=True, blank=True)
    dtinicioafst = models.DateField(null=True, blank=True)
    dtfimafst = models.DateField(null=True, blank=True)
    obsafst = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.codfol)

    class Meta:
        db_table = 'sfp017'
        verbose_name = 'SFP017'
        verbose_name_plural = 'Afastementos'


class Dependentes(models.Model):
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE)
    matricula = models.ForeignKey('SFP001.SFP001', related_name='matricula_depen', on_delete=models.CASCADE)
    nomedep = models.CharField(max_length=100, null=True, blank=True)
    dependsocial = models.CharField(max_length=1, null=True, blank=True)
    cpf_dependente = models.CharField(max_length=11, null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=CH_SEXO, null=True, blank=True)
    nascdep = models.DateField(null=True, blank=True)
    parent = models.CharField(max_length=1, choices=CH_PARENTESCO, null=True, blank=True)
    identdepend = models.CharField(max_length=20, null=True, blank=True)
    sus_numcartdep = models.CharField(max_length=50, null=True, blank=True)
    sus_dtemissaodep = models.DateField(null=True, blank=True)
    depir = models.BooleanField(default=False, null=True, blank=True)
    depsf = models.BooleanField(default=False, null=True, blank=True)
    incap_fisica = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.nomedep, self.cpf_dependente, self.parent)

    class Meta:
        db_table = 'dependente'
        verbose_name = 'Dependente'
        verbose_name_plural = 'Dependentes'


class SFP001(models.Model):
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE, blank=True, db_index=True)

    status = models.CharField(max_length=1, choices=CH_STATUS, null=True, blank=True)

    matricula = models.CharField(max_length=8, null=True, blank=True, db_index=True)
    sistema = models.ForeignKey('CFG_VINC.CFG_VINC', null=True, blank=True, on_delete=models.CASCADE, db_index=True)
    cdsecreta = models.ForeignKey('SFP006.SFP006', null=True, blank=True,
                                  related_name='secretaria',
                                  limit_choices_to={'cdsetor': '000'},
                                  on_delete=models.CASCADE,
                                  db_index=True)
    cdsetor = models.ForeignKey('SFP006.SFP006',
                                related_name='setor',
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
                                db_index=True)
    cddepart = models.CharField(max_length=3, null=True, blank=True)
    nome = models.CharField(max_length=70, null=True, blank=True, db_index=True)
    funcao = models.ForeignKey('SFP005.SFP005', null=True, blank=True, on_delete=models.CASCADE)
    nomepai = models.CharField(max_length=100, null=True, blank=True)
    nomemae = models.CharField(max_length=100, null=True, blank=True)
    dtnasc = models.DateField(null=True, blank=True)
    cidnasc = models.ForeignKey('IBGE.Municipios', related_name='cidnasc', null=True, blank=True,
                                on_delete=models.DO_NOTHING)
    ufnasc = models.ForeignKey('IBGE.Uf', related_name='uf_nascimento', null=True, blank=True,
                               on_delete=models.DO_NOTHING)
    endereco = models.CharField(max_length=30, null=True, blank=True)
    endnum = models.CharField(max_length=5, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    cidade = models.ForeignKey('IBGE.Municipios', related_name='cidade', null=True, blank=True,
                               on_delete=models.DO_NOTHING)
    uf = models.ForeignKey('IBGE.Uf', related_name='uf_end', null=True, blank=True, on_delete=models.DO_NOTHING)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    fone = models.CharField(max_length=15, null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=CH_SEXO, null=True, blank=True)
    raca = models.CharField(max_length=1, choices=CH_RACA, null=True, blank=True)
    tpsanguineo = models.CharField(max_length=1, choices=CH_TIPO_SANGUINEO, null=True, blank=True)
    grinstr = models.CharField(max_length=1, choices=CH_GRAU_INSTRUCAO, null=True, blank=True)
    estcivil = models.CharField(max_length=1, choices=CH_ESTCIVIL, null=True, blank=True)
    dtadmissao = models.DateField(null=True, blank=True)
    dtadmissao2 = models.DateField(null=True, blank=True)
    dtopcao = models.DateField(null=True, blank=True)

    #    <!-- RG-Registro Geral  -->
    identidade = models.CharField(max_length=20, null=True, blank=True)
    orgaoident = models.CharField(max_length=5, null=True, blank=True)
    ufident = models.ForeignKey('IBGE.Uf', related_name='uf_ident', null=True, blank=True, on_delete=models.DO_NOTHING)
    dtident = models.DateField(null=True, blank=True)
    #   <!-- RG-Registro Geral -->

    cpf = models.CharField(max_length=11, null=True, blank=True)

    #   <!-- CTPS - Carteira de Trabalho e Previdência Social -->
    numcartprof = models.CharField(max_length=8, null=True, blank=True)
    seriecartprof = models.CharField(max_length=5, null=True, blank=True)
    ufcartprof = models.ForeignKey('IBGE.Uf', related_name='uf_cartprof', null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    datexpctps = models.DateField(null=True, blank=True)
    ctps_digital = models.CharField(max_length=1, choices=CH_TRUE_FALSE, null=True, blank=True)
    #   <!-- CTPS - Carteira de Trabalho e Previdência Social -->

    pispasep = models.CharField(max_length=11, null=True, blank=True)

    #   <!-- Título de Eleitor -->
    titeleitor = models.CharField(max_length=14, null=True, blank=True)
    zona = models.CharField(max_length=4, null=True, blank=True)
    secao = models.CharField(max_length=4, null=True, blank=True)
    #   <!-- Título de Eleitor -->

    #   <!-- CNH -->
    cnh = models.CharField(max_length=11, null=True, blank=True)
    cnhcat = models.CharField(max_length=2, null=True, blank=True)
    cnhdtexp = models.DateField(null=True, blank=True)
    dtcnh = models.DateField(null=True, blank=True)
    cnhorgao = models.CharField(max_length=10, null=True, blank=True)
    dtprimcnh = models.DateField(null=True, blank=True)
    ufcnh = models.ForeignKey('IBGE.Uf', related_name='ufcnh', null=True, blank=True, on_delete=models.DO_NOTHING)
    #   <!-- CNH -->

    #   <! -- Outras Documentações -->
    ncertcasamento = models.CharField(max_length=20, null=True, blank=True)
    ncertnascimento = models.CharField(max_length=20, null=True, blank=True)
    naverbdivorcio = models.CharField(max_length=20, null=True, blank=True)
    jacotribregime = models.BooleanField(default=False, null=True)
    dataregimeprev = models.DateField(null=True, blank=True)
    sus_numcart = models.CharField(max_length=50, null=True, blank=True)
    sus_dtemissao = models.DateField(null=True, blank=True)
    #   <! -- Outras Documentações -->

    marcarel = models.CharField(max_length=1, null=True, blank=True)
    apelido = models.CharField(max_length=100, null=True, blank=True)
    contafgts = models.CharField(max_length=11, null=True, blank=True)
    banco = models.ForeignKey('banco.Bancos', null=True, blank=True, on_delete=models.DO_NOTHING)
    agencia = models.CharField(max_length=4, null=True, blank=True)
    dvagencia = models.CharField(max_length=1, null=True, blank=True)
    tipoconta = models.ForeignKey('banco.TipoConta', null=True, blank=True, on_delete=models.DO_NOTHING)
    conta = models.CharField(max_length=10, null=True, blank=True)
    dvconta = models.CharField(max_length=1, null=True, blank=True)
    hortrab = models.CharField(max_length=3, null=True, blank=True)
    horbase = models.CharField(max_length=3, null=True, blank=True)
    codigofun = models.CharField(max_length=25, null=True, blank=True)
    obs = models.CharField(max_length=150, null=True, blank=True)
    codesc = models.CharField(max_length=3, null=True, blank=True)
    codesc2 = models.CharField(max_length=3, null=True, blank=True)
    funcao2 = models.ForeignKey('SFP005.SFP005', related_name='funcao2', null=True, blank=True,
                                on_delete=models.CASCADE)

    # <!-- Informativo -->
    cargo_acumulo = models.CharField(max_length=60, null=True, blank=True)
    lotacao_acumulo = models.CharField(max_length=60, null=True, blank=True)
    data_ingresso_acumulo = models.DateField(null=True, blank=True)
    jornada_acumulo = models.TimeField(null=True, blank=True)
    carga_horaria_acumulo = models.TimeField(null=True, blank=True)
    esfera_acumulo = models.CharField(max_length=1, choices=CH_ESFERA, null=True, blank=True)
    regime_juridico_acumulo = models.CharField(max_length=1, choices=CH_REGIME, null=True, blank=True)
    # <!-- Informativo -->

    # <!-- Situação Funcional -->
    efetivo_fuc_gratif = models.BooleanField(default=False)
    efetivo_sec_municp = models.BooleanField(default=False)
    efetivo_org_inst = models.BooleanField(default=False)
    efetivo_lic_venc = models.BooleanField(default=False)
    nomeados_estg_prob = models.BooleanField(default=False)
    dt_efetivo_vencimento = models.DateField(null=True, blank=True)
    dt_efetivo_venci_fim = models.DateField(null=True, blank=True)
    dt_nomeados_probatorio = models.DateField(null=True, blank=True)
    dt_nomeados_prob_fim = models.DateField(null=True, blank=True)

    classe = models.CharField(max_length=5, null=True, blank=True)

    ophorext = models.CharField(max_length=1, null=True, blank=True)
    opadicnot = models.CharField(max_length=1, null=True, blank=True)
    ophoraula = models.CharField(max_length=1, null=True, blank=True)
    opvaltrans = models.CharField(max_length=1, null=True, blank=True)
    contfolha = models.CharField(max_length=1, null=True, blank=True)
    fecfolha = models.CharField(max_length=1, null=True, blank=True)
    tribunal = models.CharField(max_length=6, null=True, blank=True)
    pagtonline = models.CharField(max_length=15, null=True, blank=True)
    impconsig = models.CharField(max_length=40, null=True, blank=True)
    dtats = models.DateField(null=True, blank=True)
    brasileiro = models.CharField(max_length=1, choices=CH_SIM_NAO, null=True, blank=True)
    codnacion = models.CharField(max_length=2, null=True, blank=True)
    nacionalid = models.CharField(max_length=2, choices=CH_NACIONALIDADE, null=True, blank=True)
    naturaliza = models.CharField(max_length=1, null=True, blank=True)
    dtconcurso = models.DateField(null=True, blank=True)
    classific = models.CharField(max_length=5, null=True, blank=True)
    dtconcurs2 = models.DateField(null=True, blank=True)
    classific2 = models.CharField(max_length=5, null=True, blank=True)
    dtposse = models.DateField(null=True, blank=True)
    contrato = models.CharField(max_length=7, null=True, blank=True)
    tipdecreto = models.CharField(max_length=1, null=True, blank=True)
    numdecreto = models.CharField(max_length=10, null=True, blank=True)
    dtdecreto = models.DateField(null=True, blank=True)
    matricfun = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=80, null=True, blank=True)
    tipoadmis = models.CharField(max_length=1, null=True, blank=True)
    deficiente = models.CharField(max_length=1, null=True, blank=True)
    formacao = models.CharField(max_length=1, null=True, blank=True)
    fone2 = models.CharField(max_length=15, null=True, blank=True)
    fonecel = models.CharField(max_length=15, null=True, blank=True)
    certmilit = models.CharField(max_length=20, null=True, blank=True)
    cidvota = models.CharField(max_length=40, null=True, blank=True)
    dtpispasep = models.DateField(null=True, blank=True)
    raistrab = models.CharField(max_length=2, null=True, blank=True)
    raiscor = models.CharField(max_length=1, null=True, blank=True)
    tipamparo = models.CharField(max_length=10, null=True, blank=True)
    numamparo = models.CharField(max_length=10, null=True, blank=True)
    datamparo = models.DateField(null=True, blank=True)
    pubamparo = models.DateField(null=True, blank=True)
    tpreingres = models.CharField(max_length=1, null=True, blank=True)
    exreingres = models.CharField(max_length=1, null=True, blank=True)
    nureingres = models.CharField(max_length=10, null=True, blank=True)
    dtreingres = models.DateField(null=True, blank=True)
    pureingres = models.DateField(null=True, blank=True)
    exampreing = models.CharField(max_length=1, null=True, blank=True)
    nuampreing = models.CharField(max_length=10, null=True, blank=True)
    dtampreing = models.DateField(null=True, blank=True)
    puampreing = models.DateField(null=True, blank=True)
    paramtcm = models.CharField(max_length=10, null=True, blank=True)
    obsreserva = models.CharField(max_length=150, null=True, blank=True)
    calcinss = models.CharField(max_length=1, null=True, blank=True)
    calcirrf = models.CharField(max_length=1, null=True, blank=True)
    calcprev = models.CharField(max_length=1, null=True, blank=True)
    calcsalfam = models.CharField(max_length=1, null=True, blank=True)
    regcons = models.CharField(max_length=7, choices=CH_CONSELHOS, null=True, blank=True)
    numcons = models.CharField(max_length=20, null=True, blank=True)
    numproc_pa = models.CharField(max_length=12, null=True, blank=True)
    cpf_segurado = models.CharField(max_length=11, null=True, blank=True)
    he1 = models.CharField(max_length=5, null=True, blank=True)
    he2 = models.CharField(max_length=5, null=True, blank=True)
    hs1 = models.CharField(max_length=5, null=True, blank=True)
    hs2 = models.CharField(max_length=5, null=True, blank=True)
    cong_ats = models.CharField(max_length=1, choices=CH_TRUE_FALSE, null=True, blank=True)
    dtprogress = models.DateField(null=True, blank=True)
    msnccp = models.CharField(max_length=100, null=True, blank=True)
    agregmatirrf = models.CharField(max_length=1, null=True, blank=True)
    marcaserv = models.CharField(max_length=1, null=True, blank=True)
    res_propria = models.CharField(max_length=1, null=True, blank=True)
    tipo_defic = models.CharField(max_length=4, null=True, blank=True)
    defic_fis = models.BooleanField(default=False)
    defic_vis = models.BooleanField(default=False)
    defic_ment = models.BooleanField(default=False)
    defic_aud = models.BooleanField(default=False)
    defic_intlec = models.BooleanField(default=False)
    cota_def_hab_reab = models.BooleanField(default=False)
    reabilitado = models.BooleanField(default=False)
    tipo_defic_fis = models.CharField(max_length=2, choices=CH_TIPO_DEF_FISICA, null=True, blank=True)
    tipo_defic_vis = models.CharField(max_length=2, choices=CH_TIPO_DEF_VISUAL, null=True, blank=True)
    tipo_defic_ment = models.CharField(max_length=2, choices=CH_TIPO_DEF_MENTAL, null=True, blank=True)
    complemento = models.CharField(max_length=20, null=True, blank=True)
    tempcontr = models.IntegerField(null=True, blank=True)
    tpcontrato = models.CharField(max_length=1, null=True, blank=True)
    gestprop = models.CharField(max_length=1, choices=CH_TRUE_FALSE, null=True, blank=True)
    und_fimcontr = models.CharField(max_length=1, null=True, blank=True)
    dt_fimcontr = models.DateField(null=True, blank=True)
    nome_segurado = models.CharField(max_length=40, null=True, blank=True)
    codatuacao = models.CharField(max_length=3, null=True, blank=True)
    transpessoal = models.CharField(max_length=1, choices=CH_TRUE_FALSE, null=True, blank=True)
    dtnaturalizacao = models.DateField(null=True, blank=True)
    dtlaudodeficiente = models.DateField(null=True, blank=True)
    tplogradouro = models.CharField(max_length=50, null=True, blank=True)
    codibge_municipio = models.IntegerField(null=True, blank=True)
    # codibge_cidnasc = models.ForeignKey('', on_delete=models.PROTECT)
    obs_manter = models.CharField(max_length=1, choices=CH_TRUE_FALSE, null=True, blank=True)
    instpensao_nome = models.CharField(max_length=40, null=True, blank=True)
    instpensao_cpf = models.CharField(max_length=11, null=True, blank=True)
    instpensao_matricula = models.CharField(max_length=8, null=True, blank=True)
    instpensao_funcao = models.CharField(max_length=3, null=True, blank=True)
    instpensao_natureza_cargo = models.CharField(max_length=1, null=True, blank=True)
    categoria_situacao = models.CharField(max_length=5, null=True, blank=True)
    dt_inicio_serv_pub = models.DateField(null=True, blank=True)
    tp_cat_siop = models.CharField(max_length=5, null=True, blank=True)
    cat_siop = models.CharField(max_length=5, null=True, blank=True)
    cdsecretaorigem = models.ForeignKey('SFP006.SFP006', null=True, blank=True,
                                        related_name='secretaria_origem',
                                        limit_choices_to={'cdsetor': '000'},
                                        on_delete=models.CASCADE)
    cdsetororigem = models.ForeignKey('SFP006.SFP006', related_name='setor_origem',
                                      null=True, blank=True, on_delete=models.CASCADE)

       #<---------- ESTRANGEIRO -----------------...

    estrangeiro = models.CharField(max_length=1, choices=CH_SIM_NAO, null=True, blank=True)
    paisorigem = models.CharField(max_length=40, null=True, blank=True)
    cartbrasil = models.CharField(max_length=10, null=True, blank=True)
    dtbrasil = models.DateField(null=True, blank=True)
    casadocombr = models.CharField(max_length=1, choices=CH_SIM_NAO, null=True, blank=True)
    filhocombr = models.CharField(max_length=1, choices=CH_SIM_NAO, null=True, blank=True)
    estado_estrangeiro = models.CharField(max_length=50, null=True, blank=True)
    cidade_estrangeiro = models.CharField(max_length=50, null=True, blank=True)
    rnenum = models.CharField(max_length=8, null=True, blank=True)
    rneorgao = models.CharField(max_length=30, null=True, blank=True)
    rnedataemi = models.DateField(null=True, blank=True)
    dtchegadaestran = models.DateField(null=True, blank=True)
    tmpresidestrang = models.CharField(max_length=30, choices=CH_TEMPO_RESIDENCIA, null=True, blank=True)
    condingestrang = models.CharField(max_length=100, choices=CH_CONDICAO_ESTRANGEIRO, null=True, blank=True)


    #------------------------------------------------------------------------>
    ocorrencia_gfip = models.CharField(max_length=2, null=True, blank=True)
    qualifcadastral = models.CharField(max_length=2, null=True, blank=True)
    anomes_criacao = models.CharField(max_length=6, null=True, blank=True)
    dt_nomeacao_tcema = models.DateField(null=True, blank=True)
    dt_instpensao_obito = models.DateField(null=True, blank=True)
    parentesco_instpensao = models.CharField(max_length=1, null=True, blank=True)
    obsfuncionais = models.TextField(max_length=400, null=True, blank=True)
    inativacao_sagres_pe = models.CharField(max_length=1, null=True, blank=True)
    siap_mot_cont_temp = models.CharField(max_length=10, null=True, blank=True)
    siap_tipo_cont_temp = models.CharField(max_length=10, null=True, blank=True)
    siap_veic_publicacao = models.CharField(max_length=10, null=True, blank=True)
    siap_motivo_contratacao = models.CharField(max_length=100, null=True, blank=True)
    eventoats = models.CharField(max_length=2, null=True, blank=True)
    data_reintegracao = models.DateField(null=True, blank=True)
    nome_social = models.CharField(max_length=70, null=True, blank=True)
    maternidade13 = models.CharField(max_length=1, choices=CH_TRUE_FALSE, null=True, blank=True)
    fechamento_individual = models.CharField(max_length=1, choices=CH_TRUE_FALSE, null=True, blank=True)
    nao_calc_patronal = models.CharField(max_length=1, null=True, blank=True)

    registro = models.JSONField(null=True)
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.nome)

    def save(self, *args, **kwargs):
        #salva os registros em um campo jsonfield
        if self.registro is None:
            reg = {}
            for key, value in self.__dict__.items():
                if key not in 'registro id status _state foto':
                    reg[key] = value
            self.registro = json.dumps(reg, default=str)
        super().save(*args, **kwargs)

    @property
    def ListaCursos(self):
        return self.pessoas.all()

    @property
    def nomeMae(self):
        if self.nomemae:
            return self.nomemae
        else:
            return ""

    @property
    def Matricula(self):
        if self.matricula:
            return self.matricula
        else:
            return ""

    @property
    def Nome(self):
        if self.nome:
            return self.nome
        else:
            return ""

    @property
    def CPF(self):
        if self.cpf:
            return self.cpf
        else:
            return ""

    class Meta:
        db_table = 'sfp001'
        verbose_name = 'sfp001'
        verbose_name_plural = 'Pessoas'
        index_together = (('entidade', 'matricula'), ('entidade', 'nome'))


class Fotos(models.Model):
    pessoa = models.ForeignKey(SFP001, related_name='fotos', on_delete=models.CASCADE, db_index=True)
    foto = models.TextField()

    class Meta:
        db_table = 'sfp001_foto'
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'


class Documentos(models.Model):
    pessoa = models.ForeignKey(SFP001, related_name='documentos', on_delete=models.PROTECT, db_index=True)
    tipo = models.CharField(max_length=5, choices=CH_TIPOS_DOCS)
    data_criacao = models.DateTimeField(auto_created=True, null=True)
    documento = models.TextField()

    class Meta:
        db_table = 'sfp001_documentos'
        verbose_name = 'Documentos'
        verbose_name_plural = 'Documentos'
