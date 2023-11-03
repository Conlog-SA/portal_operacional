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

let loader_sup_tma = document.getElementById("loader_sup_tma");


$(document).on('click', 'button', function(){
	var nomeDoButton = $(this).attr('name');
	var idDoButton = $(this).attr('id');
	var valButton = $(this).val();

	if (nomeDoButton == "btnPesqFormTeqGeraTMA") {
	    povoa_table_req_atendidas();

	} else if (nomeDoButton=='btnVinculaAtendenteFormGeraTMA') {
	    $.ajax({
	        type: 'POST',
	        url: '/suprimentos_tma_app/vincula_comprador_req_atendida_tma',
	        success: function(data) {
	            povoa_table_req_atendidas();
	        },
	        error: function(request, status, error){
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


function povoa_table_req_atendidas(){
    var var_data_ini = $("#textFieldFormReqGeraTMAIni").val();
    var var_data_fim = $("#textFieldFormReqGeraTMAFim").val();
    loader_sup_tma.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/suprimentos_tma_app/retorna_requisicoes_atendidas_benner',
        data : {
            'data_ini': var_data_ini,
            'data_fim': var_data_fim
        },
        success: function(data){
            var lista_req_atendidas = [];
            data.tab_req_atendidas.forEach(req => {
                var var_campo_data_prevista_validada = req.data_atendida_prevista;
                var var_campo_data_atendida_validada = req.data_atendida;
                var var_campo_status_atendimento_validado = req.status_atendimento;

                if( req.status_atendimento == 'Fora do Prazo'){
                    var_campo_data_prevista_validada = "<span style='background:#fa6163;color:#FFFFFF'>"+req.data_atendida_prevista+"</span>";
                    var_campo_data_atendida_validada = "<span style='background:#fa6163;color:#FFFFFF'>"+req.data_atendida+"</span>";
                    var_campo_status_atendimento_validado = "<span style='background:#fa6163;color:#FFFFFF'>"+req.status_atendimento+"</span>";
                }

                var var_status_ordem = '';
                if(req.status_ordem == 'E'){
                    var_status_ordem = 'Emergencial';
                } else if(req.status_ordem == 'NE'){
                   var_status_ordem = ' Não Emergencial';
                } else if(req.status_ordem == 'P'){
                   var_status_ordem = 'Planejada';
                }
                var reg = [
                    `<i class="fa-solid fa-caret-right" style="color: #f46424;"></i>`,
                    req.nome_filial,
                    req.num_req_pai,
                    req.desc_familia,
                    req.data_confirmada,
                    var_campo_data_prevista_validada,
                    req.tma_previsto,
                    var_campo_data_atendida_validada,
                    req.tma,
                    req.nome_comprador,
                    var_status_ordem,
                    var_campo_status_atendimento_validado,
                    req.status_importacao
                ];
                lista_req_atendidas.push(reg);
            });
            $("#tabReqAtendidasTMA").DataTable({
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 7,
                "dom": 'Bfrtip',
                "searching": true,
                "buttons": [
                    'copyHtml5'
                ],
                "data":lista_req_atendidas,
                "columns": [
                    { title: "" },
                    { title: "Filial" },
                    { title: "Núm. Req." },
                    { title: "Desc. Familia" },
                    { title: "Data Confirmada" },
                    { title: "Data Prevista" },
                    { title: "TMA Previsto" },
                    { title: "Data Atendida" },
                    { title: "TMA" },
                    { title: "Comprador" },
                    { title: "Status Ordem" },
                    { title: "Status Atend." },
                    { title: "Status Importação" }
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
                loader_sup_tma.style.display = "none";
        },
        error:function(request, status, error) {
            loader_sup_tma.style.display = "none";
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