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

$(document).on('change', '#cb_usuarios', function(){
    let let_cod_usu =$(this).val();
    retorna_menu_sub_menu(let_cod_usu);
});


$(document).on('change','input', function(){
    let let_name_input = $(this).attr('name');
    let let_id_input = $(this).attr('id');

    if (let_name_input == "chk_ativa_menu") {
        let let_cod_usu = $("#cb_usuarios").val();

        let let_cod_menu = let_id_input.split('_')[3];
        let let_check_comp = $(this).prop("checked");

        let let_novo_status_menu = 'A';
        if (let_check_comp == false) {
            let_novo_status_menu = 'D';
        }

        $.ajax({

            type: "POST",
            url: '/usuario_app/destativa_ativa_item_usuario_menu',
            data: {
                'cod_menu'       :   let_cod_menu,
                'cod_usu'        :   let_cod_usu,
                'status'         :   let_novo_status_menu
            },
            dataType: 'json',
            success: function (data) {
                let let_cod_usu = $("#cb_usuarios").val();
                retorna_menu_sub_menu(let_cod_usu);
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            },
            error: function (request, status, error) {
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

$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_abre_modal_replica_acessos") {
        $("#modal_replicacao_acesso_modulos").show();
    } else if (let_nome_btn == "bnt_fecha_modal_replicacao_acesso_modulos") {
        $("#modal_replicacao_acesso_modulos").hide();
    } else if (let_nome_btn=="btn_replica_acesso_modulos"){
        let let_cod_usu = $("#cb_usuarios").val();
        let let_list_cod_usus_string = $("#cb_usu_replicacao").val().toString();

        $.ajax({
            type: "POST",
            url: '/usuario_app/replica_modulos_ativos_usuarios',
            data: {
                'cod_usu_origem'              :   let_cod_usu,
                'lista_cod_usu_string'        :   let_list_cod_usus_string
            },
            dataType: 'json',
            success: function (data) {
                $("#modal_replicacao_acesso_modulos").hide();
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            },
            error: function (request, status, error) {
                $("#modal_replicacao_acesso_modulos").hide();
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


function retorna_menu_sub_menu(cod_usuario_param){
    $("#div_modulos_usu").html("");
    $.ajax({
        type:"GET",
        url:"/usuario_app/menus_ativos_menus_usu",
        data: {
            'cod_usu'       :   cod_usuario_param
         },
        dataType: 'json',
        success: function(dados){
            let let_html_pagina = `
                <div class="accordion" id="acc_modulos">
            `;

            dados.list_menu_form.forEach( menu => {
                let let_check_menu = `
                    <div class="d-flex flex-column ">
                        <div class="container">
                            <input type="checkbox" class="checkbox" name="chk_ativa_menu"
                            id="chk_ativa_menu_${menu.cod_menu}">
                            <label class="switch" for="chk_ativa_menu_${menu.cod_menu}">
                                <span class="slider"></span>
                            </label>
                        </div>
                    </div>
                `;
                if(menu.status_usu == 'A'){
                    let_check_menu = `
                    <div class="d-flex flex-column ">
                        <div class="container">
                            <input type="checkbox" class="checkbox" checked name="chk_ativa_menu_${menu.cod_menu}" id="chk_ativa_menu_${menu.cod_menu}">
                            <label class="switch" for="chk_ativa_menu_${menu.cod_menu}">
                                <span class="slider"></span>
                            </label>
                        </div>
                    </div>
                    `;
                }


                let_html_pagina += `

                <div class="accordion-item">
                    <h2 class="accordion-header d-flex justify-content-between align-items-center" id="heading_${menu.cod_menu}">
                        <button class="accordion-button collapsed d-flex justify-content-between" type="button" data-bs-toggle="collapse" data-bs-target="#collapse_${menu.cod_menu}" aria-expanded="false" aria-controls="collapse_${menu.cod_menu}">
                            <div class="d-flex justify-content-center align-items-center">
                                <i class="iconeMenu ${menu.nome_icone}" alt="${menu.desc_menu}"></i>
                                <p style="margin:0; padding:0;">${menu.desc_menu}</p>
                            </div>
                            </button>
                            ${let_check_menu}
                    </h2>
                    
                    <div id="collapse_${menu.cod_menu}" class="accordion-collapse collapse" aria-labelledby="heading_${menu.cod_menu}" data-bs-parent="#accordionExample">
                    <div class="accordion-body flex-wrap d-flex justify-content-between align-items-center">
                `;
                dados.lista_sub_menu_form.forEach( sub_menu => {
                    if ( sub_menu.pai_menu == menu.cod_menu) {
                        let let_check_sub_menu = `
                            <div class="d-flex flex-column">
                                <div class="container">
                                    <input type="checkbox" class="checkbox" name="chk_ativa_menu_${sub_menu.cod_sub_menu}" id="chk_ativa_menu_${sub_menu.cod_sub_menu}">
                                    <label class="switch" for="chk_ativa_menu_${sub_menu.cod_sub_menu}">
                                        <span class="slider"></span>
                                    </label>
                                </div>
                            </div>
                        `;
                        if(sub_menu.status_usu == 'A'){
                            let_check_sub_menu = `
                            <div class="d-flex flex-column ">
                                <div class="container">
                                    <input type="checkbox" class="checkbox" checked name="chk_ativa_menu_${sub_menu.cod_sub_menu}" id="chk_ativa_menu_${sub_menu.cod_sub_menu}">
                                    <label class="switch" for="chk_ativa_menu_${sub_menu.cod_sub_menu}">
                                        <span class="slider"></span>
                                    </label>
                                </div>
                            </div>
                            `;
                        }
                        let_html_pagina += `
                            <div class="w-100 mb-3 d-flex justify-content-between align-items-center">
                                <div class="d-flex justify-content-between align-items-center">
                                    <i class="${sub_menu.nome_icone}" alt="${sub_menu.desc_sub_menu}" style="margin-right:1rem; margin-left:2rem;"></i>
                                    <p style="margin:0; padding:0;">${sub_menu.desc_sub_menu}</p>       
                                </div>
                                `
                                +
                                let_check_sub_menu
                                +
                                `
                            </div>
                        `;
                    }
                });
                let_html_pagina += `
                    </div>
                      </div>
                    </div>
                `;
            });
            let_html_pagina += `
                </div>
            `;
            $("#div_modulos_usu").html(let_html_pagina);


        },
        error: function (request, status, error) {
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