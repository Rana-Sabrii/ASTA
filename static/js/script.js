// team page ///////////////////////////////////////////////////
const wrapper = document.querySelector(".wrapper");
const carousel = document.querySelector(".carousel");
const firstCardWidth = carousel.querySelector(".card").offsetWidth;
const arrowBtns = document.querySelectorAll(".wrapper i");
const carouselChildrens = [...carousel.children];

let isDragging = false, isAutoPlay = true, startX, startScrollLeft, timeoutId;

// Get the number of cards that can fit in the carousel at once
let cardPerView = Math.round(carousel.offsetWidth / firstCardWidth);

// Insert copies of the last few cards to beginning of carousel for infinite scrolling
carouselChildrens.slice(-cardPerView).reverse().forEach(card => {
    carousel.insertAdjacentHTML("afterbegin", card.outerHTML);
});

// Insert copies of the first few cards to end of carousel for infinite scrolling
carouselChildrens.slice(0, cardPerView).forEach(card => {
    carousel.insertAdjacentHTML("beforeend", card.outerHTML);
});

// Scroll the carousel at appropriate postition to hide first few duplicate cards on Firefox
carousel.classList.add("no-transition");
carousel.scrollLeft = carousel.offsetWidth;
carousel.classList.remove("no-transition");

// Add event listeners for the arrow buttons to scroll the carousel left and right
arrowBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        carousel.scrollLeft += btn.id == "left" ? -firstCardWidth : firstCardWidth;
    });
});

const dragStart = (e) => {
    isDragging = true;
    carousel.classList.add("dragging");
    // Records the initial cursor and scroll position of the carousel
    startX = e.pageX;
    startScrollLeft = carousel.scrollLeft;
}

const dragging = (e) => {
    if(!isDragging) return; // if isDragging is false return from here
    // Updates the scroll position of the carousel based on the cursor movement
    carousel.scrollLeft = startScrollLeft - (e.pageX - startX);
}

const dragStop = () => {
    isDragging = false;
    carousel.classList.remove("dragging");
}

const infiniteScroll = () => {
    // If the carousel is at the beginning, scroll to the end
    if(carousel.scrollLeft === 0) {
        carousel.classList.add("no-transition");
        carousel.scrollLeft = carousel.scrollWidth - (2 * carousel.offsetWidth);
        carousel.classList.remove("no-transition");
    }
    // If the carousel is at the end, scroll to the beginning
    else if(Math.ceil(carousel.scrollLeft) === carousel.scrollWidth - carousel.offsetWidth) {
        carousel.classList.add("no-transition");
        carousel.scrollLeft = carousel.offsetWidth;
        carousel.classList.remove("no-transition");
    }

    // Clear existing timeout & start autoplay if mouse is not hovering over carousel
    clearTimeout(timeoutId);
    if(!wrapper.matches(":hover")) autoPlay();
}

const autoPlay = () => {
    if(window.innerWidth < 800 || !isAutoPlay) return; // Return if window is smaller than 800 or isAutoPlay is false
    // Autoplay the carousel after every 2500 ms
    timeoutId = setTimeout(() => carousel.scrollLeft += firstCardWidth, 1500);
}
autoPlay();

carousel.addEventListener("mousedown", dragStart);
carousel.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragStop);
carousel.addEventListener("scroll", infiniteScroll);
wrapper.addEventListener("mouseenter", () => clearTimeout(timeoutId));
wrapper.addEventListener("mouseleave", autoPlay);


// ////////////////////////////////////////////////////////////////////




const navbarMenu = document.querySelector(".navbar .links");
const hamburgerBtn = document.querySelector(".hamburger-btn");
const hideMenuBtn = navbarMenu.querySelector(".close-btn");


const showPopupBtn = document.querySelector(".info");
const showProfile = document.querySelector("#ProfileLink");
const EditIcon = document.querySelector("#EditIcon");

const formPopup = document.querySelector(".form-popup");
const ProfilePopup = document.querySelector(".profile-popup");
const EditPopup = document.querySelector(".edit-popup");

const hideProfile = ProfilePopup.querySelector(".close-btn");
const hideEdit = EditPopup.querySelector(".close-btn");


const hidePopupBtn = formPopup.querySelector(".close-btn");
const signupLoginLink = formPopup.querySelectorAll(".bottom-link a");
const UserInfo = document.getElementById('UserData');
const logOutElement = document.getElementById('LogOut');
const Login = document.getElementById('Login');

const specializationSection = document.getElementById('specialization-section');
const userTypeSelect = document.getElementById('edit-type');

let isEditProfilePopulated = false; // Flag to track if the form is populated

// Show mobile menu
hamburgerBtn.addEventListener("click", () => {
    navbarMenu.classList.toggle("show-menu");
});

// Hide mobile menu
hideMenuBtn.addEventListener("click", () =>  hamburgerBtn.click());

// Show user info popup
showPopupBtn.addEventListener("click", () => {
    document.body.classList.toggle("show-popup");
    // formPopup.style.display ='block';
});
//Hide user info popup
hidePopupBtn.addEventListener("click", () => showPopupBtn.click());




