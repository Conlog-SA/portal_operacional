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
                'cod_check'      :   valPickerCheckExistente,
                'desc_check'     :   valDescricao,
                'versao'         :   valVersao,
                'data_desativacao'     :   valDesativar,
                'medida_periodicidade'         :   valMedidaPeriodicidade,
                'periodicidade'         :   valPeriodicidade
             },
            success: function (data) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                if (data.novo_check == true) {
                    $("#modelos_existentes").append("<option selected='true' value='"+
                            data.cod_check+"'>"+data.desc_check+"</option>");
                    $("#modelos_existentes").val(data.cod_check);
                }
                else {
                    $("#modelos_existentes").find(":selected").text(data.desc_check)
                }
                $('#modelos_existentes').selectpicker('refresh');
                $("#modelos_existentes").trigger("change");
            },
            error: function (request, status, error) {
			    $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    }

    else if ( nomeDoButton == 'btn_reset_check' ) {
        $('#modelos_existentes').val('');
        $('#modelos_existentes').selectpicker('refresh');

        $('#descricao_new_check').val('');
        $('#versao_new_check').val('');
        $('#desativar_new_check_date').val('');
        $('#medida_periodicidade_new_check').val('');
        $('#medida_periodicidade_new_check').selectpicker('refresh')
        $('#periodicidade_new_check').val('');
        $('#btn_reset_check').attr("hidden",true);
        $('#btn_new_check').text('Criar Check');
        $('#btn_new_check').prepend('<i class="fa-solid fa-folder-plus" style="margin-right:5px"></i>')
        $('#liberado_filiais option').remove();
        $('#liberado_filiais').selectpicker('refresh')

        $('#descricao_item_check').val('');
        $('#descricao_item_check').prop('disabled',true);
        $('#select_tipo_item').val('');
        $('#select_tipo_item').prop('disabled',true);
        $('#select_tipo_resposta').val('');
        $('#select_tipo_item').selectpicker('refresh');
        $('#select_tipo_resposta').prop('disabled',true);
        $('#select_tipo_resposta').selectpicker('refresh');
        $('#input_ordem_check').val('');
        $('#input_ordem_check').prop('disabled',true);
        $('#desativar_item_date').val('');
        $('#desativar_item_date').prop('disabled',true);
        $('#obs_imagem_check_box').prop('checked', false);
        $('#obs_imagem_check_box').prop('disabled',true);
        Popular_Itens('');

        $('#btn_reset_item').attr("hidden",true);
        $('#btn_new_item').text('Criar Item');
        $('#btn_new_item').prepend('<i class="fa-solid fa-file-circle-plus" style="margin-right:5px"></i>')
        $('#btn_new_item').val('');
    }

    if ( nomeDoButton == 'btn_new_item' ) {

        let valItemExistente = $(this).val();
        let valPickerCheckExistente = $("#modelos_existentes").val();
        let valDescricaoItem = $("#descricao_item_check").val();
        let valTipoItem = $("#select_tipo_item").val();
        let valTipoResposta = $("#select_tipo_resposta").val();
        let valOrdemItem = $("#input_ordem_check").val();
        let valDesativarItem = $("#desativar_item_date").val();
        let valImagemObs = 0;
        if($('#obs_imagem_check_box').prop('checked') == true) {
            valImagemObs = 1;
        }

        $.ajax({
            type:"POST",
            url: '/safety_layout_checklist_app/registra_item',
            dataType: 'json',
            data: {
                'cod_item_check':   valItemExistente,
                'cod_check'     :   valPickerCheckExistente,
                'desc_item'     :   valDescricaoItem,
                'tipo_item'         :   valTipoItem,
                'tipo_resposta'     :   valTipoResposta,
                'ordem'         :   valOrdemItem,
                'desativar_item'         :   valDesativarItem,
                'imagem_obs'         :   valImagemObs,
                'flag_arrastar_sortable': 0
             },
            success: function (data) {
                $('#tipo_item').selectpicker('refresh')
                $('#tipo_resposta').selectpicker('refresh')
                Popular_Itens(valPickerCheckExistente);
                $('#sortable').sortable('refresh');
            },
            error: function (request, status, error) {

            }
        });
    }

    else if ( nomeDoButton == 'btn_reset_item' ) {

        $('#descricao_item_check').val('');
        $('#select_tipo_item').val('');
        $('#select_tipo_item').selectpicker('refresh')
        $('#select_tipo_resposta').val('');
        $('#select_tipo_resposta').selectpicker('refresh')
        $('#input_ordem_check').val('');
        $('#desativar_item_date').val('');
        $('#obs_imagem_check_box').prop('checked', false);
        $('#btn_reset_item').attr("hidden",true);
        $('#btn_new_item').text('Criar Item');
        $('#btn_new_item').prepend('<i class="fa-solid fa-file-circle-plus" style="margin-right:5px"></i>')
        $('#btn_new_item').val('');

    }
});

