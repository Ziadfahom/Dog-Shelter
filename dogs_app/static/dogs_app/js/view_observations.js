// Show toasts for success messages instead of alert when deleting entities
const obsSuccessToastEl = document.getElementById('obsSuccessToast');
const obsToastEl = new bootstrap.Toast(obsSuccessToastEl, {
    autohide: true,
    delay: 2000
});

const stanceSuccessToastEl = document.getElementById('stanceSuccessToast');
const stanceToastEl = new bootstrap.Toast(stanceSuccessToastEl, {
    autohide: true,
    delay: 2000
});



// Initialize Flatpick Time picker for the sessionDurationInMins attribute in the form
function initializeTimeFlatpickr(defaultTime) {
    flatpickr("#timepicker", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i:S",
        defaultDate: defaultTime,
        time_24hr: true,
        minuteIncrement: 1,
        enableSeconds: true,
        allowInput: true
    });
}

// Display tooltips on action buttons
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

// Initialize Flatpick DateTime picker for the obsDateTime attribute in the form
function initializeDateTimeFlatpickr(defaultDate) {
    flatpickr("#datetimepicker", {
        enableTime: true,
        clickOpens: true,
        allowInput: true,
        minuteIncrement: 1,
        dateFormat: "Y-m-dTH:i:S\\Z",  // Format for submission
        altInput: true,  // Enable alternative input
        altFormat: "Y-m-d H:i:S",  // User-friendly format for display
        timeZone: 'Asia/Jerusalem',
        defaultDate: defaultDate,
        plugins: [new confirmDatePlugin({
            confirmText: "Confirm",
        })]
    });
}

// Display form errors in the modal
function displayErrors(errors, formName, modalId) {
    // Clear existing errors
    $('.form-error').remove();
    $('.form-general-error').remove();

    // Handle simple string errors
    if (typeof errors === 'string') {
        let errorContainer = $('#' + formName + '-general-error');
        if (errorContainer.length) {
            // If the error container exists, update its content
            errorContainer.html('<div class="alert alert-danger form-general-error" role="alert">' + errors + '</div>');
        } else {
            // If the error container doesn't exist, create it
            $('#'+ formName + '-form').prepend('<div id="' + formName + '-general-error" class="alert alert-danger form-general-error" role="alert">' + errors + '</div>');
        }

    }
    // Check if general error exists and is not already displayed
    else if ((errors['__all__'] || errors['non_field_errors']) && !$('.form-general-error').length) {
        let generalErrors = errors['__all__'] || errors['non_field_errors'];
        let errorString = generalErrors.join('<br>');

        let errorContainer = $('#' + formName + '-general-error');
        if (errorContainer.length) {
            // If the error container exists, update its content
            errorContainer.html('<div class="alert alert-danger form-general-error" role="alert">' + errorString + '</div>');
        } else {
            // If the error container doesn't exist, create it
            $('#'+ formName + '-form').prepend('<div id="' + formName + '-general-error" class="alert alert-danger form-general-error" role="alert">' + errorString + '</div>');
        }
    }
    else {
        // Display field-specific errors
        $.each(errors, function(field, messages) {
            if (field !== '__all__' && field !== 'non_field_errors') {
                let errorString = messages.join('<br>');

                let inputField = $('#' + formName + '-form [name=' + field + ']');
                if (!inputField.length) {
                    // Use the class name if the name attribute is not available
                    inputField = $('.' + field);
                }

                let formRow = inputField.closest('.form-row');
                let errorContainer = formRow.prev('.form-error-row');

                if (!errorContainer.length) {
                    // Create the .form-error-row div and insert it before the .form-row
                    errorContainer = $('<div class="form-error-row"></div>').insertBefore(formRow);
                }
                // Populate the .form-error-row div with the error messages
                errorContainer.html('<span class="text-danger form-error">' + errorString + '</span>');
            }
        });
    }
    // Open the modal if it's not already open
    if (!$('#' + modalId).hasClass('show')) {
        $('#' + modalId).modal('show');
    }
}

