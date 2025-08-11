$(document).on('click','.create-check-pci' , function(){
    let unidade = $('#unidade_pci').val();
    let local = $('#local_pci').val();
    let cod_item = $('#item_pci').val();

    msg_erro = '';
    if (unidade == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (cod_item == '') {
        msg_erro += 'Selecione o item a ser avaliado!<br>';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_pci_app/pci_check',
            data: {
                'filial'   :   unidade,
                'local'    :   local,
                'cod_item'   :   cod_item
            },
            success: function (dados) {
                $("#div_corpo_pci").html(dados);
                $("#div_corpo_pci").css('background-color', 'rgba(0,0,0,0)')
            },
            error: function (xhr, status, error) {
                 $.gritter.add({
                    title: 'Erro!',
                    text: xhr.responseText,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
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