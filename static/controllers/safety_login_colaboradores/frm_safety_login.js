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

    if (let_data_nascimento == '') {
        msg_erro_form += 'Informe a data de nascimento!<br>';
    }
    let let_data_nasc_split = let_data_nascimento.split('/');
    if (!isNaN(let_data_nasc_split[0]) && !isNaN(let_data_nasc_split[1]) && !isNaN(let_data_nasc_split[2])) {
        if ((let_data_nasc_split[0].length != 2 || Number(let_data_nasc_split[0]) > 31 || Number(let_data_nasc_split[0]) < 1) || (let_data_nasc_split[1].length != 2 || Number(let_data_nasc_split[1]) > 12 || Number(let_data_nasc_split[1]) < 1) || (let_data_nasc_split[2].length != 4 || Number(let_data_nasc_split[2] < 1900) )) {
            msg_erro_form += 'Informe uma data de nascimento válida!<br>';
        }
    }
    else {
        msg_erro_form += 'Informe uma data de nascimento válida! (apenas números)<br>';
    }

    if (msg_erro_form == '') {
        let let_data_nasc_date = let_data_nasc_split[2] + '-' + let_data_nasc_split[1] + '-' + let_data_nasc_split[0];
        $.ajax({
            type: 'POST',
            url: '/safety_login_colaboradores_app/safe_login_colab',
            data: {
                'cpf_colaborador'   :   let_cpf_colaborador,
                'data_nasc_colaborador'   :   let_data_nasc_date,
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

$(document).on('keydown','.input-data-nascimento' , function(e){
    let let_dt_nascimento = $(this).val();
    let dt_nasc_len = let_dt_nascimento.length;
    if (e.key != 'Backspace') {
        if (dt_nasc_len == 2) {
            $(this).val(let_dt_nascimento.concat('/'));
        }
        if (dt_nasc_len == 5) {
            $(this).val(let_dt_nascimento.concat('/'));
        }
    }
});