//////////////////////
showProfile.addEventListener("click", () => {
    document.body.classList.toggle("show-profile");
    showPopupBtn.click();

    // formPopup.style.display ='none'
    
});
//hide user profile
hideProfile.addEventListener("click", () => showProfile.click());
//hide edit 
hideEdit.addEventListener("click", () => EditIcon.click());

//Hide userinfo
logOutElement.addEventListener('click', function() {
    UserInfo.style.display = 'none';
    formPopup.style.display ='none';
    Login.style .display='block';

});


// Function to populate Account Info
function populateAccountInfo(data) {
    document.getElementById('name').textContent = data.username;
    document.getElementById('email').textContent = data.email;
    document.getElementById('phoneNumber').textContent = data.phoneNum;
    document.getElementById('age').textContent = data.Age;
    document.getElementById('userType').textContent = data.statusSelect;
    document.getElementById('gender').textContent = data.genderSelect;
    document.getElementById('username-display').textContent = data.username;

    const specializationSpan = document.getElementById('specialization');
    if (data.statusSelect === 'Pathologist') {
        specializationSpan.textContent = data.specialization || "";
        specializationSpan.parentElement.style.display = 'block';
    } else {
        specializationSpan.parentElement.style.display = 'none';
    }
}

// DOMContentLoaded Event 
document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-user-data')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching user data:', data.error);
                return;
            }
            populateAccountInfo(data); // Populate Account Info 
        })
        .catch(error => {
            console.error('An error occurred:', error);
        }); 
});

// Edit Icon Click Event

//show edit icon
EditIcon.addEventListener("click", () => {
    document.body.classList.toggle("show-edit");

    if (!isEditProfilePopulated) { 
        fetch('/get-user-data')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error fetching user data:', data.error);
                    return;
                }

                // Populate Edit Profile form
                document.getElementById('edit-name').value = data.username;
                document.getElementById('edit-email').value = data.email;
                document.getElementById('edit-phone').value = data.phoneNum;
                document.getElementById('edit-age').value = data.Age;
                document.getElementById('edit-type').value = data.statusSelect;

                // Set selected option for Gender dropdown
                const genderSelect = document.getElementById('edit-gender');
                const genderToSelect = data.genderSelect; 
                setTimeout(() => {
                    for (let i = 0; i < genderSelect.options.length; i++) {
                        if (genderSelect.options[i].value === genderToSelect) {
                            genderSelect.selectedIndex = i; 
                            break;
                        }
                    } 
                }, 0); 

                // Show specialization section if user type is Pathologist
                const specializationSpan = document.getElementById('specialization');
                if (data.statusSelect === 'Pathologist') {
                    specializationSpan.textContent = data.specialization;
                    specializationSpan.parentElement.style.display = 'block'; // Show the entire <p> tag
                } else {
                    specializationSpan.parentElement.style.display = 'none'; // Hide the entire <p> tag 
                }

                
                // show specialization section in edit form if pathologist
                const specializationSectionEdit = document.getElementById('specialization-section'); 
                if (data.statusSelect === 'Pathologist') {
                    specializationSectionEdit.style.display = 'block';
                    document.getElementById('edit-specialization').value = data.specialization; // Pre-select the specialization
                } else {
                    specializationSectionEdit.style.display = 'none'; 
                }

                isEditProfilePopulated = true;
            })
            .catch(error => {
                console.error('An error occurred:', error);
            }); 
    }
});
////////////////////////////////
// Sending a request to check the login status
fetch('/check-login-status')
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Error occurred while calling the API');
    })
    .then(data => {
        if (data.loggedIn) {
            // User is logged in
            document.getElementById('UserData').style.display = 'block';
            document.getElementById('Login').style.display='none';
        } else {
            // User is not logged in
            document.getElementById('UserData').style.display = 'none';
        }
    })
    .catch(error => {
        console.error('An error occurred:', error);
    });










/////////////////////////////////////////////////////









document.getElementById('editProfileForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const updatedData = {
        username: document.getElementById('edit-name').value,
        email: document.getElementById('edit-email').value,
        password: document.getElementById('edit-password').value,
        phoneNum: document.getElementById('edit-phone').value,
        Age: document.getElementById('edit-age').value,
        genderSelect: document.getElementById('edit-gender').value,
        statusSelect: document.getElementById('edit-type').value,
        specialization: document.getElementById('edit-specialization').value // Add specialization if it's available
    };

    fetch('/update-profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error updating profile:', data.error);
            return;
        }

        alert('Profile updated successfully!');
        window.location.reload();
    })
    .catch(error => {
        console.error('An error occurred:', error);
    });
});

// Show/hide specialization section based on user type selection
userTypeSelect.addEventListener('change', function() {
    if (this.value === 'Pathologist') {
        specializationSection.style.display = 'block';
    } else {
        specializationSection.style.display = 'none';
    }
});

