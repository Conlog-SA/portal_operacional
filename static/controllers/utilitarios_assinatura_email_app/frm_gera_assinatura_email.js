


$(document).on('click', '#sp_nome_colab', function(){
    const span = document.getElementById('sp_nome_colab');

    const currentText = span.textContent;
    //Cria um campo text
    const input = document.createElement('input');
    input.type = 'text';
    input.value = currentText;
    input.style.width = `${span.offsetWidth}px`;

    //Substitui span pelo input
    span.replaceWith(input);

    //Foca no input para facilitar a edição
    input.focus();

    const saveText = () => {
        span.textContent = input.value || currentText;
        input.replaceWith(span);
    }

    //Evento para perder o foco ou pressionar Enter
    input.addEventListener('blur', saveText);
    input.addEventListener('keydown', function(event) {
        if(event.key == 'Enter') {
            saveText();
        }
    });

});

$(document).on('click', '#sp_cargo_colab', function(){
    const span = document.getElementById('sp_cargo_colab');

    const currentText = span.textContent;
    //Cria um campo text
    const input = document.createElement('input');
    input.type = 'text';
    input.value = currentText;
    input.style.width = `${span.offsetWidth}px`;

    //Substitui span pelo input
    span.replaceWith(input);

    //Foca no input para facilitar a edição
    input.focus();

    const saveText = () => {
        span.textContent = input.value || currentText;
        input.replaceWith(span);
    }

    //Evento para perder o foco ou pressionar Enter
    input.addEventListener('blur', saveText);
    input.addEventListener('keydown', function(event) {
        if(event.key == 'Enter') {
            saveText();
        }
    });

});

$(document).on('click', '#sp_filial_colab', function(){
    const span = document.getElementById('sp_filial_colab');

    const currentText = span.textContent;
    //Cria um campo text
    const input = document.createElement('input');
    input.type = 'text';
    input.value = currentText;
    input.style.width = `${span.offsetWidth}px`;

    //Substitui span pelo input
    span.replaceWith(input);

    //Foca no input para facilitar a edição
    input.focus();

    const saveText = () => {
        span.textContent = input.value || currentText;
        input.replaceWith(span);
    }

    //Evento para perder o foco ou pressionar Enter
    input.addEventListener('blur', saveText);
    input.addEventListener('keydown', function(event) {
        if(event.key == 'Enter') {
            saveText();
        }
    });

});

$(document).on('click', '#sp_local_colab', function(){
    const span = document.getElementById('sp_local_colab');

    const currentText = span.textContent;
    //Cria um campo text
    const input = document.createElement('input');
    input.type = 'text';
    input.value = currentText;
    input.style.width = `${span.offsetWidth}px`;

    //Substitui span pelo input
    span.replaceWith(input);

    //Foca no input para facilitar a edição
    input.focus();

    const saveText = () => {
        span.textContent = input.value || currentText;
        input.replaceWith(span);
    }

    //Evento para perder o foco ou pressionar Enter
    input.addEventListener('blur', saveText);
    input.addEventListener('keydown', function(event) {
        if(event.key == 'Enter') {
            saveText();
        }
    });

});

$(document).on('click', '#sp_email_colab', function(){
    const span = document.getElementById('sp_email_colab');

    const currentText = span.textContent;
    //Cria um campo text
    const input = document.createElement('input');
    input.type = 'text';
    input.value = currentText;
    input.style.width = `${span.offsetWidth}px`;

    //Substitui span pelo input
    span.replaceWith(input);

    //Foca no input para facilitar a edição
    input.focus();

    const saveText = () => {
        span.textContent = input.value || currentText;
        input.replaceWith(span);
    }

    //Evento para perder o foco ou pressionar Enter
    input.addEventListener('blur', saveText);
    input.addEventListener('keydown', function(event) {
        if(event.key == 'Enter') {
            saveText();
        }
    });

});


$(document).on('click', '#sp_tel_colab', function(){
    const span = document.getElementById('sp_tel_colab');

    const currentText = span.textContent;
    //Cria um campo text
    const input = document.createElement('input');
    input.type = 'text';

    input.value = currentText;
    input.style.width = `${span.offsetWidth}px`;

    //Substitui span pelo input
    span.replaceWith(input);

    //Foca no input para facilitar a edição
    input.focus();

    const saveText = () => {
        span.textContent = input.value || currentText;
        input.replaceWith(span);
        const tel = input.value || currentText;
        $.ajax({
            type: 'POST',
            url: "/utilitarios_assinatura_email_app/update_tel_colab",
            data: {
                'transacao': 'update_tel',
                'tel': tel
            },
            dataType: 'json',
            success: function(data){
                console.log(data.msg)
            },
            error: function (request, status, error) {
                console.log(error);
            }
        });

    }

    //Evento para perder o foco ou pressionar Enter
    input.addEventListener('blur', saveText);
    input.addEventListener('keydown', function(event) {
        if(event.key == 'Enter') {
            saveText();
        }
    });

});

/*
$(document).on('click', '#dv_foto_colab', function(){
    const div = document.getElementById('dv_foto_colab');
    const fileInput = document.getElementById('file-input');


});
*/

const div = document.getElementById('dv_foto_colab');
const img = document.getElementById('img_foto_colab')
const fileInput = document.getElementById('file-input');

    // Adiciona evento de clique na div
    div.addEventListener('click', () => {
      fileInput.click(); // Simula o clique no input de arquivo
    });

    // Adiciona evento ao input de arquivo para alterar o fundo da div
    fileInput.addEventListener('change', function (event) {
      const file = event.target.files[0]; // Obtém o arquivo selecionado

      if (file) {
        const reader = new FileReader();

        // Executa quando o arquivo é carregado
        reader.onload = function (e) {
            let let_frm_data = new FormData();
			let_frm_data.append("file", $('#file-input')[0].files[0]);
			let_frm_data.append('transacao', 'update_foto')
			$.ajax({
				type: 'POST',
				enctype: "multipart/form-data; charset=utf-8",
				url: "/utilitarios_assinatura_email_app/carrega_salva_foto_colab",
				data: let_frm_data,
				dataType: 'json',
				processData: false,
				contentType: false,
				cache: false,
				success: function(data){
					let caminho_foto_server = 'https://operacional.conlogsa.com.br/media/' + data.foto_postada;
					console.log(data.foto_postada);
					const timestamp = new Date().getTime();
					img.src = `{caminho_foto_server}?_=${timestamp}`;
					div.style.backgroundImage = `url('${caminho_foto_server}?_=${timestamp}')`;
					//div.textContent = ''; // Remove o texto da div
				},
				error: function (request, status, error) {
					let caminho_foto_server = 'https://operacional.conlogsa.com.br/media/fotos/user_default.jpg';
					div.style.backgroundImage = `url('${caminho_foto_server}?_=${timestamp}')`;
					img.src = `{caminho_foto_server}?_=${timestamp}`;
					console.log(error);
				}
			});
        };

        reader.readAsDataURL(file); // Lê o arquivo como uma URL base64
      }
    });





