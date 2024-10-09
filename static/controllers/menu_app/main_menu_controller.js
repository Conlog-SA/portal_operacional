//const loader = document.getElementById("loader");

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



$(document).ready(function(){

    $("#main_menu").html("");

    $('#value_prejuizo_eqp').inputmask({
        alias: 'numeric',
        groupSeparator: '.',
        autoGroup: true,
        digits: 2,
        radixPoint: ',',
        allowMinus: false,
        prefix: 'R$ ',
        rightAlign: false,
        unmaskAsNumber: true,
        numericInput: true
    });

});

$(document).on('click', 'a', function(){
	let let_nomeA = $(this).attr('name');
	let let_idA = $(this).attr('id');

	if ( let_nomeA == "a_sub_menu") {
	    $("#main_menu").empty();
	    //let loader_menu = document.getElementById("loader_menu");
	    //loader_menu.style.display = "flex";

	    let let_url_menu = $("#hd_url_sub_menu_"+let_idA.split('_')[3]).val();
	    $.ajax({
            url:let_url_menu,
            success: function(dados){

                $("#main_menu").html(dados);

                $('.selectpicker').selectpicker();
                $('.class_mask_campo_val').mask('###0,00', {reverse: true});

                $(".class_mask_negative_number").inputmask({
                    alias: 'decimal',
                    radixPoint: ',',
                   // groupSeparator: ',',
                    inputtype: "text",
                    autoGroup: true,
                    digits: 2,
                    allowMinus: true,
                    rightAlign: true

                });

                /*
                    "bJQueryUI": true,
                    "pageLength": 10,
                    "destroy": true,
                    "paging": true,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],

                */

                    //loader_menu.style.display = "none";
                if ( let_url_menu == '/ti_comitec_app/') {
                    $('#tab_ideias_comitec').DataTable( {
                        "bJQueryUI": true,
                        "destroy": true,
                        "fixedHeader": true,
                        "scrollY": true,
                        "scrollX": true,
                        "scrollCollapse": true,
                        "paging": true,
                        "pageLength": 6,
                        "dom": 'Bfrtip',
                        "buttons": [
                            'copyHtml5'
                        ],
                        "columnDefs": [
                            {"className": "dt-center", "targets": [0,1,2,3,4,5,6,12,13]},
                            {"className": "dt-left", "targets": [7,8]},
                            {"className": "dt-right", "targets": [9,10,11]}
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
                } else {
                    $(".display").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "50vh", //"50vh" 770px
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": false,
                    //"pageLength": 7,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [0,1,2]}
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
                    } );
                }

            },
            error: function (request, status, error) {
                //loader_menu.style.display = "none";
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