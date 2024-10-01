from django import template

register = template.Library()

@register.filter
def valida_null(valor):
    if valor:
        return valor
    return ""

@register.filter
def divisao_inteira(valor, total_de_elementos):
    print(valor)
    if (valor + 1) % 20 == 0 and (valor + 1) < total_de_elementos:
        return True
    else:
        return False


@register.filter
def divisao_listagem_funcionario(valor, total_de_elementos):
    print(valor)
    if (valor + 1) % 16 == 0 and (valor + 1) < total_de_elementos:
        return True
    else:
        return False


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.pop('page', None)
    query.update(kwargs)
    return query.urlencode()
