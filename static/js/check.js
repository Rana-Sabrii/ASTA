// Email Check Form (in email_check.html)
document.querySelector('#reset form').addEventListener('submit', function(event) {
    // event.preventDefault(); <--- Make sure this is REMOVED 

    const email = document.getElementById('em').value;
    const errorMessageDiv = document.getElementById('error-message'); 

    fetch('/check_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `email=${email}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Use the email from the form input
            window.location.href = `/change_password?email=${email}`; 
        } else if (data.status === 'error') {
            errorMessageDiv.textContent = data.message;
            errorMessageDiv.style.color = 'red';
        }
    });
});