$(document).on('click','.ui-sortable-handle', function(){
    let cod_item = $(this).val();
    $.ajax({
            type: 'GET',
            url: '/safety_layout_checklist_app/sortable',
            data: {
                'cod_item_check'   :   cod_item,
            },
            dataType: 'json',
            success: function (dados) {
                console.log(dados)

                let data_retorno = new Date(dados.item_selecionado.data_desativacao)

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

                $('#descricao_item_check').val(dados.item_selecionado.desc_check);
                $('#select_tipo_item').val(dados.item_selecionado.tipo_item);
                $('#select_tipo_item').selectpicker('refresh');
                $('#select_tipo_resposta').val(dados.item_selecionado.tipo_resposta);
                $('#select_tipo_resposta').selectpicker('refresh');
                $('#input_ordem_check').val(dados.item_selecionado.ordem_item);
                $('#desativar_item_date').val(today);
                $('#btn_new_item').val(cod_item);
                $('#btn_new_item').text("Editar Item");
                $('#btn_new_item').prepend('<i class="fa-solid fa-file-circle-plus" style="margin-right:5px"></i>');
                $('#btn_reset_item').attr("hidden",false);
                let CheckTrueOrFalse = false;
                if (dados.item_selecionado.campo_obs_img == 1) {
                    CheckTrueOrFalse = true;
                }
                $('#obs_imagem_check_box').prop('checked', CheckTrueOrFalse);
            }
    });
});

