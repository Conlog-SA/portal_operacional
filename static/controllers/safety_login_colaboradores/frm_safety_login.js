$(document).on('click','.btn-login-safety' , function(){
    let let_cpf_colaborador = $('#input_cpf').val();
    let let_data_nascimento = $('#input-data-nascimento').val();

    $.ajax({
        type: 'POST',
        url: '/safety_login_colaboradores_app/safe_login_colab',
        data: {
            'cpf_colaborador'   :   let_cpf_colaborador,
            'data_nasc_colaborador'   :   let_data_nascimento,
        },
        success: function (dados) {
            $('#main_container_safety').removeClass('align-items-center');
            $('#main_container_safety').removeClass('w-75');
            $('#main_container_safety').removeClass('h-75');

            $('#main_container_safety').addClass('safety-container-screen');

            $('#main_container_safety').html(dados);
        }
    });
});

$(document).on('click','.safety-app-empilhadeiras' , function(){
    $.ajax({
        type: 'POST',
        url: '/safety_login_colaboradores_app/safe_main_menu',
        data: {
            'tipo_check'   :   0,
        },
        success: function (dados) {
            $('#main_container_safety').html(dados)
            $('#main_container_safety').removeClass('safety-container-screen text-white justify-content-center align-items-center d-flex homeApp_loginContainer')
            $('#main_container_safety').addClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal')
            $('#main_container_safety').css("margin-left","0px");
            $('#main_container_safety').css('width', '100%');

            $('.selectpicker').selectpicker();
        }
    });
});

$(document).on('click','.safety-app-relatos' , function(){

    $.ajax({
        type: 'POST',
        url: '/safety_login_colaboradores_app/safe_main_menu',
        data: {
            'tipo_check'   :   1,
        },
        success: function (dados) {
            $('#main_container_safety').html(dados)
            $('#main_container_safety').removeClass('safety-container-screen text-white justify-content-center align-items-center d-flex homeApp_loginContainer')
            $('#main_container_safety').addClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal')
            $('#main_container_safety').css("margin-left","0px");
            $('#main_container_safety').css('width', '100%');

            $('.selectpicker').selectpicker();
        }
    });
});

$(document).on('click','.btn-sair-safety' , function(){

    $.ajax({
        type: 'POST',
        url: '/safety_login_colaboradores_app/safe_main_menu',
        data: {
            'tipo_check'   :   999,
        },
        success: function (dados) {
            $('#main_container_safety').html(dados)
            $('#main_container_safety').removeClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal')
            $('#main_container_safety').addClass('safety-container-screen text-white justify-content-center align-items-center d-flex homeApp_loginContainer')
            $('#main_container_safety').css("margin-left","0px");

        }
    });
});