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
    let let_status_login = $("#hd_indica_status_login").val();
    let let_msg_return = $("#hd_msg_return").val();
    let let_cod_empresa = $("#hd_cod_empresa").val().toString();



    if( let_cod_empresa == '12'){
        $('body').css('background-image', "url('../../static/img/background.jpg')");
    } else {
        $('body').css('background-image', "url('../../static/img/background-deep.jpg')");
    }


    let let_span = $("<span/>");
    let_span.attr({
        class:"fa fa-user-check"
    });



    if (let_status_login == 1){
        $.gritter.add({
            title: 'Atenção!',
            text: let_msg_return,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });

        form_login = document.getElementById('form_login')
        form_login.action = 'logon'
    }

});

