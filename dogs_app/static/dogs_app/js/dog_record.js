// Initialize global variables to keep track of the current pages for pagination
let currentTreatmentPage = 1;
let currentExaminationPage = 1;
let currentPlacementPage = 1;
let currentSessionPage = 1;

// Handle "Back" button for returning to previous page
function goBack() {
    const referrer = document.referrer;
    if (referrer.includes('update_dog')) {
        window.location.href = '/dogs/';
    } else {
        window.history.back();
    }
}


// Handle updating the content of a table with the new page's data
function updateTableContent(tableSelector, data) {
    const $tableBody = $(tableSelector);
    $tableBody.empty();
    data.forEach(row => {
        $tableBody.append(row);
    });
}

// Updates the current pagination for one of the 4 tables
function updatePagination(paginationSelector, html) {
    const paginationElement = document.querySelector(paginationSelector);
    if (paginationElement) {
        paginationElement.innerHTML = html;
    }
}


// AJAX call for updating pagination for one of the 4 tables
function fetchTablePage(paramName, pageNumber) {
    $.ajax({
        url: window.location.pathname,
        data: {
            [paramName]: pageNumber
        },
        headers: { 'X-CSRFToken': '{{ csrf_token }}' },
        type: "GET",
        dataType: "json",
        success: function(response) {
            const navbarHeight = 50; // To account for Navbar when scrolling to top of the table
            if (paramName === "treatments_page") {
                currentTreatmentPage = pageNumber;
                updateTableContent("#treatments_table tbody", response.data);
                updatePagination("#treatments_table #pagination", response.pagination);
                smoothScrollWithOffset("#treatments_container", navbarHeight+15);
            } else if (paramName === "examinations_page") {
                currentExaminationPage = pageNumber;
                updateTableContent("#examinations_table tbody", response.data);
                updatePagination("#examinations_table #pagination", response.pagination);
                smoothScrollWithOffset("#examinations_container", navbarHeight);
            } else if (paramName === "placements_page") {
                currentPlacementPage = pageNumber;
                updateTableContent("#placements_table tbody", response.data);
                updatePagination("#placements_table #pagination", response.pagination);
                smoothScrollWithOffset("#placements_container", navbarHeight);
            } else if (paramName === "sessions_page") {
                currentSessionPage = pageNumber;
                updateTableContent("#sessions_table tbody", response.data);
                updatePagination("#sessions_table #pagination", response.pagination);
                smoothScrollWithOffset("#sessions_container", navbarHeight);
            }
        }
    });
}


// Function for smooth scrolling to the top of a table with offset to account for Navbar
function smoothScrollWithOffset(containerID, offset = 60) {
    const elementPosition = $(containerID).offset().top;
    const offsetPosition = elementPosition - offset;

    $('html, body').animate({
        scrollTop: offsetPosition
    }, 100);
}


