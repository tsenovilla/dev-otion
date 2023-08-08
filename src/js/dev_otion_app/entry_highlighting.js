/**
 * This function changes the innerHTML of each piece of code written in the article (encapsulated under [code][/code] marks in the database) in order to apply code highlighting.
 * @param {HTMLElement} article
 */
export default function(article)
{
    article.innerHTML = article.innerHTML.replace(/\[code\](.*?)\[\/code\]/gs,'<pre><code>$1</code></pre>');
    hljs.highlightAll();
}