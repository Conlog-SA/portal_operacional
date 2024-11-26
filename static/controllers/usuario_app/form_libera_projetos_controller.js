
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
    /* Variaveis globais */
    let lista_proj_usuario;
});

$(document).on('change', '#cb_usuarios_frm_libera_proj', function(){
    let let_cod_usu = $(this).val();
    atualiza_tab_proj_usu(let_cod_usu);
});

$(document).on('change', '#cb_emp_frm_libera_proj', function(){
    let let_cod_emp =$(this).val();
    $.ajax({
        type: 'GET',
        url:"/usuario_app/povoa_cd_filial_por_empresa",
        data: {
            'cod_empresa': let_cod_emp
        },
        dataType: 'json',
        success: function(data){
            $("#cb_filial_frm_libera_proj option").remove();
            data.lista_filiais.forEach(fil => {
                $("#cb_filial_frm_libera_proj").append("<option value='"+fil.cod_filial+"'>"+fil.desc_filial+"</option>");
            });
            $("#cb_filial_frm_libera_proj").selectpicker('refresh');

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
});

$(document).on('change','input', function(){
    let let_name_input = $(this).attr('name');
    let let_id_input = $(this).attr('id');

    if (let_name_input == "chk_seleciona_filiais_frm_libera_proj") {
        let let_check_comp = $(this).prop("checked");

        if (let_check_comp == true) {
            $("#cb_filial_frm_libera_proj").selectpicker('selectAll');
        } else if (let_check_comp == false) {
            $("#cb_filial_frm_libera_proj").selectpicker('deselectAll');
        }
    } else if (let_name_input == "chk_seleciona_proj_frm_libera_proj") {
        let let_check_comp = $(this).prop("checked");

        if (let_check_comp == true) {
            $("#cb_proj_frm_libera_proj").selectpicker('selectAll');
        } else if (let_check_comp == false) {
            $("#cb_proj_frm_libera_proj").selectpicker('deselectAll');
        }

    }


});

$(document).on('change', '#cb_filial_frm_libera_proj', function(){
    let let_lista_cod_filiais =$(this).val().toString();
    let let_cod_empresa = $("#cb_emp_frm_libera_proj").val();
    if (let_lista_cod_filiais != '' && let_cod_empresa != ''){
        $.ajax({
        type: 'GET',
        url:"/usuario_app/povoa_cd_proj_por_filial",
        data: {
            'lista_cod_filiais': let_lista_cod_filiais,
            'cod_empresa': let_cod_empresa
        },
        dataType: 'json',
        success: function(data){
            $("#cb_proj_frm_libera_proj option").remove();
            data.lista_proj.forEach(proj => {
                $("#cb_proj_frm_libera_proj").append("<option value='"+proj.cod_proj+"'>"+proj.nome_proj+"</option>");
            });
            $("#cb_proj_frm_libera_proj").selectpicker('refresh');

        },
        error: function (request, status, error) {
              alert(error);
        }
    });
    }

});


$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_libera_projetos_usu_form_libera_projetos") {
        let let_cod_usu = $("#cb_usuarios_frm_libera_proj").val().toString();
        let let_lista_proj = $("#cb_proj_frm_libera_proj").val().toString();
        $.ajax({
            type: 'POST',
            url: '/usuario_app/salva_permissoes_projeto_form_libera_proj',
            data: {
                'cod_usu'       :   let_cod_usu,
                'lista_projetos'    :   let_lista_proj

            },
            dataType: 'json',
            success: function (data) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.lista_msg.toString(),
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                atualiza_tab_proj_usu(let_cod_usu);
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
    else if (let_nome_btn == "btn_bloquear_proj_usu") {
        let let_cod_proj_usu = $("#btn_bloquear_proj_usu_"+let_val_btn).val();
        let let_bloqueia_registro = 'N';
        $.ajax({
            type: 'POST',
            url: '/usuario_app/bloqueia_desbloqueia_permissoes_projeto_form_libera_proj',
            data: {
                'cod_proj_usu'      :   let_cod_proj_usu,
                'valor_bloqueio'    :   let_bloqueia_registro

            },
            dataType: 'json',
            success: function (data) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                atualiza_tab_proj_usu(data.cod_usu);
            },error: function (request, status, error) {
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
    else if (let_nome_btn == "btn_liberar_proj_usu") {
        let let_cod_proj_usu = $("#btn_liberar_proj_usu_"+let_val_btn).val();
        let let_bloqueia_registro = 'S';
        $.ajax({
            type: 'POST',
            url: '/usuario_app/bloqueia_desbloqueia_permissoes_projeto_form_libera_proj',
            data: {
                'cod_proj_usu'      :   let_cod_proj_usu,
                'valor_bloqueio'    :   let_bloqueia_registro
            },
            dataType: 'json',
            success: function (data) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                atualiza_tab_proj_usu(data.cod_usu);
            },error: function (request, status, error) {
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



function atualiza_tab_proj_usu(cod_usu){
    $.ajax({
        type: 'GET',
        url: '/usuario_app/retorna_proj_usu',
        data: {
            'cod_usu'   :   cod_usu
        },
        dataType: 'json',
        success: function (data) {
            $("#tabLiberacoesProjUsu").DataTable().clear().draw();
            lista_proj_usuario = [];
            data.lista_liberacoes.forEach(pro_usu => {
                let let_perfil_usu  = '';
                if ( pro_usu.cod_usu__perfil_usu == 'A') {
                    let_perfil_usu = 'Administrador';
                } else if ( pro_usu.cod_usu__perfil_usu == 'C') {
                    let_perfil_usu = 'Colaborador';
                }
                let let_corporativo_usu = '';
                if ( pro_usu.cod_usu__corporativo == 'S') {
                    let_corporativo_usu = 'Sim';
                } else if ( pro_usu.cod_usu__corporativo == 'N') {
                    let_corporativo_usu = 'Não';
                }
                let let_img_status_proj_usu = '';
                let let_btn_bloqueia_desbloqueia_proj_usu = '';
                if ( pro_usu.status_proj_usu == 'S') {
                    let_img_status_proj_usu = `
                        <i class="fa-solid fa-circle-check" title="Ativo" "></i>
                    `;
                    let_btn_bloqueia_desbloqueia_proj_usu = `
                        <button type='button'
                            class='btn btn-rounded btn-space'
                            id='btn_bloquear_proj_usu_${pro_usu.cod_proj_usu}' title='Bloquear'
                            name='btn_bloquear_proj_usu' value='${pro_usu.cod_proj_usu}'>
                            <i class="fa-solid fa-lock" style="color: white;"></i>
                        </button>
                    `;
                } else if ( pro_usu.status_proj_usu == 'N') {
                    let_img_status_proj_usu = `
                        <i class="fa-sharp fa-regular fa-circle-xmark" title="Desativado"></i>
                    `;
                    let_btn_bloqueia_desbloqueia_proj_usu = `
                        <button type='button'
                            class='btn btn-rounded btn-space'
                            id='btn_liberar_proj_usu_${pro_usu.cod_proj_usu}' title='Desbloquear'
                            name='btn_liberar_proj_usu' value='${pro_usu.cod_proj_usu}'>
                            <i class="fa-solid fa-unlock" style="color: white;"></i>
                        </button>
                    `;
                }
                var registro = [
                    let_img_status_proj_usu,
                    pro_usu.cod_usu__nome_usu,
                    pro_usu.cod_projeto__desc_proj,
                    let_perfil_usu,
                    let_corporativo_usu,
                    pro_usu.data_fim_proj_usu,
                    let_btn_bloqueia_desbloqueia_proj_usu

                ];
                lista_proj_usuario.push(registro);
            });
            $('#tab_liberacoes_proj_usu').DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 10,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":lista_proj_usuario,
                "columns": [
                    { title: "" },
                    { title: "Colaborador" },
                    { title: "Projeto" },
                    { title: "Perfil" },
                    { title: "Corporativo?" },
                    { title: "Liberado Até" },
                    { title: "Bloqueia/Desbloqueia" }
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [0,3,4,5,6]},
                    {"className": "dt-left", "targets": [1,2]}
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

