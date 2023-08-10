/**
 * This function adds the functionality of closing the alert to the inner button of an alert. Also, the alert itself is deleted after 10 seconds.
 * @param {HTMLElement} alert
 */
export default function error_management(alert)
{
    const button = alert.querySelector('button');
    button.addEventListener("click",()=>alert.remove());
    setTimeout(()=>alert.remove(),10000);
}