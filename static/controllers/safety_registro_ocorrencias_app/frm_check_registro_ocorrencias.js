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


$(document).on('click','.create-check-registro-ocorrencias' , function(){

    const componentes = document.querySelectorAll('.campo-obgo-reg-ocor');
    tem_campos_obrigatorios_branco = 0;
    msg_erro = ``;
    componentes.forEach(comp => {
        if(comp.value == '' || comp == null){
            tem_campos_obrigatorios_branco += 1;
            msg_erro += `${comp.title}<br/>`;
        }
    });

    if (tem_campos_obrigatorios_branco == 0) {
        $.ajax({
            type: 'POST',
            url: '/safety_registro_ocorrencias_app/preencher_itens_check_reg_ocorrencia',
            data: {
                'cod_unidade'       :  $('#sl_cod_unidade_reg_ocor').val(),
                'cod_negocio'       : $("#sl_negocio_reg_ocor").val(),
                'cod_tipo_relato'   : $("#sl_tipo_relato_reg_ocor").val(),
                'nome_empresa_envolvida': $("#txt_nome_empresa_envolvida").val(),
                'turno'                 : $("#sl_turno_reg_ocor").val(),
                'cod_nexo'              : $("#sl_nexo_reg_ocor").val(),
                'cod_local_ocorrencia'  : $("#sl_local_reg_ocor").val(),
                'area_detalhada'        : $("#txt_desc_detalhe_area").val(),
                'cod_atividade'         : $("#sl_atividade_reg_ocor").val(),
                'cod_natureza'          : $("#sl_natureza_reg_ocor").val(),
                'dt_reg_ocorencia'      : $("#dt_ocorrencia_reg_ocor").val(),
                'hr_reg_ocorencia'      : $("#hr_ocorrencia_reg_ocor").val(),
                'classificacao_ocorrencia'  : $("#sl_classificacao_reg_ocor").val(),
                'risco_real'                : $("#sl_risco_real_reg_ocor").val(),
                'causa'                     : $("#sl_causa_reg_ocor").val(),
            },
            dataType: 'html',
            success: function (dados) {
                $("#div_corpo_registro_ocorrencia").html(dados);
                $("#div_corpo_registro_ocorrencia").css('background-color', 'rgba(0,0,0,0)')
            },
            error: function (xhr, status, error) {
                console.log(`Erro ${error}`);
                console.log(`Status ${status}`);
                 $.gritter.add({
                    title: 'Erro!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    }
    else {
        $.gritter.add({
            title: 'Campos obrigatórios. Verifique:',
            text: msg_erro,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });

    }
});