/** BOTON RESPONSIVO **/
const boton = document.querySelector('#boton')
const mobile_menu = document.querySelector('#mobile-menu')

boton.addEventListener('click', () => {
    mobile_menu.classList.toggle('hidden')
})

/** CAROUSEL **/
// Initialization for ES Users
import {
    Carousel,
    initTE,
  } from "tw-elements";
  
  initTE({ Carousel });

  const myCarousel = new Carousel(document.getElementById("myCarousel"), options);


