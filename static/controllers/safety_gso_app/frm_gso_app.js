$(document).on('click','.create-check-gso' , function(){
    let let_unidade_avaliado_gso = $('#unidade_avaliado_gso').val();
    let let_nome_avaliado_gso = $('#nome_avaliado_gso').val();
    let let_placa_onibus_gso = $('#placa_onibus_gso').val();

    msg_erro = '';
    if (let_unidade_avaliado_gso == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_nome_avaliado_gso == '') {
        msg_erro += 'Informe o nome do motorista!<br>';
    }

    if (let_placa_onibus_gso == '') {
        msg_erro += 'Informe a placa do caminhão!';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_gso_app/gso_check',
            data: {
                'unidade_avaliado_gso'   :   let_unidade_avaliado_gso,
                'nome_avaliado_gso'   :   let_nome_avaliado_gso,
                'placa_onibus_gso'   :   let_placa_onibus_gso
            },
            success: function (dados) {
                $("#div_corpo_gso").html(dados);
                $("#div_corpo_gso").css('background-color', 'rgba(0,0,0,0)')
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


