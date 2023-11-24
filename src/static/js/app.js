/** BOTON RESPONSIVO **/
const boton = document.querySelector('#boton')
const mobile_menu = document.querySelector('#mobile-menu')

boton.addEventListener('click', () => {
    mobile_menu.classList.toggle('hidden')
})




