$(document).on('change','.selectpicker',function(){
    let nome_select = $(this).attr('name');

    if (nome_select == "tipo_operador") {
        let cod_resposta = $(this).val();
        let let_unidade = $('#unidade_operador').val();
        console.log(let_unidade)
        if (let_unidade == "") {
            $('#tipo_operador').val('');
            $('#tipo_operador').selectpicker('refresh');
            $.gritter.add({
                title: 'Erro!',
                text: 'Selecione uma filial!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
        else if (cod_resposta == 1) {
            if ($('#nome_operador option').length == 1) {
                $('#tipo_operador').val("2");
                $('#tipo_operador').selectpicker('refresh');
                $('#tipo_operador').trigger('change');

                $.gritter.add({
                    title: 'Erro!',
                    text: 'Não foram encontrados colaboradores para a unidade selecionada!',
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            } else {
                $('#div_operador').removeClass('hidden-div');
                $('#div_operador_terceiro').addClass('hidden-div');
                $('#nome_operador_terceiro').val('');
                $('#nome_operador').prop('disabled',false);
                $('#nome_operador').selectpicker('refresh');

                $('#documento_operador').val('');
                $('#documento_operador').prop('disabled',true);
            }
        }
        else if (cod_resposta == 2) {
            $('#div_operador').addClass('hidden-div');
            $('#div_operador_terceiro').removeClass('hidden-div');
            $('#nome_operador').val('');
            $('#nome_operador').selectpicker('refresh');

            $('#documento_operador').val('');
            $('#documento_operador').prop('disabled',false);
        }
    }
    if (nome_select == "modelo_empilhadeira") {
        let cod_empilhadeira = $(this).val();
            $.ajax({
                type: 'GET',
                url: '/safety_gab_op_emp_app/operacao_empilhadeira',
                data: {
                    'cod_empilhadeira'   :   cod_empilhadeira,
                },
                dataType: 'json',
                success: function (dados) {
                    $('#tipo_operacao option').remove();
                    dados.lista_operacao.forEach(operacao => {
                        $("#tipo_operacao").append("<option value='"+
                        operacao.cod_tipo_operacao_emp+"'>"+operacao.desc_tipo_operacao_desc+"</option>");
                    });
                    $('#tipo_operacao').selectpicker('refresh');
                    $('#main_container_safety').css('width', '100%');
                }
            });
    }
    if (nome_select == "unidade_operador") {
        let cod_unidade = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/safety_gab_op_emp_app/empilhadeiras_filial',
            data: {
                'cod_unidade'   :   cod_unidade,
            },
            dataType: 'json',
            success: function (dados) {
                if (dados.lista_empilhadeiras.length > 0) {
                    $('#placa_empilhadeira').prop('disabled',false);
                    $('#placa_empilhadeira option').remove();
                    dados.lista_empilhadeiras.forEach(emp => {
                        $("#placa_empilhadeira").append("<option value='"+
                        emp.cod_emp+"'>"+emp.placa+"</option>");
                    });
                    $('#placa_empilhadeira').selectpicker('refresh');

                    $.ajax({
                        type: 'GET',
                        url: '/safety_login_colaboradores_app/lista_colaboradores',
                        data: {
                            'cod_unidade'   :   cod_unidade,
                        },
                        dataType: 'json',
                        success: function (dados) {
                            console.log(dados)
                            $('#nome_operador option').remove();
                            dados.lista_colaboradores.forEach(operacao => {
                                $("#nome_operador").append("<option value='"+
                                operacao.cod_colaborador+"'>"+operacao.nome_colaborador+" (" + operacao.desc_cargo+")</option>");
                            });

                            $('#nome_operador').selectpicker('refresh');
                            $('#tipo_operador').trigger('change');
                        }
                    });
                }
                else {
                    $('#unidade_operador').val('');
                    $('#unidade_operador').selectpicker('refresh');
                    $('#tipo_operador').val('');
                    $('#tipo_operador').selectpicker('refresh');
                    $('#placa_empilhadeira').val('');
                    $('#placa_empilhadeira').prop('disabled',true);
                    $('#placa_empilhadeira').selectpicker('refresh');
                    $.gritter.add({
                        title: 'Erro!',
                        text: 'Sem empilhadeiras cadastradas nesta filial.',
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }

            }
        });
    }
    if (nome_select == "nome_operador") {
        $('#documento_operador').val('');
        let cod_colaborador = $('#nome_operador').val();
        $.ajax({
            type: 'GET',
            url: '/safety_login_colaboradores_app/documento_colaborador',
            data: {
                'cod_colaborador'   :   cod_colaborador,
            },
            dataType: 'json',
            success: function (dados) {
                $('#documento_operador').val(dados);
            }
        });
    }
});

$(document).on('click','.create-check' , function(){
    let let_unidade_operador = $('#unidade_operador').val();
    let let_tp_operador = $('#tipo_operador').val();
    let let_nome_operador = null;
    if (let_tp_operador == '1') {
        let_nome_operador = $('#nome_operador').val();
    }
    else if (let_tp_operador == '2') {
        let_nome_operador = $('#nome_operador_terceiro').val();
    }

    let let_doc_operador = $('#documento_operador').val();
    let let_cod_empilhadeira = $('#placa_empilhadeira').val();
    let let_tp_operacao = $('#tipo_operacao').val();

    msg_erro = '';
    if (let_unidade_operador == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_tp_operador == '') {
        msg_erro += 'Selecione um tipo para o operador!<br>';
    }
    if (let_nome_operador == '' || let_nome_operador == null) {
        msg_erro += 'Informe o nome do operador!<br>';
    }

    if (let_doc_operador == '') {
        msg_erro += 'Informe o CPF do operador!<br>';
    }
    else if (let_doc_operador.length != 11) {
        msg_erro += 'CPF Inválido, deve ter 11 digitos!<br>';
    }
    else if (isNaN(let_doc_operador)) {
        msg_erro += 'CPF Inválido, apenas números!<br>';
    }

    if (let_cod_empilhadeira == '') {
        msg_erro += 'Selecione uma empilhadeira!';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_gab_op_emp_app/empilhadeira_check',
            data: {
                'unidade_operador'   :   let_unidade_operador,
                'tipo_operador'   :   let_tp_operador,
                'nome_operador'   :   let_nome_operador,
                'documento_operador'   :   let_doc_operador,
                'cod_empilhadeira'   :   let_cod_empilhadeira,
            },
            success: function (dados) {
                $("#div_corpo_gab_op_emp").html(dados);
                $("#div_corpo_gab_op_emp").css('background-color', 'rgba(0,0,0,0)')
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

$(document).on('click','.btn-voltar-menu-safety' , function(){
    $.ajax({
        type: 'POST',
        url: '/safety_login_colaboradores_app/safe_login_colab',
        data: {
                    'flag_voltar'      :   1,
                 },
        success: function (dados) {
            $('#main_container_safety').html(dados);
            $('#main_container_safety').removeClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal');
            $('#main_container_safety').addClass('safety-container-screen text-white justify-content-center align-items-center d-flex homeApp_loginContainer');
            $('#main_container_safety').css('width', '85%');

        }
    });
});

