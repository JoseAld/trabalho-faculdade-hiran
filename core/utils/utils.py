from io import BytesIO

from django.core.exceptions import ValidationError
import re
import pycep_correios
from pycep_correios.excecoes import ExcecaoPyCEPCorreios
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

def valida_cpf(cpf):
    if cpf.isdigit() == False:
        raise ValidationError('Cpf deve conter apenas números: %s' % cpf)

    if len(cpf) != 11:
        raise ValidationError('Tamanho do cpf inválido: %s' % cpf)

    cpf_invalidos = [11 * str(i) for i in range(10)]
    if cpf in cpf_invalidos:
        raise ValidationError('CPF inválido')

    self_cpf = [int(x) for x in cpf]
    cpf_lista = self_cpf[:9]

    while len(cpf_lista) < 11:
        r = sum([(len(cpf_lista) + 1 - i) * v for i, v in [(x, cpf_lista[x]) for x in range(len(cpf_lista))]]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0

        cpf_lista.append(f)

    if not (cpf_lista == self_cpf):
        raise ValidationError('CPF inválido')
    else:
        return True


def validar_cnpj(cnpj):
    """
    Valida CNPJs, retornando apenas a string de números válida.

    # CNPJs errados
    >>> validar_cnpj('abcdefghijklmn')
    False
    >>> validar_cnpj('123')
    False
    >>> validar_cnpj('')
    False
    >>> validar_cnpj(None)
    False
    >>> validar_cnpj('12345678901234')
    False
    >>> validar_cnpj('11222333000100')
    False

    # CNPJs corretos
    >>> validar_cnpj('11222333000181')
    '11222333000181'
    >>> validar_cnpj('11.222.333/0001-81')
    '11222333000181'
    >>> validar_cnpj('  11 222 333 0001 81  ')
    '11222333000181'
    """
    cnpj = ''.join(re.findall('\d', str(cnpj)))

    cnpj = cnpj.replace('.', '')
    cnpj = cnpj.replace('/', '')
    cnpj = cnpj.replace('-', '')

    if (not cnpj) or (len(cnpj) < 14) or (cnpj == '0' * 14) or (cnpj == '1' * 14) \
            or (cnpj == '2' * 14) or (cnpj == '3' * 14) \
            or (cnpj == '4' * 14) or (cnpj == '5' * 14) \
            or (cnpj == '6' * 14) or (cnpj == '7' * 14) \
            or (cnpj == '8' * 14) or (cnpj == '9' * 14):
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = [int(pi) for pi in cnpj]
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    return (novo == inteiros)


def validar_cep(cep):
    try:
        return pycep_correios.consultar_cep(cep)
    except ExcecaoPyCEPCorreios as exc:
        raise ValidationError("CEP %s inválido" % cep)


def mes_extenso(mes):
    if mes == 12:
        return 'Dezembro'
    elif mes == 11:
        return 'Novembro'
    elif mes == 10:
        return 'Outubro'
    elif mes == 9:
        return 'Setembro'
    elif mes == 8:
        return 'Agosto'
    elif mes == 7:
        return 'Julho'
    elif mes == 6:
        return 'Junho'
    elif mes == 5:
        return 'Maio'
    elif mes == 4:
        return 'Abril'
    elif mes == 3:
        return 'Março'
    elif mes == 2:
        return 'Fevereiro'
    elif mes == 1:
        return 'Janeiro'


def ImagetoString(filename):
    with open(filename, 'rb') as image_file:
        # Converte o arquivo em um array de bytes
        base64_bytes = base64.b64encode(image_file.read())
        # Converte o Array de bytes em uma string
        base64_string = base64_bytes.decode()
        return base64_string


def StringtoImage(filename, base64_string):
    with open(filename, 'wb') as filename_wr:
        filename_wr.write(base64.decodebytes(base64_string))


# Retornar arquivo em memoria
def base64_to_image(base64_string):
  byte_data = base64.b64decode(base64_string)
  content_type = "image/png"
  filename = "image.png"
  return InMemoryUploadedFile(
    BytesIO(byte_data),
    filename,
    content_type,
    len(byte_data),
  )