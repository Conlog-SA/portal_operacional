$(document).on('change','#unidade_check_emp',function(){
    let cod_unidade = $(this).val();
    $.ajax({
        type: 'GET',
        url: '/safety_gab_empilhadeira_app/empilhadeiras_filial',
        data: {
            'cod_unidade'   :   cod_unidade,
        },
        dataType: 'json',
        success: function (dados) {
            if (dados.lista_empilhadeiras.length > 0) {
                $('#placa_empilhadeira_emp').prop('disabled',false);
                $('#placa_empilhadeira_emp option').remove();
                dados.lista_empilhadeiras.forEach(emp => {
                    $("#placa_empilhadeira_emp").append("<option value='"+
                    emp.cod_emp+"'>"+emp.placa+"</option>");
                });
                $('#placa_empilhadeira_emp').selectpicker('refresh');

            }
            else {
                $('#unidade_check_emp').val('');
                $('#unidade_check_emp').selectpicker('refresh');
                $('#placa_empilhadeira_emp').val('');
                $('#placa_empilhadeira_emp').prop('disabled',true);
                $('#placa_empilhadeira_emp').selectpicker('refresh');
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


});

$(document).on('click','.create-check-equipamento-empilhadeira' , function(){
    let let_unidade_check_equipamentos_emp = $('#unidade_check_emp').val();
    let let_cod_equipamentos_empilhadeira = $('#placa_empilhadeira_emp').val();

    msg_erro = '';

    if (let_unidade_check_equipamentos_emp == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_cod_equipamentos_empilhadeira == '') {
        msg_erro += 'Selecione uma empilhadeira!';
    }

    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_gab_empilhadeira_app/empilhadeira_check',
            data: {
                'unidade_operador'   :   let_unidade_check_equipamentos_emp,
                'cod_empilhadeira'   :   let_cod_equipamentos_empilhadeira,
            },
            success: function (dados) {
                $("#div_corpo_gab_empilhadeira_emp").html(dados);
                $("#div_corpo_gab_empilhadeira_emp").css('background-color', 'rgba(0,0,0,0)')
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


