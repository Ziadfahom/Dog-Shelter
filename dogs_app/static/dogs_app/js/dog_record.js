// Initialize global variables to keep track of the current pages for pagination
let currentTreatmentPage = (userIsVet === true) ? 1 : null;
let currentExaminationPage = (userIsVet === true) ? 1 : null;
let currentPlacementPage = (userIsVet === true) ? 1 : null;
let currentSessionPage = (userIsVet === true) ? 1 : null;


// Return HeatmapLegend depending on user permissions
function getHeatmapLegend() {
    if (userIsVet === true) {
        return document.getElementById('heatmap-legend');
    }
    else {
        return null;
    }
}

// Hold the heatmap legend for hiding and showing (depending on user permissions)
const heatmapLegend = getHeatmapLegend();

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

    if (fromObservations === 'observations' && userIsVet === true) {
        const sessionsContainer = $('#sessions_container');
        sessionsContainer.next().removeClass('hide');
        sessionsContainer.find('i').removeClass('fa-angle-down').addClass('fa-angle-up');

        // Scroll the page to bring the opened collapsible into view
        smoothScrollWithOffset("#sessions_container", 60);
    }


    var allContainers = (userIsVet === true) ? [
        '#treatments_container',
        '#examinations_container',
        '#placements_container',
        '#sessions_container',
    ] : [];

    // Function to check if all containers are visible or hidden
    var checkAllContainersState = function() {
        var allVisible = allContainers.every(function(container) {
            return !$(container).next().hasClass('hide');
        });

        var allHidden = allContainers.every(function(container) {
            return $(container).next().hasClass('hide');
        });

        if (allVisible) {
            $('#toggleTables').html('Collapse All ' + doubleUpIcon);
        } else if (allHidden) {
            $('#toggleTables').html('Expand All ' + doubleDownIcon);
        }

    }
    if (userIsVet === true) {
        // Call the function immediately after defining it if the user has permissions to view the data
        checkAllContainersState();
    }

    // Setting the click event for image modal
    $('#imageModal').on('show.bs.modal', function (event) {
        var imgElement = document.querySelector('#dog_picture');
        var fullImageElement = document.querySelector('#fullImage');
        var dogNameElement = document.querySelector('#dogName');
        fullImageElement.setAttribute('src', imgElement.getAttribute('src'));
        dogNameElement.textContent = dogImageLoad;
    });

    if (userIsVet === true) {
        // Setting the click event for all containers
        allContainers.forEach(function (container) {
            $(container).click(function () {
                $(this).next().toggleClass('hide');
                $(this).find('i').toggleClass('fa-angle-down fa-angle-up');
                checkAllContainersState();
            });
        });


        $('#toggleTables').click(function () {
            var hasDownIcon = $(this).find('.fa-angle-double-down').length > 0;

            if (hasDownIcon) {
                allContainers.forEach(function (container) {
                    $(container).next().removeClass('hide');
                    $(container).find('i').removeClass('fa-angle-down').addClass('fa-angle-up');
                });
                $(this).html('Collapse All ' + doubleUpIcon);
            } else {
                allContainers.forEach(function (container) {
                    $(container).next().addClass('hide');
                    $(container).find('i').removeClass('fa-angle-up').addClass('fa-angle-down');
                });
                $(this).html('Expand All ' + doubleDownIcon);
            }
        });


        // Handle user requesting to empty the expirationDate datefield in Placement modal
        $("#clearExpirationDate").on('click', function (e) {
            e.preventDefault();
            $("#id_expirationDate").val("");
        });
    }

});

// Open the New Treatment/Examination/Placement/Session modal when the button for adding new entity is clicked
function showModalOnClick(buttonSelector, modalId) {
    document.querySelector(buttonSelector).addEventListener('click', function(event) {
        event.preventDefault();
        var modalElement = document.getElementById(modalId);
        var modal = new bootstrap.Modal(modalElement);

        // Reset the form
        var form = modalElement.querySelector('form');
        if (form) {
            form.reset();
        }

        // Clear existing error messages
        var errorMessages = modalElement.querySelectorAll('.error');
        errorMessages.forEach(function(error) {
            error.remove();
        });

        modal.show();
    });
}
if (userIsVet === true) {
    showModalOnClick('.new-treatment', 'addTreatmentModal');
    showModalOnClick('.new-examination', 'addExaminationModal');
    showModalOnClick('.new-placement', 'addPlacementModal');
    showModalOnClick('.new-session', 'addSessionModal');
    }


