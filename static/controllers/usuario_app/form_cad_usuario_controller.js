

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
    /* Variáveis globais */
    let let_lista_dados_usuarios;

    atualiza_tab_usuarios();

});

document.title = "Cadastro de Usuários | Portal Operacional";

$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_add_usu") {
        let let_nome_usu = $("#txt_nome_usu").val();
        let let_habilita_usu = $("#chk_ativa_usu").prop("checked");
        let let_tipo_acesso_menu = $("#chk_ativa_corporativo").prop("checked");
        let let_email_usu = $("#txt_email_usu").val();
        let let_perfil_usu = $("#cb_perfil_usu").val();
        let let_login_usu = $("#txt_login_usu").val();
        let let_cod_filial_usu = $("#cb_filial_usu").val();

        if ( let_nome_usu == '' || let_email_usu == '' ||  let_perfil_usu == 0 || let_login_usu == '' ||
            let_cod_filial_usu == 0) {
            $.gritter.add({
                title: 'Atenção!',
                text: "Todos os campos devem ser preenchidos. Verifique !",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $.ajax({
                type:"POST",
                url:"/usuario_app/add_novo_usu",
                data: {
                    'nome_usu'       :   let_nome_usu,
                    'habilita_usu'   :   let_habilita_usu,
                    'corporativo_usu':   let_tipo_acesso_menu,
                    'email_usu'      :   let_email_usu,
                    'perfil_usu'     :   let_perfil_usu,
                    'login_usu'      :   let_login_usu,
                    'cod_filial'     :   let_cod_filial_usu

                  },
                success: function(data){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: data.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    atualiza_tab_usuarios();
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


    }
    else if (let_nome_btn == "btn_novo_usu") {
        $("#dv_msg_form_cad_usu").html("");
        $("#txt_nome_usu").val("");
        $("#txt_email_usu").val("");
        $("#cb_perfil_usu").val("0");
        $('#cb_perfil_usu').selectpicker('refresh');
        $("#txt_login_usu").val("");
        $("#cb_filial_usu").val('0');
        $('#cb_filial_usu').selectpicker('refresh');

    }
    else if (let_nome_btn == "btn_editar_usu") {
        let let_indice_registro = let_val_btn;

        if ( let_lista_dados_usuarios[let_indice_registro][9] == 'A' ){
            $("#chk_ativa_usu").prop("checked", true);
        } else {
            $("#chk_ativa_usu").prop("checked", false);
        }

        if ( let_lista_dados_usuarios[let_indice_registro][10] == 'S' ){
            $("#chk_ativa_corporativo").prop("checked", true);
        } else {
            $("#chk_ativa_corporativo").prop("checked", false);
        }

        $("#txt_nome_usu").val(let_lista_dados_usuarios[let_indice_registro][1]);
        $("#txt_email_usu").val(let_lista_dados_usuarios[let_indice_registro][6]);
        $("#cb_perfil_usu").val(let_lista_dados_usuarios[let_indice_registro][8]);
        $("#txt_login_usu").val(let_lista_dados_usuarios[let_indice_registro][5]);
        $("#cb_filial_usu").val(let_lista_dados_usuarios[let_indice_registro][11]);
        $('#cb_filial_usu').selectpicker('refresh');


        $('html,body').scrollTop(0);
    }


});



function atualiza_tab_usuarios(){
    $.ajax({
        url:"/usuario_app/list_usuarios",
        success: function(data){
            $("#tab_usuarios").DataTable().clear().draw();
            let_lista_dados_usuarios = [];

            for (var i = 0; i < data.list_usuario_cadastrados.length; i++) {
                let let_img_status_usu  = '';
                if (data.list_usuario_cadastrados[i].status_usu == 'A'){
                    let_img_status_usu = `
                        <i class="fa-solid fa-user fa-2xl fa-beat" style="color: #f46424;" title="Ativo"></i>
                    `;
                } else if (data.list_usuario_cadastrados[i].status_usu == 'D'){
                    let_img_status_usu = `
                        <i class="fa-regular fa-2xl fa-user" style="color: #f46424;" title="Desativado"></i>
                    `;
                }
                let let_perfil_usu = '';
                if (data.list_usuario_cadastrados[i].perfil_usu == 'A'){
                    let_perfil_usu = "Administrador";
                } else if (data.list_usuario_cadastrados[i].perfil_usu == 'C'){
                    let_perfil_usu = "Colaborador";
                }

                let let_tipo_acesso = '';
                if (data.list_usuario_cadastrados[i].corporativo == 'S') {
                    let_tipo_acesso = 'Corporativo';
                } else if (data.list_usuario_cadastrados[i].corporativo == 'N') {
                    let_tipo_acesso = 'Restrito';
                }

                let let_btn_edita_usu = `
                    <button type='button' id='btn_editar_usu_${i}'
                    name='btn_editar_usu' value='${i}' class='btn btn-sm btn-primary btn-rounded cadastro__botaoTabela'>
                        <i class="fa-solid fa-user-pen" style="color: #fff;" ></i>
                    </button>
                `;

                let let_reg = [
                    /* 0 */let_img_status_usu,
                    /* 1 */data.list_usuario_cadastrados[i].nome_usu,
                    /* 2 */data.list_usuario_cadastrados[i].cod_filial__desc_filial,
                    /* 3 */let_perfil_usu,
                    /* 4 */let_tipo_acesso,
                    /* 5 */data.list_usuario_cadastrados[i].login_usu,
                    /* 6 */data.list_usuario_cadastrados[i].email_usu,
                    /* 7 */let_btn_edita_usu,
                    /* 8 */data.list_usuario_cadastrados[i].perfil_usu,
                    /* 9 */data.list_usuario_cadastrados[i].status_usu,
                    /* 10 */data.list_usuario_cadastrados[i].corporativo,
                    /* 11 */data.list_usuario_cadastrados[i].cod_filial__cod_filial
                ];
                let_lista_dados_usuarios.push(let_reg);
                

            }
            $('#tab_usuarios').DataTable( {
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": ['excelHtml5',
                            'pdfHtml5'
                ],
                "data":let_lista_dados_usuarios,
                "columns": [
                    { title: "Ativo?" },
                    { title: "Nome Usuário" },
                    { title: "Filial" },
                    { title: "Perfil" },
                    { title: "Tipo Acesso" },
                    { title: "Login" },
                    { title: "Email" },
                    { title: "Editar" }
                ],
                "oLanguage": {
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
                    }
                }
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


