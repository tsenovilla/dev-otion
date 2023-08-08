/**
 * This function delete the predefined style attributes set by Django-CKEditor to the images loaded by this library. In order to make responsive images inside blog entries, we need to delete these attributes
 * @param {HTMLElement} article
 */
export default function(article)
{
    const images = article.querySelectorAll('img');
    images.forEach(image=>image.removeAttribute('style'));
}