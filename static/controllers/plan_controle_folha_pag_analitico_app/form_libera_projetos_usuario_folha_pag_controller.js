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

$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if (nomeDoButton == 'btn_libera_proj_usuario_tab_usu'){
        var var_cod_usuario = $("#sel_usuarios_folha_pag_tab_usu").val();
        var var_lista_projetos = $("#sel_projetos_folha_pag_tab_usu").val().toString();
        if (var_cod_usuario == 0 || var_lista_projetos == 0) {
            $.gritter.add({
                title: 'Atenção!',
                text: "Informe o Usuário e o(s) Projeto(s) para liberação !!!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $.ajax({
                type: "POST",
                data: {
                    'cod_liberacao' : 0,
                    'cod_usuario'   : var_cod_usuario,
                    'lista_projetos': var_lista_projetos
                  },
                url:"/plan_controle_folha_pag_analitico_app/libera_bloqueia_proj_usu_tab_usu",
                success: function(dados){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });

                    atualiza_tab_liberacoes_usuario(var_cod_usuario);

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

    } else if (nomeDoButton == 'btn_libera_proj_usuario_tab_proj'){
           var var_dados_proj = $("#sel_projetos_folha_pag_tab_proj").val();
           var var_lista_usuarios = $("#sel_usuarios_folha_pag_tab_proj").val().toString();
           if (var_dados_proj == 0 || var_lista_usuarios == 0) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: "Informe o Projeto e o(s) Usuários(s) para liberação !!!",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
           } else {
            $.ajax({
               type: "POST",
               data: {
                   'cod_liberacao' : 0,
                   'dados_proj'   : var_dados_proj,
                   'lista_usuarios': var_lista_usuarios
                 },
               url:"/plan_controle_folha_pag_analitico_app/libera_bloqueia_proj_usu_tab_proj",
               success: function(dados){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });

                   atualiza_tab_liberacoes_projeto(var_dados_proj.split('_')[0]);

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

    } else if (nomeDoButton == 'btn_desmarcar_projetos_folha_pag_tab_usu'){
        $("#sel_projetos_folha_pag_tab_usu").selectpicker('deselectAll');
    }
    else if (nomeDoButton == 'sel_marca_projetos_folha_pag_tab_usu'){
        $("#sel_projetos_folha_pag_tab_usu").selectpicker('selectAll');
    } else if (nomeDoButton == 'btn_desmarcar_usuarios_folha_pag_tab_proj'){
        $("#sel_usuarios_folha_pag_tab_proj").selectpicker('deselectAll');
    }
    else if (nomeDoButton == 'sel_marca_usuarios_folha_pag_tab_proj'){
        $("#sel_usuarios_folha_pag_tab_proj").selectpicker('selectAll');
    }

});

/*
$(document).on('change', '#cb_emp_libera_proj_usu_folha_pag', function(){
    let let_cod_empresa = $(this).val();
    let let_loader_libera_proj_usu_folha_pag = document.getElementById("loader_libera_proj_usu_folha_pag");
    let_loader_libera_proj_usu_folha_pag.style.display = "flex";
    $.ajax({
        type: 'GET',
        data: {
            'cod_empresa'         : let_cod_empresa
        },
        url:"/plan_controle_folha_pag_analitico_app/pesq_projetos_by_emp",
        success: function(dados){
            $("#sel_projetos_folha_pag_tab_usu option").remove();
            dados.lista_projetos.forEach(proj => {
                $("#sel_projetos_folha_pag_tab_usu").append("<option value='"+
                proj.handle_benner+"'>"+proj.desc_proj_benner+"</option>");

            });
            $("#sel_projetos_folha_pag_tab_usu").selectpicker('refresh');

            let_loader_libera_proj_usu_folha_pag.style.display = "none";


        },
        error: function (request, status, error) {
            let_loader_libera_proj_usu_folha_pag.style.display = "none";
            $.gritter.add({
                title: 'Atenção!',
                text: error,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });

});
*/
/*
$(document).on('change', '#sel_empresa_folha_pag_tab_proj', function(){
    let let_cod_empresa = $(this).val();
    let let_loader_libera_proj_usu_folha_pag = document.getElementById("loader_libera_proj_usu_folha_pag");
    let_loader_libera_proj_usu_folha_pag.style.display = "flex";
    $.ajax({
        type: 'GET',
        data: {
            'cod_empresa'         : let_cod_empresa
        },
        url:"/plan_controle_folha_pag_analitico_app/pesq_projetos_by_emp",
        success: function(dados){
            $("#sel_projetos_folha_pag_tab_proj option").remove();
            dados.lista_projetos.forEach(proj => {
                $("#sel_projetos_folha_pag_tab_proj").append("<option value='"+
                proj.handle_benner+"'>"+proj.desc_proj_benner+"</option>");

            });
            $("#sel_projetos_folha_pag_tab_proj").selectpicker('refresh');

            let_loader_libera_proj_usu_folha_pag.style.display = "none";


        },
        error: function (request, status, error) {
            let_loader_libera_proj_usu_folha_pag.style.display = "none";
            $.gritter.add({
                title: 'Atenção!',
                text: error,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });

});
*/

$(document).on('change', '#sel_usuarios_folha_pag_tab_usu', function(){
    var var_cod_usuario = $(this).val();
    if (var_cod_usuario == 0 || var_cod_usuario == null ) {
        $.gritter.add({
            title: 'Atenção!',
            text: "Informe o Usuário!",
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    } else {
        atualiza_tab_liberacoes_usuario(var_cod_usuario);
    }
});

$(document).on('change', '#sel_projetos_folha_pag_tab_proj', function(){
    var var_handle_proj = $(this).val().split('_')[0];
    if ( var_handle_proj == 0 || var_handle_proj == null ){
        $.gritter.add({
            title: 'Atenção!',
            text: "Informe o Projeto!",
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    } else {
        atualiza_tab_liberacoes_projeto(var_handle_proj);
    }

});

$(document).on('click','input', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if (nomeDoButton == 'rbn_libera_proj_folha_pag_tab_usu'){
        var var_dados = idDoButton.split("_")
        var var_acao_ativa_desativa = $(this).prop("checked");

        var var_ativa_desativa = 'N'
        if (var_acao_ativa_desativa == true) {
            var_ativa_desativa = 'S';
        }

        $.ajax({
            type: 'POST',
            data: {
                cod_liberacao   : var_dados[7],
                acao            : var_ativa_desativa
            },
            url:"/plan_controle_folha_pag_analitico_app/libera_bloqueia_proj_usu_tab_usu",
            success: function(dados){
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

                atualiza_tab_liberacoes_usuario($("#sel_usuarios_folha_pag_tab_usu").picker('get'));

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

    } else if (nomeDoButton == 'rbn_libera_proj_folha_pag_tab_proj'){
           var var_dados = idDoButton.split("_")
           var var_acao_ativa_desativa = $(this).prop("checked");

           var var_ativa_desativa = 'N'
           if (var_acao_ativa_desativa == true) {
               var_ativa_desativa = 'S';
           }

           $.ajax({
               type: 'POST',
               data: {
                   cod_liberacao   : var_dados[7],
                   acao            : var_ativa_desativa
               },
               url:"/plan_controle_folha_pag_analitico_app/libera_bloqueia_proj_usu_tab_proj",
               success: function(dados){
                   $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });

                   atualiza_tab_liberacoes_projeto($("#sel_projetos_folha_pag_tab_proj").picker('get').split('_')[0]);

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

function atualiza_tab_liberacoes_usuario(cod_usuario) {
    let let_loader_libera_proj_usu_folha_pag = document.getElementById("loader_libera_proj_usu_folha_pag");
    let_loader_libera_proj_usu_folha_pag.style.display = "flex";
    $.ajax({
        type: "GET",
        data: {
            'cod_usuario': cod_usuario
          },
        url:"/plan_controle_folha_pag_analitico_app/pesquisa_proj_liberados_do_usuario",
        success: function(dados){
            lista_liberacoes = [];
            dados.lista_liberacoes_usu.forEach(liberacao => {
                var var_rb_libera_proj =
                `
                    <div class="container">
                        <input type="checkbox" class="checkbox"
                               name="rbn_libera_proj_folha_pag_tab_usu"
                               id="rbn_libera_proj_folha_pag_tab_usu_${liberacao.cod_libera_usu_proj}">
                        <label class="switch" for="rbn_libera_proj_folha_pag_tab_usu_${liberacao.cod_libera_usu_proj}">
                            <span class="slider"></span>
                        </label>
                    </div>

                `;
                if (liberacao.ativo_app_folha_pagamento == 'S'){
                    var_rb_libera_proj =
                    `
                        <div class="container">
                            <input type="checkbox" class="checkbox"
                                   name="rbn_libera_proj_folha_pag_tab_usu"
                                   id="rbn_libera_proj_folha_pag_tab_usu_${liberacao.cod_libera_usu_proj}"
                                   checked="checked">
                            <label class="switch" for="rbn_libera_proj_folha_pag_tab_usu_${liberacao.cod_libera_usu_proj}">
                                <span class="slider"></span>
                            </label>
                        </div>
                    `;
                }

                let let_nome_empresa = 'CONLOG';
                if (liberacao.cod_empresa == '17'){
                    let_nome_empresa = 'DEEP';
                }

                reg = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    liberacao.handle_benner,
                    liberacao.desc_proj_benner + '(' + let_nome_empresa + ')',
                    var_rb_libera_proj
                ];
                lista_liberacoes.push(reg);
            });

            $("#tab_proj_liberados_by_usu").DataTable({
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "fixedHeader": {
                    header: true,
                    footer: false
                },
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copy'
                ],
                "data":lista_liberacoes,
                "columns": [
                    { title: "" },
                    { title: "Handle Benner" },
                    { title: "Projeto" },
                    { title: "Libera/Bloqueia" }
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [0,1,3]},
                    {"className": "dt-left", "targets": [2]}
                ],
                "language": {
                    "decimal": ",",
                    "thousands": ".",
                    "sProcessing":   "Processando...",
                    "sLengthMenu":   "Mostrar _MENU_ registros",
                    "sZeroRecords":  "Não foram encontrados resultados",
                    "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
                    "sInfoEmpty":    "Mostrando de 0 até 0 de 0 registros",
                    "sInfoFiltered": "",
                    "sInfoPostFix":  "",
                    "sSearch":       "Pesquisar:",
                    "sUrl":          "",
                    "oPaginate": {
                        "sFirst":    "Primeiro",
                        "sPrevious": "Anterior",
                        "sNext":     "Proximo",
                        "sLast":     "Último"
                    },
                    "buttons":{
                        "copyTitle": 'Dados Copiados',
                        "copySuccess": {
                            _: '%d linhas copiadas',
                            1: '1 linha copiada'
                        }
                    }
                }
            });

            let_loader_libera_proj_usu_folha_pag.style.display = "none";

        },
        error: function (request, status, error) {
            let_loader_libera_proj_usu_folha_pag.style.display = "none";
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

function atualiza_tab_liberacoes_projeto(handle_projeto) {
    let let_loader_libera_proj_usu_folha_pag = document.getElementById("loader_libera_proj_usu_folha_pag");
    let_loader_libera_proj_usu_folha_pag.style.display = "flex";
    $.ajax({
        type: "GET",
        data: {
            'handle_proj': handle_projeto
          },
        url:"/plan_controle_folha_pag_analitico_app/pesquisa_usu_liberados_do_projeto",
        success: function(dados){
            lista_liberacoes = [];
            dados.lista_liberacoes_proj.forEach(liberacao => {
                var var_rb_libera_proj =
                `
                    <div class="container">
                        <input type="checkbox" class="checkbox"
                               name="rbn_libera_proj_folha_pag_tab_proj"
                               id="rbn_libera_proj_folha_pag_tab_proj_${liberacao.cod_libera_usu_proj}">
                        <label class="switch" for="rbn_libera_proj_folha_pag_tab_proj_${liberacao.cod_libera_usu_proj}">
                            <span class="slider"></span>
                        </label>
                    </div>

                `;
                if (liberacao.ativo_app_folha_pagamento == 'S'){
                    var_rb_libera_proj =
                    `
                        <div class="container">
                        <input type="checkbox" class="checkbox"
                               name="rbn_libera_proj_folha_pag_tab_proj"
                               id="rbn_libera_proj_folha_pag_tab_proj_${liberacao.cod_libera_usu_proj}"
                               checked="checked">
                        <label class="switch" for="rbn_libera_proj_folha_pag_tab_proj_${liberacao.cod_libera_usu_proj}">
                            <span class="slider"></span>
                        </label>
                    </div>

                    `;
                }

                reg = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    liberacao.cod_usu__nome_usu,
                    var_rb_libera_proj
                ];
                lista_liberacoes.push(reg);
            });

            $("#tab_proj_liberados_by_proj").DataTable({
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "fixedHeader": {
                    header: true,
                    footer: false
                },
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copy'
                ],
                "data":lista_liberacoes,
                "columns": [
                    { title: "" },
                    { title: "Usuário" },
                    { title: "Libera/Bloqueia" }
                ],
                /* Propriedade para alinhar as colunas da DataTable*/
                "columnDefs": [
                    {"className": "dt-center", "targets": [0,2]},
                    {"className": "dt-left", "targets": [1]}
                ],
                "language": {
                    "decimal": ",",
                    "thousands": ".",
                    "sProcessing":   "Processando...",
                    "sLengthMenu":   "Mostrar _MENU_ registros",
                    "sZeroRecords":  "Não foram encontrados resultados",
                    "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
                    "sInfoEmpty":    "Mostrando de 0 até 0 de 0 registros",
                    "sInfoFiltered": "",
                    "sInfoPostFix":  "",
                    "sSearch":       "Pesquisar:",
                    "sUrl":          "",
                    "oPaginate": {
                        "sFirst":    "Primeiro",
                        "sPrevious": "Anterior",
                        "sNext":     "Proximo",
                        "sLast":     "Último"
                    },
                    "buttons":{
                        "copyTitle": 'Dados Copiados',
                        "copySuccess": {
                            _: '%d linhas copiadas',
                            1: '1 linha copiada'
                        }
                    }
                }
            });
            let_loader_libera_proj_usu_folha_pag.style.display = "none";

        },
        error: function (request, status, error) {
            let_loader_libera_proj_usu_folha_pag.style.display = "none";
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