$(document).on('click','.clickable' , function(){
    let URL = $(this).attr("value");
    window.open(URL,'_blank','','');
});

$(document).on('click','.button-check-post' , function(){
    $(this).addClass("selected");
    quantidade_botoes = $(this).siblings().length;
    for (let i = 0; i < quantidade_botoes; i++) {
      element = $(this).siblings().eq(i);
      element.removeClass("selected");
    }
    let resposta_check = 2;
    let name =  $(this).attr("name").split('@')
    let cod_item_check = name[0]
    let cod_check_aplicado = name[1]

    if ($(this).hasClass("ok-button-check")) {
        resposta_check = 0;
    }
    else if ($(this).hasClass("nok-button-check")) {
        resposta_check = 1;
    }
    else if ($(this).hasClass("blue-button-check")) {
        resposta_check = 2;
    }
    else if ($(this).hasClass("yellow-button-check")) {
        resposta_check = 3;
    }
    else if ($(this).hasClass("orange-button-check")) {
        resposta_check = 4;
    }

    if (resposta_check < 5) {
        $.ajax({
            type: 'POST',
            url: '/safety_checks_aplicados_app/item_aplicado',
            data: {
                'tipo_input'   :   'button',
                'resposta'     :   resposta_check,
                'cod_item_check' : cod_item_check,
                'cod_check_aplicado' : cod_check_aplicado
            },
            success: function (dados) {
            }
        });
    }
});

$(document).on('change', '.textarea-check-post', function(){
    let name =  $(this).attr("name").split('@')

    let cod_item_check = name[0];
    let cod_check_aplicado = name[1];
    let resposta_check = $(this).val();

    $.ajax({
        type: 'POST',
        url: '/safety_checks_aplicados_app/item_aplicado',
        data: {
            'tipo_input'   :   'text',
            'resposta'     :   resposta_check,
            'cod_item_check' : cod_item_check,
            'cod_check_aplicado' : cod_check_aplicado
        },
        success: function (dados) {
        }
    });
});

async function compressImage(file) {
  console.log('originalFile instanceof Blob', file instanceof Blob); // true
  console.log(`originalFile size ${file.size / 1024 / 1024} MB`);

  const options = {
    maxSizeMB: 1,
    //maxWidthOrHeight: 1920,
    useWebWorker: true
  };

  try {
    const compressedFile = await imageCompression(file, options);
    console.log('compressedFile instanceof Blob', compressedFile instanceof Blob); // true
    console.log(`compressedFile size ${compressedFile.size / 1024 / 1024} MB`); // smaller than maxSizeMB
    return compressedFile;
  } catch (error) {
    console.error('Compression error:', error);
    return file;
  }
}

$(document).on('change','.file-check-post' , async function(event){
    let file = event.target.files[0];
    element = $(this).siblings().eq(0);

    if (file) {
        let compressedFile = await compressImage(file);
        element.css("background-color", "#f46424");
        element.addClass("clickable");
        element.attr("value", URL.createObjectURL(compressedFile));

            let name =  $(this).attr("name").split('@')

        let cod_item_check = name[0];
        let cod_check_aplicado = name[1];

        var formDataImg = new FormData();
        //formDataImg.append("file", $(this)[0].files[0]);
        formDataImg.append("file", compressedFile, compressedFile.name);
        formDataImg.append("tipo_input", 'image');
        formDataImg.append("cod_item_check", cod_item_check);
        formDataImg.append("cod_check_aplicado", cod_check_aplicado);

        $.ajax({
            type: 'POST',
            enctype: "multipart/form-data; charset=utf-8",
            url: '/safety_checks_aplicados_app/item_aplicado',
            data: formDataImg,
            processData: false,
            contentType: false,
            cache: false,
            success: function (dados) {
                $(this).attr("value", "");
            }
        });
    }
    else {
        element.css("background-color", "#9fa3a7");
        element.removeClass("clickable");
        element.attr("value", '');
    }

});

$(document).on('click','.btn-voltar-menu-safety' , function(){

    if ($('.background-check-preenchido').length == 0) {
        $.ajax({
            type: 'POST',
            url: '/safety_login_colaboradores_app/',
            data: {
                        'flag_voltar'      :   1,
                     },
            success: function (dados) {
                $('#main_container_safety').html(dados);
                $('#main_container_safety').removeClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal');
                $('#main_container_safety').addClass('safety-container-screen text-white justify-content-center align-items-center d-flex homeApp_loginContainer');
                $('#main_container_safety').css('width', '85%');
            }
        });
    }
    else {
        let flag_invalido = 0;

        $('.background-check-preenchido').each(function(){
            if($(this).find('.obrigatorio').val() == "1") {
                if($(this).find('.input-item').val() == '') {
                    flag_invalido = 1;
                }
                let lista_botoes = $(this).find('.input-botao');
                if (lista_botoes.length > 0 && !lista_botoes.hasClass("selected")) {
                    flag_invalido = 1;
                }
            }
        });

        if (flag_invalido == 0) {
            $.ajax({
                type: 'POST',
                url: '/safety_login_colaboradores_app/',
                data: {
                            'flag_voltar'      :   1,
                         },
                success: function (dados) {
                    $('#main_container_safety').html(dados);
                    $('#main_container_safety').removeClass('d-flex align-items-center justify-content-center text-white text-center conteudoPrincipal');
                    $('#main_container_safety').addClass('safety-container-screen text-white justify-content-center align-items-center d-flex homeApp_loginContainer');
                    $('#main_container_safety').css('width', '85%');

                    flag_visitante = $('#button_flag_visitante').val();
                    if (flag_visitante != "True") {
                        $.gritter.add({
                            title: 'Sucesso!',
                            text: 'Check preenchido com sucesso',
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                    }

                }
            });
        }
        else if (flag_invalido == 1) {
            $.gritter.add({
                title: 'Erro!',
                text: 'Existem perguntas obrigatórias não respondidas!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    }
});


