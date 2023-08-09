export default function (menu)
{
    const button = menu.querySelector(".menu_icon");
    const menu_list = menu.querySelector(".menu_list");
    button.addEventListener('click', e=>
        {
            if(menu.hasAttribute('open'))
            {
                e.preventDefault();
                menu_list.classList.add('menu_animation_close');
            }
        }
    );

    menu_list.addEventListener('animationend', () =>
        {
            if(menu_list.classList.contains('menu_animation_close'))
            {
                menu_list.classList.remove('menu_animation_close');
                menu.removeAttribute('open');
            }
        }
    );
}