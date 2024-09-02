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


$(document).on('change','input', function(){
	let let_nome_input = $(this).attr('name');
    let let_id_input = $(this).attr('id');
    let let_val_input = $(this).attr('value');

    if ( let_nome_input == 'fl_arquivo_remunerado') {
        let let_frm_data = new FormData();
        let_frm_data.append("tipo_planilha", $('#sl_arquivo_remunerado').val());
		let_frm_data.append("file", $('input[type=file]')[0].files[0]);
		let let_loader_frm_imp_plan_freightech = document.getElementById("loader_frm_imp_plan_freightech");
		let_loader_frm_imp_plan_freightech.style.display = "flex";
		$.ajax({
		    type: 'POST',
            enctype: "multipart/form-data; charset=utf-8",
            url: "/freightech_remunerado_qlp_app/importa_plan_remunerado_selecionada",
            data: let_frm_data,
            dataType: 'json',
            processData: false,
            contentType: false,
            cache: false,
            success: function(data){

				$.gritter.add({
                    title: 'Atenção!',
                    text: data.tipo_planilha_frm,
                    image: '../../static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let_loader_frm_imp_plan_freightech.style.display = "none";




			},
			error: function (request, status, error) {
			    let_loader_frm_imp_plan_freightech.style.display = "none";
			    $.gritter.add({
                    title: 'Atenção!',
                    text: "Erro na importação, contate o adm.",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
			}
		});

    }

});
