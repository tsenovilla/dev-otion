/**
 * This function activates the slider via Swiper
 * @param {HTMLElement} slider 
 */
export default function post_slider(slider)
{
    const swiper_config = {
        slidesPerView:'auto',
        spaceBetween: 10,
        freeMode:true,
        navigation:
        {
            prevEl: '.swiper-button-prev',
            nextEl: '.swiper-button-next'
        },
        loop:true,
        effect:'coverflow',
        centeredSlides:true,
        coverflowEffect: {
            rotate: 40,
            stretch: 0,
            depth: 100,
            modifier: 1,
            slideShadows: true,
        },
    };
    new Swiper(slider, swiper_config);
    const posts = slider.querySelectorAll('.post-slider__slide');
    posts.forEach(post=>set_bkg_image(post)); // Set the bkg image for each post in the slider
}

function set_bkg_image(post)
{
    const route = post.getAttribute('data-background');
    post.style.setProperty('--slide_bkg_image','url('+route+')'+', linear-gradient(to right, rgba(0,0,0, .65) 0% ,rgba(0,0,0,.3) 70%, rgba(0,0,0,.1)100%)');
}