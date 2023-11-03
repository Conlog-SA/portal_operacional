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
        let let_loader_dash_evolucao_preco = document.getElementById("loader_dash_evolucao_preco");
        var var_handle_filial = $("#cb_filial_dash_evolucao_precos").val().toString();
        var var_data_ini = $("#txt_data_ini_dash_evolucao_precos").val();
        var var_data_fim = $("#txt_data_fim_dash_evolucao_precos").val();
        if( var_handle_filial=='' || var_data_ini=='' || var_data_fim=='') {
            $.gritter.add({
                title: 'Atenção!',
                text: "Informe os dados obrigatórios(*)",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $("#div_grafico_status_resumo").html("");
            $("#div_grafico_status_familia").html("");
            $("#div_grafico_status_atendente").html("");
            $("#div_grafico_status_filial").html("");
            let_loader_dash_evolucao_preco.style.display = "flex";
            $.ajax({
                type: 'GET',
                data: {
                    'handle_filial'     :   var_handle_filial,
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

        }

    }

});