// For Sign In.
const loginForm = document.getElementById('login-form');
const loginSubmitButton = document.querySelector('button[type="submit"]');
const loginMessageBox = document.querySelector('.message');

loginForm.addEventListener('submit', function (event) {
    event.preventDefault();
    handleLoginFormSubmission();
})

function handleLoginFormSubmission() {
    const userName = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'authentication/login');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            window.location.href = '/personality_test';
        } else if (xhr.status === 401){
            const response = JSON.parse(xhr.responseText);
            loginMessageBox.textContent = response.message;
        } else {
            loginMessageBox.textContent = 'Error: ' + xhr.statusText;
        }
    };

    xhr.send(JSON.stringify({ userName: userName, password: password }));
}

// For Sign Up.
const signupForm = document.getElementById('signup-form');
const signupSubmitButton = document.getElementsByClassName('submit-btn2')[0];
const signupMessageBox = document.querySelector('.message2');

signupForm.addEventListener('submit', function (event) {
    event.preventDefault();
    handleSignupFormSubmission();
})

function handleSignupFormSubmission() {
    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const userName = document.getElementById('username2').value;
    const password = document.getElementById('password2').value;
    const email = document.getElementById('email_id').value;
    const mobileNumber = document.getElementById('mobile_number').value;
    const dateOfBirth = document.getElementById('dob').value;

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'authentication/signup');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            window.location.href = '/';
        } else if (xhr.status === 401) {
            const response = JSON.parse(xhr.responseText);
            signupMessageBox.textContent = response.message;
        } else {
            signupMessageBox.textContent = 'Error: ' + xhr.statusText;
        }
    };

    xhr.send(JSON.stringify({ firstName: firstName, lastName: lastName, email: email, mobileNumber: mobileNumber, userName: userName, password: password, dateOfBirth: dateOfBirth }));
}
