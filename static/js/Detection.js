const dropArea = document.querySelector(".img-area"),
dragText = dropArea.querySelector("header")
const selectImage = document.querySelector('.select-image');
const inputFile = document.querySelector('#file');
// const imgArea = document.querySelector('.img-area');

//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload image";
});
//If user drop File on DropArea
dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile(); //calling function
});







////////////////////////////////////////////////////


selectImage.addEventListener('click', function () {
  inputFile.click();
 })

 inputFile.addEventListener("change", function(){
//getting user select file and [0] this means if user select multiple files then we'll select only the first one
file = this.files[0];
dropArea.classList.add("active");
showFile(); //calling function
});
///////////////////////////////////////////////////////////


function showFile() {
  let fileType = file.type; //getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; //adding some valid image extensions in array
  if (validExtensions.includes(fileType)) { //if user selected file is an image file
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = () => {
      let fileURL = fileReader.result; //passing user file source in fileURL variable
      let imgTag = `<img src="${fileURL}" alt="">`; //creating an img tag and passing user selected file source inside src attribute
      dropArea.innerHTML = imgTag; //adding that created img tag inside dropArea container
    }
    fileReader.readAsDataURL(file);
  } else {
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}

// Function to send image data to server
function sendImageToServer() {
  if (imgTag) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'your_server_url');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          console.log(response);
        } else {
          console.error('Error:', xhr.status);
        }
      }
    };
    xhr.send(JSON.stringify({ image: fileURL }));
  } else {
    console.error('No image selected.');
  }
}
