const loginForm = document.getElementById('login_form');
loginForm.addEventListener('submit', validateLoginForm);

function validateLoginForm(event) {
    event.preventDefault();

    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const errorMessages = document.getElementById('loginErrorMessages');
    errorMessages.innerHTML = '';

    // Validate email
    if (!validateEmail(email.value)) {
        errorMessages.innerHTML += '<p>Please enter a valid email address.</p>';
        return;
    }

    // Validate password
    if (!validatePassword(password.value)) {
        errorMessages.innerHTML += '<p>Please enter a valid password.</p>';
        return;
    }
}

function validateEmail(email) {
    // Use a regular expression to check if the email is valid
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    // Customize these rules to match your password requirements
    const minLength = 4;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);

    return (
        password.length >= minLength &&
        hasUpperCase &&
        hasLowerCase &&
        hasNumber
    );
}