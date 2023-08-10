/**
 * This function sends a FetchAPI request to the server when the user writes something in the search bar. Its goal is to show to the user all the entries whose titles contain the user's input 
 * @param {HTMLElement} search_input
 */
export default function search_entry(search_input)
{
    search_input.addEventListener('input', async(e) =>
        {
            delete_previous_search()
            const input = e.target.value;
            if(input.length > 5) // We do not call the API for lengths smaller than 5, just to avoid showing 213434 results
            {
                const response = await API_call(input);
                if(Object.keys(response).length > 0) // We check if we get something :)
                {
                    const result_container = document.querySelector('.result_container');
                    for (let entry in response)
                    {
                        const obtained_entry = document.createElement('A');
                        obtained_entry.textContent = entry;
                        obtained_entry.setAttribute('href',response[entry]);
                        obtained_entry.classList.add('search_result');
                        result_container.appendChild(obtained_entry);
                    }   
                }
            }
        }
    )
}

/**
 * This function performs the API call to retrieve the entries matching the input
 * @param {String} input 
 * @returns {Promise} A promise that contains entries that match the introduced input
 */
async function API_call (input)
{
    const lang = window.location.pathname.match(/\/(?<lang>[a-z]+)/).groups.lang
    const fetch_config = {
        method: 'POST',
        headers:
        {
            'Content-Type':'application/json',
            'X-CSRFToken': csrfToken
        },
        body:JSON.stringify({'input':input})
    }
    try
    {
        const API_request = await fetch(`/${lang}/search_API`,fetch_config);
        const API_response = await API_request.json();
        return API_response
    }
    catch(error)
    {
    }
}

/**
 * This function deletes the ChildNode tree of the result container each time the input changes
 */
function delete_previous_search()
{
    const result_container = document.querySelector('.result_container');
    while (result_container.hasChildNodes())
    {
        result_container.removeChild(result_container.firstChild)
    }
}