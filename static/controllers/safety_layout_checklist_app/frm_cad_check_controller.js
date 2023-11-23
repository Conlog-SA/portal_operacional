$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if ( nomeDoButton == 'btn_new_check' ) {

        let valPickerCheckExistente = $("#modelos_existentes").val();
        let valDescricao = $("#descricao_new_check").val();
        let valVersao = $("#versao_new_check").val();
        let valDesativar = $("#desativar_new_check_date").val();
        let valMedidaPeriodicidade = $("#medida_periodicidade_new_check").val();
        let valPeriodicidade = $("#periodicidade_new_check").val();

        $.ajax({
            type:"POST",
            url: '/safety_layout_checklist_app/registra_check',
            dataType: 'json',
            data: {
                'desc_check'     :   valDescricao,
                'versao'         :   valVersao,
                'data_desativacao'     :   valDesativar,
                'medida_periodicidade'         :   valMedidaPeriodicidade,
                'periodicidade'         :   valPeriodicidade,
             },
            success: function (data) {
                $('#modelos_existentes').selectpicker('refresh')
            },
            error: function (request, status, error) {

            }
        });
    }

    else if ( nomeDoButton == 'btn_reset_check' ) {
        $('#modelos_existentes').val('');
        $('#modelos_existentes').selectpicker('refresh')

        $('#descricao_new_check').val('');
        $('#versao_new_check').val('');
        $('#desativar_new_check_date').val('');
        $('#medida_periodicidade_new_check').val('');
        $('#medida_periodicidade_new_check').selectpicker('refresh')
        $('#periodicidade_new_check').val('');
        $('#btn_reset_check').attr("hidden",true);
        $('#btn_new_check').text('Criar Check');
        $('#btn_new_check').prepend('<i class="fa-solid fa-folder-plus" style="margin-right:5px"></i>')
    }
});

$(document).on('change','.selectpicker',function(){
    let nome_select = $(this).attr('name');
    console.log($(this).attr('name'))
    if (nome_select == "modelos_existentes") {
        let cod_check = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/safety_layout_checklist_app/registra_check',
            data: {
                'cod_check'   :   cod_check,
            },
            dataType: 'json',
            success: function (dados) {
                console.log(dados.check_selecionado.data_desativacao)
                let data_retorno = new Date(dados.check_selecionado.data_desativacao)

                let day = ("0" + data_retorno.getDate()).slice(-2);

                mes_desativacao = data_retorno.getMonth();
                let month = 0;
                if (mes_desativacao < 9) {
                    month = ("0" + (mes_desativacao + 1));
                }
                else if (mes_desativacao >= 9) {
                    month = mes_desativacao + 1;
                }

                let today = data_retorno.getFullYear()+"-"+(month)+"-"+(day);

                $('#descricao_new_check').val(dados.check_selecionado.desc_check);
                $('#versao_new_check').val(dados.check_selecionado.versao);
                $('#desativar_new_check_date').val(today);
                $('#medida_periodicidade_new_check').val(dados.check_selecionado.medida_periodicidade);
                $('#medida_periodicidade_new_check').selectpicker('refresh')
                $('#periodicidade_new_check').val(dados.check_selecionado.periodicidade);
                $('#btn_new_check').text("Editar Check");
                $('#btn_new_check').prepend('<i class="fa-solid fa-file-export" style="margin-right:5px"></i>')
                $('#btn_reset_check').attr("hidden",false);


                console.log(dados);
            }
        });
    }
});