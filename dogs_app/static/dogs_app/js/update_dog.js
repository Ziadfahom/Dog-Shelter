// Event listener for the 'customUploadButton' button. When this button is clicked...
document.getElementById('customUploadButton').addEventListener('click', function() {
    // ...it triggers a click event on the hidden file input ('id_dogImage'),
    // opening the file chooser dialog.
    document.getElementById('id_dogImage').click();
});

// Event listener for the file input ('id_dogImage'). When a file is selected...
document.getElementById('id_dogImage').addEventListener('change', function(e) {
    // ...it gets the selected file.
    var file = e.target.files[0];
    var reader = new FileReader();

    // When the file has been read...
    reader.onloadend = function() {
        // ...it updates the source of the 'dog_picture' image to be the selected file,
        // and shows the 'image_change_alert' alert message.
        document.getElementById('dog_picture').src = reader.result;
        document.getElementById('image_change_alert').style.display = 'block';  // Show the alert
    }

    // If a file was selected, read it as a data URL.
    // This will trigger the 'loadend' event when done.
    if (file) {
        reader.readAsDataURL(file);
    } else {
        // If no file was selected, reset the 'dog_picture' image to the default.
        document.getElementById('dog_picture').src = "/media/dog_pictures/default_dog.jpg";
    }
});

// Get all date fields and reset links
var dateFields = document.querySelectorAll('.date-field');
var resetLinks = document.querySelectorAll('.reset-date-link');

// For each reset link...
resetLinks.forEach((link, index) => {
    // ...add a click event listener. When the link is clicked...
    link.addEventListener('click', function(e) {
        e.preventDefault();  // Prevent the default action
        // ...it clears the associated date field.
        dateFields[index].value = "";
    });
});