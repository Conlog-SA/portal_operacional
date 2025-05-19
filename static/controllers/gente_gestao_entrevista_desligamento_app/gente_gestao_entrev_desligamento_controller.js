$(document).on('click','.btn-busca-desligamentos' , function(){
    inicio_periodo_desligamentos = $('#data_inicio_pesquisa_desligados').val();
    fim_periodo_desligamentos = $('#data_fim_pesquisa_desligados').val();

    $.ajax({
	        type: 'GET',
	        data: {
                'inicio_periodo_desligamentos'   :   inicio_periodo_desligamentos,
                'fim_periodo_desligamentos'   :   fim_periodo_desligamentos,
            },
            dataType : "html",
	        url: '/gente_gestao_entrevista_desligamento_app/pesquisa_desligamentos',
	        success: function(response) {
                let_lista_desligamentos_periodo = [];
                dados.forEach(desligamento => {
                    if (desligamento['existe_resposta'] == true) {
                        str_nome_colaborador = '<a class="abrir-relatorio-desligamento" href="operacional.conlogsa.com.br/'+desligamento['matricula']+'>'+desligamento['nome']+'</a>';
                    }
                    else {
                        str_cancelar = desligamento['nome'];
                    }
                    let let_dado_desligamento = [
                        desligamento['matricula'],
                        desligamento['nome'],
                        desligamento['unidade'],
                        new Date(arquivo['data_admissao']).toLocaleString("pt-BR"),
                        new Date(arquivo['data_desligamento']).toLocaleString("pt-BR"),
                        desligamento['cargo'],
                        desligamento['contato_telefone'],
                        desligamento['contato_email'],
                    ];
                    let_lista_desligamentos_periodo.push(let_dado_arquivo);
                });

                ({'matricula': desligamento.matricula,
                 'nome': desligamento.nome,
                 'unidade': desligamento.unidade,
                 'data_admissao': desligamento.data_admissao,
                 'data_desligamento': desligamento.data_desligamento,
                 'cargo': desligamento.cargo,
                 'contato_telefone': desligamento.contato_telefone,
                 'contato_email': desligamento.contato_email,
                 'existe_resposta': flag_existe_resposta})
            }
    });
});
