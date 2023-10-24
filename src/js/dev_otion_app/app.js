import menu_animation from './menu_animation_helper';
import menu_autocloser from './menu_autocloser';
import search_entry from './search_entry';
import dark_mode from './dark_mode';
import entry_highlighting from './entry_highlighting';
import alert_management from './alert_management';
import post_slider from './post_slider';
import window_reloader from './window_reloader';

const menu = document.querySelector('.menu');
const search = document.querySelector('.search_input');
document.addEventListener('DOMContentLoaded',menu_animation(menu));
document.addEventListener('DOMContentLoaded',menu_autocloser(menu));
document.addEventListener('DOMContentLoaded',dark_mode());
document.addEventListener('DOMContentLoaded',search_entry(search));

let window_width = window.innerWidth
window.addEventListener('resize', window_reloader(window_width));


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

const slider = document.querySelector('.post-slider');
if(slider)
{
    post_slider(slider);
}