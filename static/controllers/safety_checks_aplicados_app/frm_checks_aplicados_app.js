$(document).on('click','.clickable' , function(){
    let URL = $(this).attr("value");
    window.open(URL,'_blank','','');
});

$(document).on('click','.button-check-post' , function(){
    $(this).addClass("selected");
    element = $(this).siblings().eq(0);
    element.removeClass("selected");

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

    if (resposta_check != 2) {
        $.ajax({
            type: 'POST',
            url: '/safety_gab_op_emp_app/item_check_empilhadeira',
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
        url: '/safety_gab_op_emp_app/item_check_empilhadeira',
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

$(document).on('change','.file-check-post' , function(event){
    let file = event.target.files[0];
    element = $(this).siblings().eq(0);
    if (file) {
        console.log(element)
        element.css("background-color", "#f46424");
        element.addClass("clickable");
        element.attr("value", URL.createObjectURL(file))
    }
    else {
        element.css("background-color", "#9fa3a7");
        element.removeClass("clickable");
        element.attr("value", '')
    }
    let name =  $(this).attr("name").split('@')

    let cod_item_check = name[0];
    let cod_check_aplicado = name[1];

    var formDataImg = new FormData();
    formDataImg.append("file", $(this)[0].files[0]);
    formDataImg.append("tipo_input", 'image');
    formDataImg.append("cod_item_check", cod_item_check);
    formDataImg.append("cod_check_aplicado", cod_check_aplicado);

    $.ajax({
        type: 'POST',
        enctype: "multipart/form-data; charset=utf-8",
        url: '/safety_gab_op_emp_app/item_check_empilhadeira',
        data: formDataImg,
        processData: false,
        contentType: false,
        cache: false,
        success: function (dados) {
        }
    });
});



