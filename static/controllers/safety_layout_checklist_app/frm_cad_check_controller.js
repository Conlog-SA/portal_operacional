{
let html_old = null
}

$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if ( nomeDoButton == 'btn_new_check' ) {
        let valPickerCheckExistente = $("#modelos_existentes").val();
        let valDescricao = $("#descricao_new_check").val();
        let valVersao = $("#versao_new_check").val();
        let valInicio = $("#inicio_new_check_date").val();
        let valDesativar = $("#desativar_new_check_date").val();
        let valMedidaPeriodicidade = $("#medida_periodicidade_new_check").val();
        let valPeriodicidade = $("#periodicidade_new_check").val();
        let valTipo = $("#tipo_check").val();

        msg_erro = '';
        if (valDescricao == '') {
            msg_erro += 'Informe uma descrição para o check!<br>';
        }
        valInicioDate = new Date(valInicio);
        if (isNaN(valInicioDate.getDay()) || isNaN(valInicioDate.getMonth()) || isNaN(valInicioDate.getFullYear())) {
            msg_erro += 'Data de inicio inválida!<br>';
        }
        valDesativarDate = new Date(valDesativar);
        if (isNaN(valDesativarDate.getDay()) || isNaN(valDesativarDate.getMonth()) || isNaN(valDesativarDate.getFullYear())) {
            msg_erro += 'Data final inválida!<br>';
        }
        if (valMedidaPeriodicidade == '' || valMedidaPeriodicidade == null) {
            msg_erro += 'Informe uma medida para a periodicidade!<br>';
        }
        if ((valPeriodicidade == '') && valMedidaPeriodicidade != 4) {
            msg_erro += 'Informe um valor para a periodicidade!<br>';
        } else if (isNaN(valPeriodicidade)) {
            msg_erro += 'A periodicidade deve ser um número!<br>';
        }
        if (valVersao == '') {
            msg_erro += 'Informe uma versão para o check!<br>';
        } else if (isNaN(valVersao)) {
            msg_erro += 'A versão deve ser um número!<br>'
        }
        if (msg_erro == '') {
            $.ajax({
                type:"POST",
                url: '/safety_layout_checklist_app/registra_check',
                dataType: 'json',
                data: {
                    'cod_check'      :   valPickerCheckExistente,
                    'desc_check'     :   valDescricao,
                    'versao'         :   valVersao,
                    'data_inicio'     :   valInicio,
                    'data_desativacao'     :   valDesativar,
                    'medida_periodicidade'         :   valMedidaPeriodicidade,
                    'periodicidade'         :   valPeriodicidade,
                    'tipo' :    valTipo
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
        else {
            $.gritter.add({
                title: 'Erro!',
                text: msg_erro,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }

    }

    else if ( nomeDoButton == 'btn_reset_check' ) {
        $('#modelos_existentes').val('');
        $('#modelos_existentes').selectpicker('refresh');

        $('#descricao_new_check').val('');
        $('#versao_new_check').val('');
        $('#inicio_new_check_date').val('')
        $('#inicio_new_check_date').prop('disabled',false);
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
        $('#inicio_item_date').val('');
        $('#inicio_item_date').prop('disabled',true);
        $('#obs_imagem_check_box').prop('checked', false);
        $('#obs_imagem_check_box').prop('disabled',true);
        Popular_Itens('');

        $('#btn_reset_item').attr("hidden",true);
        $('#btn_new_item').text('Criar Item');
        $('#btn_new_item').prepend('<i class="fa-solid fa-file-circle-plus" style="margin-right:5px"></i>')
        $('#btn_new_item').val('');
    }

    else if ( nomeDoButton == 'btn_new_item' ) {

        let valItemExistente = $(this).val();
        let valPickerCheckExistente = $("#modelos_existentes").val();
        let valDescricaoItem = $("#descricao_item_check").val();
        let valTipoItem = $("#select_tipo_item").val();
        let valTipoResposta = $("#select_tipo_resposta").val();
        let valOrdemItem = $("#input_ordem_check").val();
        let valInicioItem = $("#inicio_item_date").val();
        let valDesativarItem = $("#desativar_item_date").val();
        let valImagemObs = 0;
        if($('#obs_imagem_check_box').prop('checked') == true) {
            valImagemObs = 1;
        }
        let valObrigatorio = 0;
        if($('#resposta_obrigatoria_check_box').prop('checked') == true) {
            valObrigatorio = 1;
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
                'inicio_item'   :   valInicioItem,
                'desativar_item'         :   valDesativarItem,
                'imagem_obs'         :   valImagemObs,
                'resposta_obrigatoria' : valObrigatorio,
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
        $('#inicio_item_date').val('');
        $('#obs_imagem_check_box').prop('checked', false);
        $('#resposta_obrigatoria_check_box').prop('checked', false);
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

                let data_desativacao = new Date(dados.item_selecionado.data_desativacao)

                let day = ("0" + data_desativacao.getDate()).slice(-2);

                mes_desativacao = data_desativacao.getMonth();
                let month = 0;
                if (mes_desativacao < 9) {
                    month = ("0" + (mes_desativacao + 1));
                }
                else if (mes_desativacao >= 9) {
                    month = mes_desativacao + 1;
                }
                let desativar = data_desativacao.getFullYear()+"-"+(month)+"-"+(day);

                let data_inicio = new Date(dados.item_selecionado.data_inicio)

                day = ("0" + data_inicio.getDate()).slice(-2);

                mes_inicio = data_inicio.getMonth();
                let month_inicio = 0;
                if (mes_inicio < 9) {
                    month_inicio = ("0" + (mes_inicio + 1));
                }
                else if (mes_desativacao >= 9) {
                    month_inicio = mes_desativacao + 1;
                }
                let inicio = data_inicio.getFullYear()+"-"+(month_inicio)+"-"+(day);

                $('#descricao_item_check').val(dados.item_selecionado.desc_check);
                $('#select_tipo_item').val(dados.item_selecionado.tipo_item);
                $('#select_tipo_item').selectpicker('refresh');
                if (dados.item_selecionado.tipo_item == 1) {
                    $('#select_tipo_resposta').prop('disabled',false);
                    $('#select_tipo_resposta').val(dados.item_selecionado.tipo_resposta);
                    $('#select_tipo_resposta').selectpicker('refresh');
                    $("#select_tipo_resposta").trigger("change");

                    $('#obs_imagem_check_box').prop('disabled',false);
                    $('#resposta_obrigatoria_check_box').prop('disabled',false);

                    let CheckTrueOrFalse = false;
                    if (dados.item_selecionado.campo_obs_img == 1) {
                        CheckTrueOrFalse = true;
                    }
                    $('#obs_imagem_check_box').prop('checked', CheckTrueOrFalse);
                    let CheckTrueOrFalseObg = false;
                    if (dados.item_selecionado.obrigatorio == 1) {
                        CheckTrueOrFalseObg = true;
                    }
                    $('#resposta_obrigatoria_check_box').prop('checked', CheckTrueOrFalseObg);
                }
                else if (dados.item_selecionado.tipo_item == 2) {
                    $('#select_tipo_resposta').prop('disabled',true);
                    $('#select_tipo_resposta').val('');
                    $('#select_tipo_resposta').selectpicker('refresh');

                    $('#obs_imagem_check_box').prop('disabled',true);
                    $('#obs_imagem_check_box').prop('checked', false);
                    $('#resposta_obrigatoria_check_box').prop('disabled',true);
                    $('#resposta_obrigatoria_check_box').prop('checked', false);
                }

                $('#input_ordem_check').val(dados.item_selecionado.ordem_item);
                $('#desativar_item_date').val(desativar);
                $('#inicio_item_date').val(inicio);
                $('#btn_new_item').val(cod_item);
                $('#btn_new_item').text("Editar Item");
                $('#btn_new_item').prepend('<i class="fa-solid fa-file-circle-plus" style="margin-right:5px"></i>');
                $('#btn_reset_item').attr("hidden",false);
            }
    });
});

$(document).on('change','.selectpicker',function(){
    let nome_select = $(this).attr('name');

    if (nome_select == "tipo_check") {
        $('#filial_check_aplicado').val('');
        $('#filial_check_aplicado').selectpicker('refresh');
        $('#tab_frm_checks_aplicados').empty();

        let cod_tipo = $(this).val();
        if (cod_tipo == 1) {
            $('#medida_periodicidade_new_check').find('[value="4"]').remove();
        }
        else if (cod_tipo == 2 && $('#medida_periodicidade_new_check').find('[value="4"]').length == 0) {
            $('#medida_periodicidade_new_check').append('<option value="4">Não há</option>');
        }

        $.ajax({
            type: 'GET',
            url: '/safety_layout_checklist_app/lista_check',
            data: {
                'cod_tipo'   :   cod_tipo
            },
            dataType: 'json',
            success: function (dados) {
                $('#btn_reset_check').trigger('click');
                $('#modelos_existentes option').remove();
                dados.lista_checks.forEach(check => {
                    $("#modelos_existentes").append("<option selected='false' value='"+
                    check.cod_check+"'>"+check.desc_check+"</option>");
                    $('#modelos_existentes').val('');
                    $('#modelos_existentes').selectpicker('refresh');
                });
            }
        })
    }

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
                let data_desativar = new Date(dados.check_selecionado.data_desativacao)

                let day = ("0" + data_desativar.getDate()).slice(-2);

                mes_desativacao = data_desativar.getMonth();
                let month = 0;
                if (mes_desativacao < 9) {
                    month = ("0" + (mes_desativacao + 1));
                }
                else if (mes_desativacao >= 9) {
                    month = mes_desativacao + 1;
                }

                let dt_desativacao = data_desativar.getFullYear()+"-"+(month)+"-"+(day);

                let data_inicio = new Date(dados.check_selecionado.data_inicio)

                day = ("0" + data_inicio.getDate()).slice(-2);

                mes_inicio = data_inicio.getMonth();
                month = 0;
                if (mes_inicio < 9) {
                    month = ("0" + (mes_inicio + 1));
                }
                else if (mes_inicio >= 9) {
                    month = mes_inicio + 1;
                }

                let dt_inicio = data_inicio.getFullYear()+"-"+(month)+"-"+(day);
                if (dados.check_selecionado.flag_aplicado == 1) {
                    $("#sortable").addClass('disabled')
                }
                else if (dados.check_selecionado.flag_aplicado == 0) {
                    $("#sortable").removeClass('disabled')
                }
                //if (!($("#sortable").hasClass('disabled'))) {
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
                $("#sortable").sortable();
                if ($("#sortable").hasClass('disabled')) {
                    $("#sortable").sortable("destroy")
                }
                $('#descricao_new_check').val(dados.check_selecionado.desc_check);
                $('#versao_new_check').val(dados.check_selecionado.versao);
                $('#desativar_new_check_date').val(dt_desativacao);
                $('#inicio_new_check_date').val(dt_inicio);
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
                $('#inicio_item_date').prop('disabled',false);
                $('#obs_imagem_check_box').prop('disabled',false);
                $('#resposta_obrigatoria_check_box').prop('disabled',false);

                $('#descricao_item_check').val('');
                $('#select_tipo_item').val('');
                $('#select_tipo_item').selectpicker('refresh')
                $('#select_tipo_resposta').val('');
                $('#select_tipo_resposta').selectpicker('refresh')
                $('#input_ordem_check').val('');
                $('#desativar_item_date').val('');
                $('#inicio_item_date').val('');
                $('#obs_imagem_check_box').prop('checked', false);
                $('#resposta_obrigatoria_check_box').prop('checked', false);
                $('#btn_reset_item').attr("hidden",true);
                $('#btn_new_item').text('Criar Item');
                $('#btn_new_item').prepend('<i class="fa-solid fa-file-circle-plus" style="margin-right:5px"></i>')
                $('#btn_new_item').val('');

                if (dados.check_selecionado.flag_aplicado == 1) {
                    $('#inicio_new_check_date').prop('disabled',true);
                    $('#descricao_item_check').prop('disabled',true);
                    $('#select_tipo_item').prop('disabled',true);
                    $('#select_tipo_item').selectpicker('refresh')
                    $('#select_tipo_resposta').prop('disabled',true);
                    $('#select_tipo_resposta').selectpicker('refresh');
                    $('#input_ordem_check').prop('disabled',true);
                    $('#inicio_item_date').prop('disabled',true);
                    $('#desativar_item_date').prop('disabled',true);
                    $('#obs_imagem_check_box').prop('disabled',true);
                    $('#resposta_obrigatoria_check_box').prop('disabled',true);
                    $('#btn_new_item').prop('disabled',true);
                }
                else if (dados.check_selecionado.flag_aplicado == 0) {
                    $('#inicio_new_check_date').prop('disabled',false);
                    $('#descricao_item_check').prop('disabled',false);
                    $('#select_tipo_item').prop('disabled',false);
                    $('#select_tipo_item').selectpicker('refresh')
                    $('#select_tipo_resposta').prop('disabled',false);
                    $('#select_tipo_resposta').selectpicker('refresh');
                    $('#input_ordem_check').prop('disabled',false);
                    $('#inicio_item_date').prop('disabled',false);
                    $('#desativar_item_date').prop('disabled',false);
                    $('#obs_imagem_check_box').prop('disabled',false);
                    $('#resposta_obrigatoria_check_box').prop('disabled',false);
                    $('#btn_new_item').prop('disabled',false);
                }


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

    if (nome_select == "medida_periodicidade_new_check") {
        let periodicidade = $(this).val();

        if (periodicidade == 4) {
            $('#periodicidade_new_check').val('');
            $('#periodicidade_new_check').prop('disabled',true);
        }
        else {
            $('#periodicidade_new_check').prop('disabled',false);
        }
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

    if (nome_select == "select_tipo_item") {
        let tipo_resposta = $(this).val();
        if (tipo_resposta == 1) {
            $('#select_tipo_resposta').prop('disabled',false);
            $('#select_tipo_resposta').selectpicker('refresh');
            $("#select_tipo_resposta").trigger("change");

            $('#obs_imagem_check_box').prop('disabled',false);
            $('#resposta_obrigatoria_check_box').prop('disabled',false);

            $('#label_imagem_obs').text('Campos Imagem e OBS?');
        }
        else if (tipo_resposta == 2) {
            $('#select_tipo_resposta').prop('disabled',true);
            $('#select_tipo_resposta').val('');
            $('#select_tipo_resposta').selectpicker('refresh');

            $('#obs_imagem_check_box').prop('disabled',true);
            $('#obs_imagem_check_box').prop('checked', false);
            $('#resposta_obrigatoria_check_box').prop('disabled',true);
            $('#resposta_obrigatoria_check_box').prop('checked', false);
            $('#label_imagem_obs').text('Campo Imagem?');
        }
    }
    if (nome_select == "select_tipo_resposta") {
        let tipo_resposta = $(this).val();
        if (tipo_resposta == 1) {
            $('#label_imagem_obs').text('Campos Imagem e OBS?');
        }
        if (tipo_resposta == 2) {
            $('#label_imagem_obs').text('Campo Imagem?');
        }
    }
});

$(document).on('click','button.busca-checks-aplicados' , function(event){
    let cod_filial =  $('#filial_check_aplicado').val();
    let tipo_check = $("#tipo_check").val();
    /*
    let data_ini = new Date($('#dt_periodo_check_ini').val());
    let day = data_ini.getUTCDate();
    let month = data_ini.getUTCMonth()+1;
    let year = data_ini.getUTCFullYear();
	let let_data_ini = [year, month, day].join('-')
	*/
	let let_data_ini  = $('#dt_periodo_check_ini').val();

    /*
    let data_fim = new Date($('#dt_periodo_check_fim').val());
    let day_final = data_fim.getUTCDate();
    let month_final = data_fim.getUTCMonth()+1;
    let year_final = data_fim.getUTCFullYear();
    let let_data_fim = [year_final, month_final, day_final].join('-')
    */
    let let_data_fim = $('#dt_periodo_check_fim').val();

    let erro = ""
    if (tipo_check == '')
        erro += "|Preencha o tipo do check!"
    if (cod_filial == '')
        erro += "|Preencha o código da filial!"
        /*
    if (isNaN(day) || isNaN(month) || isNaN(year))
        erro += "|Preencha corretamente a data de inicio!"
    if (isNaN(day_final) || isNaN(month_final) || isNaN(year_final))
        erro += "|Preencha corretamente a data final!"
        */
    console.log(erro)
    if (erro == "") {

        $.ajax({
        type: 'GET',
        url: '/safety_checks_aplicados_app/check_aplicado',
        data: {
            'cod_filial_check_aplicado'   :   cod_filial,
            'tipo_check_aplicado'   :   tipo_check,
            'inicio_periodo_check_aplicado'  :   let_data_ini,
            'fim_periodo_check_aplicado'  :   let_data_fim,
        },
        dataType: 'json',
        success: function (dados) {

            let lista_checks_aplicados = [];
                dados.forEach(reg => {
                    let let_checks_aplicados = [
                        reg.cod_checks_aplicados,
                        reg.desc_check,
                        reg.nome_colaborador_aplicante,
                        reg.nome_colaborador_avaliado,
                        reg.data_registro,
                        reg.qtd_total,
                        reg.qtd_ok,
                        reg.qtd_nok,
                        reg.qtd_nao_respondidos,
                        reg.pdf
                    ]
                    lista_checks_aplicados.push(let_checks_aplicados)
                });
                $('#tab_frm_checks_aplicados').DataTable({
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5',
                ],
                "data":lista_checks_aplicados,
                    "columns": [
                            { title: "Codigo" },
                            { title: "Descrição" },
                            { title: "Avaliador" },
                            { title: "Avaliado" },
                            { title: "Data registro" },
                            { title: "Qtd. Itens" },
                            { title: "Qtd. OK" },
                            { title: "Qtd. NOK" },
                            { title: "Qtd. s/ resposta" },
                            { title: "PDF" },
                        ],
                //    "columnDefs": [
                //    //{
                //    //    "orderable": false, "targets": [5, 6, 7]
                //    //},
                //    {
                //    "targets": 0,
                //    "mRender": function(lista_tma_ti, type)
                //        {
                //        console.log(type)
                //        if (type !== 'display')
                //        {
                //            return lista_tma_ti;
                //        }
//
                //            return '<i class="fas fa-dot-circle" ' + lista_tma_ti + '></i>';
                //        }
                //    }
                //],
                    "oLanguage": {
                        "sProcessing":   "Processando...",
                        "sLengthMenu":   "Mostrar _MENU_ registros",
                        "sZeroRecords":  "Não foram encontrados resultados",
                        "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
                        "sInfoEmpty":    "Mostrando de 0 até 0 de 0 registros",
                        "sInfoFiltered": "",
                        "sInfoPostFix":  "",
                        "sSearch":       "Pesquisar:",
                        "sUrl":          "",
                        "oPaginate": {
                            "sFirst":    "Primeiro",
                            "sPrevious": "Anterior",
                            "sNext":     "Proximo",
                            "sLast":     "Último"
                        },
                        "buttons":{
                            "copyTitle": 'Dados Copiados',
                            "copySuccess": {
                                _: '%d linhas copiadas',
                                1: '1 linha copiada'
                            }
                        }
                    }
	            });
            }
        });
    }
    else {
        let split_erro_str = erro.split('|')
        split_erro_str.forEach((str) => {
            if (str != "") {
                $.gritter.add({
                    title: 'Atenção!',
                    text: str,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    }
});

$(document).on('click','.check-preenchido-element' , function(){
    let let_cod_check_aplicado = $(this).text().split(' - ')[0]
    console.log(let_cod_check_aplicado)

     $.ajax({
	        type: 'GET',
	        data: {
                'cod_check_aplicado'   :   let_cod_check_aplicado,
            },
            dataType : "html",
	        url: '/safety_checks_aplicados_app/itens_check_aplicado',
	        success: function(response) {
                //var file = new Blob([response], {type: 'application/pdf'});
                //console.log(file.size, file.type)
                //var fileURL = URL.createObjectURL(file);
                //console.log(fileURL)
                //window.open(fileURL, '_blank');
                html_old = $('#lista_checks_aplicados').html()
                $('#lista_checks_aplicados').html(response)
            }
    });
});

$(document).on('click','.btn-novo-colab' , function(){
    let let_nome_colab = $('#nome_colab').val();
    let let_cpf_colab = $('#cpf_colab').val();
    let let_dt_nasc_colab = $('#dt_nascimento_colab').val();
    let let_filial_cad_colab = $('#filial_cad_colab').val();
    let msg_erro = '';
    let data_temp = new Date(let_dt_nasc_colab);

    if (isNaN(data_temp.getDay()) || isNaN(data_temp.getMonth()) || isNaN(data_temp.getFullYear())) {
        msg_erro += 'Data de nascimento inválida!<br>';
    }
    if (let_nome_colab == '' || let_nome_colab == null) {
        msg_erro += 'Informe o nome completo do colaborador!<br>';
    }
    if (let_cpf_colab == '' || let_cpf_colab == null || isNaN(let_cpf_colab)) {
        msg_erro += 'CPF Inválido!<br>';
    }
    else if (let_cpf_colab.length < 11) {
        msg_erro += 'O CPF deve conter 11 números!<br>';
    }
    if (let_filial_cad_colab == '' || let_filial_cad_colab == 0) {
        msg_erro += 'Informe a filial do colaborador!<br>';
    }

    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            data: {
                'nome_colab'   :   let_nome_colab,
                'cpf_colab'  :  let_cpf_colab,
                'dt_nasc_colab'  : let_dt_nasc_colab,
                'filial_cad_colab'  : let_filial_cad_colab
            },
            url: '/safety_layout_checklist_app/cadastro_colaborador',
            success: function(response) {
                $.gritter.add({
                   title: 'Sucesso!',
                   text: response,
                   image: '/static/icons/triangle-exclamation-solid.svg',
                   sticky: false,
                   time: '',
                });
            },
            error: function(xhr, status, error) {
                var errorMessage = xhr.responseText || error;
                $.gritter.add({
                    title: 'Erro!',
                    text: errorMessage,
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

$(document).on('click','.a_tab_check_criados',function(){
    $('#modelos_existentes button').prop('disabled',true);
});

$(document).on('click','.a_tab_new_check',function(){
    $('#modelos_existentes button').prop('disabled',false);
});

$(document).on('click','.arrow-go-back' , function(){
    $('#lista_checks_aplicados').html(html_old)
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
                                item.cod_item_check+"'><b>"+item.desc_check+"</b></li>");
                    }
                    if (item.tipo_item == 2) {
                        $("#sortable").append("<li class=\"ui-state-default agrupador_li_sortable\" value='"+
                        item.cod_item_check+"'><b>"+item.desc_check+"</b></li>");
                    }
                });
                if (!$('#sortable').hasClass('disabled')) {
                    $('#sortable').sortable('refresh');
                }

            }
        });
    }
}