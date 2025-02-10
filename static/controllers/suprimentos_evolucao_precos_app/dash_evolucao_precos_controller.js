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





$(document).on('change', '#cb_empresas_dash_evolucao_precos', function(){
    var var_cod_empresa_selecionada = $(this).val();
    $.ajax({
        type: 'GET',
        url:"/suprimentos_evolucao_precos_app/povoa_cd_filial_por_empresa",
        data: {
            'cod_empresa': var_cod_empresa_selecionada
        },
        dataType: 'json',
        success: function(data){
            $("#cb_filial_dash_evolucao_precos option").remove();
            data.lista_filiais.forEach(fil => {
                $("#cb_filial_dash_evolucao_precos").append("<option value='"+fil.handle+"'>"+fil.nome+"</option>");
            });
            $("#cb_filial_dash_evolucao_precos").selectpicker('refresh');

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




});

$(document).on('click', 'button', function(){
    var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if( nomeDoButton == 'btn_gera_dash_evolucao_precos' ) {
        let let_tem_elemento_vazio = 'N';
        let let_componentes = document.querySelectorAll('.campo_dash');
        let_componentes.forEach(comp => {
            if(comp.name != null) {
                if(comp.value == '' || comp.value == null) {
                    let_tem_elemento_vazio = 'S';
                    let let_div = document.querySelector('.div_' + comp.name);

                    let_div.style.border = "2px solid red";
                    let_div.style.borderRadius = ".5rem";
                    let_div.style.padding = ".25rem";
                    setTimeout(function() {
                        let_div.style.border = "0px";
                        let_div.style.borderRadius = "0rem";
                        let_div.style.padding = "0rem";
                        let_div.style.paddingLeft = ".25rem";
                    }, 3000);
                }
            }
        });
        if(let_tem_elemento_vazio == 'N') {
            let let_loader_dash_evolucao_preco = document.getElementById("loader_dash_evolucao_preco");
            var var_handle_filial = $("#cb_filial_dash_evolucao_precos").val().toString();
            let let_lista_handle_atendentes = $("#cb_atendente_dash_evolucao_precos").val().toString();
            var var_data_ini = $("#txt_data_ini_dash_evolucao_precos").val();
            var var_data_fim = $("#txt_data_fim_dash_evolucao_precos").val();
            var var_handle_familia = $("#cb_familia_dash_evolucao_precos").val().toString();

            $("#div_grafico_status_resumo").html("");
            $("#div_grafico_status_atendente").html("");
            $("#div_grafico_status_familia").html("");
            $("#div_grafico_status_filial").html("");
            $("#div_grafico_qtd_itens_filial").html("");
            let_loader_dash_evolucao_preco.style.display = "flex";
            $.ajax({
                type: 'GET',
                data: {
                    'handle_filial'     :   var_handle_filial,
                    'lista_handle_atendentes' : let_lista_handle_atendentes,
                    'handle_familia'    :   var_handle_familia,
                    'data_ini'          :   var_data_ini,
                    'data_fim'          :   var_data_fim
                },
                url:'/suprimentos_evolucao_precos_app/gera_dash_evolucao_precos',
                success: function(dados){
                    $("#div_grafico_status_resumo").html(dados.grafico_pizza_resumo_status);
                    $("#div_grafico_status_familia").html(dados.grafico_barra_agrupado);
                    $("#div_grafico_status_atendente").html(dados.grafico_atendente_barra_agrupado);
                    $("#div_grafico_status_filial").html(dados.grafico_barra_agrupado_filial);
                    $("#div_grafico_qtd_itens_filial").html(dados.grafico_barra_agrupado_itens_filial);

                     /*$("#div_grafico_status_resumo").fadeOut(100).fadeIn(100);
                    //var graphs = JSON.parse(dados.grafico_pizza_resumo_status);
                    console.log(dados.grafico_pizza_resumo_status);
                    Plotly.react('graph', dados.grafico_pizza_resumo_status, {});*/

                    let_loader_dash_evolucao_preco.style.display = "none";
                },
                error: function(request, status, error){
                    let_loader_dash_evolucao_preco.style.display = "none";
                    $.gritter.add({
                        title: 'Atenção!',
                        text: error,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
            });

        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: "Informe os filtros indicados corretamente!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }





    } else if (nomeDoButton == 'btn_marcar_unidade_dash_evolucao_precos'){
        $("#cb_filial_dash_evolucao_precos").selectpicker('selectAll');
    }
    else if (nomeDoButton == 'btn_desmarcar_unidade_dash_evolucao_precos'){
        $("#cb_filial_dash_evolucao_precos").selectpicker('deselectAll');
    } else if (nomeDoButton == 'btn_marcar_atendente_dash_evolucao_precos'){
        $("#cb_atendente_dash_evolucao_precos").selectpicker('selectAll');
    }
    else if (nomeDoButton == 'btn_desmarcar_atendente_dash_evolucao_precos'){
        $("#cb_atendente_dash_evolucao_precos").selectpicker('deselectAll');
    } else if (nomeDoButton == 'btn_marcar_familia_dash_evolucao_precos'){
        $("#cb_familia_dash_evolucao_precos").selectpicker('selectAll');
    }
    else if (nomeDoButton == 'btn_desmarcar_familia_dash_evolucao_precos'){
        $("#cb_familia_dash_evolucao_precos").selectpicker('deselectAll');
    }

});


/*
$(document).on('hide.bs.select', '#cb_familia_dash_evolucao_precos', function(){
    let let_filial = $("#cb_filial_dash_evolucao_precos").val().toString();

    if (let_filial != null && let_filial != ''){
        var var_cod_familia_selecionada = $(this).val().toString();
        var var_handle_filial = $("#cb_filial_dash_evolucao_precos").val().toString();
        if (var_cod_familia_selecionada != '') {
            $.ajax({
                type: 'GET',
                url:"/suprimentos_evolucao_precos_app/povoa_cd_itens_by_familia",
                data: {
                    'handle_familia': var_cod_familia_selecionada,
                    'handle_filial': var_handle_filial
                },
                dataType: 'json',
                success: function(data){
                    $("#cb_item_dash_evolucao_precos option").remove();
                    $("#cb_item_dash_evolucao_precos").append("<option value='0' selected='selected'> -- Todos os itens -- </option>");
                    data.lista_itens.forEach(item => {
                        $("#cb_item_dash_evolucao_precos").append("<option value='"+item.cod_ref+"'>"+item.nome+"("+item.cod_ref+")</option>");
                    });
                    $('#cb_item_dash_evolucao_precos').selectpicker('refresh');
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

    } else {
        $(this).val('0');
        $(this).selectpicker('refresh');
        $.gritter.add({
            title: 'Atenção!',
            text: 'Selecione a filial',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }



});

*/