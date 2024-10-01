from django.db import models


# Create your models here.


class Entidade(models.Model):
    codigo_entidade = models.IntegerField('Código da entidades')
    cnpj = models.CharField('CNPJ', max_length=14)
    razao = models.CharField(max_length=100)
    fone = models.CharField('Telefone', max_length=11)
    fax = models.CharField(max_length=11)
    email = models.EmailField('E-mail', max_length=100, unique=True)
    cep = models.CharField('CEP', max_length=8)
    logradouro = models.CharField(max_length=60)
    log_numero = models.CharField('Número', max_length=5)
    complemento = models.CharField(null=True, blank=True, max_length=40)
    bairro = models.CharField(max_length=40)
    cidade = models.CharField(max_length=40)
    estado = models.CharField(max_length=50, null=True, blank=True)
    brasao = models.ImageField(upload_to='logos/', null=True, blank=True)
    arqv_importacao = models.FileField(upload_to='arqv_importacao/', null=True, blank=True)
    entidade_ativo = models.BooleanField('Ativo', default=True)

    def formatar(self):
        fone = f'({self.fone[:2]}){self.fone[2:6]}-{self.fone[6:]}'
        fax = f'({self.fax[:2]}){self.fax[2:6]}-{self.fax[6:]}'
        cnpj = f'{self.cnpj[:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:]}'
        cep = f'{self.cep[:2]}.{self.cep[2:5]}-{self.cep[5:]}'
        return {'fone': fone, 'fax': fax, 'cnpj': cnpj, 'cep': cep}

    def __str__(self):
        return '{}'.format(self.razao)
