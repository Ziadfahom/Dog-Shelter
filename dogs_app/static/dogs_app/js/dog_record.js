$(document).ready(function(){
    var allContainers = [
        '#treatments_container',
        '#examinations_container',
        '#placements_container',
        '#observations_container'
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

function goBack() {
    const referrer = document.referrer;
    if (referrer.includes('update_dog')) {
        window.location.href = '/dogs/';
    } else {
        window.history.back();
    }
}

// Open the New Treatment modal when the "Add Treatment" button is clicked
document.querySelector('.new-treatment').addEventListener('click', function(event) {
    event.preventDefault();
    var treatmentModal = new bootstrap.Modal(document.getElementById('addTreatmentModal'));
    treatmentModal.show();
});

// Open the New Examination modal when the "Add Examination" button is clicked
document.querySelector('.new-examination').addEventListener('click', function(event) {
    event.preventDefault();
    var examinationModal = new bootstrap.Modal(document.getElementById('addExaminationModal'));
    examinationModal.show();
});

// Open the New Placement modal when the "Add Placement" button is clicked
document.querySelector('.new-placement').addEventListener('click', function(event) {
    event.preventDefault();
    var placementModal = new bootstrap.Modal(document.getElementById('addPlacementModal'));
    placementModal.show();
});

// Activate Bootstrap Datepicker script
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

    // Handle form submission for new Treatment
    $('#addTreatmentModal form').submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(data) {
                // Close the modal after successful addition
                $('#addTreatmentModal').modal('hide');

                // Show success alert
                $('#treatments-success-alert').show();

                // Set a timer to hide the success alert after 5 seconds
                setTimeout(function() {
                    $('#treatments-success-alert').hide();
                }, 4000);

                // Update the treatments table with new data
                updateTableContent("#treatments_table tbody", data.data);

                // Update pagination controls
                updatePagination("#treatments_table #pagination", data.pagination);

            }
        });
    });

    // Handle form submission for new Examination
    $('#addExaminationModal form').submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(data) {
                // Close the modal after successful addition
                $('#addExaminationModal').modal('hide');

                // Show success alert
                $('#examinations-success-alert').show();

                // Set a timer to hide the success alert after 5 seconds
                setTimeout(function() {
                    $('#examinations-success-alert').hide();
                }, 4000);

                // Update the examinations table with new data
                updateTableContent("#examinations_table tbody", data.data);

                // Update pagination controls
                updatePagination("#examinations_table #pagination", data.pagination);

            }
        });
    });

    // Handle form submission for new Placement
    $('#addPlacementModal form').submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(data) {
                // Close the modal after successful addition
                $('#addPlacementModal').modal('hide');

                // Show success alert
                $('#placements-success-alert').show();

                // Set a timer to hide the success alert after 5 seconds
                setTimeout(function() {
                    $('#placements-success-alert').hide();
                }, 4000);

                // Update the treatments table with new data
                updateTableContent("#placements_table tbody", data.data);

                // Update pagination controls
                updatePagination("#placements_table #pagination", data.pagination);

            }
        });
    });
});


// Updates the current pagination
function updatePagination(paginationSelector, html) {
    $(paginationSelector).replaceWith(html);
}


// AJAX call for updating pagination for a table
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
            if (paramName === "treatments_page") {
                updateTableContent("#treatments_table tbody", response.data);
                updatePagination("#treatments_table #pagination", response.pagination);
            } else if (paramName === "examinations_page") {
                updateTableContent("#examinations_table tbody", response.data);
                updatePagination("#examinations_table #pagination", response.pagination);
            } else if (paramName === "placements_page") {
                updateTableContent("#placements_table tbody", response.data);
                updatePagination("#placements_table #pagination", response.pagination);
            } else if (paramName === "observations_page") {
                updateTableContent("#observations_table tbody", response.data);
                updatePagination("#observations_table #pagination", response.pagination);
            }
        }
    });
}

function updateTableContent(tableSelector, data) {
    const $tableBody = $(tableSelector);
    $tableBody.empty();
    data.forEach(row => {
        $tableBody.append(row);  // Assumes each row is formatted HTML
    });
}


