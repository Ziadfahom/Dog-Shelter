function submitDogForm() {
    const form = document.querySelector('.stylish-form');
    form.submit();
}

function goBack() {
    window.history.back();
}

// Function to toggle visibility of Adoption Date field based on dropdown selection
function toggleAdoptionDateField() {
    var adoptionStatus = document.getElementById("adoptionStatus");
    var adoptionDateField = document.getElementById("adoptionDate");
    var adoptionDateAndLabel = document.getElementById("adoptionDateAndLabel");

    if (adoptionStatus.value == "Yes") {
        if (adoptionDateField.value == "") {
            // Set the field value to today's date
            adoptionDateField.value = new Date().toISOString().split('T')[0];
        }
        adoptionDateField.style.display = "block";
        adoptionDateAndLabel.style.display = "block";
    } else {
        adoptionDateField.value = "";  // Clear the field value
        adoptionDateField.style.display = "none";
        adoptionDateAndLabel.style.display = "none";

    }
}

// Initial call to toggleAdoptionDateField function on page load
toggleAdoptionDateField();

// Event listener for dropdown change
document.getElementById("adoptionStatus").addEventListener("change", toggleAdoptionDateField);
