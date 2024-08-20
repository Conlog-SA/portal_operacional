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
	let let_nome_btn = $(this).attr('name');
	let let_id_btn = $(this).attr('id');
	let let_val_btn = $(this).val();

    if (let_nome_btn == 'btn_desmarcar_projetos_frm_custos_placa'){
        $("#sl_proj_custos_placa").selectpicker('deselectAll');

    } else if (let_nome_btn == 'btn_seleciona_todas_proj_frm_custos_placa') {
        $("#sl_proj_custos_placa").selectpicker('selectAll');
    } else if (let_nome_btn == 'btn_desmarcar_tipo_veic_equip_frm_custos_placa'){
        $("#sl_tipo_veic_equip_custos_placa").selectpicker('deselectAll');

    } else if (let_nome_btn == 'btn_seleciona_todas_tipo_veic_equip_frm_custos_placa') {
        $("#sl_tipo_veic_equip_custos_placa").selectpicker('selectAll');
    } else if ( let_nome_btn == 'btn_gera_dados_custos_placas_proj' ) {
        let let_lista_handle_proj = $("#sl_proj_custos_placa").val().toString();
        let let_lista_handle_contas = $("#sl_tipo_veic_equip_custos_placa").val().toString();
        let let_comp = $("#dt_comp_frm_custos_placa").val();

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'lista_handle_proj'         :   let_lista_handle_proj,
                'lista_handle_contas'       :   let_lista_handle_contas,
                'comp'                      :   let_comp
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){
                $("#div_placas_frm_custos_placa").html(dados);

                let_loader_frm_custos_placa.style.display = "none";


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
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