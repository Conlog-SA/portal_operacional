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

$(document).on('change', '#cb_pac_vinc_resp', function(){
    let let_cod_pacote = $(this).val();
    atualiza_comp_contas_form_vincula_resp_pac_contas(let_cod_pacote);
});



function atualiza_comp_contas_form_vincula_resp_pac_contas(cod_pacote){
    let let_loader_vincula_resp = document.getElementById("loader_vincula_resp");
    let_loader_vincula_resp.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/atualiza_contas_cb_contas_pac_doc_m1',
        data: {
            'cod_pacote_conta'    :  cod_pacote
        },
        dataType: 'json',
        success: function (dados) {
            $("#cb_pac_contas_imp_doc_pac_conta_m1 option").remove();
            dados.lista_contas.forEach(conta => {
                $("#cb_pac_contas_imp_doc_pac_conta_m1").append("<option value='"+
                conta.cod_conta+"'>"+conta.cod_conta+ " - " + conta.desc_conta+" - Cód. red. CP - "+conta.cod_red_conta_contabil_cp+
                " Cód. red. LP - "+conta.cod_red_conta_contabil_lp+"</option>");
            });
            $("#cb_pac_contas_imp_doc_pac_conta_m1").selectpicker('refresh');

            let_loader_vincula_resp.style.display = "none";

        },
        error: function (request, status, error) {
            let_loader_vincula_resp.style.display = "none";
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