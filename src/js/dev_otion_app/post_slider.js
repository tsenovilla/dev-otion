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
    let swiper_config = {
        slidesPerView:'auto',
        spaceBetween: 15,
        freeMode:true,
        loop:false,
        centeredSlides:true,
    };
    if(window.innerWidth>=768) // Using breakpoints does not compleyely discard cards effect, leading into a weird performance of coverflow. Then it is better to provide two different objects depending on the screensize. We also take advantage of this conditional to destroy the navigation in small screensizes
    {
        swiper_config = 
        {
            ...swiper_config,
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
    }
    else
    {
        swiper_config = 
        {
            ...swiper_config,
            effect:'cards', 
            grabCursor:true
        }
        slider.querySelector('.swiper-button-prev').remove();
        slider.querySelector('.swiper-button-next').remove();
    }

    Swiper.use([Navigation, EffectCoverflow, EffectCards]);
    const swiper = new Swiper(slider, swiper_config);
    const posts = slider.querySelectorAll('.post-slider__slide');
    posts.forEach(post=>set_bkg_image(post)); // Set the bkg image for each post in the slider
    if(window.innerWidth>=768)
    {
        const prev_button = document.querySelector('.swiper-button-prev');
        prev_button.setAttribute('style','display:none'); // First time the page is loaded, the prev_button should not be visible
        swiper.on('transitionEnd', swiper_buttons_handler); // In bigger devices, Navigation is activated, then we have to handle the navigation buttons (neither show the previous one if there's not a left element, nor the last one if there's not a right element)
    }
    else
    {
        resize_cards(posts); // In small devices, the cards appear in a stack, so it's prettier if all cards have the same height (their heights depend on the content, so there may be contents longer than others)
    }
}

function set_bkg_image(post)
{
    const route = post.getAttribute('data-background');
    const image_set = 'image-set(url('+route.split('.')[0]+'.avif) 1x, url(' + route.split('.')[0]+'.webp) 1x, url(' + route +')1x)'
    'image-set(url('+route.split('.')[0]+'.avif) 1x, url(' + route.split('.')[0]+'.webp) 1x, url(' + route +')1x)';
    
    if (window.innerWidth>=768)
    {
        post.style.setProperty('--slide_bkg_image',image_set +', linear-gradient(to right, rgba(245, 124, 0, .8) 0% ,rgba(245, 124, 0,.45) 70%, rgba(245, 124, 0,.1)100%)');
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
