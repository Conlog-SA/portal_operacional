$(document).ready(function(){
    json_respostas = JSON.parse(str_respostas.replaceAll("&quot;", '"'));
    console.log(json_respostas);

    $('#input-nome').val(json_respostas.nome);
    $('#input-whatsapp').val(json_respostas.num_whatsapp);
    $('#input-ultimo-dia').val(json_respostas.ultimo_dia);
    $('#input-unidade').val(json_respostas.unidade);
    $('#input-unidade').selectpicker('refresh')
    $('#input-cargo').val(json_respostas.cargo);
    $('#input-gestor-imediato').val(json_respostas.gestor_imediato);
    $('#input-setor-atuacao').val(json_respostas.setor_atuacao);
    $('#input-setor-atuacao').selectpicker('refresh')

	$(".iniciativa").each(function(i) {
        if (this.value == json_respostas.iniciativa_checked) {
          this.checked = true;
        }
    });

    $('#input-motivo-desligamento').val(json_respostas.motivo_desligamento);

	$(".comunicacao-visual-interna").each(function(i) {
        if (this.value == json_respostas.comunicacao_visual_interna_checked) {
          this.checked = true;
        }
    });

	$(".materiais-equipamentos").each(function(i) {
        if (this.value == json_respostas.materiais_equipamentos_checked) {
          this.checked = true;
        }
    });

	$(".oportunidades-crescimento").each(function(i) {
        if (this.value == json_respostas.oportunidades_crescimento_checked) {
          this.checked = true;
        }
    });

	$(".solicitar-ajuda").each(function(i) {
        if (this.value == json_respostas.solicitar_ajuda_checked) {
          this.checked = true;
        }
    });

	$(".reconhecido-lider").each(function(i) {
        if (this.value == json_respostas.reconhecido_lider_checked) {
          this.checked = true;
        }
    });

	$(".frequencia-feedback").each(function(i) {
        if (this.value == json_respostas.frequencia_feedback_checked) {
          this.checked = true;
        }
    });

	$(".feedback-util").each(function(i) {
        if (this.value == json_respostas.feedback_util_checked) {
          this.checked = true;
        }
    });

	$(".ideias-ouvidas").each(function(i) {
        if (this.value == json_respostas.ideias_ouvidas_checked) {
          this.checked = true;
        }
    });

	$(".banco-horas").each(function(i) {
        if (this.value == json_respostas.banco_horas_checked) {
          this.checked = true;
        }
    });

	$(".satisfacao-beneficios").each(function(i) {
        if (this.value == json_respostas.satisfacao_beneficios_checked) {
          this.checked = true;
        }
    });

	$(".satisfacao-salario").each(function(i) {
        if (this.value == json_respostas.satisfacao_salario_checked) {
          this.checked = true;
        }
    });

	$(".salario-justo").each(function(i) {
        if (this.value == json_respostas.salario_justo_checked) {
          this.checked = true;
        }
    });

	$(".responsabilidades-coerente").each(function(i) {
        if (this.value == json_respostas.responsabilidades_coerente_checked) {
          this.checked = true;
        }
    });

	$(".tratamento-justo").each(function(i) {
        if (this.value == json_respostas.tratamento_justo_checked) {
          this.checked = true;
        }
    });

	$(".discriminacao-proprio").each(function(i) {
        if (this.value == json_respostas.discriminacao_proprio_checked) {
          this.checked = true;
        }
    });

	$(".discriminacao-colega").each(function(i) {
        if (this.value == json_respostas.discriminacao_colega_checked) {
          this.checked = true;
        }
    });

	$(".praticas-etica").each(function(i) {
        if (this.value == json_respostas.praticas_etica_checked) {
          this.checked = true;
        }
    });

	$(".canal-denuncias").each(function(i) {
        if (this.value == json_respostas.canal_denuncias_checked) {
          this.checked = true;
        }
    });

	$(".opiniao-reunioes").each(function(i) {
        if (this.value == json_respostas.opiniao_reunioes_checked) {
          this.checked = true;
        }
    });

    $('#input-registro-livre').val(json_respostas.registro_livre);
    $('#input-melhores-pontos').val(json_respostas.melhores_pontos);
    $('#input-piores-pontos').val(json_respostas.piores_pontos);
    $('#input-motivo-desvinculamento').val(json_respostas.motivo_desvinculamento);
});

