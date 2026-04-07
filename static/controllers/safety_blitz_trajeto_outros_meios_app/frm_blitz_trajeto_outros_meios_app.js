$(document).on('click','.create-check-blitz-trajeto-outros_meios' , function(){
    let let_unidade_avaliado_outros_meios = $('#unidade_colaborador_outros_meios').val();
    let let_situacao_avaliado_outros_meios = $('#situacao_avaliado_outros_meios').val();
    let let_meio_transporte_outros_meios = $('#meio_transporte').val();
    let let_nome_avaliado_outros_meios = "";

    if (let_situacao_avaliado_outros_meios == '1') {
        let_nome_avaliado_outros_meios = $('#nome_avaliado_outros_meios').val();
    }
    else if (let_situacao_avaliado_outros_meios == '2' || let_situacao_avaliado_outros_meios == '3' || let_situacao_avaliado_outros_meios == '4') {
        let_nome_avaliado_outros_meios = $('#nome_avaliado_terceiro_outros_meios').val();
    }


    msg_erro = '';
    if (let_unidade_avaliado_outros_meios == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_situacao_avaliado_outros_meios == '') {
        msg_erro += 'Informe a situação do avaliado!<br>';
    }
    if (let_nome_avaliado_outros_meios == '') {
        msg_erro += 'Informe o nome do avaliado!<br>';
    }
    if (let_meio_transporte_outros_meios == '') {
        msg_erro += 'Informe o meio de transporte!<br>';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_blitz_trajeto_outros_meios_app/blitz_trajeto_outros_meios_check',
            data: {
                'unidade_avaliado'   :   let_unidade_avaliado_outros_meios,
                'situacao_avaliado'  :  let_situacao_avaliado_outros_meios,
                'nome_avaliado'   :   let_nome_avaliado_outros_meios,
                'meio_transporte' :   let_meio_transporte_outros_meios
            },
            success: function (dados) {
                $("#div_corpo_relato_blitz_trajeto").html(dados);
                $("#div_corpo_relato_blitz_trajeto").css('background-color', 'rgba(0,0,0,0)')
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

$(document).on('change','#situacao_avaliado_outros_meios',function(){
    let let_cod_unidade = $('#unidade_colaborador_outros_meios').val();
    if (let_cod_unidade != '') {
        if ($(this).val() == '1') {
            $.ajax({
                type: 'GET',
                url: '/safety_login_colaboradores_app/lista_colaboradores',
                data: {
                    'cod_unidade'   :   let_cod_unidade,
                    'tipo_check'    :   '7'
                },
                dataType: 'json',
                success: function (dados) {
                    console.log(dados);
                    $('#nome_avaliado_outros_meios option').remove();
                    dados.lista_colaboradores.forEach(operacao => {
                        $("#nome_avaliado_outros_meios").append("<option value='"+
                        operacao.cod_colaborador+"'>"+operacao.nome_colaborador+" (" + operacao.desc_cargo+")</option>");
                    });
                    if ($('#nome_avaliado_outros_meios option').length == 0) {
                        $('#situacao_avaliado_outros_meios').val("4");
                        $('#situacao_avaliado_outros_meios').selectpicker('refresh');
                        $('#situacao_avaliado_outros_meios').trigger('change');

                        $.gritter.add({
                            title: 'Erro!',
                            text: 'Não foram encontrados colaboradores para a unidade selecionada!',
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                    } else {
                        $('#nome_avaliado_outros_meios').prop('disabled',false);
                        $('#div_avaliado_outros_meios').removeClass('hidden-div');
                        $('#nome_avaliado_outros_meios').selectpicker('refresh');
                        $('#div_avaliado_terceiro_outros_meios').addClass('hidden-div');
                        $('#nome_avaliado_terceiro_outros_meios').val('');
                    };
                }
            });
        }
    }
    else {
        $('#situacao_avaliado_outros_meios').val('');
        $('#situacao_avaliado_outros_meios').selectpicker('refresh');

        $.gritter.add({
            title: 'Atenção!',
            text: 'Selecione a unidade primeiro!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }

    if ($(this).val() == '2' || $(this).val() == '3' || $(this).val() == '4') {
        $('#div_avaliado_terceiro_outros_meios').removeClass('hidden-div');
        $('#div_avaliado_outros_meios').addClass('hidden-div');
        $('#nome_avaliado_outros_meios').val('');
        $('#nome_avaliado_outros_meios').selectpicker('refresh');
    }


});
