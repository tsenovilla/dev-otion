/**
 * This function closes the menu if the user clicks outside.
 * @param {HTMLElement} menu
 */
export default function (menu)
{
    document.addEventListener('click', event =>
        {
            if(menu.hasAttribute('open') && !menu.contains(event.target))
            {
                const menu_list = menu.querySelector(".menu_list");
                menu_list.classList.add('menu_animation_close');
            }
        }
    )
}