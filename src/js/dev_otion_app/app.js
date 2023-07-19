import menu_animation from './menu_animation_helper';
import entry_highlighting from './entry_highlighting';
import dark_mode from './dark_mode';

const menu = document.querySelector('.menu');
document.addEventListener('DOMContentLoaded',menu_animation(menu));
document.addEventListener('DOMContentLoaded',dark_mode());

const article = document.querySelector('.blog_entry');
if(article)
{
    entry_highlighting(article);
}
