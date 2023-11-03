//Data Form
const today = new Date().toISOString().slice(0, 10);
document.getElementById("data_lancamento").value = today;


//Botão Cadastro formulário
/*$('#form_cadastro_5s').submit(function(event){
    event.preventDefault();
    cod_filial = document.getElementById("filial").value
    matricula_motorista = document.getElementById("matricula_motorista").value
    placa = document.getElementById("placa").value
    avaliador = document.getElementById("avaliador").value
    mapa = document.getElementById("mapa").value
    cabine_livre = document.getElementById("cabine_livre").value
    estofado_bom = document.getElementById("estofados_cabine").value
    doc_veiculo_lug_adequado = document.getElementById("doc_veiculo_lug_adequado").value
    aparelho_trk_bom = document.getElementById("aparelho_tracking").value
    notas_organizadas = document.getElementById("notas_organizadas").value
    baias_bom = document.getElementById("baias_bom_estado").value
    chapatex_organizados = document.getElementById("chapatex_organizados").value
    plast_papel_segregados = document.getElementById("plast_papel_segregados").value
    pallets_bom = document.getElementById("pallets_bom").value
    vasilhames_separados = document.getElementById("vasilhames_separados").value
    cabine_limpa = document.getElementById("cabine_limpa").value
    baias_limpas = document.getElementById("baias_limpas")
    eqpe_saber_func_limp = document.getElementById("equipe_saber_fluxo_limp").value
    eqpe_saber_func_s = document.getElementById("equipe_saber_5s").value
    eqpe_saber_func_rotina_aud = document.getElementById("equipe_saber_rot_audit")
    eqpe_recorda_gaps = document.getElementById("equipe_recorda_gaps").value
    eqpq_saber_prog_reconhecimento = document.getElementById("equipe_sabe_prog").value
    obs = document.getElementById("obs").value
    button_inserir = document.getElementById("button_inserir").value

    $.ajax({
        type: "POST",
        url: "/seguranca_5s_app/salva_reg_5s_app",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            cod_filial : cod_filial,
            matricula_motorista : matricula_motorista,
            placa : placa,
            avaliador : avaliador,
            mapa : mapa,
            cabine_livre : cabine_livre,
            estofado_bom : estofado_bom,
            doc_veiculo_lug_adequado,
            aparelho_trk_bom : aparelho_trk_bom,
            notas_organizadas : notas_organizadas,
            baias_bom : baias_bom,
            chapatex_organizados : chapatex_organizados,
            plast_papel_segregados : plast_papel_segregados,
            pallets_bom : pallets_bom,
            vasilhames_separados : vasilhames_separados,
            cabine_limpa : cabine_limpa,
            baias_limpas : baias_limpas,
            eqpe_saber_func_limp : eqpe_saber_func_limp,
            eqpe_saber_func_s : eqpe_saber_func_s,
            eqpe_saber_func_rotina_aud : eqpe_saber_func_rotina_aud,
            eqpe_recorda_gaps : eqpe_recorda_gaps,
            eqpq_saber_prog_reconhecimento : eqpq_saber_prog_reconhecimento,
            obs : obs,
            button_inserir : button_inserir
        },
        success: function(data) {
            $.gritter.add({
                title: 'Sucesso!',
                text: "Lançamento registrado com sucesso!",
                image: '/static/icons/sucess_icon.svg',
                sticky: false,
                time: '',
            });
        },
        error: function(error) {
            $.gritter.add({
                title: 'Erro!',
                text: "Por gentileza contate o adm.",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });
});
*/



$(document).on('click','button', function(){
   let let_id_btn = $(this).attr('id');
   let let_name_btn = $(this).attr('name');
   let let_value_btn = $(this).attr('value');



   if (let_name_btn == "button_novo_cadastro"){
        document.getElementById("form_cadastro_5s").reset();
        $(window).scrollTop(0); // Rolando a página para o topo
        $("#filial_id").focus();
    }

   if (let_name_btn=="button_inserir"){
        data_lancamento = document.getElementById("data_lancamento").value
        filial = document.getElementById("filial_id").value
        matricula_motorista = document.getElementById("matricula_motorista").value
        placa = document.getElementById("placa").value
        avaliador = document.getElementById("avaliador").value
        mapa = document.getElementById("mapa").value
        cabine_livre = document.getElementById("cabine_livre").value
        estofado_bom = document.getElementById("estofados_cabine").value
        doc_veiculo_lug_adequado = document.getElementById("doc_veiculo_lug_adequado").value
        aparelho_trk_bom = document.getElementById("aparelho_tracking").value
        notas_organizadas = document.getElementById("notas_organizadas").value
        baias_bom = document.getElementById("baias_bom_estado").value
        chapatex_organizados = document.getElementById("chapatex_organizados").value
        plast_papel_segregados = document.getElementById("plast_papel_segregados").value
        pallets_bom = document.getElementById("pallets_bom").value
        vasilhames_separados = document.getElementById("vasilhames_separados").value
        cabine_limpa = document.getElementById("cabine_limpa").value
        baias_limpas = document.getElementById("baias_limpas").value
        eqpe_saber_func_limp = document.getElementById("equipe_saber_fluxo_limp").value
        eqpe_saber_func_s = document.getElementById("equipe_saber_5s").value
        eqpe_saber_func_rotina_aud = document.getElementById("equipe_saber_rot_audit").value
        eqpe_recorda_gaps = document.getElementById("equipe_recorda_gaps").value
        eqpq_saber_prog_reconhecimento = document.getElementById("equipe_sabe_prog").value
        obs = document.getElementById("obs").value
        ajudante_1 = document.getElementById("ajudante_1").value
        ajudante_2 = document.getElementById("ajudante_2").value
        button_inserir = document.getElementById("button_inserir").value

        $.ajax({
            type: "POST",
            url: "/seguranca_5s_app/salva_reg_5s_app",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                data_lancamento : data_lancamento,
                filial : filial,
                matricula_motorista : matricula_motorista,
                placa : placa,
                avaliador : avaliador,
                mapa : mapa,
                cabine_livre : cabine_livre,
                estofado_bom : estofado_bom,
                doc_veiculo_lug_adequado,
                aparelho_trk_bom : aparelho_trk_bom,
                notas_organizadas : notas_organizadas,
                baias_bom : baias_bom,
                chapatex_organizados : chapatex_organizados,
                plast_papel_segregados : plast_papel_segregados,
                pallets_bom : pallets_bom,
                vasilhames_separados : vasilhames_separados,
                cabine_limpa : cabine_limpa,
                baias_limpas : baias_limpas,
                eqpe_saber_func_limp : eqpe_saber_func_limp,
                eqpe_saber_func_s : eqpe_saber_func_s,
                eqpe_saber_func_rotina_aud : eqpe_saber_func_rotina_aud,
                eqpe_recorda_gaps : eqpe_recorda_gaps,
                eqpq_saber_prog_reconhecimento : eqpq_saber_prog_reconhecimento,
                obs : obs,
                button_inserir : button_inserir,
                ajudante_1 : ajudante_1,
                ajudante_2 : ajudante_2
            },
            success: function(data) {

                $.gritter.add({
                    title: 'Sucesso!',
                    text: "Lançamento registrado com sucesso!",
                    image: '/static/icons/sucess_icon.svg',
                    sticky: false,
                    time: '',
                });
            },
            error: function(error) {
                $.gritter.add({
                    title: 'Erro!',
                    text: "Por gentileza contate o adm.",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }

        });

   }
});

