window.addEventListener('load', () => {

    let bouton = document.querySelector('.bouton1')

    function afficher() {
        console.log('ok')
        document.querySelector('.contact_div').style.display = "flex";
        document.querySelector('.popup_question').style.display = "flex";
    }

    bouton.addEventListener('click', afficher)

})