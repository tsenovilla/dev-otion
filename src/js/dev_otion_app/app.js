import menu_animation from './menu_animation_helper';
import code_highlighting from './code_highlighting';
import dark_mode from './dark_mode';

const menu = document.querySelector('.menu');
document.addEventListener('DOMContentLoaded',menu_animation(menu));
document.addEventListener('DOMContentLoaded',dark_mode());