$(document).ready(function() {
    // Initialize flatpickr with the current date for Add New Entity
    initializeDateTimeFlatpickr(new Date().setSeconds(0, 0));

    // Set a timeout to hide success message after 3 seconds
    setTimeout(function() {
        $('#messageContainer .alert').fadeOut('slow');
    }, 3000);

    // Check if the sessionStorage flag is set to show the toast for deleted observation
    if (sessionStorage.getItem('obsDeleted') === 'true') {
        obsToastEl.show();
        sessionStorage.removeItem('obsDeleted');
    }

    // Check if the sessionStorage flag is set to show the toast for deleted stance
    if (sessionStorage.getItem('stanceDeleted') === 'true') {
        stanceToastEl.show();
        sessionStorage.removeItem('stanceDeleted');
    }

    // Check for URL parameters to expand a specific observation
    const urlParams = new URLSearchParams(window.location.search);
    const expandObservation = urlParams.get('expandObservation');

    if(expandObservation){
        // Trigger the click event to expand the specified Observation
        $("#observation-" + expandObservation + " .clickable-row").click();

        // Scroll smoothly to the expanded Observation
        document.querySelector("#observation-" + expandObservation).scrollIntoView({
            behavior: 'smooth'
        });
    }
    else {
        // Scroll to #observations-table-title
        // Scroll smoothly to the expanded Observation
        document.querySelector("#observations-table-top").scrollIntoView({
            behavior: 'smooth'
        });
    }


    // Handle user clicking the #add-observation-button to display the modal
    $('#add-observation-button').click(function() {

        initializeDateTimeFlatpickr(new Date().setSeconds(0, 0));
        // Set the default values for the form fields
        $('#newObservationModal input[name="sessionDurationInMins"]').val('2');
        $('#newObservationModal select[name="isKong"]').val('N');

        // Adjust Italy-specific fields
        if (branch === 'Italy') {
            $('#newObservationModal select[name="isDog"]').val('N');
            $('#newObservationModal select[name="isHuman"]').val('N');
        }

        // Empty the csvFile field
        $('#newObservationModal input[name="csvFile"]').val('');
        $('#newObservationModal input[name="rawVideo"]').val('');

        //Empty the form errors
        $('.form-error-row').remove();
        $('.form-general-error').remove();
        $('#newObservationModal').modal('show');
    });

    // Handle the form submission
    $('#add-observation-form').submit(function(e) {
        e.preventDefault();

        let formData = new FormData(this);
        formData.append('form_type', 'add_observation'); // Add an identifier

        $.ajax({
            url: window.location.href,
            type: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success') {
                    $('#newObservationModal').modal('hide');
                    document.dispatchEvent(new CustomEvent('observationAdded'));

                } else {
                    // Display errors in the modal
                    displayErrors(response.errors, 'add-observation', 'newObservationModal');
                }
            },
            error: function(xhr, status, error) {
                // Check if the error is a 400 Bad Request (validation error)
                if (xhr.status === 400) {
                    displayErrors(xhr.responseJSON.errors, 'add-observation', 'newObservationModal');
                } else {
                    // Handle non-validation errors (e.g., network issues)
                    $('#newObservationModal').find('.modal-body').prepend('<div class="alert alert-danger form-add-observation-general-error" role="alert">An error occurred. Please try again.</div>');
                }
            }
        });
    });



    // Switch between dropdown and dropup icons when expanded or collapsed rows detected
    $(".clickable-row").click(function(event) {
        const expandIcon = $(this).find('i'); // Find the specific icon inside the clicked row
        expandIcon.toggleClass('fa-angle-down fa-angle-up');
    });

    // Handle the delete button click
    $(".delete-observation-btn").click(function(){
        var observationId = $(this).data('observation-id');
        $('#deleteObservationModal').data('observation-id', observationId);
        $('#deleteObservationModal').modal('show');
    });

    $('#confirmObservationDeleteBtn').click(function(){
        var observationId = $('#deleteObservationModal').data('observation-id');
        $('#deleteObservationModal').modal('hide');
        deleteObservation(observationId);
    });

    function deleteObservation(observationId) {
        var observationRow = $('#observation-' + observationId); // the main observation row
        var detailsRow = $('#stances-' + observationId); // the expandable details row

        // Check if details row is expanded
        if (detailsRow.hasClass('show')) {
            // If expanded, collapse it first
            detailsRow.collapse('hide');
            // Wait for the collapse to complete before deleting
            detailsRow.on('hidden.bs.collapse', function () {
                performDeletion(observationId);
                detailsRow.off('hidden.bs.collapse'); // Unbind the event
            });
        } else {
            // If it's not expanded, delete right away
            performDeletion(observationId);
        }
    }

    function performDeletion(observationId){
        var observationRow = $('#observation-' + observationId); // the main observation row
        var currentPage = new URLSearchParams(window.location.search).get('page') || 1;
        var expandObservation = new URLSearchParams(window.location.search).get('expandObservation');

        $.ajax({
            url: '/delete_observation/',
            type: 'post',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data: {
                observation_id: observationId,
                page_number: currentPage || 1,
            },
            success: function(response) {
                if(response.status == 'success'){
                    observationRow.remove();

                    var newUrl = window.location.pathname;
                    var queryParams = [];

                    // Remove expandObservation from URL if it matches the deleted observation
                    if (expandObservation && expandObservation != observationId.toString()) {
                        queryParams.push('expandObservation=' + expandObservation);
                    }

                    // If no observations left, move to the previous page if possible
                    if(!response.is_current_page_empty){
                        queryParams.push('page=' + currentPage);
                        observationRow.remove();
                    } else {
                        // If no observations left, move to the previous page if possible
                        var prevPage = currentPage > 1 ? currentPage - 1 : 1;
                        queryParams.push('page=' + prevPage);
                    }

                    // Construct the new URL
                    if (queryParams.length > 0) {
                        newUrl += '?' + queryParams.join('&');
                    }

                    // Set flag in the sessionStorage to show the toast
                    sessionStorage.setItem('obsDeleted', 'true');

                    window.location.href = newUrl;
                } else if (response.status == 'error') {
                    alert('Error: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                alert('Error: ' + response.message);
            }
        });
    }

    // Handle the edit Observation button click
    $(".edit-observation-btn").click(function(){
      var observationId = $(this).data('observation-id');

      //Empty the form errors
      $('.form-error-row').remove();
      $('.form-general-error').remove();

      // Fetch the current observation data
      $.ajax({
          url: '/edit_observation/' + observationId + '/',
          type: 'get',
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
          success: function(response) {
              if(response.status == 'success'){
                    // Populate the form fields with the current observation data
                    // Convert the obsDateTime to a JavaScript Date object

                    // Create a new Date object and set the seconds and milliseconds to 0
                    let obsDate = new Date(response.observation.obsDateTime);
                    obsDate.setSeconds(0, 0);
                    // Re-initialize flatpickr with the fetched date
                    initializeDateTimeFlatpickr(obsDate);

                    // Populate the form fields with the current observation data
                    $('#editObservationModal input[name="sessionDurationInMins"]').val(response.observation.sessionDurationInMins);
                    $('#editObservationModal select[name="isKong"]').val(response.observation.isKong);

                    // Empty the csvFile and video fields
                    $('#editObservationModal input[name="csvFile"]').val('');
                    $('#editObservationModal input[name="rawVideo"]').val('');

                    // Use the original CSV file name for display
                    let csvFileName = response.observation.original_csv_file_name;
                    // Use the file URL for the link's href attribute
                    let csvFileUrl = response.observation.csvFile;

                    // Check if both CSV fileName and fileUrl are not null
                    if (csvFileName && csvFileUrl) {
                        // Create a clickable link with the file name as text
                        $('#currentCSVFileName').html(`<a href="${csvFileUrl}" target="_blank">${csvFileName}</a>`);
                    } else {
                        // Handle case where there is no file (display a default message or leave blank)
                        $('#currentCSVFileName').text('No existing CSV file');
                    }

                    // Use the original Video file name for display
                    let videoFileName = response.observation.original_video_file_name;
                    // Use the file URL for the link's href attribute
                    let videoFileUrl = response.observation.rawVideo;

                    // Check if both video fileName and fileUrl are not null
                    if (videoFileName && videoFileUrl) {
                        // Create a clickable link with the file name as text
                        $('#currentVideoFileName').html(`<a href="${videoFileUrl}" target="_blank">${videoFileName}</a>`);
                    } else {
                        // Handle case where there is no file (display a default message or leave blank)
                        $('#currentVideoFileName').text('No existing video file');
                    }


                    // Adjust Italy-specific fields
                    if (branch === 'Italy') {
                        $('#editObservationModal select[name="isDog"]').val(response.observation.isDog);
                        $('#editObservationModal select[name="isHuman"]').val(response.observation.isHuman);
                    }

                    // Store the observation ID so it can be used when submitting the form
                    $('#editObservationModal').data('observation-id', observationId);

                    // Show the modal
                    $('#editObservationModal').modal('show');
              } else if (response.status == 'error') {
                  alert('Error: ' + response.message);
              }
          }
      });
    });

    $('#editObservationModal form').submit(function(e){
         e.preventDefault();
         var formData = new FormData(this);
         var observationId = $('#editObservationModal').data('observation-id');

         $.ajax({
             url: '/edit_observation/' + observationId + '/',
             type: 'post',
             headers: { 'X-CSRFToken': getCookie('csrftoken') },
             processData: false, // Important for FormData
             contentType: false, // Important for FormData
             data: formData,
             success: function(response) {
                if (response.status === 'success') {
                    $('#editObservationModal').modal('hide');
                    document.dispatchEvent(new CustomEvent('observationEdited'));

                } else {
                    // Display errors in the modal
                    displayErrors(response.errors, 'edit-observation', 'editObservationModal');
                }
            },
            error: function(xhr, status, error) {
                // Check if the error is a 400 Bad Request (validation error)
                if (xhr.status === 400) {
                    displayErrors(xhr.responseJSON.errors, 'edit-observation', 'editObservationModal');
                } else {
                    // Handle non-validation errors (e.g., network issues)
                    $('#editObservationModal').find('.modal-body').prepend('<div class="alert alert-danger form-edit-observation-general-error" role="alert">An error occurred. Please try again.</div>');
                }
            }
         });
    });

    // Handle the DogStance delete button click
    $(".delete-stance-btn").click(function(){
        var stanceId = $(this).data('stance-id');
        var observationId = $(this).data('observation-id'); // Get the observation id
        var currentPage = new URLSearchParams(window.location.search).get('page'); // Get current page number

        $('#deleteStanceModal').data('stance-id', stanceId);
        $('#deleteStanceModal').data('observation-id', observationId); // Store the observation_id
        $('#deleteStanceModal').data('current-page', currentPage); // Store current page number
        $('#deleteStanceModal').modal('show');
    });

    // Handle the DogStance delete button click
    $('#confirmStanceDeleteBtn').click(function(){
        var stanceId = $('#deleteStanceModal').data('stance-id');
        var observationId = $('#deleteStanceModal').data('observation-id'); // Retrieve the observation id
        var currentPage = $('#deleteStanceModal').data('current-page'); // Retrieve the current page number

        $('#deleteStanceModal').modal('hide');

        deleteStance(stanceId, observationId, currentPage);
    });

    function deleteStance(stanceId, observationId, currentPage){
        var stanceRow = $('#stance-' + stanceId); // the main stance row

        $.ajax({
            url: '/delete_stance/',
            type: 'post',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data: {
                stance_id: stanceId,
            },
            success: function(response) {
               if(response.status == 'success'){
                    // Construct URL with parameters for expanded observation and current page
                    var reloadUrl = window.location.pathname;
                    var queryParams = '?expandObservation=' + observationId;
                    if (currentPage) {
                        queryParams += '&page=' + currentPage;
                    }

                    // Set flag in the sessionStorage to show the toast
                    sessionStorage.setItem('stanceDeleted', 'true');

                    window.location.href = reloadUrl + queryParams;
               } else if (response.status == 'error') {
                     alert('Error: ' + response.message);
               }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert('Error: ' + response.message);
            }
       });
    }

    // Handle the DogStance edit button click
    $(".edit-stance-btn").click(function(){
        // Empty the form errors
        $('.form-error-row').remove();
        $('.form-general-error').remove();

       var stanceId = $(this).data('stance-id');

       $.ajax({
           url: '/edit_dog_stance/' + stanceId + '/',
           type: 'get',
           headers: { 'X-CSRFToken': getCookie('csrftoken') },
           success: function(response) {
               if(response.status == 'success'){

                    // Populate the flatpickr time-only picker with the current stanceStartTime
                    let hour = response.stance.stanceStartTime.split(':')[0];
                    let minute = response.stance.stanceStartTime.split(':')[1];
                    let second = response.stance.stanceStartTime.split(':')[2];
                    let time = new Date();
                    time.setHours(hour, minute, second, 0); // Set the time to the current stanceStartTime
                    initializeTimeFlatpickr(time);

                    // Populate the form fields with the current stance data
                    $('#editDogStanceModal select[name="dogStance"]').val(response.stance.dogStance);
                    $('#editDogStanceModal select[name="dogLocation"]').val(response.stance.dogLocation);

                    // Store the stance ID so it can be used when submitting the form
                    $('#editDogStanceModal').data('stance-id', stanceId);

                    // Show the modal
                    $('#editDogStanceModal').modal('show');

                    // Store the current page number for later use
                    var currentPage = new URLSearchParams(window.location.search).get('page');
                    $('#editDogStanceModal').data('current-page', currentPage);
               } else if (response.status == 'error') {
                     alert('Error: ' + response.message);
               }
           },
           error: function(jqXHR, textStatus, errorThrown) {
       console.log('AJAX Error: ' + textStatus + ', ' + errorThrown);
     }
       });
    });

    $('#editDogStanceModal form').submit(function(e){
       e.preventDefault();
       var formData = $(this).serialize();
       var stanceId = $('#editDogStanceModal').data('stance-id');
       var currentPage = $('#editDogStanceModal').data('current-page');

       $.ajax({
           url: '/edit_dog_stance/' + stanceId + '/',
           type: 'post',
           headers: { 'X-CSRFToken': getCookie('csrftoken') },
           data: formData,
           success: function(response) {
               if(response.status == 'success'){
                   // Reload the page with the observation expanded and the current page number
                   var reloadUrl = window.location.pathname;
                   var queryParams = '?expandObservation=' + response.observationId;
                   if (currentPage) {
                       queryParams += '&page=' + currentPage;
                   }
                   window.location.href = reloadUrl + queryParams;
               } else {
                    // Display errors in the modal
                    displayErrors(response.errors, 'edit-stance', 'editDogStanceModal');
                }
            },
            error: function(xhr, status, error) {
                // Check if the error is a 400 Bad Request (validation error)
                if (xhr.status === 400) {
                    displayErrors(xhr.responseJSON.errors, 'edit-stance', 'editDogStanceModal');
                } else {
                    // Handle non-validation errors (e.g., network issues)
                    $('#editDogStanceModal').find('.modal-body').prepend('<div class="alert alert-danger form-edit-stance-general-error" role="alert">An error occurred. Please try again.</div>');
                }
            }
       });
    });

});