$(document).on('click', '.envio-entrevista-desligamento', function(){
	let token = $(this).attr('name');

    let nome = $('#input-nome').val();
    let num_whatsapp = $('#input-whatsapp').val();
    let ultimo_dia = $('#input-ultimo-dia').val();
    let unidade = $('#input-unidade').val();
    let cargo = $('#input-cargo').val();
    let gestor_imediato = $('#input-gestor-imediato').val();
    let setor_atuacao = $('#input-setor-atuacao').val();

    let iniciativa_checked = "0";
	$(".iniciativa").each(function(i) {
        if (this.checked == true) {
          iniciativa_checked = this.value;
        }
    });

    let motivo_desligamento = $('#input-motivo-desligamento').val();

    let comunicacao_visual_interna_checked = "0";
	$(".comunicacao-visual-interna").each(function(i) {
        if (this.checked == true) {
          comunicacao_visual_interna_checked = this.value;
        }
    });

    let materiais_equipamentos_checked = "0";
	$(".materiais-equipamentos").each(function(i) {
        if (this.checked == true) {
          materiais_equipamentos_checked = this.value;
        }
    });

    let oportunidades_crescimento_checked = "0";
	$(".oportunidades-crescimento").each(function(i) {
        if (this.checked == true) {
          oportunidades_crescimento_checked = this.value;
        }
    });

    let solicitar_ajuda_checked = "0";
	$(".solicitar-ajuda").each(function(i) {
        if (this.checked == true) {
          solicitar_ajuda_checked = this.value;
        }
    });

    let reconhecido_lider_checked = "0";
	$(".reconhecido-lider").each(function(i) {
        if (this.checked == true) {
          reconhecido_lider_checked = this.value;
        }
    });

    let frequencia_feedback_checked = "0";
	$(".frequencia-feedback").each(function(i) {
        if (this.checked == true) {
          frequencia_feedback_checked = this.value;
        }
    });

    let feedback_util_checked = "0";
	$(".feedback-util").each(function(i) {
        if (this.checked == true) {
          feedback_util_checked = this.value;
        }
    });

    let ideias_ouvidas_checked = "0";
	$(".ideias-ouvidas").each(function(i) {
        if (this.checked == true) {
          ideias_ouvidas_checked = this.value;
        }
    });

    let banco_horas_checked = "0";
	$(".banco-horas").each(function(i) {
        if (this.checked == true) {
          banco_horas_checked = this.value;
        }
    });

    let satisfacao_beneficios_checked = "0";
	$(".satisfacao-beneficios").each(function(i) {
        if (this.checked == true) {
          satisfacao_beneficios_checked = this.value;
        }
    });

    let satisfacao_salario_checked = "0";
	$(".satisfacao-salario").each(function(i) {
        if (this.checked == true) {
          satisfacao_salario_checked = this.value;
        }
    });

    let salario_justo_checked = "0";
	$(".salario-justo").each(function(i) {
        if (this.checked == true) {
          salario_justo_checked = this.value;
        }
    });

    let responsabilidades_coerente_checked = "0";
	$(".responsabilidades-coerente").each(function(i) {
        if (this.checked == true) {
          responsabilidades_coerente_checked = this.value;
        }
    });

    let tratamento_justo_checked = "0";
	$(".tratamento-justo").each(function(i) {
        if (this.checked == true) {
          tratamento_justo_checked = this.value;
        }
    });

    let discriminacao_proprio_checked = "0";
	$(".discriminacao-proprio").each(function(i) {
        if (this.checked == true) {
          discriminacao_proprio_checked = this.value;
        }
    });

    let discriminacao_colega_checked = "0";
	$(".discriminacao-colega").each(function(i) {
        if (this.checked == true) {
          discriminacao_colega_checked = this.value;
        }
    });

    let praticas_etica_checked = "0";
	$(".praticas-etica").each(function(i) {
        if (this.checked == true) {
          praticas_etica_checked = this.value;
        }
    });

    let canal_denuncias_checked = "0";
	$(".canal-denuncias").each(function(i) {
        if (this.checked == true) {
          canal_denuncias_checked = this.value;
        }
    });

    let opiniao_reunioes_checked = "0";
	$(".opiniao-reunioes").each(function(i) {
        if (this.checked == true) {
          opiniao_reunioes_checked = this.value;
        }
    });

    let registro_livre = $('#input-registro-livre').val();
    let melhores_pontos = $('#input-melhores-pontos').val();
    let piores_pontos = $('#input-piores-pontos').val();
    let motivo_desvinculamento = $('#input-motivo-desvinculamento').val();

    let msg_erro = '';
    if (token == '') {
        location.reload();
        throw new Error('Problema com o seu link, por gentileza contate o responsável pelo envio.');
    }

    if (nome == '') {
        msg_erro += 'Nome não informado!<br>';
    }

    if (num_whatsapp == '') {
        msg_erro += 'Número do whatsapp não informado!<br>';
    }
    else if (num_whatsapp.length < 11) {
        msg_erro += 'Informe o número do whatsapp completo (com DDD)!<br>';
    }

    let valUltimoDiaTrabDate = new Date(ultimo_dia);
    if (isNaN(valUltimoDiaTrabDate.getDay()) || isNaN(valUltimoDiaTrabDate.getMonth()) || isNaN(valUltimoDiaTrabDate.getFullYear())) {
        msg_erro += 'Data do último dia trabalhado inválida!<br>';
    }

    if (unidade == '') {
        msg_erro += 'Selecione uma unidade!<br>';
    }

    if (cargo == '') {
        msg_erro += 'Informe o cargo de atuação!<br>';
    }

    if (gestor_imediato == '') {
        msg_erro += 'Identifique o gestor imediato!<br>';
    }

    if (setor_atuacao == '') {
        msg_erro += 'Informe o setor de atuação!<br>';
    }

    if (iniciativa_checked == "0") {
        msg_erro += 'Identifique o gestor imediato!<br>';
    }

    if (motivo_desligamento == '') {
        msg_erro += 'Informe o motivo do desligamento!<br>';
    }

    if (comunicacao_visual_interna_checked == "0" || materiais_equipamentos_checked == "0" || oportunidades_crescimento_checked == "0") {
        msg_erro += 'Questão(ões) não respondida(s) em: Percepções Gerais!<br>';
    }

    if (solicitar_ajuda_checked == "0" || reconhecido_lider_checked == "0" || frequencia_feedback_checked == "0" || feedback_util_checked == "0" || ideias_ouvidas_checked == "0" || banco_horas_checked == "0") {
        msg_erro += 'Questão(ões) não respondida(s) em: Liderança imediata!<br>';
    }

    if (satisfacao_beneficios_checked == "0" || satisfacao_salario_checked == "0" || salario_justo_checked == "0" || responsabilidades_coerente_checked == "0") {
        msg_erro += 'Questão(ões) não respondida(s) em: Remuneração e Benefícios!<br>';
    }

    if (tratamento_justo_checked == "0" || discriminacao_proprio_checked == "0" || discriminacao_colega_checked == "0" || praticas_etica_checked == "0" || canal_denuncias_checked == "0" || opiniao_reunioes_checked == "0") {
        msg_erro += 'Questão(ões) não respondida(s) em: Diversidade e inclusão!<br>';
    }

    if (msg_erro == '') {
        let string_json_respostas = JSON.stringify({token: token,
                                                    nome: nome,
                                                    num_whatsapp: num_whatsapp,
                                                    ultimo_dia: ultimo_dia,
                                                    unidade: unidade,
                                                    cargo: cargo,
                                                    gestor_imediato: gestor_imediato,
                                                    setor_atuacao: setor_atuacao,
                                                    iniciativa_checked: iniciativa_checked,
                                                    motivo_desligamento: motivo_desligamento,
                                                    comunicacao_visual_interna_checked: comunicacao_visual_interna_checked,
                                                    materiais_equipamentos_checked: materiais_equipamentos_checked,
                                                    oportunidades_crescimento_checked: oportunidades_crescimento_checked,
                                                    solicitar_ajuda_checked: solicitar_ajuda_checked,
                                                    reconhecido_lider_checked: reconhecido_lider_checked,
                                                    frequencia_feedback_checked: frequencia_feedback_checked,
                                                    feedback_util_checked: feedback_util_checked,
                                                    ideias_ouvidas_checked: ideias_ouvidas_checked,
                                                    banco_horas_checked: banco_horas_checked,
                                                    satisfacao_beneficios_checked: satisfacao_beneficios_checked,
                                                    satisfacao_salario_checked: satisfacao_salario_checked,
                                                    salario_justo_checked: salario_justo_checked,
                                                    responsabilidades_coerente_checked: responsabilidades_coerente_checked,
                                                    tratamento_justo_checked: tratamento_justo_checked,
                                                    discriminacao_proprio_checked: discriminacao_proprio_checked,
                                                    discriminacao_colega_checked: discriminacao_colega_checked,
                                                    praticas_etica_checked: praticas_etica_checked,
                                                    canal_denuncias_checked: canal_denuncias_checked,
                                                    opiniao_reunioes_checked: opiniao_reunioes_checked,
                                                    registro_livre: registro_livre,
                                                    melhores_pontos: melhores_pontos,
                                                    piores_pontos: piores_pontos,
                                                    motivo_desvinculamento: motivo_desvinculamento});

        $.ajax({
            type:"POST",
            url: '/gente_gestao_entrevista_desligamento_app/frm_entrevista_desligamento',
            dataType: 'html',
            data: {
                'token' : token,
                'json_respostas'   : string_json_respostas,
                'finalizada': true
            },
            success: function (data) {
                $("body").html(data);
            },
            error: function (request, status, error) {

            }
        });
    }
    else {
        $.gritter.add({
            title: 'Erro!',
            text: msg_erro,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }

});

$(document).on('change', 'input, select, textarea', function(){
	let token = $('#btn_submit').attr('name');

    let nome = $('#input-nome').val();
    let num_whatsapp = $('#input-whatsapp').val();
    let ultimo_dia = $('#input-ultimo-dia').val();
    let unidade = $('#input-unidade').val();
    let cargo = $('#input-cargo').val();
    let gestor_imediato = $('#input-gestor-imediato').val();
    let setor_atuacao = $('#input-setor-atuacao').val();

    let iniciativa_checked = "0";
	$(".iniciativa").each(function(i) {
        if (this.checked == true) {
          iniciativa_checked = this.value;
        }
    });

    let motivo_desligamento = $('#input-motivo-desligamento').val();

    let comunicacao_visual_interna_checked = "0";
	$(".comunicacao-visual-interna").each(function(i) {
        if (this.checked == true) {
          comunicacao_visual_interna_checked = this.value;
        }
    });

    let materiais_equipamentos_checked = "0";
	$(".materiais-equipamentos").each(function(i) {
        if (this.checked == true) {
          materiais_equipamentos_checked = this.value;
        }
    });

    let oportunidades_crescimento_checked = "0";
	$(".oportunidades-crescimento").each(function(i) {
        if (this.checked == true) {
          oportunidades_crescimento_checked = this.value;
        }
    });

    let solicitar_ajuda_checked = "0";
	$(".solicitar-ajuda").each(function(i) {
        if (this.checked == true) {
          solicitar_ajuda_checked = this.value;
        }
    });

    let reconhecido_lider_checked = "0";
	$(".reconhecido-lider").each(function(i) {
        if (this.checked == true) {
          reconhecido_lider_checked = this.value;
        }
    });

    let frequencia_feedback_checked = "0";
	$(".frequencia-feedback").each(function(i) {
        if (this.checked == true) {
          frequencia_feedback_checked = this.value;
        }
    });

    let feedback_util_checked = "0";
	$(".feedback-util").each(function(i) {
        if (this.checked == true) {
          feedback_util_checked = this.value;
        }
    });

    let ideias_ouvidas_checked = "0";
	$(".ideias-ouvidas").each(function(i) {
        if (this.checked == true) {
          ideias_ouvidas_checked = this.value;
        }
    });

    let banco_horas_checked = "0";
	$(".banco-horas").each(function(i) {
        if (this.checked == true) {
          banco_horas_checked = this.value;
        }
    });

    let satisfacao_beneficios_checked = "0";
	$(".satisfacao-beneficios").each(function(i) {
        if (this.checked == true) {
          satisfacao_beneficios_checked = this.value;
        }
    });

    let satisfacao_salario_checked = "0";
	$(".satisfacao-salario").each(function(i) {
        if (this.checked == true) {
          satisfacao_salario_checked = this.value;
        }
    });

    let salario_justo_checked = "0";
	$(".salario-justo").each(function(i) {
        if (this.checked == true) {
          salario_justo_checked = this.value;
        }
    });

    let responsabilidades_coerente_checked = "0";
	$(".responsabilidades-coerente").each(function(i) {
        if (this.checked == true) {
          responsabilidades_coerente_checked = this.value;
        }
    });

    let tratamento_justo_checked = "0";
	$(".tratamento-justo").each(function(i) {
        if (this.checked == true) {
          tratamento_justo_checked = this.value;
        }
    });

    let discriminacao_proprio_checked = "0";
	$(".discriminacao-proprio").each(function(i) {
        if (this.checked == true) {
          discriminacao_proprio_checked = this.value;
        }
    });

    let discriminacao_colega_checked = "0";
	$(".discriminacao-colega").each(function(i) {
        if (this.checked == true) {
          discriminacao_colega_checked = this.value;
        }
    });

    let praticas_etica_checked = "0";
	$(".praticas-etica").each(function(i) {
        if (this.checked == true) {
          praticas_etica_checked = this.value;
        }
    });

    let canal_denuncias_checked = "0";
	$(".canal-denuncias").each(function(i) {
        if (this.checked == true) {
          canal_denuncias_checked = this.value;
        }
    });

    let opiniao_reunioes_checked = "0";
	$(".opiniao-reunioes").each(function(i) {
        if (this.checked == true) {
          opiniao_reunioes_checked = this.value;
        }
    });

    let registro_livre = $('#input-registro-livre').val();
    let melhores_pontos = $('#input-melhores-pontos').val();
    let piores_pontos = $('#input-piores-pontos').val();
    let motivo_desvinculamento = $('#input-motivo-desvinculamento').val();

    if (token == '') {
        location.reload();
        throw new Error('Erro de identificação, informe a especialista por favor.');
    }

    let valUltimoDiaTrabDate = new Date(ultimo_dia);
    if (isNaN(valUltimoDiaTrabDate.getDay()) || isNaN(valUltimoDiaTrabDate.getMonth()) || isNaN(valUltimoDiaTrabDate.getFullYear())) {
        $('#input-ultimo-dia').val('');
        ultimo_dia = '';
    }

    let string_json_respostas = JSON.stringify({token: token,
                                                nome: nome,
                                                num_whatsapp: num_whatsapp,
                                                ultimo_dia: ultimo_dia,
                                                unidade: unidade,
                                                cargo: cargo,
                                                gestor_imediato: gestor_imediato,
                                                setor_atuacao: setor_atuacao,
                                                iniciativa_checked: iniciativa_checked,
                                                motivo_desligamento: motivo_desligamento,
                                                comunicacao_visual_interna_checked: comunicacao_visual_interna_checked,
                                                materiais_equipamentos_checked: materiais_equipamentos_checked,
                                                oportunidades_crescimento_checked: oportunidades_crescimento_checked,
                                                solicitar_ajuda_checked: solicitar_ajuda_checked,
                                                reconhecido_lider_checked: reconhecido_lider_checked,
                                                frequencia_feedback_checked: frequencia_feedback_checked,
                                                feedback_util_checked: feedback_util_checked,
                                                ideias_ouvidas_checked: ideias_ouvidas_checked,
                                                banco_horas_checked: banco_horas_checked,
                                                satisfacao_beneficios_checked: satisfacao_beneficios_checked,
                                                satisfacao_salario_checked: satisfacao_salario_checked,
                                                salario_justo_checked: salario_justo_checked,
                                                responsabilidades_coerente_checked: responsabilidades_coerente_checked,
                                                tratamento_justo_checked: tratamento_justo_checked,
                                                discriminacao_proprio_checked: discriminacao_proprio_checked,
                                                discriminacao_colega_checked: discriminacao_colega_checked,
                                                praticas_etica_checked: praticas_etica_checked,
                                                canal_denuncias_checked: canal_denuncias_checked,
                                                opiniao_reunioes_checked: opiniao_reunioes_checked,
                                                registro_livre: registro_livre,
                                                melhores_pontos: melhores_pontos,
                                                piores_pontos: piores_pontos,
                                                motivo_desvinculamento: motivo_desvinculamento});

    $.ajax({
        type:"POST",
        url: '/gente_gestao_entrevista_desligamento_app/frm_entrevista_desligamento',
        dataType: 'html',
        data: {
            'token' : token,
            'json_respostas'   : string_json_respostas,
            'finalizada': false
        },
        success: function (data) {
        },
        error: function (request, status, error) {

        }
    });
});
