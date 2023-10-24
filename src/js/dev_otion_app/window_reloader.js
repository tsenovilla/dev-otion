/**
 * We use this to reload styles and Swiper if the window size changes the critical point of 768 px
 * @param window_width: The starting window with
 */
export default function()
{
    if((window_width>=768 && window.innerWidth < 768) || (window_width < 768 && window.innerWidth>=768))
    {
        location.reload();
        window_width = window.innerWidth;
    }
}