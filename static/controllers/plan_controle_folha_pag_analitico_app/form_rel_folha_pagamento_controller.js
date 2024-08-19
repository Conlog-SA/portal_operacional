// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).on('click', 'button', function(){
	var nomeDoButton = $(this).attr('name');
	var idDoButton = $(this).attr('id');
	var valButton = $(this).val();

    if (nomeDoButton == 'btnPesqDadosFolhaPag'){
        let let_loader_folha_pagamento = document.getElementById("loader_folha_pagamento");
        var var_cod_competencia = $("#cb_competencia_folha_pag").val();
        var var_lista_handle_proj = $("#cb_proj_folha_pag").val().toString();

        if(var_cod_competencia == "0" || (var_lista_handle_proj == "0" && var_lista_handle_proj.length == 1) ||
            var_lista_handle_proj == null || var_lista_handle_proj == '' ) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: "Informe a competência e o projeto para gerar os dados!",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

            } else {
                let_loader_folha_pagamento.style.display = "flex";
                $.ajax({
                    type: 'GET',
                    data: {
                        'cod_competencia'         : var_cod_competencia,
                        'lista_handle_proj'       : var_lista_handle_proj
                    },
                    url:"/plan_controle_folha_pag_analitico_app/pesquisa_folha_pag",
                    success: function(dados){

                        lista_dados_folha = [];
                        dados.dados_folha_pag.forEach( reg => {
                            reg = [
                                "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                                reg.matricula_colab,
                                reg.nome_colab,
                                reg.desc_cargo,
                                reg.desc_filial,
                                reg.desc_projeto,
                                reg.desc_conta_contabil,
                                reg.cod_evento,
                                reg.desc_evento,
                                reg.proeventos.toLocaleString('pt-BR'),
                                reg.hora_min_ref.toLocaleString('pt-BR'),
                                reg.desc_sit_atual
                            ];
                            lista_dados_folha.push(reg);
                        });


                        $("#tab_dados_folha_pagamento").DataTable({
                            "bJQueryUI": true,
                            "destroy": true,
                            "fixedHeader": true,
                            "scrollY": "770px",
                            "scrollX": true,
                            "scrollCollapse": true,
                            "paging": true,
                            "pageLength": 7,
                            "dom": 'Bfrtip',
                            "buttons": [
                                'copyHtml5'
                            ],
                            "data":lista_dados_folha,
                            "columns": [
                                { title: "" },
                                { title: "Matrícula" },
                                { title: "Colaborador" },
                                { title: "Cargo" },
                                { title: "Filial" },
                                { title: "Projeto" },
                                { title: "Conta Contábil" },
                                { title: "Cód. Evento" },
                                { title: "Evento" },
                                { title: "Proeventos" },
                                { title: "Horas e Min. Referência" },
                                { title: "Situação Atual" }
                            ],
                            "columnDefs": [
                                {"className": "dt-center", "targets": [0,1,7,8]},
                                {"className": "dt-left", "targets": [2,3,4,5,6]},
                                {"className": "dt-right", "targets": [9,10,11]}
                            ],
                            "language": {
                                "decimal": ",",
                                "thousands": ".",
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

                        let_loader_folha_pagamento.style.display = "none";


                    },
                    error: function (request, status, error) {
                        let_loader_folha_pagamento.style.display = "none";
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

    }
    else if (nomeDoButton == 'btn_desmarcar_projetos_folha_pag'){
        $("#cb_proj_folha_pag").selectpicker('deselectAll');
        /*var var_cb_proj = $("#cb_proj_folha_pag").val().toString().split(',');
        for(var i = 0; i < var_cb_proj.length; i++){
            $("#cb_proj_folha_pag").picker('remove', var_cb_proj[i]);
        }*/

    } else if (nomeDoButton == 'btn_seleciona_todas_proj_folha_pag') {
        $("#cb_proj_folha_pag").selectpicker('selectAll');
    }

});
/*
$(document).on('change', '#cb_emp_folha_pag', function(){
    let let_cod_empresa = $(this).val();
    let let_loader_folha_pagamento = document.getElementById("loader_folha_pagamento");
    let_loader_folha_pagamento.style.display = "flex";
    $.ajax({
        type: 'GET',
        data: {
            'cod_empresa'         : let_cod_empresa
        },
        url:"/plan_controle_folha_pag_analitico_app/pesq_projetos_by_emp",
        success: function(dados){
            $("#cb_proj_folha_pag option").remove();
            dados.lista_projetos.forEach(proj => {
                $("#cb_proj_folha_pag").append("<option value='"+
                proj.handle_benner+"'>"+proj.desc_proj_benner+"</option>");

            });
            $("#cb_proj_folha_pag").selectpicker('refresh');



            let_loader_folha_pagamento.style.display = "none";


        },
        error: function (request, status, error) {
            let_loader_folha_pagamento.style.display = "none";
            $.gritter.add({
                title: 'Atenção!',
                text: error,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });

});
*/