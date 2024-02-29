$(document).on('change','.selectpicker',function(){
    let nome_select = $(this).attr('name');
    console.log(nome_select)
    if (nome_select == "tipo_operador") {
        let cod_resposta = $(this).val();
        if (cod_resposta == 1) {
            $.ajax({
                type: 'GET',
                url: '/safety_gab_op_emp_app/operador_colaborador',
                dataType: 'json',
                success: function (dados) {
                    console.log(dados)
                    $('#unidade_operador').val(dados.filial_colaborador);
                    $('#nome_operador').val(dados.nome_colaborador);
                    $('#unidade_operador').prop('disabled',true);
                    $('#nome_operador').prop('disabled',true);
                }
            })
        }
        if (cod_resposta == 2) {
            $('#unidade_operador').val('');
            $('#nome_operador').val('');
            $('#unidade_operador').prop('disabled',false);
            $('#nome_operador').prop('disabled',false);
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
                    console.log(dados)
                    $('#tipo_operacao option').remove();
                    dados.lista_operacao.forEach(operacao => {
                        $("#tipo_operacao").append("<option value='"+
                        operacao.cod_tipo_operacao_emp+"'>"+operacao.desc_tipo_operacao_desc+"</option>");
                    });
                    $('#tipo_operacao').selectpicker('refresh');
                }
            });
    }
});

$(document).on('click','.create-check' , function(){
    let let_unidade_operador = $('#unidade_operador').val();
    let let_tp_operador = $('#tipo_operador').val();
    let let_nome_operador = $('#nome_operador').val();
    let let_doc_operador = $('#documento_operador').val();
    let let_model_empilhadeira = $('#modelo_empilhadeira').val();
    let let_tp_operacao = $('#tipo_operacao').val();

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
        }
    });
});


