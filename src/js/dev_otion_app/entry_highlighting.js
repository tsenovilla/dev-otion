/**
 * This function changes the innerHTML of each piece of code written in the article (encapsulated under [code][/code] marks in the database) in order to apply code highlighting. It also embed the content encapsulated under [p][/p] into p tags.
 * @param {HTMLElement} article
 */
export default function(article)
{
    article.innerHTML = article.innerHTML.replace(/\[p\](.*?)\[\/p\]/gs,'<p>$1</p>');
    article.innerHTML = article.innerHTML.replace(/\[code\](.*?)\[\/code\]/gs,'<pre><code>$1</code></pre>');
    hljs.highlightAll();
}