import Swiper from 'swiper';
import { Navigation, EffectCoverflow, EffectCards } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/effect-coverflow';
import 'swiper/css/effect-cards';
/**
 * This function creates the slider via Swiper
 * @param {HTMLElement} slider 
 */
export default function post_slider(slider)
{
    const swiper_config_global = {
        slidesPerView:'auto',
        spaceBetween: 15,
        freeMode:true,
        loop:false,
        centeredSlides:true
    };

    const swiper_config_coverflow = 
    {
        ...swiper_config_global,
        navigation:
        {
            prevEl: '.swiper-button-prev',
            nextEl: '.swiper-button-next'
        },
        effect:'coverflow',
        coverflowEffect: 
        {
            rotate: 40,
            stretch: 0,
            depth: 100,
            modifier: 1,
            slideShadows: false
        }
    }

    const swiper_config_cards = 
    {
        ...swiper_config_global,
        effect:'cards', 
        grabCursor:true
    }

    Swiper.use([Navigation, EffectCoverflow, EffectCards]);
    let swiper = new Swiper(slider, swiper_config_coverflow);

    const prev_button = document.querySelector('.swiper-button-prev');
    const next_button = document.querySelector('.swiper-button-next');
    const posts = slider.querySelectorAll('.post-slider__slide');

    prev_button.setAttribute('style','display:none'); // First time the page is loaded in big devices, the prev_button should not be visible. In small devices, it's never shown.

    swiper.on('transitionEnd', swiper_buttons_handler); // In big devices, Navigation is activated, then we have to handle the navigation buttons (neither show the previous one if there's not a left element, nor the last one if there's not a right element)

    let window_width = window.innerWidth;
    
    if(window_width < 768)
    {
        swiper.destroy(true,true);
        swiper = new Swiper(slider, swiper_config_cards);
        next_button.setAttribute('style','display:none');
        resize_cards(posts); // In small devices, the cards appear in a stack, so it's prettier if all cards have the same height (their heights depend on the content, so there may be contents longer than others)
    }

    posts.forEach(post=>set_bkg_image(post)); // Set the bkg image for each post in the slider

    // Remake the swiper if the screen changes from 'small' to 'big' or the other way around
    window.addEventListener('resize', ()=>
        {
            if(window_width < 768 && window.innerWidth >= 768)
            {
                swiper.destroy(true,true);
                swiper = new Swiper(slider, swiper_config_coverflow);
                next_button.removeAttribute('style'); // The previous button remains invisible since it only appears when the user moves the swiper.
                swiper.on('transitionEnd', swiper_buttons_handler);
                posts.forEach(post=>set_bkg_image(post)); // Destroying the swiper destroys the bkg image as well. As the styles are not the same in big and small devices, we have to rerun the function instead of destroying swiper without cleaning up the styles (swiper.destroy(true,false))
                window_width = window.innerWidth; 
            }
            else if(window_width >= 768 && window.innerWidth < 768)
            {
                swiper.destroy(true,true);
                swiper = new Swiper(slider, swiper_config_cards);
                prev_button.setAttribute('style','display:none');
                next_button.setAttribute('style','display:none');
                posts.forEach(post=>set_bkg_image(post));
                resize_cards(posts);
                window_width = window.innerWidth;
            }
        }
    );

}

function set_bkg_image(post)
{
    const route = post.getAttribute('data-background');
    const image_set = 'image-set(url('+route.split('.').slice(0,-1).join('.')+'.avif) 1x, url(' + route.split('.').slice(0,-1).join('.')+'.webp) 1x, url(' + route +')1x)';
    
    if (window.innerWidth>=768)
    {
        post.style.setProperty('--slide_bkg_image',image_set +', linear-gradient(to right, rgba(245, 124, 0, .8) 0% ,rgba(245, 124, 0, .45) 70%, rgba(245, 124, 0, .1)100%)');
    }
    else
    {
        post.style.setProperty('--slide_bkg_image',image_set);
    }
}

function resize_cards(cards)
{
    const heights = [];
    cards.forEach(card=>heights.push(card.getBoundingClientRect().height));
    const max_height = Math.max(...heights);
    cards.forEach(card=>card.style.setProperty('height', `${max_height}px`));
}

function swiper_buttons_handler(swiper)
{
    const prev_button = document.querySelector('.swiper-button-prev');
    const next_button = document.querySelector('.swiper-button-next');
    if (swiper.activeIndex == 0)
    {
        prev_button.setAttribute('style','display:none');
    }
    else
    {
        prev_button.removeAttribute('style');
    }

    if(swiper.isEnd)
    {
        next_button.setAttribute('style','display:none');
    }
    else
    {
        next_button.removeAttribute('style');
    }
}
