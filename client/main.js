// Function to convert a file to base64
const loader = document.getElementById('loader')
function fileToBase64(file, callback) {
    const reader = new FileReader();
    reader.onload = function () {
        callback(reader.result);
    };
    reader.readAsDataURL(file);
}

// Function to send the base64-encoded image to the server
function sendImageToServer(base64Image) {
    // Create an object with the image data
    const imageData = { image: base64Image };

    // Send the image data to the server using a fetch request
    fetch("http://127.0.0.1:5000/verify", {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(imageData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server Response:', data);
        // Assuming data is an array of image paths
        const imagePaths = data.data;
        loader.style.display = 'none'
        // Get a container element where you want to display the images
        const container = document.getElementById('imageContainer');

        // Create img elements and append them to the container
        imagePaths.forEach(path => {
            const fileName = path.substring(path.lastIndexOf("\\data\\"));
            const div = document.createElement('div');
            const a= document.createElement('a')
            div.className = 'item selfie col-4 mt-3 mb-2'
            const img = document.createElement('img');
            a.className = 'fancylight popup-btn'
            a.href = 'fileName'
            img.className = 'img-fluid'
            img.src = fileName;
            console.log(fileName)
            div.appendChild(img)
            div.appendChild(a)
            container.appendChild(div);
        });        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Attach a change event listener to the file input
document.getElementById('imageInput').addEventListener('change', function () {
    const selectedFile = this.files[0];
    fileToBase64(selectedFile, function (base64String) {
        // Store the base64-encoded image in a variable
        const base64Image = base64String;
        // Display the image in the preview area
        const preview = document.getElementById('imagePreview');
        preview.style.display = 'block';
        preview.src = base64Image;

        // Store the base64Image in a global variable for later use
        window.base64Image = base64Image;
    });
});

// Attach a click event listener to the upload button
document.getElementById('uploadButton').addEventListener('click', function (e) {
    // Send the image to the server
    sendImageToServer(window.base64Image);
    loader.style.display = 'block'

});

$(document).ready(function() {
    var popup_btn = $('.popup-btn');
    popup_btn.magnificPopup({
    type : 'image',
    gallery : {
        enabled : true
    }
  });
});