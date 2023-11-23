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
	let let_name_btn = $(this).attr('name');
	let let_id_btn = $(this).attr('id');
	let let_val_btn = $(this).val();
	var data_ini = new Date($('#dt_gera_tma_ti_ini').val());
    var day = data_ini.getUTCDate();
    var month = data_ini.getUTCMonth()+1;
    var year = data_ini.getUTCFullYear();
	let let_data_ini = [year, month, day].join('-')

    var data_fim = new Date($('#dt_gera_tma_ti_fim').val());
    day = data_fim.getUTCDate();
    month = data_fim.getUTCMonth()+1;
    year = data_fim.getUTCFullYear();
    let let_data_fim = [year, month, day].join('-')

	if (let_name_btn == "btn_pesq_tma_ti") {
	    $.ajax({
	        type: 'POST',
	        data: {
                'data_inicio'   :   let_data_ini,
                'data_fim'      :   let_data_fim
            },
	        url: '/ti_tma_app/gera_tma_chamados_ti',
	        success: function(response) {

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