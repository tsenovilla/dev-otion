const body = document.querySelector('body');
const light_code_highlight = document.querySelector('.light_code_highlight');
const dark_code_highlight = document.querySelector('.dark_code_highlight');
function enable_light_theme()
{
    body.classList.remove('dark_mode');
    light_code_highlight.removeAttribute('disabled');
    dark_code_highlight.setAttribute('disabled','');
}

function enable_dark_theme()
{
    body.classList.add('dark_mode');
    light_code_highlight.setAttribute('disabled','');
    dark_code_highlight.removeAttribute('disabled');
}
export default function()
{
    const button = document.querySelector('.dark_mode_button');
    const article = document.querySelector('.blog_entry');
    const default_light_theme = window.matchMedia('(prefers-color-scheme:light)');
    if(default_light_theme.matches || sessionStorage.getItem('dark_mode')==='deactivated')
    {
        enable_light_theme();
    }
    if(!default_light_theme.matches || sessionStorage.getItem('dark_mode')==='activated')
    {
        enable_dark_theme();
    }

    default_light_theme.addEventListener('change',()=>
        {
            if(default_light_theme.matches)
            {
                enable_light_theme();
            }
            else
            {
                enable_dark_theme();
            }
        }
    )
    
    button.addEventListener('click',()=>
        {
            if(body.classList.contains('dark_mode'))
            {
                sessionStorage.setItem('dark_mode','deactivated');
                enable_light_theme();
            }
            else
            {
                sessionStorage.setItem('dark_mode','activated');
                enable_dark_theme();
            }
        }
    )
}