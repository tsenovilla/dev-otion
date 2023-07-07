export default function (menu, button)
{
    button.addEventListener('click', e=>
        {
            if(menu.hasAttribute('open'))
            {
                e.preventDefault();
                menu.classList.add('menu_animation_close');
            }
        }
    );

    menu.addEventListener('animationend', () =>
        {
            if(menu.classList.contains('menu_animation_close'))
            {
                menu.classList.remove('menu_animation_close');
                menu.removeAttribute('open');
            }
        }
    );
}