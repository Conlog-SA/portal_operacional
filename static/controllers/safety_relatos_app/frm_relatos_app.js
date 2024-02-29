$(document).on('click','.clickable' , function(){
    let URL = $(this).attr("value");
    window.open(URL,'_blank','','');
});

$(document).on('click','.create-check-relatos' , function(){
    let let_unidade_relato = $('#unidade').val();
    let let_tipo_relato = $('#tipo_relato').val();
    let let_situacao_envolvido = $('#situacao_envolvido').val();
    let let_nome_relatado = $('#nome_relatado').val();
    let let_local_relato = $('#local_relato').val();
    let let_atividade_relato = $('#atividade_relato').val();
    let let_descricao_situacao = $('#descricao_situacao').val();

    $.ajax({
        type: 'POST',
        url: '/safety_relatos_app/relatos_check',
        data: {
            'unidade_relato'   :   let_unidade_relato,
            'tipo_relato'   :   let_tipo_relato,
            'situacao_envolvido'   :   let_situacao_envolvido,
            'nome_relatado'   :   let_nome_relatado,
            'local_relato'   :   let_local_relato,
            'atividade_relato' : let_atividade_relato,
            'situacao_relato' : let_descricao_situacao
        },
        success: function (dados) {
            $("#div_corpo_relatos").html(dados);
        }
    });
});


