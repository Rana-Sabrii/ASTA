const dropArea = document.querySelector('.drop-section')
const listSection = document.querySelector('.list-section')
const listContainer = document.querySelector('.list')
const fileSelector = document.querySelector('.file-selector')
const fileSelectorInput = document.querySelector('.file-selector-input')
const DropContent=document.querySelector('.cloud-icon')

fileSelector.onclick = () => fileSelectorInput.click();
fileSelectorInput.onchange = () => {
    [...fileSelectorInput.files].forEach((file) => {
         
            uploadFile(file);
        
    });
}


dropArea.ondragover = (e) => {
    e.preventDefault();
    dropArea.classList.add('drag-over-effect');
}

dropArea.ondragleave = () => {
    dropArea.classList.remove('drag-over-effect');
}


dropArea.ondrop = (e) => {
    e.preventDefault();
    dropArea.classList.remove('drag-over-effect');
    
    [...e.dataTransfer.files].forEach((file) => {
    
            uploadFile(file);
        
    });
}




// check the file type
// function typeValidation(type){
//     var splitType = type.split('/')[0]
//     if(type == 'application/pdf' || splitType == 'image' || splitType == 'video'){
//         return true
//     }
// }

// upload file function
function uploadFile(file){
    listSection.style.display = 'block'
    var li = document.createElement('li')
    li.classList.add('in-prog')
    li.innerHTML = `
        <div class="col">
            <img src="../static/images/photo.jpg" height="50" width="50" alt="">
        </div>
        <div class="col">
            <div class="file-name">
                <div class="name">${file.name}</div>
                <span>0%</span>
            </div>
            <div class="file-progress">
                <span></span>
            </div>
            <div class="file-size">${(file.size/(1024*1024)).toFixed(2)} MB</div>
        </div>
        <div class="col">
        <svg xmlns="http://www.w3.org/2000/svg" class="delete-icon" height="20" width="20"><path d="m5.979 14.917-.854-.896 4-4.021-4-4.062.854-.896 4.042 4.062 4-4.062.854.896-4 4.062 4 4.021-.854.896-4-4.063Z"/></svg>
        
        </div>
    `
    const deleteIcon = li.querySelector('.delete-icon');
    deleteIcon.onclick = () => {
        if (confirm('Are you sure you want to delete')) {
            li.remove();}}
    listContainer.appendChild(li);

    const formData = new FormData();
    formData.append('file', file);

    const xhr = new XMLHttpRequest();
    xhr.onload = () => {
        li.querySelector('.file-progress span').innerText = 'Complete';
        li.classList.add('complete');
        li.classList.remove('in-prog')
    };

    xhr.upload.onprogress = (e) => {
        var percent_complete = (e.loaded / e.total)*100
        li.querySelectorAll('span')[0].innerHTML = Math.round(percent_complete) + '%'
        li.querySelectorAll('span')[1].style.width = percent_complete + '%'
    };

    xhr.open('POST', 'https://your-backend-endpoint', true); 
    xhr.send(formData);}







    // function predict() {
    //     // Make an API request to your .NET backend
    //     fetch('https://your-dotnet-api-endpoint')
    //         .then(response => response.json())
    //         .then(data => {
    //             // Display the result in the result container
    //             displayResult(data.result);
    //         })
    //         .catch(error => {
    //             console.error('Error fetching prediction:', error);
    //         });
    // }







    
    
    // function displayResult(result) {
    //     const resultContainer = document.getElementById('predictionResult');
    //     resultContainer.textContent = 'Prediction Result: ' + result;
    //     resultContainer.style.display = 'block';
    //     DropContent.style.display='none';
    // }
    