function getCookie(name) {
   var cookieValue = null;
   if (document.cookie && document.cookie !== '') {
       var cookies = document.cookie.split(';');
       for (var i = 0; i < cookies.length; i++) {
           var cookie = jQuery.trim(cookies[i]);
           if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
   return cookieValue;
}

// Listen for the observationAdded success event
document.addEventListener('observationAdded', function() {
    // Check if messages are already present
    if (!$('#messageContainer').find('.alert').length) {
        // If not, create and append a success message
        var successMessage = $('<div class="alert alert-success alert-dismissible fade show text-center" role="alert">New observation added successfully!<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        $('#messageContainer').append(successMessage);
    }

    // Reload to update the table and display the Django message
    location.reload();
});

// Listen for the observationEdited success event
document.addEventListener('observationEdited', function() {
    // Check if messages are already present
    if (!$('#messageContainer').find('.alert').length) {
        // If not, create and append a success message
        var successMessage = $('<div class="alert alert-success alert-dismissible fade show text-center" role="alert">Observation has been edited successfully!<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        $('#messageContainer').append(successMessage);
    }

    // Reload to update the table and display the Django message
    location.reload();
});


// Add click listener to the Add Dog Stance button
$(".add-stance-btn").click(function() {
    // Empty Errors
    $('.form-error-row').remove();
    $('.form-general-error').remove();

    const observationId = $(this).data("observation-id");
    $("#observation_id").val(observationId);

    // Store the current page number
    var currentPage = new URLSearchParams(window.location.search).get('page');
    $("#addDogStanceModal").data('current-page', currentPage);

    // Initialize Flatpick Time picker for the stanceStartTime attribute in the form
    const defaultTime = new Date();
    defaultTime.setHours(0, 0, 0, 0); // Set the time to 00:00:00
    initializeTimeFlatpickr(defaultTime);
    // Set the default values for the form fields

    $('#addDogStanceModal select[name="dogStance"]').val('');
    $('#addDogStanceModal select[name="dogLocation"]').val('');
    $("#addDogStanceModal").modal('show');
});

// Handle form submission
$("#saveDogStanceBtn").click(function() {
    const formData = $("#add-stance-form").serialize() + "&form_type=dog_stance&observation_id=" + $("#observation_id").val();
    var currentPage = $("#addDogStanceModal").data('current-page'); // Retrieve the current page number

    $.post({
        url: window.location.href,
        data: formData,
        headers: { 'X-CSRFToken': '{{ csrf_token }}' },
        success: function(response) {
            if (response.status === "success") {

                // Construct URL with parameters for expanded observation and current page
                var reloadUrl = window.location.pathname;
                var queryParams = '?expandObservation=' + response.new_stance.observation;
                if (currentPage) {
                    queryParams += '&page=' + currentPage;
                }
                window.location.href = reloadUrl + queryParams;
            }
            else {
                // Display errors in the modal
                displayErrors(response.errors, 'add-stance', 'addDogStanceModal');
            }
        },
        error: function(xhr, status, error) {
            // Check if the error is a 400 Bad Request (validation error)
            if (xhr.status === 400) {
                displayErrors(xhr.responseJSON.errors, 'add-stance', 'addDogStanceModal');
            } else {
                // Handle non-validation errors (e.g., network issues)
                $('#addDogStanceModal').find('.modal-body').prepend('<div class="alert alert-danger form-add-stance-general-error" role="alert">An error occurred. Please try again.</div>');
            }
        }

    });
});

$(document).ready(function(){
    $('.dog-stance-table').each(function() {
        $(this).DataTable({
            "scrollCollapse": true,
            "pageLength": 8,
            "lengthMenu": [[5, 8, 10, 25, -1], [5, 8, 10, 25, "All"]],
            "autoWidth": false, // Disables auto width calculation
            "order": [[0, 'asc']],
            "stateSave": true,
            "language": {
                "emptyTable": "No Dog Activities found."
            },
            "columnDefs": [
                {
                    "targets": 3,
                    "orderable": false,
                    "searchable": false,
                    "className": "text-center"
                }
            ],
            "pagingType": "simple_numbers",
        });
    });
    $('.dataTables_length select').val('8');
});


document.addEventListener('DOMContentLoaded', (event) => {
    const modal = document.getElementById('videoModal');
    const modalBody = modal.querySelector('.modal-body-video');

    // Define a variable outside to hold the player instance
    let player;

    modal.addEventListener('hidden.bs.modal', function () {
        if (player) {
            player.destroy(); // Destroy the player instance
            player = null; // Set player to null to avoid memory leaks
        }
        modalBody.innerHTML = ''; // Clear the modal body
    });

    // Setup video when a link is clicked
    document.querySelectorAll('a[data-bs-toggle="modal"][data-video-url]').forEach(item => {
        item.addEventListener('click', event => {
            // Prevent default link behavior
            event.preventDefault();

            // Setup modal body with video
            const videoUrl = item.getAttribute('data-video-url');
            modalBody.innerHTML = `
                <div class="plyr__video-embed" id="player">
                    <video id="plyr-video-player" playsinline controls muted preload="auto">
                        <source src="${videoUrl}" type="video/mp4">
                    </video>
                </div>
            `;

            // Initialize or re-initialize Plyr
            player = new Plyr('#plyr-video-player', {
                muted: true,
                autoplay: true,
                hideControls: true,
                resetOnEnd: true,
                controls: ['play', 'progress', 'current-time', 'mute', 'volume', 'settings', 'pip', 'download', 'fullscreen'],
            });

            // Attempt to play the video
            player.play().catch(error => console.error("Autoplay was prevented.", error));
        });
    });
});