// retrieve the CSRF token from the cookie and add it to the AJAX request header
function getCookie(name) {
   var cookieValue = null;
   if (document.cookie && document.cookie !== '') {
       var cookies = document.cookie.split(';');
       for (var i = 0; i < cookies.length; i++) {
           var cookie = cookies[i].trim();
           if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
   return cookieValue;
}


// Handle opening containers for the four tables below
$(document).ready(function(){
    // Check if user is returning from Observations page, make sure Sessions table is opened then scroll towards it
    const urlParams = new URLSearchParams(window.location.search);
    const fromObservations = urlParams.get('from');

    if (fromObservations === 'observations') {
        const sessionsContainer = $('#sessions_container');
        sessionsContainer.next().removeClass('hide');
        sessionsContainer.find('i').removeClass('fa-angle-down').addClass('fa-angle-up');

        // Scroll the page to bring the opened collapsible into view
        smoothScrollWithOffset("#sessions_container", 60);
    }


    var allContainers = [
        '#treatments_container',
        '#examinations_container',
        '#placements_container',
        '#sessions_container',
    ];

    // Function to check if all containers are visible or hidden
    var checkAllContainersState = function() {
        var allVisible = allContainers.every(function(container) {
            return !$(container).next().hasClass('hide');
        });

        var allHidden = allContainers.every(function(container) {
            return $(container).next().hasClass('hide');
        });

        if (allVisible) {
            $('#toggleTables').text('Collapse All');
        } else if (allHidden) {
            $('#toggleTables').text('Expand All');
        }
    }
    // Call the function immediately after defining it
    checkAllContainersState();


    // Setting the click event for image modal
    $('#imageModal').on('show.bs.modal', function (event) {
        var imgElement = document.querySelector('#dog_picture');
        var fullImageElement = document.querySelector('#fullImage');
        var dogNameElement = document.querySelector('#dogName');
        fullImageElement.setAttribute('src', imgElement.getAttribute('src'));
        dogNameElement.textContent = dogImageLoad;
    });

    // Setting the click event for all containers
    allContainers.forEach(function(container) {
        $(container).click(function() {
            $(this).next().toggleClass('hide');
            $(this).find('i').toggleClass('fa-angle-down fa-angle-up');
            checkAllContainersState();
        });
    });

    // Setting the click event for toggleTables
    $('#toggleTables').click(function(){
        var toggleState = $(this).text();

        if (toggleState === 'Expand All') {
            allContainers.forEach(function(container) {
                $(container).next().removeClass('hide');
                $(container).find('i').removeClass('fa-angle-down').addClass('fa-angle-up');
            });
            $(this).text('Collapse All');
        } else {
            allContainers.forEach(function(container) {
                $(container).next().addClass('hide');
                $(container).find('i').removeClass('fa-angle-up').addClass('fa-angle-down');
            });
            $(this).text('Expand All');
        }
    });

    // Handle user requesting to empty the expirationDate datefield in Placement modal
    $("#clearExpirationDate").on('click', function(e) {
        e.preventDefault();
        $("#id_expirationDate").val("");
    });
});

// Open the New Treatment/Examination/Placement/Session modal when the button for adding new entity is clicked
function showModalOnClick(buttonSelector, modalId) {
    document.querySelector(buttonSelector).addEventListener('click', function(event) {
        event.preventDefault();
        var modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    });
}

showModalOnClick('.new-treatment', 'addTreatmentModal');
showModalOnClick('.new-examination', 'addExaminationModal');
showModalOnClick('.new-placement', 'addPlacementModal');
showModalOnClick('.new-session', 'addSessionModal');


// Handle new form submissions, deletions and updating for the 4 tables
// Also activates Bootstrap Datepicker script for Date attributes
$(document).ready(function() {
    var date_input = $('[data-provide="datepicker"]');

    date_input.datepicker({
        format: 'yyyy-mm-dd',
        todayHighlight: true,
        autoclose: true,
    });

    // Force the datepicker to show on focus
    date_input.focus(function() {
        $(this).datepicker('show');
    });

    // Handle form submission for new Treatment/Examination/Placement/Session
    function handleFormSubmission(modalId, alertId, tableId, paginationId) {
        $(`${modalId} form`).submit(function(e) {
            e.preventDefault();

            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                success: function(data) {
                    // Close the modal after successful addition
                    $(modalId).modal('hide');

                    // Show success alert
                    $(alertId).show();

                    // Set a timer to hide the success alert after 5 seconds
                    setTimeout(function() {
                        $(alertId).hide();
                    }, 4000);

                    // Update the table with new data
                    updateTableContent(`${tableId} tbody`, data.data);

                    // Update pagination controls
                    updatePagination(`${paginationId}`, data.pagination);
                }

            });
        });
    }

    handleFormSubmission('#addTreatmentModal', '#treatments-success-alert', '#treatments_table', '#treatments_table #pagination');
    handleFormSubmission('#addExaminationModal', '#examinations-success-alert', '#examinations_table', '#examinations_table #pagination');
    handleFormSubmission('#addPlacementModal', '#placements-success-alert', '#placements_table', '#placements_table #pagination');
    handleFormSubmission('#addSessionModal', '#sessions-success-alert', '#sessions_table', '#sessions_table #pagination');


    // Handle deletion of a Treatment/Examination/Placement/Session entity
    function handleEntityDeletion(entityName, entityId, modalId, confirmButtonId) {
        $(document).on('click', '.delete-' + entityName + '-btn', function() {
            var entityIdValue = $(this).data(entityName + "-id");
            $("#" + modalId).modal('show');
            $("#" + confirmButtonId).data(entityName + "-id", entityIdValue);
        });

        // Handle confirmation of deletion
        $(document).on('click', '#' + confirmButtonId, function() {
            var entityIdValue = $(this).data(entityName + "-id");
            var deleteUrl = '/delete_' + entityName + '/' + entityIdValue + '/';
            var csrftoken = getCookie('csrftoken');

            $.ajax({
                url: deleteUrl,
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                data: {
                    _method: 'DELETE'
                },success: function() {
                    $("#" + modalId).modal('hide');

                    // Update Page variable for current page
                    let currentPage = 1;
                    switch (entityName) {
                    case 'treatment':
                        currentPage = currentTreatmentPage;
                        break;
                    case 'examination':
                        currentPage = currentExaminationPage;
                        break;
                    case 'placement':
                        currentPage = currentPlacementPage;
                        break;
                    case 'session':
                        currentPage = currentSessionPage;
                        break;
                    }
                    fetchTablePage(entityName + 's_page', currentPage);
                }
            });
        });
    }

    handleEntityDeletion('treatment', 'treatmentId', 'deleteTreatmentModal', 'confirmTreatmentDeleteBtn');
    handleEntityDeletion('examination', 'examinationId', 'deleteExaminationModal', 'confirmExaminationDeleteBtn');
    handleEntityDeletion('placement', 'placementId', 'deletePlacementModal', 'confirmPlacementDeleteBtn');
    handleEntityDeletion('session', 'sessionId', 'deleteSessionModal', 'confirmSessionDeleteBtn');


    // Handle updating of a Treatment
    // Function to open the Edit Treatment Modal and populate it with data
    function openTreatmentEditModal(treatmentId) {
        // Fetch the treatment data using AJAX
        $.ajax({
            url: '/edit_treatment/' + treatmentId + '/',
            method: 'GET',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                // Populate the form fields with the treatment details
                $('#editTreatmentModal input[name="treatmentName"]').val(response.treatmentName);
                $('#editTreatmentModal input[name="treatmentDate"]').val(response.treatmentDate);
                $('#editTreatmentModal input[name="treatedBy"]').val(response.treatedBy);
                $('#editTreatmentModal textarea[name="comments"]').val(response.comments);

                // Store the treatment ID in the submit button for later reference
                $('#editTreatmentModal .edit-treatment-confirm-btn').data('treatment-id', treatmentId);

                // Show the modal
                $('#editTreatmentModal').modal('show');
            }
        });
    }

    // Attach event listener to each Edit button in the treatments table
    $(document).on('click', '.edit-treatment-btn', function() {
        var treatmentId = $(this).data('treatment-id');
        openTreatmentEditModal(treatmentId);
    });

    // Submit handler for Edit Treatment Modal
    $('#editTreatmentModal .edit-treatment-confirm-btn').click(function(e) {
        e.preventDefault();

        var treatmentId = $(this).data('treatment-id');  // Retrieve the treatment ID stored earlier
        var $form = $('#editTreatmentModal form');  // Get the form inside the modal

        // Remove existing error spans
        $('.error').remove();

        // Send the updated treatment data to the server via AJAX
        $.ajax({
            url: '/edit_treatment/' + treatmentId + '/',
            method: 'POST',
            data: $form.serialize(),  // Serialize form data for submission
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                if (response.status === 'success') {
                    // Hide the modal
                    $('#editTreatmentModal').modal('hide');

                    // Reset the form
                    $form[0].reset();

                    // Refresh the treatments table to show the updated data
                    fetchTablePage('treatments_page', currentTreatmentPage);


                } else {
                   // Display error messages
                   for (var field in response.errors) {
                      var errorMessage = response.errors[field];
                      $('#editTreatmentModal input[name="' + field + '"]').after('<span class="error">' + errorMessage + '</span>');
                   }
                }
            }
        });
    });


    // Handle updating of an Examination
    // Function to open the Edit Examination Modal and populate it with data
    function openExaminationEditModal(examinationId) {
        // Fetch the examination data using AJAX
        $.ajax({
            url: '/edit_examination/' + examinationId + '/',
            method: 'GET',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                // Populate the form fields with the examination details
                $('#editExaminationModal input[name="examinationDate"]').val(response.examinationDate);
                $('#editExaminationModal input[name="examinedBy"]').val(response.examinedBy);
                $('#editExaminationModal input[name="results"]').val(response.results);
                $('#editExaminationModal input[name="dogWeight"]').val(response.dogWeight);
                $('#editExaminationModal input[name="dogTemperature"]').val(response.dogTemperature);
                $('#editExaminationModal input[name="dogPulse"]').val(response.dogPulse);
                $('#editExaminationModal textarea[name="comments"]').val(response.comments);

                // Store the examination ID in the submit button for later reference
                $('#editExaminationModal .edit-examination-confirm-btn').data('examination-id', examinationId);

                // Show the modal
                $('#editExaminationModal').modal('show');
            }
        });
    }

    // Attach event listener to each Edit button in the examinations table
    $(document).on('click', '.edit-examination-btn', function() {
        var examinationId = $(this).data('examination-id');
        openExaminationEditModal(examinationId);
    });

    // Submit handler for Edit Examination Modal
    $('#editExaminationModal .edit-examination-confirm-btn').click(function(e) {
        e.preventDefault();

        var examinationId = $(this).data('examination-id');  // Retrieve the examination ID stored earlier
        var $form = $('#editExaminationModal form');  // Get the form inside the modal

        // Remove existing error spans
        $('.error').remove();

        // Send the updated examination data to the server via AJAX
        $.ajax({
            url: '/edit_examination/' + examinationId + '/',
            method: 'POST',
            data: $form.serialize(),  // Serialize form data for submission
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                if (response.status === 'success') {
                    // Hide the modal
                    $('#editExaminationModal').modal('hide');

                    // Reset the form
                    $form[0].reset();

                    // Refresh the examination table to show the updated data
                    fetchTablePage('examinations_page', currentExaminationPage);


                } else {
                   // Display error messages
                   for (var field in response.errors) {
                      var errorMessage = response.errors[field];
                      $('#editExaminationModal input[name="' + field + '"]').after('<span class="error">' + errorMessage + '</span>');
                   }
                }
            }
        });
    });

    // Handle updating of a DogPlacement
    // Function to open the Edit Placement Modal and populate it with data
    function openPlacementEditModal(placementId) {
        // Fetch the placement data using AJAX
        $.ajax({
            url: '/edit_placement/' + placementId + '/',
            method: 'GET',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                // Populate the form fields with the placement details
                // Parse the kennel string into a JavaScript object
                var kennel = JSON.parse(response.kennel)[0];

                // Extract the pk from the kennel object
                var kennelId = kennel.pk;

                // Populate the form fields with the placement details
                $('#editPlacementModal select[name="kennel"]').val(kennelId);
                $('#editPlacementModal input[name="entranceDate"]').val(response.entranceDate);
                $('#editPlacementModal input[name="expirationDate"]').val(response.expirationDate);
                $('#editPlacementModal input[name="placementReason"]').val(response.placementReason);

                // Store the placement ID in the submit button for later reference
                $('#editPlacementModal .edit-placement-confirm-btn').data('placement-id', placementId);

                // Show the modal
                $('#editPlacementModal').modal('show');
            }
        });
    }

    // Attach event listener to each Edit button in the placement table
    $(document).on('click', '.edit-placement-btn', function() {
        var placementId = $(this).data('placement-id');
        openPlacementEditModal(placementId);
    });

    // Submit handler for Edit Placement Modal
    $('#editPlacementModal .edit-placement-confirm-btn').click(function(e) {
        e.preventDefault();

        var placementId = $(this).data('placement-id');  // Retrieve the placement ID stored earlier
        var $form = $('#editPlacementModal form');  // Get the form inside the modal

        // Remove existing error spans
        $('.error').remove();

        // Send the updated placement data to the server via AJAX
        $.ajax({
            url: '/edit_placement/' + placementId + '/',
            method: 'POST',
            data: $form.serialize(),  // Serialize form data for submission
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                if (response.status === 'success') {
                    // Hide the modal
                    $('#editPlacementModal').modal('hide');

                    // Reset the form
                    $form[0].reset();

                    // Refresh the placement table to show the updated data
                    fetchTablePage('placements_page', currentPlacementPage);

                } else {
                   // Display error messages
                   for (var field in response.errors) {
                       var errorMessage = response.errors[field];

                       // Get the element
                       var $element = $('#editPlacementModal [name="' + field + '"]');

                       // Check the tag name of the element
                       switch ($element.prop('tagName')) {
                           case 'SELECT':
                               $element.after('<span class="error">' + errorMessage + '</span>');
                               break;
                           case 'INPUT':
                               $element.after('<span class="error">' + errorMessage + '</span>');
                               break;
                           case 'TEXTAREA':
                               $element.after('<span class="error">' + errorMessage + '</span>');
                               break;
                           default:
                               console.log('Unknown field type: ' + $element.prop('tagName'));
                               break;
                       }
                   }
                }
            }
        });
    });

    // Handle updating of a Session (Observes)
    // Function to open the Edit Session Modal and populate it with data
    function openSessionEditModal(sessionId) {
        // Fetch the session data using AJAX
        $.ajax({
            url: '/edit_session/' + sessionId + '/',
            method: 'GET',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                // Populate the form fields with the session details
                // Parse the camera string into a JavaScript object
                var camera = JSON.parse(response.camera)[0];

                // Extract the pk from the camera object
                var cameraId = camera.pk;

                // Populate the form fields with the session details
                $('#editSessionModal select[name="camera"]').val(cameraId);
                $('#editSessionModal input[name="sessionDate"]').val(response.sessionDate);
                $('#editSessionModal textarea[name="comments"]').val(response.comments);

                // Store the session ID in the submit button for later reference
                $('#editSessionModal .edit-session-confirm-btn').data('session-id', sessionId);

                // Show the modal
                $('#editSessionModal').modal('show');
            }
        });
    }

    // Attach event listener to each Edit button in the session table
    $(document).on('click', '.edit-session-btn', function() {
        var sessionId = $(this).data('session-id');
        openSessionEditModal(sessionId);
    });

    // Submit handler for Edit Session Modal
    $('#editSessionModal .edit-session-confirm-btn').click(function(e) {
        e.preventDefault();

        var sessionId = $(this).data('session-id');  // Retrieve the session ID stored earlier
        var $form = $('#editSessionModal form');  // Get the form inside the modal

        // Remove existing error spans
        $('.error').remove();

        // Send the updated session data to the server via AJAX
        $.ajax({
            url: '/edit_session/' + sessionId + '/',
            method: 'POST',
            data: $form.serialize(),  // Serialize form data for submission
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                if (response.status === 'success') {
                    // Hide the modal
                    $('#editSessionModal').modal('hide');

                    // Reset the form
                    $form[0].reset();

                    // Refresh the session table to show the updated data
                    fetchTablePage('sessions_page', currentSessionPage);

                } else {
                   // Display error messages
                   for (var field in response.errors) {
                       var errorMessage = response.errors[field];

                       // Get the element
                       var $element = $('#editSessionModal [name="' + field + '"]');

                       // Check the tag name of the element
                       switch ($element.prop('tagName')) {
                           case 'SELECT':
                               $element.after('<span class="error">' + errorMessage + '</span>');
                               break;
                           case 'INPUT':
                               $element.after('<span class="error">' + errorMessage + '</span>');
                               break;
                           case 'TEXTAREA':
                               $element.after('<span class="error">' + errorMessage + '</span>');
                               break;
                           default:
                               console.log('Unknown field type: ' + $element.prop('tagName'));
                               break;
                       }
                   }
                }
            }
        });
    });

    // Handle updating of an Examination
    // Function to open the Edit Examination Modal and populate it with data
    function openExaminationEditModal(examinationId) {
        // Fetch the examination data using AJAX
        $.ajax({
            url: '/edit_examination/' + examinationId + '/',
            method: 'GET',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                // Populate the form fields with the examination details
                $('#editExaminationModal input[name="examinationDate"]').val(response.examinationDate);
                $('#editExaminationModal input[name="examinedBy"]').val(response.examinedBy);
                $('#editExaminationModal input[name="results"]').val(response.results);
                $('#editExaminationModal input[name="dogWeight"]').val(response.dogWeight);
                $('#editExaminationModal input[name="dogTemperature"]').val(response.dogTemperature);
                $('#editExaminationModal input[name="dogPulse"]').val(response.dogPulse);
                $('#editExaminationModal textarea[name="comments"]').val(response.comments);

                // Store the examination ID in the submit button for later reference
                $('#editExaminationModal .edit-examination-confirm-btn').data('examination-id', examinationId);

                // Show the modal
                $('#editExaminationModal').modal('show');
            }
        });
    }

    // Attach event listener to each Edit button in the examinations table
    $(document).on('click', '.edit-examination-btn', function() {
        var examinationId = $(this).data('examination-id');
        openExaminationEditModal(examinationId);
    });

    // Submit handler for Edit Examination Modal
    $('#editExaminationModal .edit-examination-confirm-btn').click(function(e) {
        e.preventDefault();

        var examinationId = $(this).data('examination-id');  // Retrieve the examination ID stored earlier
        var $form = $('#editExaminationModal form');  // Get the form inside the modal

        // Remove existing error spans
        $('.error').remove();

        // Send the updated examination data to the server via AJAX
        $.ajax({
            url: '/edit_examination/' + examinationId + '/',
            method: 'POST',
            data: $form.serialize(),  // Serialize form data for submission
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                if (response.status === 'success') {
                    // Hide the modal
                    $('#editExaminationModal').modal('hide');

                    // Reset the form
                    $form[0].reset();

                    // Refresh the examination table to show the updated data
                    fetchTablePage('examinations_page', currentExaminationPage);


                } else {
                   // Display error messages
                   for (var field in response.errors) {
                      var errorMessage = response.errors[field];
                      $('#editExaminationModal input[name="' + field + '"]').after('<span class="error">' + errorMessage + '</span>');
                   }
                }
            }
        });
    });

    // Handle updating of an Owner
    // Function to open the Edit Owner Modal and populate it with data
    function openOwnerEditModal(ownerId) {
        // Fetch the placement data using AJAX
        $.ajax({
            url: '/edit_owner/' + ownerId + '/',
            method: 'GET',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                // Populate the form fields with the owner details
                $('#editOwnerModal input[name="firstName"]').val(response.firstName);
                $('#editOwnerModal input[name="lastName"]').val(response.lastName);
                $('#editOwnerModal input[name="ownerID"]').val(response.ownerID);
                $('#editOwnerModal input[name="ownerAddress"]').val(response.ownerAddress);
                $('#editOwnerModal input[name="city"]').val(response.city);
                $('#editOwnerModal input[name="phoneNum"]').val(response.phoneNum);
                $('#editOwnerModal input[name="cellphoneNum"]').val(response.cellphoneNum);
                $('#editOwnerModal textarea[name="comments"]').val(response.comments);

                // Store the owner ID in the submit button for later reference
$('#editOwnerModal .edit-owner-confirm-btn').attr('data-owner-id', ownerId);

                // Show the modal
                $('#editOwnerModal').modal('show');
            }
        });
    }

    // Attach event listener to the Edit button in the owner table
    $(document).on('click', '.edit-owner-btn', function() {
        var ownerId = $(this).data('owner-id');
        openOwnerEditModal(ownerId);
    });

    // Submit handler for Edit Owner Modal
    $('#editOwnerModal .edit-owner-confirm-btn').click(function(e) {
        e.preventDefault();

        var ownerId = $(this).data('owner-id');  // Retrieve the owner ID stored earlier
        var $form = $('#editOwnerModal form');  // Get the form inside the modal

        // Remove existing error spans
        $('.error').remove();

        // Send the updated owner data to the server via AJAX
        $.ajax({
            url: '/edit_owner/' + ownerId + '/',
            method: 'POST',
            data: $form.serialize(),  // Serialize form data for submission
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(response) {
                if (response.status === 'success') {
                // Set a flag in sessionStorage before reloading
                sessionStorage.setItem('ownerEditSuccess', 'true');

                // Reload the page
                location.reload();

                } else {
                    // Display error messages
                    for (var field in response.errors) {
                       if (field === '__all__') {
                           // Handle the general error message
                           $('.general-error').text(response.errors[field]);
                       } else {
                           // Handle field-specific error messages
                           var errorMessage = response.errors[field];
                           $('#editOwnerModal input[name="' + field + '"]').after('<span class="error">' + errorMessage + '</span>');
                       }
                    }

                }
            }
        });
    });

    // Check if the Owner Editing form was successfully submitted, open Owner details if so
    if (sessionStorage.getItem('ownerEditSuccess') === 'true') {
        // Trigger the click event on the #owner-button
        $("#owner-button").click();

        // Clear the flag immediately
        sessionStorage.removeItem('ownerEditSuccess');
    }

    // Disable all error messages after closing modals
    $('#editSessionModal, #editTreatmentModal, #editExaminationModal, #editPlacementModal, #editOwnerModal').on('hidden.bs.modal', function () {
        $('.error').remove();
    });

});
