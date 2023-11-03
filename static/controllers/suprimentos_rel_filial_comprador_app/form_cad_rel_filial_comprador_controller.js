var dataAtual = new Date();
var diaAtual = dataAtual.getDate();
var mesAtual = dataAtual.getMonth()+1;
var anoAtual = dataAtual.getFullYear();

var dataInicio = anoAtual + "/" + mesAtual + "/" + "01";
var dataFim = anoAtual + "/" + mesAtual + "/" + diaAtual;

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

	if (nomeDoButton == "btnAdicionaCadRelFilialComprador") {
	    var varCodFiliaSelecionada = $("#listFiliaisCadRelFilialComprador").val();
	    var varCodUsuSelecionado = $("#listUsuariosCadRelFilialComprador").val();
	    var varDataAtivacao = $("#textFieldDataIniCadRelFilialComprador").val();
	    var varDataDesativacao = $("#textFieldDataFimCadRelFilialComprador").val();
	    if (varDataAtivacao == '') {
	        $.gritter.add({
                title: 'Atenção!',
                text: "Informe a data de ativação!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });

	    } else {
	        $.ajax({
                type: 'POST',
                url: '/suprimentos_rel_filial_comprador_app/add_rel_filial_comprador',
                data: {
                    'cod_filial'      : varCodFiliaSelecionada,
                    'cod_usuario'     : varCodUsuSelecionado,
                    'data_ativacao'   : varDataAtivacao,
                    'data_desativacao': varDataDesativacao
                },
                success: function(data) {
                    $.gritter.add({
                        title: 'Atenção!',
                        text: data.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    povoa_tabela_rel_filial_comprador();
                },
                error: function(request, status, error) {
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

	} else if (nomeDoButton == "btnModalDesativarRegistroRelFilialComprador") {
	    $("#hiddenCodRegRelFilialComprador").val(valButton);

        $("#textFieldDataDesativacaoCadRelFilialComprador").val(dataFim);

        $("#modalDesativarRegFilialComprador").show();
	} else if ( nomeDoButton == "btnFechaModalDesativarRegFilialComprador") {
	     $("#modalDesativarRegFilialComprador").hide();
	} else if ( nomeDoButton == "btnDestivarRelFilialComprador") {
	     var varDataDesativacao = $("#textFieldDataDesativacaoCadRelFilialComprador").val();
	     var varCodRegFilialComprador = $("#hiddenCodRegRelFilialComprador").val();
	     if(varDataDesativacao == ''){
	        $.gritter.add({
                title: 'Atenção!',
                text: 'Informe uma data válida',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
	     } else {
	        $.ajax({
                type: 'GET',
                url: '/suprimentos_rel_filial_comprador_app/informar_data_desativacao_filial_comprador',
                data: {
                    'cod_reg_filial_comprador' : varCodRegFilialComprador,
                    'data_desativacao'      : varDataDesativacao
                },
                success: function(data) {
                    $("#modalDesativarRegFilialComprador").hide();
                    $.gritter.add({
                        title: 'Atenção!',
                        text: data.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });


                    povoa_tabela_rel_filial_comprador();
                },
                error: function(request, status, error) {
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


function povoa_tabela_rel_filial_comprador(){
    $.ajax({
        type: 'GET',
        url:  '/suprimentos_rel_filial_comprador_app/retorna_registros_rel_filial_comprador',
        success: function(data) {
            var lista_rel_filial_comprador = [];
            data.lista_filial_comprador.forEach(reg => {
                var var_btn_editar_reg =
                    "<button type='button' name='btnModalDesativarRegistroRelFilialComprador'"+
                        "id='btnModalDesativarRegistroRelFilialComprador"+reg.cod_rel_filial_comprador+
                        "' class='btn btn-rounded btn-space' "+
                        "value='"+reg.cod_rel_filial_comprador+
                        "'><i class='fa-solid fa-circle-xmark' style='color: #f46424;'></i></button>";
                var var_data_ativacao = reg.data_ini.split("-")[2]+"/"+
                        reg.data_ini.split("-")[1]+"/"+
                        reg.data_ini.split("-")[0];
                var var_data_desativacao = '';
                if ( reg.data_fim != null) {
                    var_data_desativacao = reg.data_fim.split("-")[2]+"/"+
                        reg.data_fim.split("-")[1]+"/"+
                        reg.data_fim.split("-")[0];
                }
                var obj = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    reg.cod_filial__desc_filial,
                    reg.cod_usu__nome_usu,
                    var_data_ativacao,
                    var_data_desativacao,
                    var_btn_editar_reg
                ];
                lista_rel_filial_comprador.push(obj);
            });
            $("#tabCadRelFilialComprador").DataTable( {
                "bJQueryUI": true,
                "pageLength": 5,
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
                "data":lista_rel_filial_comprador,
                "columns": [
                    { title: "" },
                    { title: "Filial" },
                    { title: "Comprador" },
                    { title: "Data Ativação" },
                    { title: "Data Desativação" },
                    { title: "Desativar" }
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
                } );

        },
        error: function(request, status, error) {
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