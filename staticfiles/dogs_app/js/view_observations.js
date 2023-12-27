
// Flatpick DateTime picker for the date attribute
flatpickr("#datetimepicker", {
    enableTime: true,
    clickOpens: true,
    allowInput: false,
    timeZone: 'Asia/Jerusalem',
    defaultDate: new Date(),
    plugins: [new confirmDatePlugin({
            confirmText: "Confirm",
    })]
});

// Style form errors when submitting, also toggle between drop down and drop up symbols for expanding rows
$(document).ready(function() {
    // Check if any form field has an error
    if ($('.form-error').length > 0) {
        // Open the modal
        $('#newObservationModal').modal('show');
    }

    // Attach click event listener to all expand-btn elements
    $(document).on('click', '.expand-btn', function() {
        var icon = $(this).find('.expand-icon');
        if (icon.hasClass('fa-angle-down')) {
            icon.removeClass('fa-angle-down');
            icon.addClass('fa-angle-up');
        } else {
            icon.removeClass('fa-angle-up');
            icon.addClass('fa-angle-down');
        }
    });

});


// Style the Observation submission success message
document.addEventListener('DOMContentLoaded', function() {
  const successAlert = document.querySelector('.alert-warning');
  if (successAlert) {
    successAlert.classList.remove('alert-warning');
    successAlert.classList.remove('col-md-6');
    successAlert.classList.remove('offset-md-3');
    successAlert.classList.add('alert-success');
    setTimeout(() => {
      successAlert.style.opacity = '0';
      setTimeout(() => {
        successAlert.style.display = 'none';
      }, 600);  // Fading duration, can be adjusted
    }, 4000);  // Time before fade starts, in milliseconds
  }
});


