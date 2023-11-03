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

let loader_vinc_roteiro_pecas = document.getElementById("loader_vinc_roteiro_pecas");
$(document).on('change', '#txt_cod_ref_item', function(){
    var var_cod_ref = $(this).val();
    $.ajax({
        type: 'GET',
        url: '/frota_vpo_app/retorna_descricao_item',
        data: {
            'cod_ref'   :   var_cod_ref
        },
        dataType: 'json',
        success: function (data) {
            if(data.descricao_item_benner == ''){
                $.gritter.add({
                    title: 'Atenção!',
                    text: "Item não encontrado no Benner. Verifique!",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            } else {
                $("#txt_desc_item").val(data.descricao_item_benner.split('_')[0]+'('+data.descricao_item_benner.split('_')[1]+')');
                $("#hd_un_item").val(data.descricao_item_benner.split('_')[1]);
            }

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


$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if ( nomeDoButton == 'btn_vincula_item_roteiro') {
        var var_handles_chave_vinculo = $("#cb_roteiros").val().toString();
        var var_desc_dados_vinculo = ''//$("#cb_roteiros :selected").text().join(', ');
        $("#cb_roteiros option:selected").each(function () {
           var $this = $(this);
           if ($this.length) {
            var_desc_dados_vinculo += $this.text().trim() + ',';
           }
        });
        var var_cod_ref_item = $("#txt_cod_ref_item").val();
        var var_desc_item = $("#txt_desc_item").val();
        var var_un_item = $("#hd_un_item").val();
        var var_qtd_item = $("#txt_qtd_peca").val();
        var var_troca_obgo = $("#ck_troca_obgo").prop("checked");

        if ( var_handles_chave_vinculo == '0' || var_desc_item == '' || var_qtd_item == 0 ) {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Dados obrigatórios não informados. Verifique!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $.ajax({
                type: 'POST',
                url: '/frota_vpo_app/vincula_roteiro_peca',
                data: {
                    'handles_chave_vinculo' :   var_handles_chave_vinculo,
                    'desc_dados_vinculo'    :   var_desc_dados_vinculo,
                    'cod_ref_item'          :   var_cod_ref_item,
                    'desc_item'             :   var_desc_item,
                    'un_item'               :   var_un_item,
                    'qtd_item'              :   var_qtd_item,
                    'troca_obgo'            :   var_troca_obgo
                },
                dataType: 'json',
                success: function (data) {
                    $.gritter.add({
                        title: 'Atenção!',
                        text: data.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    povoa_tab_vinculo_pecas_roteiro();

                    $("#cb_roteiros").selectpicker('val', '');
                    $("#txt_cod_ref_item").val('');
                    $("#txt_desc_item").val('');
                    $("#txt_qtd_peca").val('');

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
    }
    else if ( nomeDoButton == 'btn_abre_modal_desvincular_roteiro_peca' ){
        $("#btn_excluir_vinculo_roteiro_peca").val(valButton);
        $("#modal_confirma_exclusao_vinculo_roteiro_peca").show();
    }
    else if ( nomeDoButton == 'bnt_fecha_modal_confirma_exclusao_vinculo_roteiro_peca' ){
        $("#modal_confirma_exclusao_vinculo_roteiro_peca").hide();
    }
    else if ( nomeDoButton == 'btn_excluir_vinculo_roteiro_peca' ){
        var var_cod_reg = valButton;
        $.ajax({
            type: 'DELETE',
            url: '/frota_vpo_app/desvincular_roteiro_peca/'+var_cod_reg,
            dataType: 'json',
            data: {
                'cod_reg'     :   var_cod_reg
            },
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_confirma_exclusao_vinculo_roteiro_peca").hide();
                povoa_tab_vinculo_pecas_roteiro();

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



function povoa_tab_vinculo_pecas_roteiro(){
    loader_vinc_roteiro_pecas.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/frota_vpo_app/lista_roteiro_peca',
        dataType: 'json',
        success: function (data) {
            roteiros_pecas_dic = [];
            $("#tab_vinculo_pecas_roteiro").DataTable().clear().draw();
            data.lista_roteiros_pecas.forEach( roteiro => {
                var var_btn_excluir = `
                    <button type='button'
                            id="btn_abre_modal_desvincular_roteiro_peca_${ roteiro.cod_roteiro_peca }"
                            name="btn_abre_modal_desvincular_roteiro_peca"
                            value="${ roteiro.cod_roteiro_peca }"
                            class="btn btn-rounded btn-space" >
                        <i class="fa-solid fa-trash" style="color: #f46424;"></i>
                    </button>
                `;
                var var_desc_troca_obs = 'Não';
                if(roteiro.troca == 1){
                    var_desc_troca_obs = 'Sim';
                }
                var reg = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    roteiro.nome_roteiro,
                    roteiro.nome_marca,
                    roteiro.nome_modelo,
                    roteiro.cod_ref_item,
                    roteiro.desc_item+"("+roteiro.cod_ref_item+")",
                    roteiro.un_item,
                    roteiro.qtd,
                    var_desc_troca_obs,
                    var_btn_excluir
                ]
                roteiros_pecas_dic.push(reg);
            });
            $("#tab_vinculo_pecas_roteiro").DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "searching": true,
                "pageLength": 7,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":roteiros_pecas_dic,
                "columns": [
                    { title: "" },
                    { title: "Roteiro" },
                    { title: "Marca" },
                    { title: "Modelo" },
                    { title: "Cód. Ref." },
                    { title: "Peça" },
                    { title: "UN" },
                    { title: "Qtd." },
                    { title: "Troca Obgo.?" },
                    { title: "Excluir" }
                ],

                "columnDefs": [
                    {"className": "dt-center", "targets": [4,7,8,9]},
                    {"className": "dt-right", "targets": [2,3,5]},
                    {"className": "dt-left", "targets": [0,1,6]}
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
            loader_vinc_roteiro_pecas.style.display = "none";

        },
        error: function (request, status, error) {
            loader_vinc_roteiro_pecas.style.display = "none";
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