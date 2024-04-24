$(document).on('click','.btn-login-safety' , function(){
    let let_cpf_colaborador = $('#input_cpf').val();
    let let_data_nascimento = $('#input-data-nascimento').val();

    msg_erro_form = '';
    if (let_cpf_colaborador == '') {
        msg_erro_form += 'Informe um CPF!<br>';
    }
    else if (isNaN(let_cpf_colaborador)) {
        msg_erro_form += 'Digite apenas números no CPF!<br>';
    }
    let data_nasc_split = let_data_nascimento.split('-');
    console.log(let_data_nascimento);
    if (let_data_nascimento == '') {
        msg_erro_form += 'Informe a data de nascimento!<br>';
    }

    if (msg_erro_form == '') {
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
            },
            error: function (xhr, status, error) {
                let msg_erro = xhr.responseText;

                $.gritter.add({
                    title: 'Erro!',
                    text: msg_erro,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    }
    else {
        $.gritter.add({
            title: 'Erro!',
            text: msg_erro_form,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }
});

$(document).on('click','.safety-app-empilhadeiras' , function(){
    $.ajax({
        type: 'POST',
        url: '/safety_login_colaboradores_app/safe_main_menu',
        data: {
            'tipo_check'   :   0,
        },
        success: function (dados) {
            $('#main_container_safety').html(dados);
            $('#main_container_safety').removeClass('safety-container-screen text-white justify-content-center align-items-center d-flex homeApp_loginContainer');
            $('#main_container_safety').addClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal');
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
            $('#main_container_safety').html(dados);
            $('#main_container_safety').removeClass('text-white justify-content-center align-items-center d-flex homeApp_loginContainer');
            $('#main_container_safety').addClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal');
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
            //$('body').html(dados);
            $("#main_container_safety").html(dados);
            /*let newDoc = document.open("text/html", "replace");
            newDoc.write(dados);*/

            $('#main_container_safety').removeClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal');
            $('#main_container_safety').addClass('text-white justify-content-center align-items-center d-flex homeApp_loginContainer');
            $('#main_container_safety').css("margin-left","0px");

            $('.selectpicker').selectpicker();
        }
    });
});