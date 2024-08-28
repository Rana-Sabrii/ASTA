// change.js
// Change Password Form
document.querySelector('#reset form').addEventListener('submit', function(event) {
    event.preventDefault();

    const newPassword = document.getElementById('oldpass').value;
    const confirmPassword = document.getElementById('newpass').value;
    const messageDiv = document.getElementById('message');
    const errorMessageDiv = document.getElementById('error-message');

    if (newPassword !== confirmPassword) {
        errorMessageDiv.textContent = "Passwords don't match!";
        errorMessageDiv.style.color = 'red';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get('email');

    fetch('/change_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `new_password=${newPassword}&confirm_password=${confirmPassword}&email=${email}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            messageDiv.textContent = "Password updated successfully! Redirecting to login...";
            messageDiv.style.color = 'green'; 

            // Clear the password fields
            document.getElementById('oldpass').value = '';
            document.getElementById('newpass').value = '';

            // Redirect after 5 seconds
            setTimeout(function() {
                window.location.href = '/login'; // Change to your login route
            }, 3000); // 3000 milliseconds = 3 seconds 
        } else if (data.status === 'error') {
            errorMessageDiv.textContent = data.message;
            errorMessageDiv.style.color = 'red';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        errorMessageDiv.textContent = "An error occurred. Please try again later.";
        errorMessageDiv.style.color = 'red';
    });
});