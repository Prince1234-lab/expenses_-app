
const inputUsername = document.querySelector('#inputUsername');
const feedback = document.querySelector('.usernameinvalidfeedback');
const inputEmail = document.querySelector('#inputEmail');
const emailfeedback = document.querySelector('.emailinvalidfeedback');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');
const inputPassword  = document.querySelector('#inputPassword');
const showPwdToggle = document.querySelector('#showPwdToggle');
const submitBtn = document.querySelector('.submit_btn');

// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');  // Retrieve CSRF token from the cookie



const handleToggleInput= (e)=>{
    if(showPwdToggle.textContent === "SHOW"){
        showPwdToggle.textContent = "HIDE";
        inputPassword.setAttribute("type", "text");
    }else{
        showPwdToggle.textContent = "SHOW";
        inputPassword.setAttribute("type", "password");
    }
};

if (showPwdToggle) {
    showPwdToggle.addEventListener('click', handleToggleInput);
} else {
    console.error("Element with ID 'showPwdToggle' not found.");
}


inputEmail.addEventListener('keyup', (e)=>{
    console.log("777", 777); 
    const emailval = e.target.value;
    emailSuccessOutput.style.display = 'block';
    emailSuccessOutput.textContent = `Checking ${emailval}`;
    inputEmail.classList.remove('is-invalid');
    emailfeedback.style.display = "none";

    if (emailval.length > 0) {
        fetch("/authentication/validation-email", {
            method: "POST",
            body: JSON.stringify({ email: emailval}), // Send username value in request body
            headers: {
                "Content-Type": "application/json",  // Indicate the content type is JSON
                "X-CSRFToken": csrftoken,  // Send CSRF token for Django validation
            },
        })
        .then((res) => res.json()) // Parse the JSON response
        .then((data) => {            emailSuccessOutput.style.display = 'none';
            if(data.email_error){
                submitBtn.disabled = true;
                inputEmail.classList.add("is-invalid");
                emailfeedback.style.display = "block";
                emailfeedback.innerHTML= `<p>${data.email_error}</p>`;
            }else{
                submitBtn.removeAttribute("disabled");
            }
        })
        .catch((error) => {
            console.error("Error:", error); // Log any errors in the request
        });
    }

})


inputUsername.addEventListener('keyup', (e) => {
    console.log("2222", 2222); // Log a message on keyup event for debugging
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent =`Checking ${usernameVal}`;

    inputUsername.classList.remove("is-invalid");
    feedback.style.display = "none";
    
    if (usernameVal.length > 0) {
        fetch("/authentication/validation-username", {
            method: "POST",
            body: JSON.stringify({ username: usernameVal }), // Send username value in request body
            headers: {
                "Content-Type": "application/json",  // Indicate the content type is JSON
                "X-CSRFToken": csrftoken,  // Send CSRF token for Django validation
            },
        })
        .then((res) => res.json()) // Parse the JSON response
        .then((data) => {
            usernameSuccessOutput.style.display = "none";
            if(data.username_error){
                submitBtn.disabled = true;
                inputEmail.classList.add("is-invalid");
                feedback.style.display = "block";
                feedback.innerHTML= `<p>${data.username_error}</p>`;
            }else{

                submitBtn.removeAttribute("disabled");
            }
        })
        .catch((error) => {
            console.error("Error:", error); // Log any errors in the request
        });
    }
});
