const form = document.querySelector('form');
const errorDiv = document.getElementById('error-message');
const flightNumberInput = document.getElementById('flight-number');
form.addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(form);
    
    try {
        const response = await fetch('/insert-flight', {
            method: 'POST', 
            body: formData 
        });
        const result = await response.json();

        if (result.success) {

            window.location.href = '/';
        } else {
            errorDiv.innerText=result.error;
            
        }
    } catch (error) {
        errorDiv.innerText="Couldn't add this flight , try again later"
    }
});

function focusedOnInput(){
    errorDiv.innerText=""

}
flightNumberInput.addEventListener('focus',focusedOnInput);