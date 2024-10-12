const form = document.querySelector('form');
const errorDiv = document.getElementById('error-message');
const emailInput = document.getElementById('email');
form.addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(form);
    
    try {
        const response = await fetch('/insert-user', {
            method: 'POST', 
            body: formData 
        });
        const result = await response.json();

        if (result.success) {
            localStorage.setItem('loggedin', true);
            localStorage.setItem('user_id', result.user.user_id);
            localStorage.setItem('user_type', result.user.user_type);
            window.location.href = '/';
        } else {
            errorDiv.innerText=result.error;
            
        }
    } catch (error) {
        errorDiv.innerText="Couldn't sign you up , try again later"
    }
});

function focusedOnInput(){
    errorDiv.innerText=""

}
emailInput.addEventListener('focus',focusedOnInput);
