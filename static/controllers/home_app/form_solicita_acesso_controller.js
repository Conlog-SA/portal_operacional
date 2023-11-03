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
    $('#cb_filiais_sol').selectpicker();
});


$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');
/*
    if ( nomeDoButton == 'btn_solicita_acesso') {
        let login_usu_sol = $("#txt_login_usu_sol").val();
        let nome_usu_sol = $("#txt_nome_usu_sol").val();
        let email_usu_sol = $("#txt_email_usu_sol").val();
        let cod_filial_sol = $("#cb_filiais_sol").selectpicker('val');

        $.ajax({
            type: 'POST',
            url: '/cad_solicitacao_acesso_usu',
            data: {
                'login_usu'   :   login_usu_sol,
                'nome_usu'    :   nome_usu_sol,
                'email_usu'   :   email_usu_sol,
                'cod_fil'     :   cod_filial_sol
            },
            dataType: 'json',
            success: function (data) {
                var varDivMsg = document.getElementById('div_msg_vinculo_roteiro_item');
                $("#div_msg_vinculo_roteiro_item").html(data.msg);
                varDivMsg.style.display = 'block';
                setTimeout(function() {
                    varDivMsg.style.display = 'none';
                }, 1500);
                povoa_tab_vinculo_pecas_roteiro();

                $("#cb_roteiros").selectpicker('val', '');
                $("#txt_cod_ref_item").val('');
                $("#txt_desc_item").val('');
                $("#txt_qtd_peca").val('');

            },
            error: function (request, status, error) {
                alert(error);
          }
        });

    }
    */
});