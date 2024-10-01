const $select = document.getElementById('id_tipo_pessoa')

function tipo_pessoa() {
    if ($select.value == "1") {
        document.getElementById("numero_inscricao").children[0].innerHTML = "CPF";
        document.getElementById("nome-razao").children[0].innerHTML = "Nome"
        $('#id_numero_inscricao').unmask().mask('000.000.000-00');
        document.getElementById('id_numero_inscricao').setAttribute('data-mask', '000.000.000-00')
    } else {
        document.getElementById("numero_inscricao").children[0].innerHTML = "CNPJ";
        document.getElementById("nome-razao").children[0].innerHTML = "Razão social"
        $('#id_numero_inscricao').unmask().mask('00.000.000/0000-00');
        document.getElementById('id_numero_inscricao').removeAttribute('data-mask')
        document.getElementById('id_numero_inscricao').setAttribute('data-mask', '00.000.000/0000-00')
    }
}

$select.addEventListener('input', tipo_pessoa)