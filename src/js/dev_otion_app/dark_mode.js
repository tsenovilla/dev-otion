import code_highlighting from "./code_highlighting";
export default function()
{
    const body = document.querySelector('body');
    const button = document.querySelector('.dark_mode_button');
    const article = document.querySelector('.article_detail');
    const default_light_theme = window.matchMedia('(prefers-color-scheme:light)');
    const light_code_highlight = document.querySelector('.light_code_highlight');
    const dark_code_highlight = document.querySelector('.dark_code_highlight');
    if(default_light_theme.matches || sessionStorage.getItem('dark_mode')==='deactivated')
    {
        body.classList.remove('dark_mode');
        dark_code_highlight.setAttribute('disabled','');
    }
    if(!default_light_theme.matches || sessionStorage.getItem('dark_mode')==='activated')
    {
        body.classList.add('dark_mode');
        light_code_highlight.setAttribute('disabled','');
    }

    default_light_theme.addEventListener('change',()=>
        {
            if(default_light_theme.matches)
            {
                light_code_highlight.removeAttribute('disabled');
                dark_code_highlight.setAttribute('disabled','');
            }
            else
            {
                light_code_highlight.setAttribute('disabled','');
                dark_code_highlight.removeAttribute('disabled');
            }
            if(article)
            {
                code_highlighting(article);
            }
            body.classList.toggle('dark_mode');
        }
    )
    
    button.addEventListener('click',()=>
        {
            body.classList.toggle('dark_mode');
            if(body.classList.contains("dark_mode"))
            {
                sessionStorage.setItem("dark:mode","activated");
                light_code_highlight.setAttribute('disabled','');
                dark_code_highlight.removeAttribute('disabled');
            }
            else
            {
                sessionStorage.setItem("dark_mode","deactivated");
                light_code_highlight.removeAttribute('disabled');
                dark_code_highlight.setAttribute('disabled','');
            }
            if(article)
            {
                code_highlighting(article);
            }
        }
    )
}