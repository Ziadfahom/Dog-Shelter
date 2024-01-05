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

});
