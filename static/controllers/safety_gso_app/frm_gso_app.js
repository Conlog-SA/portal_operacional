$(document).on('click','.create-check-gso' , function(){
    let let_unidade_avaliado_gso = $('#unidade_avaliado_gso').val();
    let let_cod_motorista_avaliado_gso = $('#nome_avaliado_gso').val();
    let let_placa_onibus_gso = $('#placa_onibus_gso').val();

    msg_erro = '';
    if (let_unidade_avaliado_gso == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_cod_motorista_avaliado_gso == '') {
        msg_erro += 'Selecione o motorista!<br>';
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
                'cod_motorista_avaliado_gso'   :   let_cod_motorista_avaliado_gso,
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

$(document).on('change','#unidade_avaliado_gso',function(){
    let let_cod_unidade = $(this).val();
    if (let_cod_unidade != '') {
        $.ajax({
            type: 'GET',
            url: '/safety_login_colaboradores_app/lista_colaboradores',
            data: {
                'cod_unidade'   :   let_cod_unidade,
                'tipo_check'    :   '8'
            },
            dataType: 'json',
            success: function (dados) {
                $('#nome_avaliado_gso option').remove();
                dados.lista_colaboradores.forEach(operacao => {
                    $("#nome_avaliado_gso").append("<option value='"+
                    operacao.cod_colaborador+"'>"+operacao.nome_colaborador+" (" + operacao.desc_cargo+")</option>");
                });
                if ($('#nome_avaliado_gso option').length == 0) {
                    $(this).val('');
                    $(this).selectpicker('refresh');
                    $(this).trigger('change');

                    $.gritter.add({
                        title: 'Erro!',
                        text: 'Não foram encontrados colaboradores para a unidade selecionada!',
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                } else {
                    $('#nome_avaliado_gso').prop('disabled',false);
                    $('#nome_avaliado_gso').selectpicker('refresh');
                };
            }
        });
    }
    else {
        $.gritter.add({
            title: 'Atenção!',
            text: 'Selecione a unidade primeiro!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }
});