$(document).on('change','.selectpicker',function(){
    let nome_select = $(this).attr('name');
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
                $("#sortable").sortable({

                    stop: function(event, ui) {
                        let valItemCheck = $(ui.item).val();
                        let valOrdemItem;

                        $.map($(this).find('li'), function(el) {
                            if ($(el).val() == valItemCheck) {
                                valOrdemItem = $(el).index()+1;
                            }
                        });

                        $.ajax({
                            type:"POST",
                            url: '/safety_layout_checklist_app/registra_item',
                            dataType: 'json',
                            data: {
                                'cod_item_check':   valItemCheck,
                                'cod_check': cod_check,
                                'ordem': valOrdemItem,
                                'flag_arrastar_sortable': 1
                             },
                            success: function (data) {
                                Popular_Itens(cod_check);
                                $('#sortable').sortable('refresh');
                            },
                            error: function (request, status, error) {

                            }
                        });
                    }
                });

                $("#sortable").sortable();0

                $('#descricao_new_check').val(dados.check_selecionado.desc_check);
                $('#versao_new_check').val(dados.check_selecionado.versao);
                $('#desativar_new_check_date').val(today);
                $('#medida_periodicidade_new_check').val(dados.check_selecionado.medida_periodicidade);
                $('#medida_periodicidade_new_check').selectpicker('refresh');
                $('#periodicidade_new_check').val(dados.check_selecionado.periodicidade);
                $('#btn_new_check').text("Editar Check");
                $('#btn_new_check').prepend('<i class="fa-solid fa-file-export" style="margin-right:5px"></i>');
                $('#btn_reset_check').attr("hidden",false);

                $('#descricao_item_check').prop('disabled',false);
                $('#select_tipo_item').prop('disabled',false);
                $('#select_tipo_item').selectpicker('refresh');
                $('#select_tipo_resposta').prop('disabled',false);
                $('#select_tipo_resposta').selectpicker('refresh');
                $('#input_ordem_check').prop('disabled',false);
                $('#desativar_item_date').prop('disabled',false);
                $('#obs_imagem_check_box').prop('disabled',false);

                $('#descricao_item_check').val('');
                $('#select_tipo_item').val('');
                $('#select_tipo_item').selectpicker('refresh')
                $('#select_tipo_resposta').val('');
                $('#select_tipo_resposta').selectpicker('refresh')
                $('#input_ordem_check').val('');
                $('#desativar_item_date').val('');
                $('#obs_imagem_check_box').prop('checked', false);
                $('#btn_reset_item').attr("hidden",true);
                $('#btn_new_item').text('Criar Item');
                $('#btn_new_item').prepend('<i class="fa-solid fa-file-circle-plus" style="margin-right:5px"></i>')
                $('#btn_new_item').val('');

                $.ajax({
                    type: 'GET',
                    url: '/safety_layout_checklist_app/filiais_check',
                    data: {
                        'cod_check'   :   cod_check,
                    },
                    dataType: 'json',
                    success: function (dados) {
                        console.log(dados);
                        $('#liberado_filiais option').remove();
                        dados[0].lista_filiais_check.forEach(filial => {
                            let string_empresa;
                            if (filial.desc_empresa != null) {
                                string_empresa = " (" + filial.desc_empresa + ")";
                            }
                            else {
                                string_empresa = "";
                            }
                            $("#liberado_filiais").append("<option selected='true' value='"+
                            filial.cod_filial+"'>"+filial.desc_filial+string_empresa+"</option>");
                        });
                        dados[0].lista_filiais.forEach(filial => {
                            let string_empresa;
                            if (filial.desc_empresa != null) {
                                string_empresa = " (" + filial.desc_empresa + ")";
                            }
                            else {
                                string_empresa = "";
                            }
                            $("#liberado_filiais").append("<option value='"+
                            filial.cod_filial+"'>"+filial.desc_filial+string_empresa+"</option>");
                        });
                        $('#liberado_filiais').selectpicker('refresh');
                    }
                });

                Popular_Itens(cod_check);

            }
        });
    }

    if (nome_select == "liberado_filiais") {
        //let filiais_select = $(this).val();
        //var filiais_check = JSON.stringify($('#liberado_filiais option:selected')
        //        .toArray().map(item => item.text));

        var filiais_check = JSON.stringify($('#liberado_filiais option:selected')
                .toArray().map(item => item.value));
        cod_check = $('#modelos_existentes').val()
        $.ajax({
            type:"POST",
            url: '/safety_layout_checklist_app/filiais_check',
            dataType: 'json',
            data: {
                'cod_check' : cod_check,
                'filiais_check'     :   filiais_check,
            },
            success: function (data) {

            },
            error: function (request, status, error) {

            }
        });
    }

});

function Popular_Itens(cod_check) {
    if (cod_check == '') {
        $("#sortable li").remove();
    }
    else {
        $.ajax({
            type: 'GET',
            url: '/safety_layout_checklist_app/registra_item',
            data: {
                'cod_check'   :   cod_check,
            },
            dataType: 'json',
            success: function (dados) {
                console.log(dados)
                $("#sortable li").remove();
                dados.lista_itens_check.forEach(item => {
                    if (item.tipo_item == 1) {
       //                 $("#sortable").append(
       //                 "<div class=\"item_li_sortable\">"+
       //                 "<label>teste</label>"+
       //                 "<input type=\"text\" class=\"ui-state-default\"></input>"+
       //                 "</div>");
                           $("#sortable").append(
                                "<li class=\"ui-state-default item_li_sortable\" value='"+
                                item.cod_item_check+"'>"+item.desc_check+"</li>");
                    }
                    if (item.tipo_item == 2) {
                        $("#sortable").append("<li class=\"ui-state-default agrupador_li_sortable\" value='"+
                        item.cod_item_check+"'>"+item.desc_check+"</li>");
                    }
                });
                $('#sortable').sortable('refresh');
            }
        });
    }
}