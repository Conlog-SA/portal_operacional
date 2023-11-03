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

const loader_imp_2art = document.getElementById("loader_imp_2art")

$(document).on('change','input', function(){
	let let_nome_input = $(this).attr('name');
    let let_id_input = $(this).attr('id');
    let let_val_input = $(this).attr('value');

    if ( let_nome_input == 'fl_campo_arquivo_2art') {
        let let_frm_data = new FormData();
		let_frm_data.append("file", $('input[type=file]')[0].files[0]);
		loader_imp_2art.style.display = "flex";
		$.ajax({
		    type: 'POST',
            enctype: "multipart/form-data; charset=utf-8",
            url: "/frota_importa_2art_app/carrega_salva_arquivo_2art",
            data: let_frm_data,
            dataType: 'json',
            processData: false,
            contentType: false,
            cache: false,
            success: function(data){
                let let_lista_dados_2art = [];
                data.tab_mapas_nao_importados_2art.forEach( mapa => {
                    let let_dado_2art = [
						`<i class="fa-solid fa-circle-exclamation" style="color: #f46424;"></i>`,
						mapa,

					];
					let_lista_dados_2art.push(let_dado_2art);
                });

				$('#tab_mapas_nao_importados_2art').DataTable( {
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
			  		"data":let_lista_dados_2art,
			  		"columns": [
			  		    { title: "Status" },
                        { title: "Mapa/Data" }
                    ],
                    "columnDefs": [
                        { "width": "10%", "targets": 0 },
                        {"className": "dt-left", "targets": [0]},
                        {"className": "dt-left", "targets": [1]}
                    ],
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
				let let_msg = `
				    Total Registros : ${data.qtd_total_reg}<br/>
				    Novos Mapas : ${data.qtd_reg_imp}<br/>
				    Mapas Atualizados : ${data.qtd_reg_up}
				`;
				$.gritter.add({
                    title: 'Atenção!',
                    text: let_msg,
                    image: '../../static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                loader_imp_2art.style.display = "none"


			},
			error: function (request, status, error) {
			    loader_imp_2art.style.display = "none"
			    $.gritter.add({
                    title: 'Atenção!',
                    text: "Erro na importação, contate o adm.",
                    image: '../../icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
			}
		});

    }

});