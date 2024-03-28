$(document).on('change','.selectpicker',function(){
    let nome_select = $(this).attr('name');
    console.log(nome_select)
    if (nome_select == "tipo_operador") {
        let cod_resposta = $(this).val();
        if (cod_resposta == 1) {
            $('#div_operador').removeClass('hidden-div');
            $('#div_operador_terceiro').addClass('hidden-div');
            $('#nome_operador_terceiro').val('');

            $('#documento_operador').val('');
            $('#documento_operador').prop('disabled',true);
        }
        if (cod_resposta == 2) {
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
                        operacao.cod_colaborador+"'>"+operacao.nome_colaborador+"</option>");
                    });

                    $('#nome_operador').prop('disabled',false);
                    $('#nome_operador').selectpicker('refresh');
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
    let let_model_empilhadeira = $('#modelo_empilhadeira').val();
    let let_tp_operacao = $('#tipo_operacao').val();
    console.log(let_nome_operador);
    $.ajax({
        type: 'POST',
        url: '/safety_gab_op_emp_app/empilhadeira_check',
        data: {
            'unidade_operador'   :   let_unidade_operador,
            'tipo_operador'   :   let_tp_operador,
            'nome_operador'   :   let_nome_operador,
            'documento_operador'   :   let_doc_operador,
            'modelo_empilhadeira'   :   let_model_empilhadeira,
            'tipo_operacao'   :   let_tp_operacao
        },
        success: function (dados) {
            $("#div_corpo_gab_op_emp").html(dados);
            $("#div_corpo_gab_op_emp").css('background-color', 'rgba(0,0,0,0)')
        }
    });
});

$(document).on('click','.btn-voltar-menu-safety' , function(){
    $.ajax({
        type: 'POST',
        url: '/safety_login_colaboradores_app/safe_login_colab',
        success: function (dados) {
            $('#main_container_safety').html(dados);
            $('#main_container_safety').removeClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal');
            $('#main_container_safety').addClass('safety-container-screen text-white justify-content-center align-items-center d-flex homeApp_loginContainer');
            $('#main_container_safety').css('width', '85%');

        }
    });
});

