$(document).on('click','.create-check-predial' , function(){
    let unidade = $('#unidade').val();
    let cod_area = $('#area_check').val();

    msg_erro = '';
    if (unidade == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (cod_area == '') {
        msg_erro += 'Selecione a área!<br>';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_predial_app/predial_check',
            data: {
                'filial'   :   unidade,
                'cod_area'   :   cod_area
            },
            success: function (dados) {
                $("#div_corpo_predial").html(dados);
                $("#div_corpo_predial").css('background-color', 'rgba(0,0,0,0)')
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