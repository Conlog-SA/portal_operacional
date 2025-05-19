$(document).on('click', '.envio-nps', function(){
	let email = $(this).attr('name');

    let cod_filial_nps = $('#filial_nps').val();

    let satisfaction_checked = 0;
	$(".satisfaction").each(function(i) {
        if (this.checked == true) {
          satisfaction_checked = this.value;
        }
    });

    let satisfaction_justif = "";
    satisfaction_justif = $('#justification').val();

    let easy_contact_checked = 0;
	$(".easy-contact").each(function(i) {
        if (this.checked == true) {
          easy_contact_checked = this.value;
        }
    });

    let easy_contact_justif = "";
    easy_contact_justif = $('#easy_contact_justification').val();

    let rapidness_checked = 0;
	$(".rapidness").each(function(i) {
        if (this.checked == true) {
          rapidness_checked = this.value;
        }
    });
    console.log(typeof rapidness_checked);

    let rapidness_justif = "";
    rapidness_justif = $('#rapidness_justification').val();

    let resources_checked = 0;
	$(".resources").each(function(i) {
        if (this.checked == true) {
          resources_checked = this.value;
        }
    });

    let resources_justif = "";
    resources_justif = $('#resources_justification').val();

    let solutions_checked = 0;
	$(".solutions").each(function(i) {
        if (this.checked == true) {
          solutions_checked = this.value;
        }
    });

    let solutions_justif = "";
    solutions_justif = $('#solutions_justification').val();

    let feedback = "";
    feedback = $('#feedback').val();

    let msg_erro = '';
    if (email == '' || email.toLowerCase().indexOf("@conlogsa.com.br") === -1 && email.toLowerCase().indexOf("@deeplogistica.com.br") === -1) {
        location.reload();
        throw new Error('Email inválido (não é conlog ou deep).');
    }
    if (cod_filial_nps == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (satisfaction_checked == '') {
        msg_erro += 'Dê uma nota ao critério 1!<br>';
    }
    else if (Number(satisfaction_checked) < 7 && satisfaction_justif.length < 15) {
        if (satisfaction_justif == '') {
            msg_erro += 'Justifique a sua nota para o critério 1! (mínimo de 15 caracteres)<br>';
        }
        else {
            msg_erro += 'Faltam ' + (15-satisfaction_justif.length).toString() + ' caracteres na justificativa do critério 1!<br>'
        }
    }

    if (easy_contact_checked == '') {
        msg_erro += 'Dê uma nota ao critério 2!<br>';
    }
    else if (Number(easy_contact_checked) < 7 && easy_contact_justif.length < 15) {
        if (easy_contact_justif == '') {
            msg_erro += 'Justifique a sua nota para o critério 2! (mínimo de 15 caracteres)<br>';
        }
        else {
            msg_erro += 'Faltam ' + (15-easy_contact_justif.length).toString() + ' caracteres na justificativa do critério 2!<br>'
        }
    }

    if (rapidness_checked == '') {
        msg_erro += 'Dê uma nota ao critério 3!<br>';
    }
    else if (Number(rapidness_checked) < 7 && rapidness_justif.length < 15) {
        if (rapidness_justif == '') {
            msg_erro += 'Justifique a sua nota para o critério 3! (mínimo de 15 caracteres)<br>';
        }
        else {
            msg_erro += 'Faltam ' + (15-rapidness_justif.length).toString() + ' caracteres na justificativa do critério 3!<br>'
        }
    }

    if (resources_checked == '') {
        msg_erro += 'Dê uma nota ao critério 4!<br>';
    }
    else if (Number(resources_checked) < 7 && resources_justif.length < 15) {
        if (resources_justif == '') {
            msg_erro += 'Justifique a sua nota para o critério 4! (mínimo de 15 caracteres)<br>';
        }
        else {
            msg_erro += 'Faltam ' + (15-resources_justif.length).toString() + ' caracteres na justificativa do critério 4!<br>'
        }
    }

    if (solutions_checked == '') {
        msg_erro += 'Dê uma nota ao critério 5!<br>';
    }
    else if (Number(solutions_checked) < 7 && solutions_justif.length < 15) {
        if (solutions_justif == '') {
            msg_erro += 'Justifique a sua nota para o critério 5! (mínimo de 15 caracteres)<br>';
        }
        else {
            msg_erro += 'Faltam ' + (15-solutions_justif.length).toString() + ' caracteres na justificativa do critério 5!<br>'
        }
    }

    if (msg_erro == '') {
        let string_json_respostas = JSON.stringify({satisfaction_ch: satisfaction_checked,
                                                     satisfaction_just: satisfaction_justif,
                                                     easy_contact_ch: easy_contact_checked,
                                                     easy_contact_just: easy_contact_justif,
                                                     rapidness_ch: rapidness_checked,
                                                     rapidness_just: rapidness_justif,
                                                     resources_ch: resources_checked,
                                                     resources_just: resources_justif,
                                                     solutions_ch: solutions_checked,
                                                     solutions_just: solutions_justif,
                                                     feedback: feedback});

        $.ajax({
            type:"POST",
            url: '/nps_ti_app/form/',
            dataType: 'html',
            data: {
                'email' : email,
                'cod_filial_nps'   :   cod_filial_nps,
                'json_respostas'   : string_json_respostas
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