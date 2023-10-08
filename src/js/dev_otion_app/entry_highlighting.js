/**
 * This function changes the innerHTML of each piece of code written in the article (encapsulated under [code language][/code] marks in the database) in order to apply code highlighting for the written language
 * @param {HTMLElement} article
 */
export default function(article)
{
    article.innerHTML = article.innerHTML.replace(/<p>\[code (.*?)\]<\/p>(.*?)<p>\[\/code\]<\/p>/gs,'<pre><code class="language-$1">$2</code></pre>');
}