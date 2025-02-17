# Generated by Django 3.1 on 2023-09-27 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('banco', '0001_initial'),
        ('IBGE', '0001_initial'),
        ('SFP005', '0001_initial'),
        ('SFP006', '0001_initial'),
        ('entidades', '0001_initial'),
        ('CFG_VINC', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SFP001',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('I', 'Importado'), ('E', 'Editado'), ('F', 'Finalizado')], max_length=1, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='pessoa/')),
                ('matricula', models.CharField(blank=True, max_length=8, null=True)),
                ('cddepart', models.CharField(blank=True, max_length=3, null=True)),
                ('nome', models.CharField(blank=True, max_length=70, null=True)),
                ('nomepai', models.CharField(blank=True, max_length=100, null=True)),
                ('nomemae', models.CharField(blank=True, max_length=100, null=True)),
                ('dtnasc', models.DateField(blank=True, null=True)),
                ('endereco', models.CharField(blank=True, max_length=30, null=True)),
                ('endnum', models.CharField(blank=True, max_length=5, null=True)),
                ('cep', models.CharField(blank=True, max_length=8, null=True)),
                ('bairro', models.CharField(blank=True, max_length=100, null=True)),
                ('fone', models.CharField(blank=True, max_length=15, null=True)),
                ('sexo', models.CharField(blank=True, choices=[('2', 'FEMININO'), ('1', 'MASCULINO')], max_length=1, null=True)),
                ('raca', models.CharField(blank=True, choices=[('1', 'Branco'), ('2', 'Preto'), ('3', 'Pardo'), ('4', 'Amarelo'), ('5', 'Indígena')], max_length=1, null=True)),
                ('tpsanguineo', models.CharField(blank=True, choices=[('1', 'A+'), ('2', 'A-'), ('3', 'B+'), ('4', 'B-'), ('5', 'AB+'), ('6', 'AB-'), ('7', 'O+'), ('8', 'O-')], max_length=1, null=True)),
                ('grinstr', models.CharField(blank=True, choices=[('1', 'Analfabeto, inclusive o que, embora tenha recebido instrução, não se alfabetizou.'), ('2', 'Até o 5º ano incompleto do ensino fundamental.'), ('3', '5º ano completo do ensino fundamental.'), ('4', 'Do 6º ao 9º ano do ensino fundamental incompleto.'), ('5', 'Ensino fundamental completo'), ('6', 'Ensino médio incompleto.'), ('7', 'Ensino médio completo.'), ('8', 'Educação superior incompleta.'), ('9', 'Educação superior completa.'), ('A', 'Mestrado completo.'), ('B', 'Doutorado completo.'), ('C', 'Pós graduação completo')], max_length=1, null=True)),
                ('estcivil', models.CharField(blank=True, choices=[('1', 'SOLTEIRO'), ('2', 'CASADO'), ('3', 'DIVORCIADO'), ('4', 'ESTÁVEL'), ('5', 'VIÚVO'), ('6', 'DESQUITADO E OUTROS')], max_length=1, null=True)),
                ('dtadmissao', models.DateField(blank=True, null=True)),
                ('dtadmissao2', models.DateField(blank=True, null=True)),
                ('dtopcao', models.DateField(blank=True, null=True)),
                ('identidade', models.CharField(blank=True, max_length=20, null=True)),
                ('orgaoident', models.CharField(blank=True, max_length=5, null=True)),
                ('dtident', models.DateField(blank=True, null=True)),
                ('cpf', models.CharField(blank=True, max_length=11, null=True)),
                ('numcartprof', models.CharField(blank=True, max_length=8, null=True)),
                ('seriecartprof', models.CharField(blank=True, max_length=5, null=True)),
                ('datexpctps', models.DateField(blank=True, null=True)),
                ('ctps_digital', models.CharField(blank=True, choices=[('T', 'VERDADEIRO'), ('F', 'FALSO')], max_length=1, null=True)),
                ('pispasep', models.CharField(blank=True, max_length=11, null=True)),
                ('titeleitor', models.CharField(blank=True, max_length=14, null=True)),
                ('zona', models.CharField(blank=True, max_length=4, null=True)),
                ('secao', models.CharField(blank=True, max_length=4, null=True)),
                ('cnh', models.CharField(blank=True, max_length=11, null=True)),
                ('cnhcat', models.CharField(blank=True, max_length=2, null=True)),
                ('cnhdtexp', models.DateField(blank=True, null=True)),
                ('dtcnh', models.DateField(blank=True, null=True)),
                ('cnhorgao', models.CharField(blank=True, max_length=10, null=True)),
                ('dtprimcnh', models.DateField(blank=True, null=True)),
                ('ncertcasamento', models.CharField(blank=True, max_length=20, null=True)),
                ('ncertnascimento', models.CharField(blank=True, max_length=20, null=True)),
                ('naverbdivorcio', models.CharField(blank=True, max_length=20, null=True)),
                ('jacotribregime', models.BooleanField(default=False, null=True)),
                ('dataregimeprev', models.DateField(blank=True, null=True)),
                ('sus_numcart', models.CharField(blank=True, max_length=50, null=True)),
                ('sus_dtemissao', models.DateField(blank=True, null=True)),
                ('marcarel', models.CharField(blank=True, max_length=1, null=True)),
                ('apelido', models.CharField(blank=True, max_length=100, null=True)),
                ('contafgts', models.CharField(blank=True, max_length=11, null=True)),
                ('agencia', models.CharField(blank=True, max_length=4, null=True)),
                ('dvagencia', models.CharField(blank=True, max_length=1, null=True)),
                ('conta', models.CharField(blank=True, max_length=10, null=True)),
                ('dvconta', models.CharField(blank=True, max_length=1, null=True)),
                ('hortrab', models.CharField(blank=True, max_length=3, null=True)),
                ('horbase', models.CharField(blank=True, max_length=3, null=True)),
                ('codigofun', models.CharField(blank=True, max_length=25, null=True)),
                ('obs', models.CharField(blank=True, max_length=150, null=True)),
                ('codesc', models.CharField(blank=True, max_length=3, null=True)),
                ('codesc2', models.CharField(blank=True, max_length=3, null=True)),
                ('cargo_acumulo', models.CharField(blank=True, max_length=60, null=True)),
                ('lotacao_acumulo', models.CharField(blank=True, max_length=60, null=True)),
                ('data_ingresso_acumulo', models.DateField(blank=True, null=True)),
                ('jornada_acumulo', models.TimeField(blank=True, null=True)),
                ('carga_horaria_acumulo', models.TimeField(blank=True, null=True)),
                ('esfera_acumulo', models.CharField(blank=True, choices=[('1', 'FEDERAL'), ('2', 'ESTADUAL'), ('3', 'MUNICIPAL')], max_length=1, null=True)),
                ('regime_juridico_acumulo', models.CharField(blank=True, choices=[('1', 'ESTATUARIO'), ('2', 'CELETISTA'), ('3', 'OUTROS')], max_length=1, null=True)),
                ('efetivo_fuc_gratif', models.BooleanField(default=False)),
                ('efetivo_sec_municp', models.BooleanField(default=False)),
                ('efetivo_org_inst', models.BooleanField(default=False)),
                ('efetivo_lic_venc', models.BooleanField(default=False)),
                ('nomeados_estg_prob', models.BooleanField(default=False)),
                ('dt_efetivo_vencimento', models.DateField(blank=True, null=True)),
                ('dt_efetivo_venci_fim', models.DateField(blank=True, null=True)),
                ('dt_nomeados_probatorio', models.DateField(blank=True, null=True)),
                ('dt_nomeados_prob_fim', models.DateField(blank=True, null=True)),
                ('classe', models.CharField(blank=True, max_length=5, null=True)),
                ('ophorext', models.CharField(blank=True, max_length=1, null=True)),
                ('opadicnot', models.CharField(blank=True, max_length=1, null=True)),
                ('ophoraula', models.CharField(blank=True, max_length=1, null=True)),
                ('opvaltrans', models.CharField(blank=True, max_length=1, null=True)),
                ('contfolha', models.CharField(blank=True, max_length=1, null=True)),
                ('fecfolha', models.CharField(blank=True, max_length=1, null=True)),
                ('tribunal', models.CharField(blank=True, max_length=6, null=True)),
                ('pagtonline', models.CharField(blank=True, max_length=15, null=True)),
                ('impconsig', models.CharField(blank=True, max_length=40, null=True)),
                ('dtats', models.DateField(blank=True, null=True)),
                ('brasileiro', models.CharField(blank=True, choices=[('S', 'SIM'), ('N', 'NÃO')], max_length=1, null=True)),
                ('codnacion', models.CharField(blank=True, max_length=2, null=True)),
                ('nacionalid', models.CharField(blank=True, choices=[('10', 'Brasileiro'), ('20', 'Naturalizado Brasileiro'), ('21', 'Argentino'), ('22', 'Boliviano'), ('23', 'Chileno'), ('24', 'Paraguaio'), ('25', 'Uruguaio'), ('26', 'Venezuelano'), ('27', 'Colombiano'), ('28', 'Peruano'), ('29', 'Equatoriano'), ('30', 'Alemão'), ('31', 'Belga'), ('32', 'Britânico'), ('34', 'Canadense'), ('35', 'Espanhol'), ('36', 'Norte-Americano (EUA)'), ('37', 'Francês'), ('38', 'Suíço'), ('39', 'Italiano'), ('40', 'Haitiano'), ('41', 'Japonês'), ('42', 'Chinês'), ('43', 'Coreano'), ('44', 'Russo'), ('45', 'Português'), ('46', 'Paquistanês'), ('47', 'Indiano'), ('48', 'Outros'), ('49', 'Latino Americanos'), ('50', 'Outros'), ('51', 'Asiáticos'), ('52', 'Bengalês'), ('53', 'Outros'), ('54', 'Europeus'), ('55', 'Angolano'), ('56', 'Congolês'), ('57', 'Sul – Africano'), ('58', 'Ganês'), ('59', 'Senegalês'), ('60', 'Outros'), ('61', 'Africanos'), ('62', 'Outros')], max_length=2, null=True)),
                ('naturaliza', models.CharField(blank=True, max_length=1, null=True)),
                ('dtbrasil', models.DateField(blank=True, null=True)),
                ('cartbrasil', models.CharField(blank=True, max_length=10, null=True)),
                ('dtconcurso', models.DateField(blank=True, null=True)),
                ('classific', models.CharField(blank=True, max_length=5, null=True)),
                ('dtconcurs2', models.DateField(blank=True, null=True)),
                ('classific2', models.CharField(blank=True, max_length=5, null=True)),
                ('dtposse', models.DateField(blank=True, null=True)),
                ('contrato', models.CharField(blank=True, max_length=7, null=True)),
                ('tipdecreto', models.CharField(blank=True, max_length=1, null=True)),
                ('numdecreto', models.CharField(blank=True, max_length=10, null=True)),
                ('dtdecreto', models.DateField(blank=True, null=True)),
                ('matricfun', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=80, null=True)),
                ('tipoadmis', models.CharField(blank=True, max_length=1, null=True)),
                ('deficiente', models.CharField(blank=True, max_length=1, null=True)),
                ('formacao', models.CharField(blank=True, max_length=1, null=True)),
                ('fone2', models.CharField(blank=True, max_length=15, null=True)),
                ('fonecel', models.CharField(blank=True, max_length=15, null=True)),
                ('certmilit', models.CharField(blank=True, max_length=20, null=True)),
                ('cidvota', models.CharField(blank=True, max_length=40, null=True)),
                ('dtpispasep', models.DateField(blank=True, null=True)),
                ('raistrab', models.CharField(blank=True, max_length=2, null=True)),
                ('raiscor', models.CharField(blank=True, max_length=1, null=True)),
                ('tipamparo', models.CharField(blank=True, max_length=10, null=True)),
                ('numamparo', models.CharField(blank=True, max_length=10, null=True)),
                ('datamparo', models.DateField(blank=True, null=True)),
                ('pubamparo', models.DateField(blank=True, null=True)),
                ('tpreingres', models.CharField(blank=True, max_length=1, null=True)),
                ('exreingres', models.CharField(blank=True, max_length=1, null=True)),
                ('nureingres', models.CharField(blank=True, max_length=10, null=True)),
                ('dtreingres', models.DateField(blank=True, null=True)),
                ('pureingres', models.DateField(blank=True, null=True)),
                ('exampreing', models.CharField(blank=True, max_length=1, null=True)),
                ('nuampreing', models.CharField(blank=True, max_length=10, null=True)),
                ('dtampreing', models.DateField(blank=True, null=True)),
                ('puampreing', models.DateField(blank=True, null=True)),
                ('paramtcm', models.CharField(blank=True, max_length=10, null=True)),
                ('obsreserva', models.CharField(blank=True, max_length=150, null=True)),
                ('calcinss', models.CharField(blank=True, max_length=1, null=True)),
                ('calcirrf', models.CharField(blank=True, max_length=1, null=True)),
                ('calcprev', models.CharField(blank=True, max_length=1, null=True)),
                ('calcsalfam', models.CharField(blank=True, max_length=1, null=True)),
                ('regcons', models.CharField(blank=True, choices=[('CAU', 'CAU'), ('CFT', 'CFT'), ('CNV', 'CNV'), ('CONFEA', 'CONFEA'), ('COREN', 'COREN'), ('CRA', 'CRA'), ('CRB', 'CRB'), ('CRC', 'CRC'), ('CREA', 'CREA'), ('CREF', 'CREF'), ('CREFITO', 'CREFITO'), ('CREMEC', 'CREMEC'), ('CRESS', 'CRESS'), ('CRF', 'CRF'), ('CRM', 'CRM'), ('CRMV', 'CRMV'), ('CRN', 'CRN'), ('CRO', 'CRO'), ('CRP', 'CRP'), ('CRQ', 'CRQ'), ('CRSS', 'CRSS'), ('CRTR', 'CRTR'), ('OAB', 'OAB')], max_length=7, null=True)),
                ('numcons', models.CharField(blank=True, max_length=20, null=True)),
                ('numproc_pa', models.CharField(blank=True, max_length=12, null=True)),
                ('cpf_segurado', models.CharField(blank=True, max_length=11, null=True)),
                ('he1', models.CharField(blank=True, max_length=5, null=True)),
                ('he2', models.CharField(blank=True, max_length=5, null=True)),
                ('hs1', models.CharField(blank=True, max_length=5, null=True)),
                ('hs2', models.CharField(blank=True, max_length=5, null=True)),
                ('cong_ats', models.CharField(blank=True, choices=[('T', 'VERDADEIRO'), ('F', 'FALSO')], max_length=1, null=True)),
                ('dtprogress', models.DateField(blank=True, null=True)),
                ('msnccp', models.CharField(blank=True, max_length=100, null=True)),
                ('agregmatirrf', models.CharField(blank=True, max_length=1, null=True)),
                ('marcaserv', models.CharField(blank=True, max_length=1, null=True)),
                ('res_propria', models.CharField(blank=True, max_length=1, null=True)),
                ('tipo_defic', models.CharField(blank=True, max_length=4, null=True)),
                ('defic_fis', models.BooleanField(default=False)),
                ('defic_vis', models.BooleanField(default=False)),
                ('defic_ment', models.BooleanField(default=False)),
                ('defic_aud', models.BooleanField(default=False)),
                ('defic_intlec', models.BooleanField(default=False)),
                ('cota_def_hab_reab', models.BooleanField(default=False)),
                ('reabilitado', models.BooleanField(default=False)),
                ('tipo_defic_fis', models.CharField(blank=True, choices=[('1', 'CID 10 - G82 Paraplegia e tetraplegia'), ('2', 'CID 10 - G82.0 Paraplegia flácida'), ('3', 'CID 10 - G82.1 Paraplegia espástica'), ('4', 'CID 10 - G82.2 Paraplegia não especificada'), ('5', 'CID 10 - G82.3 Tetraplegia flácida'), ('6', 'CID 10 - G82.4 Tetraplegia espástica'), ('7', 'CID 10 - G82.5 Tetraplegia não especificada'), ('8', 'CID 10 - G83 Outras síndromes paralíticas'), ('9', 'CID 10 - G83.0 Diplegia dos membros superiores'), ('10', 'CID 10 - G83.1 Monoplegia do membro inferior'), ('11', 'CID 10 - G83.2 Monoplegia do membro superior'), ('12', 'CID 10 - G83.3 Monoplegia não especificada'), ('13', 'CID 10 - G83.4 Síndrome da cauda eqüina'), ('14', 'CID 10 - G83.8 Outras síndromes paralíticas especificadas'), ('15', 'CID 10 - G83.9 Síndrome paralítica não especificada'), ('16', 'CID 10 - G81 Hemiplegia'), ('17', 'CID 10 - G81 Hemiplegia'), ('18', 'CID 10 - G81.0 Hemiplegia flácida'), ('19', 'CID 10 - G81.1 Hemiplegia espástica'), ('20', 'CID 10 - G81.9 Hemiplegia não especificada'), ('21', 'CID 10 - S88 Amputação traumática da perna'), ('22', 'CID 10 - S88.0 Amputação traumática ao nível do joelho'), ('23', 'CID 10 - S88.1 Amputação traumática entre o joelho e o tornozelo'), ('24', 'CID 10 - S88.9 Amputação traumática da perna ao nível não especificado'), ('25', 'CID 10 - G80 Paralisia cerebral'), ('26', 'CID 10 - G80.0 Paralisia cerebral quadriplágica espástica'), ('27', 'CID 10 - G80.1 Paralisia cerebral diplégica espástica'), ('28', 'CID 10 - G80.2 Paralisia cerebral hemiplégica espástica'), ('29', 'CID 10 - G80.3 Paralisia cerebral discinética'), ('30', 'CID 10 - G80.4 Paralisia cerebral atáxica'), ('31', 'CID 10 - G80.8 Outras formas de paralisia cerebral'), ('32', 'CID 10 - G80.9 Paralisia cerebral não especificada'), ('33', 'CID 10 - Z93 Orifícios artificiais'), ('34', 'CID 10 - Z93.0 Traqueostomia'), ('35', 'CID 10 - Z93.1 Gastrostomia'), ('36', 'CID 10 - Z93.2 Ileostomia'), ('37', 'CID 10 - Z93.3 Colostomia'), ('38', 'CID 10 - Z93.4 Outros orifícios artificiais do trato gastrointestinal'), ('39', 'CID 10 - Z93.5 Cistostomia'), ('40', 'CID 10 - Z93.6 Outros orifícios artificiais do aparelho urinário'), ('41', 'CID 10 - Z93.8 Outros orifícios artificiais'), ('42', 'CID 10 - Z93.9 Orifício artificial não especificado')], max_length=2, null=True)),
                ('tipo_defic_vis', models.CharField(blank=True, choices=[('1', 'CID 10 - H53 Distúrbios visuais'), ('2', 'CID 10 - H53.0 Ambliopia por anopsia'), ('3', 'CID 10 - H53.1 Distúrbios visuais subjetivos'), ('4', 'CID 10 - H53.2 Diplopia'), ('5', 'CID 10 - H53.3 Outros transtornos da visão binocular'), ('6', 'CID 10 - H53.4 Defeitos do campo visual'), ('7', 'CID 10 - H53.5 Deficiências da visão cromática'), ('8', 'CID 10 - H53.6 Cegueira noturna'), ('9', 'CID 10 - H53.8 Outros distúrbios visuais'), ('10', 'CID 10 - H53.9 Distúrbio visual não especificado')], max_length=2, null=True)),
                ('tipo_defic_ment', models.CharField(blank=True, choices=[('1', 'CID 10 - Q99.2 Cromossomo X frágil'), ('2', 'CID 10 - Q90 Síndrome de Down'), ('3', 'CID 10 - Q90.0 Trissomia 21, não-disjunção meiótica'), ('4', 'CID 10 - Q90.1 Trissomia 21, mosaicismo (não-disjunção mitótica)'), ('5', 'CID 10 - Q90.2 Trissomia 21, translocação'), ('6', 'CID 10 - Q90.9 Síndrome de Down não especificada'), ('7', 'CID 10 - R62 Retardo do desenvolvimento fisiológico normal'), ('8', 'CID 10 - R62.0 Retardo de maturação'), ('9', 'CID 10 - R62.8 Outras formas de retardo do desenvolvimento fisiológico normal'), ('10', 'CID 10 - R62.9 Retardo do desenvolvimento fisiológico normal, não especificado')], max_length=2, null=True)),
                ('paisorigem', models.CharField(blank=True, max_length=40, null=True)),
                ('complemento', models.CharField(blank=True, max_length=20, null=True)),
                ('tempcontr', models.IntegerField(blank=True, null=True)),
                ('tpcontrato', models.CharField(blank=True, max_length=1, null=True)),
                ('gestprop', models.CharField(blank=True, choices=[('T', 'VERDADEIRO'), ('F', 'FALSO')], max_length=1, null=True)),
                ('und_fimcontr', models.CharField(blank=True, max_length=1, null=True)),
                ('dt_fimcontr', models.DateField(blank=True, null=True)),
                ('nome_segurado', models.CharField(blank=True, max_length=40, null=True)),
                ('codatuacao', models.CharField(blank=True, max_length=3, null=True)),
                ('transpessoal', models.CharField(blank=True, choices=[('T', 'VERDADEIRO'), ('F', 'FALSO')], max_length=1, null=True)),
                ('rneorgao', models.CharField(blank=True, max_length=20, null=True)),
                ('rnedataemi', models.DateField(blank=True, null=True)),
                ('dtchegadaestran', models.DateField(blank=True, null=True)),
                ('dtnaturalizacao', models.DateField(blank=True, null=True)),
                ('casadocombr', models.CharField(blank=True, max_length=1, null=True)),
                ('filhocombr', models.CharField(blank=True, max_length=1, null=True)),
                ('dtlaudodeficiente', models.DateField(blank=True, null=True)),
                ('tplogradouro', models.CharField(blank=True, max_length=50, null=True)),
                ('codibge_municipio', models.IntegerField(blank=True, null=True)),
                ('obs_manter', models.CharField(blank=True, choices=[('T', 'VERDADEIRO'), ('F', 'FALSO')], max_length=1, null=True)),
                ('instpensao_nome', models.CharField(blank=True, max_length=40, null=True)),
                ('instpensao_cpf', models.CharField(blank=True, max_length=11, null=True)),
                ('instpensao_matricula', models.CharField(blank=True, max_length=8, null=True)),
                ('instpensao_funcao', models.CharField(blank=True, max_length=3, null=True)),
                ('instpensao_natureza_cargo', models.CharField(blank=True, max_length=1, null=True)),
                ('categoria_situacao', models.CharField(blank=True, max_length=5, null=True)),
                ('dt_inicio_serv_pub', models.DateField(blank=True, null=True)),
                ('tp_cat_siop', models.CharField(blank=True, max_length=5, null=True)),
                ('cat_siop', models.CharField(blank=True, max_length=5, null=True)),
                ('estrangeiro', models.CharField(blank=True, choices=[('S', 'SIM'), ('N', 'NÃO')], max_length=1, null=True)),
                ('ocorrencia_gfip', models.CharField(blank=True, max_length=2, null=True)),
                ('qualifcadastral', models.CharField(blank=True, max_length=2, null=True)),
                ('anomes_criacao', models.CharField(blank=True, max_length=6, null=True)),
                ('dt_nomeacao_tcema', models.DateField(blank=True, null=True)),
                ('dt_instpensao_obito', models.DateField(blank=True, null=True)),
                ('parentesco_instpensao', models.CharField(blank=True, max_length=1, null=True)),
                ('obsfuncionais', models.TextField(blank=True, max_length=100, null=True)),
                ('inativacao_sagres_pe', models.CharField(blank=True, max_length=1, null=True)),
                ('siap_mot_cont_temp', models.CharField(blank=True, max_length=10, null=True)),
                ('siap_tipo_cont_temp', models.CharField(blank=True, max_length=10, null=True)),
                ('siap_veic_publicacao', models.CharField(blank=True, max_length=10, null=True)),
                ('siap_motivo_contratacao', models.CharField(blank=True, max_length=100, null=True)),
                ('eventoats', models.CharField(blank=True, max_length=2, null=True)),
                ('data_reintegracao', models.DateField(blank=True, null=True)),
                ('nome_social', models.CharField(blank=True, max_length=70, null=True)),
                ('maternidade13', models.CharField(blank=True, choices=[('T', 'VERDADEIRO'), ('F', 'FALSO')], max_length=1, null=True)),
                ('fechamento_individual', models.CharField(blank=True, choices=[('T', 'VERDADEIRO'), ('F', 'FALSO')], max_length=1, null=True)),
                ('nao_calc_patronal', models.CharField(blank=True, max_length=1, null=True)),
                ('estado_estrangeiro', models.CharField(blank=True, max_length=50, null=True)),
                ('cidade_estrangeiro', models.CharField(blank=True, max_length=50, null=True)),
                ('registro', models.JSONField(null=True)),
                ('banco', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='banco.bancos')),
                ('cdsecreta', models.ForeignKey(blank=True, limit_choices_to={'cdsetor': '000'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secretaria', to='SFP006.sfp006')),
                ('cdsecretaorigem', models.ForeignKey(blank=True, limit_choices_to={'cdsetor': '000'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secretaria_origem', to='SFP006.sfp006')),
                ('cdsetor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='setor', to='SFP006.sfp006')),
                ('cdsetororigem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='setor_origem', to='SFP006.sfp006')),
                ('cidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cidade', to='IBGE.municipios')),
                ('cidnasc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cidnasc', to='IBGE.municipios')),
                ('entidade', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='entidades.entidade')),
                ('funcao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SFP005.sfp005')),
                ('funcao2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funcao2', to='SFP005.sfp005')),
                ('sistema', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CFG_VINC.cfg_vinc')),
                ('tipoconta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='banco.tipoconta')),
                ('uf', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='uf_end', to='IBGE.uf')),
                ('ufcartprof', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='uf_cartprof', to='IBGE.uf')),
                ('ufcnh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ufcnh', to='IBGE.uf')),
                ('ufident', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='uf_ident', to='IBGE.uf')),
                ('ufnasc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='uf_nascimento', to='IBGE.uf')),
            ],
            options={
                'verbose_name': 'sfp001',
                'verbose_name_plural': 'Pessoas',
                'db_table': 'sfp001',
            },
        ),
        migrations.CreateModel(
            name='sfp017',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anobase', models.IntegerField(blank=True, null=True)),
                ('codfol', models.CharField(blank=True, choices=[('1', 'Afastamento'), ('2', 'Afastamento Aposnetadoria'), ('3', 'Aguardando Aposentadoria'), ('4', 'Auxílio Doença'), ('5', 'Disposição com Ônus'), ('6', 'Disposição sem Ônus'), ('7', 'Licença INSS'), ('8', 'Licença Maternidade'), ('9', 'Licença Medica'), ('10', 'Licença para Interesse Particular'), ('11', 'Licença para Tratamento de Saúde'), ('12', 'Licença Premio'), ('13', 'Licença sem Vencimento'), ('14', 'Licença Serviço Militar'), ('15', 'Demissão'), ('16', 'GESTOR'), ('17', 'Licença para Atividade Política'), ('18', 'Afastamento Preventivo - PAD'), ('19', 'Licença para Acompanhar Cônjuge')], max_length=2, null=True)),
                ('dtinicioafst', models.DateField(blank=True, null=True)),
                ('dtfimafst', models.DateField(blank=True, null=True)),
                ('obsafst', models.CharField(blank=True, max_length=150, null=True)),
                ('entidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidades.entidade')),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matricula_afast', to='SFP001.sfp001')),
            ],
            options={
                'verbose_name': 'SFP017',
                'verbose_name_plural': 'Afastementos',
                'db_table': 'sfp017',
            },
        ),
        migrations.CreateModel(
            name='RelatoriosCadastro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(blank=True, null=True)),
                ('qtde_importado', models.IntegerField()),
                ('qtde_editado', models.IntegerField()),
                ('qtde_finalizado', models.IntegerField()),
                ('entidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidades.entidade')),
            ],
            options={
                'db_table': 'relatorioscadastro',
            },
        ),
        migrations.CreateModel(
            name='Dependentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomedep', models.CharField(blank=True, max_length=100, null=True)),
                ('dependsocial', models.CharField(blank=True, max_length=1, null=True)),
                ('cpf_dependente', models.CharField(blank=True, max_length=11, null=True)),
                ('sexo', models.CharField(blank=True, choices=[('2', 'FEMININO'), ('1', 'MASCULINO')], max_length=1, null=True)),
                ('nascdep', models.DateField(blank=True, null=True)),
                ('parent', models.CharField(blank=True, choices=[('F', 'FILHO'), ('C', 'CÔNJUGE'), ('A', 'AVOS'), ('P', 'PAI'), ('M', 'MÃE'), ('I', 'FILHO INVÁLIDO'), ('E', 'NÃO ESPECIFICADO')], max_length=1, null=True)),
                ('identdepend', models.CharField(blank=True, max_length=20, null=True)),
                ('sus_numcartdep', models.CharField(blank=True, max_length=50, null=True)),
                ('sus_dtemissaodep', models.DateField(blank=True, null=True)),
                ('depir', models.BooleanField(blank=True, default=False, null=True)),
                ('depsf', models.BooleanField(blank=True, default=False, null=True)),
                ('incap_fisica', models.BooleanField(blank=True, default=False, null=True)),
                ('entidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidades.entidade')),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matricula_depen', to='SFP001.sfp001')),
            ],
            options={
                'verbose_name': 'Dependente',
                'verbose_name_plural': 'Dependentes',
                'db_table': 'dependente',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(blank=True, choices=[('1', 'LIVRE'), ('2', 'PROFISSIONALIZANTE'), ('3', 'TÉCNICO'), ('4', 'SUPERIOR SEQUENCIAL'), ('5', 'SUPERIOR TECNÓLOGO'), ('6', 'SUPERIOR GRADUAÇÃO'), ('7', 'PÓS GRAD. ESPECIALIZAÇÃO'), ('8', 'PÓS GRAD. MESTRADO'), ('9', 'DOUTORADO'), ('10', 'PÓS DOUTORADO')], max_length=2, null=True)),
                ('nomecurso', models.CharField(blank=True, max_length=60, null=True)),
                ('anobase', models.IntegerField(blank=True, null=True)),
                ('instituicao', models.CharField(blank=True, max_length=60, null=True)),
                ('carghora', models.CharField(blank=True, max_length=5, null=True)),
                ('dtiniciocurso', models.DateField(blank=True, null=True)),
                ('dtfimcurso', models.DateField(blank=True, null=True)),
                ('obscurso', models.CharField(blank=True, max_length=150, null=True)),
                ('entidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidades.entidade')),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matricula_curso', to='SFP001.sfp001')),
            ],
            options={
                'db_table': 'curso',
            },
        ),
    ]
