const form = document.querySelector('form');
const errorDiv = document.getElementById('error-message');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

// submitting the user info , get the result . 
form.addEventListener('submit', async function(event) {
    event.preventDefault();

    //forcing user to enter a long password for security
    if(passwordInput.value.length<8){
        errorDiv.innerText='password must be more than 8 characters';
        return;
    }
    
    const formData = new FormData(form);

    // const password = formData.get('password');

    try {
        // const salt = await bcrypt.genSalt(10); 
        // const hashedPassword = await bcrypt.hash(password, salt); 
        

        // formData.set('password', hashedPassword);
        const response = await fetch('/insert-user', {
            method: 'POST', 
            body: formData 
        });
        const result = await response.json();

        if (result.success) {
            
            //storing user information after signing up in the local storage
            localStorage.setItem('loggedin', true);
            localStorage.setItem('user_type', result.user.user_type);
            window.location.href = '/';
        } else {
            //show error message if email used in signing up before .

            errorDiv.innerText=result.error;
            
        }
    } catch (error) {
        
        errorDiv.innerText="Couldn't sign you up , try again later"
        // errorDiv.innerText=error
    }
});
// when user focuses on input , error goes on .
function focusedOnInput(){
    errorDiv.innerText=""

}
emailInput.addEventListener('focus',focusedOnInput);
