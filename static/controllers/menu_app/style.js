/* document.getElementById('open_btn').addEventListener('click', function (){
    document.getElementById('sidebar').classList.toggle('open-sidebar');
});
*/

document.getElementById('open_btn_menu').addEventListener('click', function (){
    document.getElementById('sidebar').classList.toggle('open-sidebar');
});

/*
document.getElementById('a_menu').addEventListener('click', function (event){
    let let_val = event.target;
    alert(let_val.value);
    document.getElementById('i_icon_seta_menu').classList.add('open_menu');
});
*/

let let_a_menu = document.querySelectorAll('a');
let_a_menu.forEach ( link => {
    link.addEventListener('click', event => {
        event.preventDefault();
        let value = link.getAttribute('value');
        let let_i_link = document.getElementById(`i_icon_seta_menu_${value}`);
        const classes_i = let_i_link.classList;
        let let_abre_menu = null;
        classes_i.forEach( classe => {
            if( classe == 'open_menu') {
                let_abre_menu = false;
            } else if( classe == 'fecha_menu'){
                let_abre_menu = true;
            }
        });
        if(let_abre_menu == true){
            let_i_link.classList.remove('fecha_menu');
            let_i_link.classList.add('open_menu');
        } else if(let_abre_menu == false) {
            let_i_link.classList.remove('open_menu');
            let_i_link.classList.add('fecha_menu');
        } else {
            let_i_link.classList.add('open_menu');
        }

    });
});