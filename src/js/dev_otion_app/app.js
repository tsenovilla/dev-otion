import menu_animation from './menu_animation_helper';
import search_entry from './search_entry';
import dark_mode from './dark_mode';
import entry_highlighting from './entry_highlighting';
import alert_management from './alert_management';

const menu = document.querySelector('.menu');
const search = document.querySelector('.search_input');
document.addEventListener('DOMContentLoaded',menu_animation(menu));
document.addEventListener('DOMContentLoaded',dark_mode());
document.addEventListener('DOMContentLoaded',search_entry(search));

const article = document.querySelector('.blog_entry');
if(article)
{
    entry_highlighting(article);
}

const alert = document.querySelector('.alert');
if(alert)
{
    alert_management(alert);
}
