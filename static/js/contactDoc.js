document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-doctors')
        .then(response => response.json())
        .then(doctors => {
            console.log('Fetched doctors:', doctors);  // Debug: log fetched data

            const pathologists = document.getElementById('pathologists');
            const multiOmicsAnalysts = document.getElementById('multi-omics-analysts');

            doctors.forEach(doctor => {
                const doctorDiv = document.createElement('div');
                doctorDiv.classList.add('contact-diabetic-doc');

                // Create the HTML dynamically based on user_type
                if (doctor.user_type === 'Pathologist') {
                    doctorDiv.innerHTML = `
                        <p class="res-num">${doctor.username}</p>
                        <div class="email-contact"><i class="fa-solid fa-envelope"></i><span>: <a href="mailto:${doctor.email}">${doctor.email}</a></span></div>
                        <div class="contact-phone"><i class="fa-solid fa-phone-flip"></i><span>: <a href="https://wa.me/20${doctor.phonenum}">${doctor.phonenum}</a></span></div>
                        <div class="specialization"><i class="fa-solid fa-user-md"></i><span>: ${doctor.specialization}</span></div> 
                    `;
                } else if (doctor.user_type === 'Multi Omics Analyst') {
                    doctorDiv.innerHTML = `
                        <p class="res-num">${doctor.username}</p>
                        <div class="email-contact"><i class="fa-solid fa-envelope"></i><span>: <a href="mailto:${doctor.email}">${doctor.email}</a></span></div>
                        <div class="contact-phone"><i class="fa-solid fa-phone-flip"></i><span>: <a href="https://wa.me/20${doctor.phonenum}">${doctor.phonenum}</a></span></div>
                    `;
                } 

                // Append the doctorDiv to the correct container
                if (doctor.user_type === 'Pathologist') {
                    console.log('Appending to pathologists:', doctor); 
                    pathologists.appendChild(doctorDiv);
                } else if (doctor.user_type === 'Multi Omics Analyst') {
                    console.log('Appending to multi-omics analysts:', doctor); 
                    multiOmicsAnalysts.appendChild(doctorDiv);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching doctor data:', error);
        });
});