// Handle new form submissions, deletions and updating for the 4 tables
// Also activates Bootstrap Datepicker script for Date attributes
$(document).ready(function() {
    if (userIsVet === true) {
        var date_input = $('[data-provide="datepicker"]');

        date_input.datepicker({
            format: 'yyyy-mm-dd',
            todayHighlight: true,
            autoclose: true,
        });

        // Force the datepicker to show on focus
        date_input.focus(function () {
            $(this).datepicker('show');
        });
    }

    // Handle form submission for new Treatment/Examination/Placement/Session
    function handleFormSubmission(modalId, alertId, tableId, paginationId) {
        $(`${modalId} form`).submit(function(e) {
            e.preventDefault();

            // Clear existing error messages
            $(`${modalId} .error`).remove();

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
                },
                error: function(xhr) {
                    // First, parse the JSON string to get the error object
                    var response = JSON.parse(xhr.responseText);

                    var errors = JSON.parse(response.errors);
                    // Check and handle form-wide errors
                    if (errors['__all__']) {
                        $(`${modalId} .form-general-error`).html('<span class="error">' + errors['__all__'][0].message + '</span>');
                    }

                    else {
                        // Iterate over field errors
                        for (var field in errors) {
                            // Check if the error message is an array and get the first message
                            var errorMessage = Array.isArray(errors[field]) ? errors[field][0].message : errors[field];
                            $(`${modalId} input[name="${field}"], ${modalId} textarea[name="${field}"]`).after('<span class="error">' + errorMessage + '</span>');
                        }
                    }

                }
            });
        });
    }
    if (userIsVet === true) {
        handleFormSubmission('#addTreatmentModal', '#treatments-success-alert', '#treatments_table', '#treatments_table #pagination');
        handleFormSubmission('#addExaminationModal', '#examinations-success-alert', '#examinations_table', '#examinations_table #pagination');
        handleFormSubmission('#addPlacementModal', '#placements-success-alert', '#placements_table', '#placements_table #pagination');
        handleFormSubmission('#addSessionModal', '#sessions-success-alert', '#sessions_table', '#sessions_table #pagination');
    }

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

    if (userIsVet === true) {
        handleEntityDeletion('treatment', 'treatmentId', 'deleteTreatmentModal', 'confirmTreatmentDeleteBtn');
        handleEntityDeletion('examination', 'examinationId', 'deleteExaminationModal', 'confirmExaminationDeleteBtn');
        handleEntityDeletion('placement', 'placementId', 'deletePlacementModal', 'confirmPlacementDeleteBtn');
        handleEntityDeletion('session', 'sessionId', 'deleteSessionModal', 'confirmSessionDeleteBtn');
    }

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

    if (userIsVet === true) {
        // Attach event listener to each Edit button in the treatments table
        $(document).on('click', '.edit-treatment-btn', function () {
            var treatmentId = $(this).data('treatment-id');
            openTreatmentEditModal(treatmentId);
        });


        // Submit handler for Edit Treatment Modal
        $('#editTreatmentModal .edit-treatment-confirm-btn').click(function (e) {
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
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                success: function (response) {
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
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                success: function (response) {
                    // Populate the form fields with the examination details
                    $('#editExaminationModal input[name="examinationDate"]').val(response.examinationDate);
                    $('#editExaminationModal input[name="examinedBy"]').val(response.examinedBy);
                    $('#editExaminationModal textarea[name="results"]').val(response.results);
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
        $(document).on('click', '.edit-examination-btn', function () {
            var examinationId = $(this).data('examination-id');
            openExaminationEditModal(examinationId);
        });

        // Submit handler for Edit Examination Modal
        $('#editExaminationModal .edit-examination-confirm-btn').click(function (e) {
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
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                success: function (response) {
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
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                success: function (response) {
                    // Populate the form fields with the placement details
                    // Parse the kennel string into a JavaScript object
                    var kennel = JSON.parse(response.kennel)[0];

                    // Extract the pk from the kennel object
                    var kennelId = kennel.pk;

                    // Populate the form fields with the placement details
                    $('#editPlacementModal select[name="kennel"]').val(kennelId);
                    $('#editPlacementModal input[name="entranceDate"]').val(response.entranceDate);
                    $('#editPlacementModal input[name="expirationDate"]').val(response.expirationDate);
                    $('#editPlacementModal textarea[name="placementReason"]').val(response.placementReason);

                    // Store the placement ID in the submit button for later reference
                    $('#editPlacementModal .edit-placement-confirm-btn').data('placement-id', placementId);

                    // Show the modal
                    $('#editPlacementModal').modal('show');
                }
            });
        }

        // Attach event listener to each Edit button in the placement table
        $(document).on('click', '.edit-placement-btn', function () {
            var placementId = $(this).data('placement-id');
            openPlacementEditModal(placementId);
        });

        // Submit handler for Edit Placement Modal
        $('#editPlacementModal .edit-placement-confirm-btn').click(function (e) {
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
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                success: function (response) {
                    if (response.status === 'success') {
                        // Hide the modal
                        $('#editPlacementModal').modal('hide');

                        // Reset the form
                        $form[0].reset();

                        // Refresh the placement table to show the updated data
                        fetchTablePage('placements_page', currentPlacementPage);

                    } else {
                        if (response.errors['__all__']) {
                            // Handle non-specific form errors
                            $('#editPlacementModal .form-general-error').html('<span class="error">' + response.errors['__all__'] + '</span>');
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
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                success: function (response) {
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
        $(document).on('click', '.edit-session-btn', function () {
            var sessionId = $(this).data('session-id');
            openSessionEditModal(sessionId);
        });

        // Submit handler for Edit Session Modal
        $('#editSessionModal .edit-session-confirm-btn').click(function (e) {
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
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                success: function (response) {
                    if (response.status === 'success') {
                        // Hide the modal
                        $('#editSessionModal').modal('hide');

                        // Reset the form
                        $form[0].reset();

                        // Refresh the session table to show the updated data
                        fetchTablePage('sessions_page', currentSessionPage);

                    } else {
                        if (response.errors['__all__']) {
                            // Handle non-specific form errors
                            $('#editSessionModal .form-general-error').html('<span class="error">' + response.errors['__all__'] + '</span>');
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
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                success: function (response) {
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
        $(document).on('click', '.edit-owner-btn', function () {
            var ownerId = $(this).data('owner-id');
            openOwnerEditModal(ownerId);
        });

        // Submit handler for Edit Owner Modal
        $('#editOwnerModal .edit-owner-confirm-btn').click(function (e) {
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
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                success: function (response) {
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
    }

});


if (userIsVet === true) {
// Load Summary Heatmap Chart
    document.addEventListener('DOMContentLoaded', function () {
        const chartContainer = document.getElementById('chart-data');
        const allHeatmapData = JSON.parse(chartContainer.getAttribute('data-daily-heatmap'));
        const yearSelector = document.getElementById('year-selector');
        const weeklyHeatmapData = JSON.parse(chartContainer.getAttribute('data-weekly-heatmap'));
        const granularitySelector = document.getElementById('granularity-selector');
        const iconsSelector = document.getElementById('detailed-check-box');
        const prevYearButton = document.getElementById('prev-year');
        const nextYearButton = document.getElementById('next-year');


        // Function to update the button states based on the current year selection
        function updateButtonStates() {
            const currentYearIndex = Array.from(yearSelector.options).findIndex(option => option.value === yearSelector.value);
            prevYearButton.disabled = currentYearIndex === 0;
            nextYearButton.disabled = currentYearIndex === yearSelector.options.length - 1;
        }

        // Populate year dropdown and set default selection
        const defaultYear = Object.keys(allHeatmapData).pop(); // Gets the last (most recent) year
        Object.keys(allHeatmapData).forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.text = year;
            yearSelector.appendChild(option);
            if (year === defaultYear) {
                yearSelector.value = year; // Set default selection
            }
        });
        updateButtonStates(); // Update button states based on the default year


        // Hide all the elements above the chart if there is no data
        if (allHeatmapData[yearSelector.value].length === 0) {
            const yearLabel = document.getElementsByClassName('year-label')[0];
            const granularityLabel = document.getElementsByClassName('granularity-label')[0];
            const iconsLabel = document.getElementsByClassName('icons-label')[0];
            yearLabel.style.display = 'none';
            granularityLabel.style.display = 'none';
            iconsLabel.style.display = 'none';
            yearSelector.style.display = 'none';
            granularitySelector.style.display = 'none';
            iconsSelector.style.display = 'none';
            prevYearButton.style.display = 'none';
            nextYearButton.style.display = 'none';
        }

        // Function to create a full grid of days and months for a year with zero counts
        function createFullYearGrid(year, firstDate, lastDate, granularity) {
            const isLeapYear = new Date(year, 1, 29).getMonth() === 1;
            const daysInMonth = [31, isLeapYear ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
            const grid = [];
            for (let month = 0; month < 12; month++) {
                if (granularity === 'daily' && branch === 'Italy') {
                    for (let day = 0; day < daysInMonth[month]; day++) {
                        const currentDate = new Date(year, month, day + 1);
                        if (currentDate >= firstDate && currentDate <= lastDate) {
                            // Day, Month, Count, isKong Count, isDog Count, isHuman Count, No Stances Count
                            grid.push([day, month, 0, 0, 0, 0, 0]);
                        }
                    }
                } else if (granularity === 'daily' && branch !== 'Italy') {
                    for (let day = 0; day < daysInMonth[month]; day++) {
                        const currentDate = new Date(year, month, day + 1);
                        if (currentDate >= firstDate && currentDate <= lastDate) {
                            // Day, Month, Count, isKong Count
                            grid.push([day, month, 0, 0]);
                        }
                    }
                } else if (granularity === 'weekly' && branch === 'Italy') {
                    for (let week = 0; week < 5; week++) {
                        const currentDateStart = new Date(year, month, (week * 7) + 1);
                        const currentDateEnd = new Date(year, month, (week * 7) + 7);
                        if (currentDateEnd >= firstDate && currentDateStart <= lastDate) {
                            if (!isLeapYear && month === 1 && week === 4) {
                                // Do Not Add 5th week for February in leap years
                                break;
                            }
                            // Week, Month, Count, isKong Count, isDog Count, isHuman Count, No Stances Count
                            grid.push([week, month, 0, 0, 0, 0, 0]);
                        }
                    }
                } else if (granularity === 'weekly' && branch !== 'Italy') {
                    for (let week = 0; week < 5; week++) {
                        const currentDateStart = new Date(year, month, (week * 7) + 1);
                        const currentDateEnd = new Date(year, month, (week * 7) + 7);
                        if (currentDateEnd >= firstDate && currentDateStart <= lastDate) {
                            if (!isLeapYear && month === 1 && week === 4) {
                                // Do Not Add 5th week for February in leap years
                                break;
                            }
                            // Week, Month, Count, isKong Count
                            grid.push([week, month, 0, 0]);
                        }
                    }
                }
            }
            return grid;
        }


        // Function to display a message when there is no data
        function displayNoDataMessage() {
            // Hide the div with ID heatmap-legend
            heatmapLegend.style.display = 'none';
            chartContainer.style.height = '100px';
            chartContainer.style.width = '100%';
            chartContainer.style.display = 'flex';
            chartContainer.style.justifyContent = 'center';
            chartContainer.style.alignItems = 'center';
            chartContainer.style.textAlign = 'center';
            // Check if allHeatmapData is an empty dictionary
            if (yearSelector.options.length === 1 && allHeatmapData[yearSelector.value].length === 0) {
                chartContainer.innerHTML = '<div class="no-data-message">No data available for this dog.</div>';
            } else if (yearSelector.options.length > 1 && allHeatmapData[yearSelector.value].length === 0) {
                chartContainer.innerHTML = '<div class="no-data-message">No data recorded for the selected year.</div>';
            }
        }

        // Function to draw heatmap
        function drawHeatmap(year, granularity = 'daily') {
            // Display the legend if it was hidden
            heatmapLegend.style.display = 'block';

            // Parse first and last dates
            const firstDate = new Date(chartContainer.getAttribute('data-first-date'));
            const lastDate = new Date(chartContainer.getAttribute('data-last-date'));

            // Check if there is no data for the selected year
            if (!allHeatmapData[year] || allHeatmapData[year].length === 0) {
                displayNoDataMessage();
                return; // Exit the function if no data is available
            }

            // Get the heatmap data for the selected year
            let heatmapData, xAxisCategories, tooltipFormatter, dataLabelsFormatter, maxValue;
            let yAxisCategories = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'];

            // Set the chart data based on the currently selected granularity
            if (granularity === 'daily') {
                heatmapData = allHeatmapData[year];

                // Hold the maximum value in each year
                maxValue = Math.max(...heatmapData.map(array => array[2]));

                xAxisCategories = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                    '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'];

                // Set up the tooltip and data labels for the daily granularity
                tooltipFormatter = function () {
                    const day = this.point.x;
                    const month = this.point.y;
                    const isKongCount = isKongMapping[`${day}-${month}`] || 0; // Access isKong count from the mapping

                    if (this.point.value === 0) {
                        return 'Date: <b>' + yAxisCategories[this.point.y] + ' ' + (this.point.x + 1) + ', ' + (year) + '</b><br>' +
                            'No Observations Recorded on this day';
                    } else if (branch === 'Italy') {  // Also access the isDog, isHuman and NoStances counts if the branch is Italy
                        const isDogCount = isDogMapping[`${day}-${month}`] || 0;
                        const isHumanCount = isHumanMapping[`${day}-${month}`] || 0;
                        const noStancesCount = noStancesMapping[`${day}-${month}`] || 0;

                        return 'Date: <b>' + yAxisCategories[this.point.y] + ' ' + (this.point.x + 1) + ', ' + (year) + '</b><br>' +
                            'Total Observations: <b>' + this.point.value + '</b><br>' +
                            'Observations With a Toy: <b>' + isKongCount + '</b><br>' +
                            'Observations With a Dog: <b>' + isDogCount + '</b><br>' +
                            'Observations With a Human: <b>' + isHumanCount + '</b><br>' +
                            'Observations Without Stimuli: <b>' + noStancesCount + '</b>';
                    } else {
                        return 'Date: <b>' + yAxisCategories[this.point.y] + ' ' + (this.point.x + 1) + ', ' + (year) + '</b><br>' +
                            'Total Observations: <b>' + this.point.value + '</b><br>' +
                            'Observations With a Toy: <b>' + isKongCount + '</b><br>' +
                            'Observations Without a Toy: <b>' + (this.point.value - isKongCount) + '</b>';
                    }
                };

                // Set up the data labels for the daily granularity
                dataLabelsFormatter = function () {
                    const day = this.point.x;
                    const month = this.point.y;
                    const count = this.point.value;
                    // Access isKong count from the mapping
                    const isKongCount = isKongMapping[`${day}-${month}`] || 0;
                    // Assign the cell icon based on the branch-specific criteria.
                    let icon;
                    // Also access the isDog, isHuman and NoStances counts if the branch is Italy
                    if (branch === 'Italy') {
                        const isDogCount = isDogMapping[`${day}-${month}`] || 0;
                        const isHumanCount = isHumanMapping[`${day}-${month}`] || 0;
                        const noStancesCount = noStancesMapping[`${day}-${month}`] || 0;

                        // In Italy icon criteria is:
                        // The maximum value between isKong, isDog, and isHuman counts (priority when equal in same corresponding order)
                        if (isKongCount === 0 && isDogCount === 0 && isHumanCount === 0) {
                            icon = '🚫';
                        } else if (isKongCount >= isDogCount && isKongCount >= isHumanCount) {
                            icon = '🦴';
                        } else if (isDogCount >= isHumanCount) {
                            icon = '🐶';
                        } else {
                            icon = '👤';
                        }
                    } else {
                        // In Israel icon criteria is:
                        //  Dog icon if there is at least one isKong on that day, and if not it's X icon
                        icon = isKongCount > 0 ? '🦴' : '🚫';
                    }

                    // Check if the user wants to see detailed icons
                    if (iconsSelector.checked) {
                        // Display the count with icons
                        return count > 0 ? (icon + '' + count) : count;
                    } else {
                        // Display only the count without icons
                        return count;
                    }
                };
            } else if (granularity === 'weekly') {
                heatmapData = weeklyHeatmapData[year];

                // Hold the maximum value in each year
                maxValue = Math.max(...heatmapData.map(array => array[2]));

                xAxisCategories = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'];

                // Set up the tooltip and data labels for the weekly granularity
                tooltipFormatter = function () {
                    const week = this.point.x;
                    const month = this.point.y;
                    // Access isKong count from the mapping
                    const isKongCount = isKongWeeklyMapping[`${week}-${month}`] || 0;
                    if (this.point.value === 0) {
                        return 'Week ' + (this.point.x + 1) + ' of ' + yAxisCategories[this.point.y] + ', ' + (year) + '<br>' +
                            'No Observations Recorded in this week';
                    } else if (branch === 'Italy') {  // Also access the isDog, isHuman and NoStances counts if the branch is Italy
                        const isDogCount = isDogWeeklyMapping[`${week}-${month}`] || 0;
                        const isHumanCount = isHumanWeeklyMapping[`${week}-${month}`] || 0;
                        const noStancesCount = noStancesWeeklyMapping[`${week}-${month}`] || 0;

                        return '<b>Week ' + (this.point.x + 1) + '</b> of ' + yAxisCategories[this.point.y] + ', ' + (year) + '<br>' +
                            'Total Observations: <b>' + this.point.value + '</b><br>' +
                            'Observations With a Toy: <b>' + isKongCount + '</b><br>' +
                            'Observations With a Dog: <b>' + isDogCount + '</b><br>' +
                            'Observations With a Human: <b>' + isHumanCount + '</b><br>' +
                            'Observations Without Stimuli: <b>' + noStancesCount + '</b>';
                    } else {
                        return '<b>Week ' + (this.point.x + 1) + '</b> of ' + yAxisCategories[this.point.y] + ', ' + (year) + '<br>' +
                            'Total Observations: <b>' + this.point.value + '</b><br>' +
                            'Observations With a Toy: <b>' + isKongCount + '</b><br>' +
                            'Observations Without a Toy: <b>' + (this.point.value - isKongCount) + '</b>';
                    }
                };

                // Function to get isDogCount for Italy branch only
                function getIsDogCount(week, month) {
                    if (branch === 'Italy') {
                        return isDogWeeklyMapping[`${week}-${month}`] || 0;
                    }
                    return 0;
                }

                // Function to get isHumanCount for Italy branch only
                function getIsHumanCount(week, month) {
                    if (branch === 'Italy') {
                        return isHumanWeeklyMapping[`${week}-${month}`] || 0;
                    }
                    return 0;
                }

                // Function to get NoStancesCount for Italy branch only
                function getNoStancesCount(week, month) {
                    if (branch === 'Italy') {
                        return noStancesWeeklyMapping[`${week}-${month}`] || 0;
                    }
                    return 0;
                }

                // Set up the data labels for the weekly granularity
                dataLabelsFormatter = function () {
                    const week = this.point.x;
                    const month = this.point.y;
                    const count = this.point.value;

                    // Return the count and the detailed icons on the right side of the cell
                    let dataLabel = count + ': ';

                    // Access isKong count from the mapping
                    const isKongCount = isKongWeeklyMapping[`${week}-${month}`] || 0;
                    // Also access the isDog, isHuman and NoStances counts if the branch is Italy
                    const isDogCount = getIsDogCount(week, month);
                    const isHumanCount = getIsHumanCount(week, month);
                    const noStancesCount = getNoStancesCount(week, month);

                    // Check if the user wants to see detailed icons
                    if (iconsSelector.checked) {
                        // Check if the branch is Israel
                        if (branch !== 'Italy') {
                            // Display the total count on the left, and the counts of isKong and isNotKong on the right
                            if (count === 0) {
                                return count;
                            } else if (count === isKongCount) {
                                return dataLabel + '[🦴' + isKongCount.toString().italics() + ']';
                            } else if (isKongCount === 0) {
                                return dataLabel + '[🚫' + count.toString().italics() + ']';
                            } else {
                                return dataLabel + '[🦴' + isKongCount.toString().italics() + '|🚫' + (count - isKongCount).toString().italics() + ']';
                            }
                        } // Check if the branch is Italy
                        else if (branch === 'Italy') {
                            // Display the total count on the left and the counts of isKong, isDog, isHuman and NoStances on the right
                            if (count === 0) {
                                return count;
                            } else if (isKongCount === 0 && isDogCount === 0 && isHumanCount === 0) {
                                return dataLabel + '[🚫' + count.toString().italics() + ']';
                            } else if (isDogCount === 0 && isHumanCount === 0 && noStancesCount === 0) {
                                return dataLabel + '[🦴' + isKongCount.toString().italics() + ']';
                            } else if (isKongCount === 0 && isHumanCount === 0 && noStancesCount === 0) {
                                return dataLabel + '[🐶' + isDogCount.toString().italics() + ']';
                            } else if (isKongCount === 0 && isDogCount === 0 && noStancesCount === 0) {
                                return dataLabel + '[👤' + isHumanCount.toString().italics() + ']';
                            } else if (isKongCount === 0) {
                                if (isDogCount === 0) {
                                    return dataLabel + '[👤' + isHumanCount.toString().italics() + '|🚫' + noStancesCount.toString().italics() + ']';
                                } else if (isHumanCount === 0) {
                                    return dataLabel + '[🐶' + isDogCount.toString().italics() + '|🚫' + noStancesCount.toString().italics() + ']';
                                } else if (noStancesCount === 0) {
                                    return dataLabel + '[🐶' + isDogCount.toString().italics() + '|👤' + isHumanCount.toString().italics() + ']';
                                } else {
                                    return dataLabel + '[🐶' + isDogCount.toString().italics() + '|👤' + isHumanCount.toString().italics() + '|🚫' + noStancesCount.toString().italics() + ']';
                                }
                            } else if (isDogCount === 0) {
                                if (isHumanCount === 0) {
                                    return dataLabel + '[🦴' + isKongCount.toString().italics() + '|🚫' + noStancesCount.toString().italics() + ']';
                                } else if (noStancesCount === 0) {
                                    return dataLabel + '[🦴' + isKongCount.toString().italics() + '|👤' + isHumanCount.toString().italics() + ']';
                                } else {
                                    return dataLabel + '[🦴' + isKongCount.toString().italics() + '|👤' + isHumanCount.toString().italics() + '|🚫' + noStancesCount.toString().italics() + ']';
                                }
                            } else if (isHumanCount === 0) {
                                if (noStancesCount === 0) {
                                    return dataLabel + '[🦴' + isKongCount.toString().italics() + '|🐶' + isDogCount.toString().italics() + ']';
                                } else {
                                    return dataLabel + '[🦴' + isKongCount.toString().italics() + '|🐶' + isDogCount.toString().italics() + '|🚫' + noStancesCount.toString().italics() + ']';
                                }
                            } else if (noStancesCount === 0) {
                                return dataLabel + '[🦴' + isKongCount.toString().italics() + '|🐶' + isDogCount.toString().italics() + '|👤' + isHumanCount.toString().italics() + ']';
                            } else {
                                return dataLabel + '[🦴' + isKongCount.toString().italics() + '|🐶' + isDogCount.toString().italics() + '|👤' + isHumanCount.toString().italics() + '|🚫' + noStancesCount.toString().italics() + ']';
                            }
                        }
                    } else { // If the user does not want to see detailed icons, simply display the count
                        return count;
                    }
                    return count;
                };
            }

            // Create a full grid for the year with zeros
            let fullYearGrid = createFullYearGrid(year, firstDate, lastDate, granularity);

            // Create a mapping for isKong counts
            const isKongMapping = {};
            const isKongWeeklyMapping = {};
            // Also include the isDog and isHuman counts for the Italy branch
            const isDogMapping = {};
            const isHumanMapping = {};
            const isDogWeeklyMapping = {};
            const isHumanWeeklyMapping = {};
            const noStancesMapping = {};
            const noStancesWeeklyMapping = {};


            // Update the grid with actual counts from heatmapData
            heatmapData.forEach(data => {
                const day = data[0];
                const month = data[1];
                const count = data[2];
                const index = fullYearGrid.findIndex(d => d[0] === day && d[1] === month);
                if (granularity === 'daily') {
                    isKongMapping[`${day}-${month}`] = data[3];
                    // Also include the isDog and isHuman counts if the branch is Italy
                    if (branch === 'Italy') {
                        isDogMapping[`${day}-${month}`] = data[4];
                        isHumanMapping[`${day}-${month}`] = data[5];
                        noStancesMapping[`${day}-${month}`] = data[6];
                    }
                    // Update the count in the full year grid
                    if (index !== -1) {
                        fullYearGrid[index][2] = count;
                    }
                } else if (granularity === 'weekly') {
                    isKongWeeklyMapping[`${day}-${month}`] = data[3];
                    // Also include the isDog, isHuman and noStances counts if the branch is Italy
                    if (branch === 'Italy') {
                        isDogWeeklyMapping[`${day}-${month}`] = data[4];
                        isHumanWeeklyMapping[`${day}-${month}`] = data[5];
                        noStancesWeeklyMapping[`${day}-${month}`] = data[6];
                    }
                    // Update the count in the full year grid
                    if (index !== -1) {
                        fullYearGrid[index][2] = count;
                    }
                }
            });

            // Use the updated full year grid for the heatmap
            heatmapData = fullYearGrid;

            // Calculate the number of unique months in the heatmap data, and set the row height
            const months = new Set(heatmapData.map(item => item[1]));
            const numberOfMonths = months.size;
            const rowHeight = numberOfMonths <= 4 ? 35 : 25;

            // Calculate the total height
            const totalHeight = numberOfMonths * rowHeight + 150;

            // Calculate the number of unique days in the heatmap data
            const days = new Set(heatmapData.map(item => item[0]));
            const numberOfDays = days.size;

            // Determine width values
            const weeklyWidth = 1200;       // for weekly granularity
            const extraNarrowWidth = 550;  // for less than 5 days
            const narrowWidth = 600;       // for 10 days or less
            const wideWidth = 1350;        // for more than 10 days

            // Determine the width based on the number of days
            let totalWidth;
            if (granularity === 'weekly') {
                totalWidth = weeklyWidth;
            } else if (numberOfDays < 5) {
                totalWidth = extraNarrowWidth;
            } else if (numberOfDays <= 10) {
                totalWidth = narrowWidth;
            } else {
                totalWidth = wideWidth;
            }

            // Set the height and width of the chart container
            chartContainer.style.height = totalHeight + 'px';
            chartContainer.style.width = totalWidth + 'px';

            // Highcharts chart configuration
            Highcharts.chart('chart-data', {
                chart: {
                    type: 'heatmap',
                    marginTop: 80,
                    marginBottom: 80,
                    plotBorderWidth: 2,
                    plotBorderColor: '#000000',
                    plotBackgroundColor: '#F5F5F5',
                },
                title: {
                    text: chartTitleDogName + 'Observations Overview Heatmap for ' + year + ' (' + granularity[0].toUpperCase() + granularity.slice(1) + ')',
                    style: {
                        fontWeight: 'bold',
                        fontSize: '25px',
                    }
                },
                xAxis: {
                    categories: xAxisCategories,
                    title: {
                        text: granularity === 'daily' ? 'Day' : 'Week',
                        style: {
                            fontWeight: 'bold',
                            fontSize: '15px',
                        }
                    },
                    labels: {
                        style: {
                            fontWeight: 'bold',
                            fontSize: '15px'
                        }
                    }
                },
                yAxis: {
                    categories: yAxisCategories,
                    reversed: true,
                    title: {
                        text: 'Month',
                        style: {
                            fontWeight: 'bold',
                            fontSize: '15px',
                        }
                    },
                    labels: {
                        style: {
                            fontWeight: 'bold',
                            fontSize: '15px'
                        }
                    },
                },
                colorAxis: {
                    min: 0,
                    max: maxValue,
                    startOnTick: false,
                    endOnTick: false,
                    stops: maxValue === 1 ? [
                        [0, '#3333FF'], // Blue for zero
                        [1, '#FF3333']  // Red for one (maxValue is 1)
                    ] : [
                        [0, '#3333FF'], // Blue for low values
                        [0.25, '#ADD8E6'], // Light blue for lower-middle
                        [0.5, '#FFFFFF'], // White for midpoint
                        [0.75, '#FFA07A'], // Light red for upper-middle
                        [1, '#FF3333']  // Red for high values (maxValue)
                    ]
                },
                legend: {
                    align: 'bottom',
                    layout: 'horizontal',
                    margin: 100,
                    verticalAlign: 'bottom',
                    y: 20,
                    x: 115,
                    // symbolHeight: 280,
                },
                tooltip: {
                    formatter: tooltipFormatter,
                    outside: true,
                    style: {
                        fontSize: '18px'
                    }
                },
                series: [{
                    name: granularity === 'daily' ? 'Observations per day' : 'Observations per week',
                    borderWidth: granularity === 'daily' ? 1 : 2,
                    data: heatmapData,
                    borderColor: '#000000',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        // Set alignment and x-offset based on granularity and icon display
                        align: 'center',
                        x: 0,
                        verticalAlign: 'middle',
                        formatter: dataLabelsFormatter,
                        style: {
                            textOutline: false,
                            fontWeight: 'bold',
                            fontSize: '15px',
                        }
                    }
                }],
                credits: {
                    enabled: false,
                }
            });
        }

        // Initial draw for the default year (latest year) and by "daily" granularity
        if (!allHeatmapData[defaultYear] || allHeatmapData[defaultYear].length === 0) {
            displayNoDataMessage();
        } else {
            drawHeatmap(defaultYear, 'daily');
        }

        // Event listener for year selector
        yearSelector.addEventListener('change', function () {
            const selectedYear = this.value;
            const selectedGranularity = granularitySelector.value;
            drawHeatmap(selectedYear, selectedGranularity);
            updateButtonStates();
        });

        // Event listener for previous year button
        prevYearButton.addEventListener('click', function () {
            const currentYearIndex = Array.from(yearSelector.options).findIndex(option => option.value === yearSelector.value);
            if (currentYearIndex > 0) {
                yearSelector.selectedIndex = currentYearIndex - 1;
                yearSelector.dispatchEvent(new Event('change'));
            }
        });

        // Event listener for next year button
        nextYearButton.addEventListener('click', function () {
            const currentYearIndex = Array.from(yearSelector.options).findIndex(option => option.value === yearSelector.value);
            if (currentYearIndex < yearSelector.options.length - 1) {
                yearSelector.selectedIndex = currentYearIndex + 1;
                yearSelector.dispatchEvent(new Event('change'));
            }
        });


        // Event listener for granularity selector
        granularitySelector.addEventListener('change', function () {
            const selectedYear = yearSelector.value;
            const selectedGranularity = this.value;
            drawHeatmap(selectedYear, selectedGranularity);
        });

        // Event listener for the Icons checkbox
        iconsSelector.addEventListener('change', function () {
            const selectedYear = yearSelector.value;
            const selectedGranularity = granularitySelector.value;
            const iconsLegend = document.getElementById('icons-legend');
            if (this.checked) {
                iconsLegend.style.display = 'block';
            } else {
                iconsLegend.style.display = 'none';
            }
            drawHeatmap(selectedYear, selectedGranularity);
        });

    });
}

if (userIsVet === true) {
// Clear all error messages after closing modals
    $('#addTreatmentModal, #editTreatmentModal, #addExaminationModal, #editExaminationModal, #addPlacementModal, #editPlacementModal, #addSessionModal, #editSessionModal\n').on('show.bs.modal hidden.bs.modal', function () {
        $('.error').remove();
    });
}

// Set a timeout to hide success message after 3 seconds
setTimeout(function() {
    $('#messageContainer .alert').fadeOut('slow');
}, 3000);