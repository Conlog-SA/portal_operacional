$(document).on('click','.create-check-gsdpq' , function(){
    let let_unidade_freteiro = $('#unidade_freteiro').val();
    let let_nome_freteiro = $('#nome_freteiro').val();
    let let_cpf_freteiro = $('#cpf_freteiro').val();
    let let_placa_caminhao = $('#placa_caminhao').val();

    msg_erro = '';
    if (let_unidade_freteiro == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_nome_freteiro == '') {
        msg_erro += 'Informe o nome do freteiro!<br>';
    }

    if (let_cpf_freteiro == '') {
        msg_erro += 'Informe o CPF do freteiro!<br>';
    }
    else if (let_cpf_freteiro.length != 11) {
        msg_erro += 'CPF Inválido, deve ter 11 digitos!<br>';
    }
    else if (isNaN(let_cpf_freteiro)) {
        msg_erro += 'CPF Inválido, apenas números!<br>';
    }

    if (let_placa_caminhao == '') {
        msg_erro += 'Informe a placa do caminhão!';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_gsdpq_app/gsdpq_check',
            data: {
                'unidade_freteiro'   :   let_unidade_freteiro,
                'nome_freteiro'   :   let_nome_freteiro,
                'cpf_freteiro'   :   let_cpf_freteiro,
                'placa_caminhao'   :   let_placa_caminhao
            },
            success: function (dados) {
                $("#div_corpo_gsdpq").html(dados);
                $("#div_corpo_gsdpq").css('background-color', 'rgba(0,0,0,0)')
            },
            error: function (xhr, status, error) {
                 $.gritter.add({
                    title: 'Erro!',
                    text: xhr.responseText,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    }
    else {
        $.gritter.add({
            title: 'Erro!',
            text: msg_erro,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });

    }
});


