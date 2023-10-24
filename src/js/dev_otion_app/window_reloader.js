/**
 * We use this to reload styles and Swiper if the window size changes the critical point of 768 px
 */
export default function()
{
    let window_width = window.innerWidth;
    window.addEventListener('resize',()=>
        {
            if((window_width>=768 && window.innerWidth < 768) || (window_width < 768 && window.innerWidth>=768))
            {
                location.reload();
                window_width = window.innerWidth;
            }
        }
    )
}