import menu_animation from "./menu_animation_helper";

const menu = document.querySelector('.menu');
const menu_button = menu.querySelector('.icon');
document.addEventListener('DOMContentLoaded',menu_animation(menu, menu_button));
