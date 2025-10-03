let let_count_tr_parametros = 9999;
let let_lista_usuarios_frm_cria_consulta = [];

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

function mostrarComponente() {
    const adcParam = document.getElementById('add_parametros');
    const slcUsu = document.getElementById('slc_selec_usu');
    adcParam.style.visibility = 'visible';
    slcUsu.style.visibility = 'visible';
}

$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_adiciona_script" ) {
        let let_desc = $("#desc_criar_consulta").val();
        let let_script = $("#txt_script").val();
        let let_obs = $("#txt_obs").val();
        let let_sl_erp_consulta = $("#sl_erp_consulta").val();
        if((let_desc != null && let_desc != '') && (let_sl_erp_consulta != null && let_sl_erp_consulta!= '') && (let_script != null && let_script!= '') && (let_obs != null && let_obs!= '')) {
            mostrarComponente()
            let let_cod_script = let_val_btn; //$("#hd_cod_script").val();
            $.ajax({
                type: 'POST',
                url: '/ti_gera_consultas_app/gera_nova_consulta',
                data: {
                    'cod_script': let_cod_script,
                    'desc': let_desc,
                    'script': let_script,
                    'cod_conexao': let_sl_erp_consulta,
                    'obs': let_obs,
                },
                success: function (dados) {
                    //$("#hd_cod_script").val(dados.cod_script);
                    $("#btn_adiciona_script").val(dados.cod_script);
                    $("#desc_criar_consulta").val(dados.desc);
                    $("#txt_script").val(dados.script);
                    $("#txt_obs").val(dados.obs);
                    $("#let_sl_erp_consulta").val(let_sl_erp_consulta);
                    $("#sl_consultas_criadas option").remove();
                    dados.lista_consultas.forEach(consulta => {
                        $("#sl_consultas_criadas").append(`<option value='${consulta.cod_script}'>${consulta.desc}</option>`);
                    });
                    $("#sl_consultas_criadas").selectpicker('refresh');
                    $("#div_cria_nova_consulta").css("visibility", "visible");
                    $("#btn_adiciona_script").html('Atualizar');

                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
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
      } else {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Descrição e/ou script e obs, não informados!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
      }
    } else if (let_nome_btn == "btn_add_param"){
        let_count_tr_parametros += 1;
        form_add_novo_param(let_count_tr_parametros, null)
    } else if (let_nome_btn == "btn_abre_modal_exec_consulta"){
        let let_cod_script = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/ti_gera_consultas_app/abre_modal_com_param_script',
            data: {
                'cod_script': let_cod_script,
            },
            success: function (dados) {
                $("#btn_gera_consulta").val(let_cod_script);
                let let_frm_param = ``;
                dados.lista_obj_param.forEach( param => {
                    if(param.tipo == 1) {
                        let_frm_param += `
                            <div class="d-flex flex-column justify-content-center align-items-between w-100" >
                                <label for="${param.cod_param}">${param.desc}</label>
                                <input class="valida_dados_componente_param" type="date" id="${param.cod_param}" name="${param.cod_param}"/>
                            </div>
                        `;
                    } else if(param.tipo == 2){
                         let_frm_param += `
                            <div class="d-flex flex-column justify-content-center align-items-between w-100" >
                                <label for="${param.cod_param}">${param.desc}</label>
                                <input class="valida_dados_componente_param" type="number" id="${param.cod_param}" name="${param.cod_param}"/>
                            </div>
                        `;
                    } else if(param.tipo == 3){
                         let_frm_param += `
                            <div class="d-flex flex-column justify-content-center align-items-between w-100" >
                                <label for="${param.cod_param}">${param.desc}</label>
                                <input class="valida_dados_componente_param" type="text" id="${param.cod_param}" name="${param.cod_param}"/>
                            </div>
                        `;
                    }
                })
                $("#div_lista_param").html(let_frm_param);
                $("#modal_acessa_consulta").show();

            },
            error: function (request, status, error) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
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
    } else if (let_nome_btn == "btn_fecha_modal_gera_consulta"){
         $("#modal_acessa_consulta").hide();
    }  else if (let_nome_btn == "btn_cria_nova_consulta"){
        $("#btn_adiciona_script").html('Adicionar');
        limpa_campos_frm_criar_consulta();
    } else if (let_nome_btn == "btn_salva_dados_parametro"){
        let let_id = let_id_btn.split('_')[4];
        let let_cod_param = let_val_btn;
        let let_cod_script = $("#btn_adiciona_script").val();
        let let_desc = $("#input_desc_param_"+let_id).val();
        let let_tipo = $("#sl_input_tipo_dado_"+let_id).val();

        if ((!let_desc || let_desc.trim() === '') || (!let_tipo || let_tipo === "0")) {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Por favor, add o nome do filtro e/ou selecione um tipo de dado.',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
            return;
        } else {

            $.ajax({
            type: 'POST',
            url: '/ti_gera_consultas_app/salva_param',
            data: {
                'cod_script': let_cod_script,
                'cod_param': let_cod_param,
                'desc': let_desc,
                'tipo': let_tipo,
            },
            success: function (dados) {
                $("#btn_salva_dados_parametro_"+let_id).val(dados.cod_param);
                $("#btnExcluirParam_"+let_id).val(dados.cod_param);
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
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
    } else if (let_nome_btn == "btn_gera_consulta"){
        let let_cod_script = let_val_btn;
        const elementosComClasse = document.querySelectorAll('.valida_dados_componente_param');
        let let_result_validacao = true;
        elementosComClasse.forEach ( elemento => {
            if (!elemento.value.trim()){
                let_result_validacao = false;
            }
        })

        if (let_result_validacao == false){
            $.gritter.add({
                    title: 'Atenção!',
                    text: 'Favor preencher todos os campos',
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
        } else {
            let let_loader_princ_frm_consultas_disponiveis = document.getElementById("loader_princ_frm_consultas_disponiveis");
            let_loader_princ_frm_consultas_disponiveis.style.display = "flex";
            const dados = Array.from(document.querySelectorAll('.valida_dados_componente_param')).map(input => ({
              id: input.id,
              value: input.value
            }));
            $.ajax({
            type: 'GET',
            url: '/ti_gera_consultas_app/executa_consulta',
            data: {
               'cod_script': let_cod_script,
               'dados': JSON.stringify(dados),
            },
            xhrFields: {
                responseType: 'blob'
            },
            success: function (response, status, xhr) {
                $("#modal_acessa_consulta").hide();
                loader_princ_frm_consultas_disponiveis.style.display = "none";
                var filename = "";
                var disposition = xhr.getResponseHeader('Content-Disposition');
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    var matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
                }
                var link = document.createElement('a');
                var url = window.URL.createObjectURL(response);
                link.href = url;
                link.download = filename;
                document.body.append(link);
                link.click();
                link.remove();
                window.URL.revokeObjectURL(url);

                $.gritter.add({
                    title: 'Atenção!',
                    text:'Arquivo gerado com sucesso!',
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
    } else if (let_nome_btn == 'btnExcluirParam') {
        var varCodParamConsulta = let_val_btn;
        $.ajax({
            type: 'DELETE',
            url:"/ti_gera_consultas_app/exclui_parametro_consulta/" + varCodParamConsulta,
            success: function(dados){
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $('#add_tr_param_' + let_val_btn).remove();
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

function form_add_novo_param(cod_linha, lista_parametros) {

    let totalLinhas = $("#add_tr_parametros tr").length;

    if (totalLinhas >= 9) {
        return;
    }

    if(lista_parametros == null) {
        $("#add_tr_parametros").append(`
            </br>
            <tr class="d-flex flex-row" id="add_tr_param" style="padding-top: 7px;">
               <th class="d-flex flex-column  justify-content-between align-items-between w-100">
                   <input placeholder="Nome do Filtro" type="text" id="input_desc_param_${cod_linha}" name="input_desc_param"/>
               </th>
               <th class="d-flex flex-column  justify-content-between align-items-between w-100" style="margin-left:0.25rem;margin-right:0.25rem">
                    <select name="sl_input_tipo_dado" id="sl_input_tipo_dado_${cod_linha}" >
                        <option value="0" selected>Selecione o tipo de dado...&nbsp;</option>
                        <option value="1">DATE</option>
                        <option value="2">INT</option>
                        <option value="3">STRING</option>
                    </select>
               </th>
               <th class="d-flex justify-content-between align-items-start w-50">
                  <button type="button" name="btn_salva_dados_parametro" id="btn_salva_dados_parametro_${cod_linha}"
                        class="btn-primary btn-rounded botaoPrincipal" style="border-radius: 5px;padding-left: 1rem;padding-right: 1rem;color: white;font-weight: bolder;"
                        value="0" title='Salvar'>
                       <i class="fa-solid fa-check" style="color: #d2660f;"></i>
                  </button>
                  <button title='Excluir' style="margin-top: -8px;" type="button" class="btn btn-rounded btn-space" id="btnExcluirParam_${cod_linha}" name="btnExcluirParam" value="0" title="Excluir Parametro">
                    <i class="fa-solid fa-trash" style="color: #f46424;"></i>
                  </button>
               </th>
            </tr>
            </br>
        `);
    } else {
      lista_parametros.forEach( parametro => {
          $("#add_tr_parametros").append(`
            <tr class="d-flex flex-row" id="add_tr_param_${parametro.cod_param}" name='add_tr_param' style="padding-top: 7px;">
               <th class="d-flex flex-column  justify-content-between align-items-between w-100">
                   <input placeholder="Nome do Filtro" type="text" id="input_desc_param_${parametro.cod_param}" name="input_desc_param" value="${parametro.desc}"/>
               </th>
               <th class="d-flex flex-column  justify-content-between align-items-between w-100" style="margin-left:0.25rem;margin-right:0.25rem">
                    <select name="sl_input_tipo_dado" id="sl_input_tipo_dado_${parametro.cod_param}" >
                        <option value="0" ${parametro.tipo === 0 ? 'selected' : ''}>Selecione o tipo de dado...&nbsp;</option>
                        <option value="1" ${parametro.tipo === 1 ? 'selected' : ''}>DATE</option>
                        <option value="2" ${parametro.tipo === 2 ? 'selected' : ''}>INT</option>
                        <option value="3" ${parametro.tipo === 3 ? 'selected' : ''}>STRING</option>
                    </select>
               </th>
               <th class="d-flex justify-content-between align-items-start w-50">
                  <button type="button" name="btn_salva_dados_parametro" id="btn_salva_dados_parametro_${parametro.cod_param}" title='Salvar'
                        class="btn-primary btn-rounded botaoPrincipal" style="border-radius: 5px;padding-left: 1rem;padding-right: 1rem;color: white;font-weight: bolder;"
                        value="${parametro.cod_param}">
                      <i class="fa-solid fa-check" style="color: #d2660f;"></i>
                  </button>
                  <button title='Excluir' style="margin-top: -8px;" type="button" class="btn btn-rounded btn-space" id="btnExcluirParam_${parametro.cod_param}" name="btnExcluirParam" value="${parametro.cod_param}" title="Excluir Parametro">
                    <i class="fa-solid fa-trash" style="color: #f46424;"></i>
                  </button>
               </th>
            </tr>
          `);
      });
    }
}

$(document).on('change', '#sl_consultas_criadas', function(){
    let let_lista_consultas = $("#sl_consultas_criadas").val().toString();
    let let_cod_script = $(this).val();
    let let_loader_carrega_consulta = document.getElementById("loader_carrega_consulta");
    let_loader_carrega_consulta.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/ti_gera_consultas_app/acessa_consulta',
        data: {
            'cod_script': let_cod_script,
        },
        success: function (dados) {
            $("#add_tr_parametros").empty();
            $("#btn_adiciona_script").val(let_cod_script);
            $("#desc_criar_consulta").val(dados.dic_script.desc);
            $("#txt_script").val(dados.dic_script.script);
            $("#txt_obs").val(dados.dic_script.obs);
            $("#sl_erp_consulta").val(dados.dic_script.cod_conexao);
            $("#sl_erp_consulta").selectpicker('refresh');
            form_add_novo_param(0, dados.dic_script.lista_obj_param);
            $("#add_parametros").css("visibility", "visible");
            $("#slc_selec_usu").css("visibility", "visible");
            $("#div_cria_nova_consulta").css("visibility", "visible");
            $("#btn_adiciona_script").html(`Atualizar`);


            lista_usuarios = dados.dic_script.lista_usuarios
            lista_usu_vinc = dados.dic_script.lista_usu_vinculados

            let_lista_usuarios_frm_cria_consulta = [];
            $("#sl_libera_consulta option").remove();
            lista_usuarios.forEach( usu => {
                let reg = [
                    usu.cod_usu,
                    usu.login_usu
                ];
                let_lista_usuarios_frm_cria_consulta.push(reg);

                let let_item_selected = ``;
                lista_usu_vinc.forEach( cod_usu_vinc => {
                   if( cod_usu_vinc.cod_usu__cod_usu == usu.cod_usu){
                        let_item_selected = `selected="selected"`;
                    }
                });
                $("#sl_libera_consulta").append(`
                    <option value="${usu.cod_usu}" ${let_item_selected}>${usu.nome_usu}</option>
                `);
            });
            $("#sl_libera_consulta").selectpicker('refresh');
            let_loader_carrega_consulta.style.display = "none";

        },
        error: function (request, status, error) {
            $.gritter.add({
                title: 'Atenção!',
                text: error,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        },
    });
});

$(document).on('change', '#sl_libera_consulta', function(){
    let let_lista_cod_usuarios = $("#sl_libera_consulta").val().toString();
    let let_cod_script = $("#btn_adiciona_script").val();

    $.ajax({
        type: 'POST',
        url: '/ti_gera_consultas_app/vincula_usuario_consulta',
        data: {
            'cod_script': let_cod_script,
            'lista_cod_usuarios': let_lista_cod_usuarios
        },
        success: function (dados) {
            $.gritter.add({
                title: 'Atenção!',
                text: dados.msg,
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
        },
    });
});

function limpa_campos_frm_criar_consulta(){
    $("#add_tr_parametros").empty();
    $("#desc_criar_consulta").val('');
    $("#txt_obs").val('');
    $("#txt_script").val('');

    $("#slc_selec_usu").val('0');
    $("#slc_selec_usu").selectpicker('refresh');

    $("#sl_consultas_criadas").val('0');
    $("#sl_consultas_criadas").selectpicker('refresh');

    $("#sl_libera_consulta").val('0');
    $("#sl_libera_consulta").selectpicker('refresh');

    $("#sl_erp_consulta").val('0');
    $("#sl_erp_consulta").selectpicker('refresh');

    $("#add_parametros").css("visibility", "hidden");
    $("#slc_selec_usu").css("visibility", "hidden");
    $("#div_cria_nova_consulta").css("visibility", "hidden");
    $("#btn_adiciona_script").val('0');

}



