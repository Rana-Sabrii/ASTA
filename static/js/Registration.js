
let CreateAccount= document.getElementById('CreateAcc');
let specializationSelect = document.getElementById('specializationSelect');

document.getElementById('statusSelect').addEventListener('change', function () {
    var status = this.value;
    var specializationInput = document.getElementById('specializationSelect'); 
    var idCardImage = document.getElementById('idCardImage');
    var selectspecializationDiv = document.getElementById('selectspecialization'); // Get the containing div

    // Show ID Card Upload for Pathologist, Multi Omics Analyst, and Other
    if (status === 'Pathologist' || status === 'Multi Omics Analyst' || status === 'other') { 
        idCardImage.style.display = 'block';
        CreateAccount.style.paddingTop="30px";
        alert("Please note that your contact information (email and phone number) will be visible to other users.");
        document.getElementById('container').style.minHeight='720px';
        

    } else {
        idCardImage.style.display = 'none';
        document.getElementById('idCardUpload').removeAttribute('required');
    }

    // Show Specialization Selection ONLY for Pathologist
    if (status === 'Pathologist') {
        selectspecializationDiv.style.display = 'block'; // Show the containing div
        specializationInput.required = true; 
    } else {
        selectspecializationDiv.style.display = 'none'; // Hide the containing div
        specializationInput.required = false; 
    }
});

document.getElementById('idCardUpload').addEventListener('change', function () {
    var file = this.files[0];
    // var img = document.getElementById('idCardPreview');
    // img.src = URL.createObjectURL(file);
    // img.style.display = 'block';
});
///////////////////////////////////

document.querySelector('form').addEventListener('submit', function(event) {
    if (!this.checkValidity()) {
        event.preventDefault();  // Prevent form submission
        let invalidFields = this.querySelectorAll(':invalid');
        if (invalidFields.length > 0) {
            invalidFields[0].focus();  // Focus the first invalid field
        }
    }});

////////////////////////////////////////////////


const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
let signINBtn = document.getElementById('signINBtn');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

//////////////////////////
document.getElementById('loginButton').addEventListener('click', function() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify({ em: email, pass: password }),
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            alert('Invalid email or password. Please try again.');
        }
    })
    .then(data => {
        console.log(data.message);
        window.location.href = '/check-login-status';  // Redirect to profile page
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });



    fetch('/check-login-status')
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url && data.loggedIn) {
            // Handle the redirect
            window.location.href = data.redirect_url;
            return; // Exit the function to avoid further processing
        }

        const userDataElement = document.getElementById('UserData');
        if (data.loggedIn) {
            userDataElement.style.display = 'block';

        } else {
            userDataElement.style.display = 'none';
        }
        
    })
    .catch(error => {
        console.error('An error occurred:', error);
    });

});