// Initialize Flatpickr for Timepicker field
document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#timepicker", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i:S",
        time_24hr: true,
        minuteIncrement: 1,
        enableSeconds: true,
        allowInput: true,

    });
});


// Display tooltips on action buttons
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })


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

// Style form errors when submitting Observation form with errors
$(document).ready(function() {

    // Check if any form field has an error
    if ($('.form-error').length > 0) {
        // Open the modal
        $('#newObservationModal').modal('show');
    }

    // Switch between dropdown and dropup icons when expanded or collapsed rows detected
    const expandIcon = $(this).find('.expand-icon');
  $(".clickable-row").click(function(event) {
      expandIcon.toggleClass('fa-angle-down fa-angle-up expanded');
    });
});


// Style the Observation submission success message when a successful Observation form is submitted
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


// Add click listener to the Add Dog Stance button
$("button[data-observation-id]").click(function() {
    const observationId = $(this).data("observation-id");
    $("#observation_id").val(observationId);
    $("#addDogStanceModal").modal('show');
});

// Handle form submission
$("#saveDogStanceBtn").click(function() {
    const formData = $("#dogStanceForm").serialize() + "&observation_id=" + $("#observation_id").val();
    $.post({
        url: window.location.href,
        data: formData,
        headers: { 'X-CSRFToken': '{{ csrf_token }}' },
        success: function(response) {
            if (response.status === "success") {
                const newStance = response.new_stance;
                const observationId = newStance.observation;
                const startTime = newStance.stanceStartTime;
                const dogStance = newStance.dogStance;
                const dogLocation = newStance.dogLocation;

                let table = $(`#stances-${observationId} table`).DataTable();

                table.row.add([
                    startTime,
                    dogStance,
                    dogLocation,
                    `
                    <div class="btn-group" role="group">
                        <button type="button" class="btn btn-outline-info btn-sm" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Edit this Stance">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button type="button" class="btn btn-outline-danger btn-sm" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Delete this Stance">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    `
                ]).draw();

                // Close the modal
                $("#addDogStanceModal").modal('hide');
            }
        },
        error: function(response) {
            const jsonResp = response.responseJSON;
            if (jsonResp && jsonResp.errors) {
                if (typeof jsonResp.errors === 'string') {
                    // Handle string errors
                    $("#errorText").html(jsonResp.errors);
                } else {
                    // Handle object errors
                    const fieldMapping = {
                        'stanceStartTime': 'Stance Start Time',
                        'dogStance': 'Dog Stance',
                        'dogLocation': 'Dog Location',
                    };

                    let errorMessages = [];
                    for (let [field, errors] of Object.entries(jsonResp.errors)) {
                        const displayName = fieldMapping[field] || field;
                        const errorMsg = Array.isArray(errors) ? errors.join(', ') : errors;
                        errorMessages.push(`${displayName}: ${errorMsg}`);
                    }
                    const formattedErrors = errorMessages.join('<br>');
                    $("#errorText").html(formattedErrors);
                }
                $("#errorModal").modal('show');
            } else {
                alert('An unknown error occurred');
            }
        }

    });
});

$(document).ready(function(){
    $('.dog-stance-table').each(function() {
        $(this).DataTable({
            "scrollCollapse": true,
            "pageLength": 6,
                    "autoWidth": false, // Disables auto width calculation
            "order": [[0, 'asc']],
            "stateSave": true,
            "language": {
            "emptyTable": "No Dog Stances found."
        }
        });
    });
});

