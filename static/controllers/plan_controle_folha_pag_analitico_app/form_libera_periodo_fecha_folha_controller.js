var date = new Date();
var anoAtual = date.getFullYear();

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

$(document).on('click','input', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if (nomeDoButton == 'rbn_ativa_periodo'){
        let let_loader_libera_periodo_fecha_folha = document.getElementById("loader_libera_periodo_fecha_folha");
        var var_dados = idDoButton.split("_")
        var var_ano =  var_dados[3];
        var var_mes =  var_dados[4];
        var var_acao_ativa_desativa = $(this).prop("checked");

        var var_ativa_desativa = 'N'
        if (var_acao_ativa_desativa == true) {
            var_ativa_desativa = 'S';
        }

        let_loader_libera_periodo_fecha_folha.style.display = "flex";
        $.ajax({
            type: 'POST',
            data: {
                competencia : var_mes,
                ano         : var_ano,
                acao        : var_ativa_desativa
            },
            url:"/plan_controle_folha_pag_analitico_app/libera_periodo_fecha_folha",
            success: function(dados){

                $('#tf_ano_pesq_periodo_libera_folha').val(anoAtual);
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let_loader_libera_periodo_fecha_folha.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_libera_periodo_fecha_folha.style.display = "none";
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


});


$(document).on('click', 'button', function(){
	var nomeDoButton = $(this).attr('name');
	var idDoButton = $(this).attr('id');
	var valButton = $(this).val();

    if (nomeDoButton == 'btn_pesq_periodo_form_libera_periodo_fecha_folha'){
        var var_ano =  $("#tf_ano_pesq_periodo_libera_folha").val();
        if(var_ano == null || var_ano == ''){
            $.gritter.add({
                title: 'Atenção!',
                text: "Informe o Período!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            let let_loader_libera_periodo_fecha_folha = document.getElementById("loader_libera_periodo_fecha_folha");
            let_loader_libera_periodo_fecha_folha.style.display = "flex";
            $.ajax({
                type: 'GET',
                data: {
                    ano  : var_ano
                },
                url:"/plan_controle_folha_pag_analitico_app/retorna_periodos_liberados_do_ano",
                success: function(dados){

                    lista_comp_liberadas = [];
                    dados.lista_competencias.forEach( comp => {
                        var var_desc_mes = '';
                        if (comp.mes_competencia_periodo == 1){
                            var_desc_mes = 'Janeiro';
                        } else if (comp.mes_competencia_periodo == 2){
                            var_desc_mes = 'Fevereiro';
                        } else if (comp.mes_competencia_periodo == 3){
                            var_desc_mes = 'Março';
                        } else if (comp.mes_competencia_periodo == 4){
                            var_desc_mes = 'Abril';
                        } else if (comp.mes_competencia_periodo == 5){
                            var_desc_mes = 'Maio';
                        } else if (comp.mes_competencia_periodo == 6){
                            var_desc_mes = 'Junho';
                        } else if (comp.mes_competencia_periodo == 7){
                            var_desc_mes = 'Julho';
                        } else if (comp.mes_competencia_periodo == 8){
                            var_desc_mes = 'Agosto';
                        } else if (comp.mes_competencia_periodo == 9){
                            var_desc_mes = 'Setembro';
                        } else if (comp.mes_competencia_periodo == 10){
                            var_desc_mes = 'Outubro';
                        } else if (comp.mes_competencia_periodo == 11){
                            var_desc_mes = 'Novembro';
                        } else if (comp.mes_competencia_periodo == 12){
                            var_desc_mes = 'Dezembro';
                        }

                        var var_rb_ativa_periodo =
                        `
                            <div class="container">
                                <input type="checkbox" class="checkbox"
                                       name="rbn_ativa_periodo"
                                       id="rbn_ativa_periodo_{{periodo.ano_competencia_periodo}}_{{periodo.mes_competencia_periodo}}_{{periodo.periodo}}"
                                       ${ comp.acao }}>
                                <label class="switch" for="rbn_ativa_periodo_{{periodo.ano_competencia_periodo}}_{{periodo.mes_competencia_periodo}}_{{periodo.periodo}}">
                                    <span class="slider"></span>
                                </label>
                            </div>
                        `;

                        reg = [
                            "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                            var_desc_mes+"/"+comp.ano_competencia_periodo,
                            var_rb_ativa_periodo
                        ];
                        lista_comp_liberadas.push(reg);
                    });
                    $("#tab_periodos_do_ano").DataTable({
                        "bJQueryUI": true,
                        "pageLength": 7,
                        "destroy": true,
                        "fixedHeader": {
                            header: true,
                            footer: false
                        },
                        "searching": true,
                        "dom": 'Bfrtip',
                        "buttons": [
                            'copy'
                        ],
                        "data":lista_comp_liberadas,
                        "columns": [
                            { title: "" },
                            { title: "Competência" },
                            { title: "Ativa/Desativa" }
                        ],
                        "columnDefs": [
                            {"className": "dt-center", "targets": [2]},
                            {"className": "dt-left", "targets": [0,1]}
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
                    let_loader_libera_periodo_fecha_folha.style.display = "none";

                },
                error: function (request, status, error) {
                    let_loader_libera_periodo_fecha_folha.style.display = "none";
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


