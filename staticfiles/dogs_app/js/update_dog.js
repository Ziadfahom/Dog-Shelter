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

// Function to toggle visibility of Adoption Date field based on dropdown selection
function toggleAdoptionDateField() {
    var adoptionStatus = document.getElementById("adoptionStatus");
    var adoptionDateField = document.getElementById("id_adoptionDate");
    var resetAdoption = document.getElementById("reset-adoption");
    var adoptionDateAndLabel = document.getElementById("adoptionDateAndLabel");
    if (adoptionStatus.value == "Yes") {
        if (adoptionDateField.value == "") {
            // Set the field value to today's date
            adoptionDateField.value = new Date().toISOString().split('T')[0];
        }
        adoptionDateField.style.display = "block";
        resetAdoption.style.display = "block";
        adoptionDateAndLabel.style.display = "block";
    } else {
        adoptionDateField.value = "";  // Clear the field value
        adoptionDateField.style.display = "none";
        resetAdoption.style.display = "none";
        adoptionDateAndLabel.style.display = "none";

    }
}

// Initial call to toggleAdoptionDateField function on page load
toggleAdoptionDateField();

// Event listener for dropdown change
document.getElementById("adoptionStatus").addEventListener("change", toggleAdoptionDateField);

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

function submitDogForm() {
    const form = document.querySelector('.stylish-form');
    form.submit();
}

function goBack() {
    window.history.back();
}