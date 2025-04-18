// Initialize ageSlider for the noUiSlider
const ageSlider = document.getElementById('ageRange');
if (userIsVet === true) {

}
else {

}

// Age filter logic
noUiSlider.create(ageSlider, {
    start: [0, 20], // This sets the two handles at the start and end
    connect: true,  // Displays a colored bar between the handles
    range: {
        'min': 0,
        'max': 20
    },
    step: 1  // Slider moves in increments of 1
});

// When the slider value changes, update the hidden input fields and the displayed ones
ageSlider.noUiSlider.on('update', function(values, handle) {
    document.getElementById('ageRangeStart').value = Math.round(values[0]);
    document.getElementById('ageRangeEnd').value = Math.round(values[1]);
    document.getElementById('selectedAgeRange').textContent = Math.round(values[0]) + " - " + Math.round(values[1]);
});

// Initialize the document, applying filters if URL parameters exist.
$(document).ready(function() {
  applyFiltersFromURL();

  // Handle pagination when a pagination link is clicked.
  $(document).on('click', '.pagination-link', function(e) {
    e.preventDefault();

    // Extract URL parameters and form values.
    let params = getURLParameters();

    params.dogName = document.getElementById('searchInput').value;
    params.breed = document.getElementById('breed').value;
    params.gender = document.getElementById('gender').value;
    params.furColor = document.getElementById('furColor').value;
    params.ageFrom = Math.round(ageSlider.noUiSlider.get()[0]);
    params.ageTo = Math.round(ageSlider.noUiSlider.get()[1]);

    // Update URL parameters matching the user's permissions (for Vets and above)
    if (userIsVet === true) {
    params.startDateOfArrival = document.getElementById('startDateOfArrival').value;
    params.endDateOfArrival = document.getElementById('endDateOfArrival').value;
    params.startDateOfVaccination = document.getElementById('startDateOfVaccination').value;
    params.endDateOfVaccination = document.getElementById('endDateOfVaccination').value;
    params.isNeutered = document.getElementById('isNeutered').value;
    params.isDangerous = document.getElementById('isDangerous').value;
    params.kongstartDateAdded = document.getElementById('kongstartDateAdded').value;
    params.kongendDateAdded = document.getElementById('kongendDateAdded').value;
    params.owner = document.getElementById('owner').value;
    }

    // Determine the selected page number from pagination link.
    let pageNumber = $(this).data('page');
    params.page = pageNumber;

    // Refresh the table with new parameters.
    refreshTable(params, pageNumber);
  });

  // Search logic for dog name
  document.getElementById('searchInput').addEventListener('input', function() {
    let searchQuery = this.value;
    let params = getURLParameters();

    // Update the current parameters with the new search query
    if (searchQuery) {
      params.dogName = searchQuery;
    } else {
      delete params.dogName;
    }

    // Update the URL with the new parameter and refresh the table depending on User's permissions
    if (userIsVet === true) {
        updateVetURL(params.page, params.sort_by, searchQuery || '', params.startDateOfArrival, params.endDateOfArrival, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo, params.startDateOfVaccination, params.endDateOfVaccination, params.isNeutered, params.isDangerous, params.kongstartDateAdded, params.kongendDateAdded, params.owner);
    } else {
        updateURL(params.page, params.sort_by, searchQuery || '', params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo);
    }
    refreshTable(params, params.page || 1);
  });

  // Sorting logic for table headers, triggered when a table header is clicked
  $(document).on('click', '.sortable-header', function() {
    // Fetch the existing URL parameters and the table header
    let params = getURLParameters();
    let clickedColumn = $(this).data('column');

    // Handle sorting logic
    if (params.sort_by.replace('-', '') === clickedColumn) {
        params.sort_by = (params.sort_by.includes('-') ? '' : '-') + clickedColumn;
    } else {
        params.sort_by = clickedColumn;
    }

    // Reset to the first page when sorting changes
    params.page = 1;

    // Refresh the table
    refreshTable(params, params.page || 1);
  });
});


// Update filters when the browser's back/forward button is clicked.
window.addEventListener('popstate', function(event) {
  applyFiltersFromURL();
});


// Refresh the table according to specified parameters.
function refreshTable(params, pageNumber) {
  // Update the page and sorting parameters, handling cases of missing values.
  params.page = pageNumber || 1;
  params.sort_by = params.sort_by || '-dateOfArrival';

  // Dispose of existing tooltips
  $('[data-bs-toggle="tooltip"]').tooltip('dispose');

  // Perform AJAX GET request to the server.
  $.ajax({
    url: '/filter/',
    type: 'GET',
    data: params,
    headers: { 'X-CSRFToken': '{{ csrf_token }}' },
    success: function(response) {
      // Replace table rows and pagination controls.
      let tableBody = document.getElementById('dog-table');
      tableBody.innerHTML = response.table_rows;
      let paginationControls = document.getElementById('pagination-container');
      paginationControls.innerHTML = response.pagination_html;

      // Display a message if no dogs are found.
      if (!response.table_rows.trim()) {
        tableBody.innerHTML = `
          <tr>
            <td colspan="11">
              <div class="text-center" role="alert" style="background-color: #E0E0E0; border-radius: 3px; padding: 15px;">
                <h4 style="color: #333333;">No Dogs Found</h4>
                <p style="color: #555555;">Please adjust your filters or check back later.</p>
              </div>
            </td>
          </tr>`;
      }

      // Update the URL to reflect the new state depending on User's permissions
      if (userIsVet === true) {
        updateVetURL(pageNumber, params.sort_by, params.dogName || '', params.startDateOfArrival, params.endDateOfArrival, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo, params.startDateOfVaccination, params.endDateOfVaccination, params.isNeutered, params.isDangerous, params.kongstartDateAdded, params.kongendDateAdded, params.owner);
      } else {
        updateURL(pageNumber, params.sort_by, params.dogName || '', params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo);
      }

      // Initialize tooltips.
      $('[data-bs-toggle="tooltip"]').tooltip({
        // Various tooltip settings
        trigger: 'hover',
        boundary: 'window',
        html: true,
        animation: false,
        container: 'body',
        placement: function(context, source) {
          var position = $(source).offset();
          if (position.left < 515) {
            return "right";
          }
          if (position.left > 515) {
            return "left";
          }
          if (position.top < 110) {
            return "bottom";
          }
          return "top";
        }
      });

      // Navigate to dog details page when a row is clicked.
      $(".dog-row").click(function() {
        window.location = $(this).data("href");
      });
    }
  });
}


// Populate filter values from the URL parameters and refresh the table.
function applyFiltersFromURL() {
  let params = getURLParameters();
  let hasFilters = false;

  // Check if any parameter exists.
  for (let key in params) {
    if (params[key] !== undefined && params[key] !== '') {
      hasFilters = true;
      break; // No need to continue if one filter is found
    }
  }

  // Ensure default values if none exists
  let page = params.page || 1;
  params.sort_by = params.sort_by || '-dateOfArrival';

  // If filters are present, populate the filter fields.
  if (hasFilters) {
    document.getElementById('searchInput').value = params.dogName || '';
    document.getElementById('breed').value = params.breed || '';
    document.getElementById('gender').value = params.gender || '';
    document.getElementById('furColor').value = params.furColor || '';
    ageSlider.noUiSlider.set([params.ageFrom || 0, params.ageTo || 20]);

    // Proceed depending on User's permissions
    if (userIsVet === true) {
        document.getElementById('startDateOfArrival').value = params.startDateOfArrival || '';
        document.getElementById('endDateOfArrival').value = params.endDateOfArrival || '';
        document.getElementById('startDateOfVaccination').value = params.startDateOfVaccination || '';
        document.getElementById('endDateOfVaccination').value = params.endDateOfVaccination || '';
        document.getElementById('isNeutered').value = params.isNeutered || '';
        document.getElementById('isDangerous').value = params.isDangerous || '';
        document.getElementById('kongstartDateAdded').value = params.kongstartDateAdded || '';
        document.getElementById('kongendDateAdded').value = params.kongendDateAdded || '';
        document.getElementById('owner').value = params.owner || '';
    }
  }

  // Refresh the table.
  refreshTable(params, page);  // Apply the filters using the retrieved parameters
}


function applyVetFilters() {
    let ageValues = ageSlider.noUiSlider.get();
    if (userIsVet === true) {
        return {
            'page': 1, // Revert to first page when applying new filters
            'sort_by': getURLParameters().sort_by || '-dateOfArrival', // Either the sorting parameter from the URL or default
            'dogName': document.getElementById('searchInput').value || '',
            'startDateOfArrival': document.getElementById('startDateOfArrival').value || '',
            'endDateOfArrival': document.getElementById('endDateOfArrival').value || '',
            'breed': document.getElementById('breed').value || '',
            'gender': document.getElementById('gender').value || '',
            'furColor': document.getElementById('furColor').value || '',
            'ageFrom': Math.round(ageValues[0]) || 0,
            'ageTo': Math.round(ageValues[1]) || 20,
            'startDateOfVaccination': document.getElementById('startDateOfVaccination').value || '',
            'endDateOfVaccination': document.getElementById('endDateOfVaccination').value || '',
            'isNeutered': document.getElementById('isNeutered').value || '',
            'isDangerous': document.getElementById('isDangerous').value || '',
            'kongstartDateAdded': document.getElementById('kongstartDateAdded').value || '',
            'kongendDateAdded': document.getElementById('kongendDateAdded').value || '',
            'owner': document.getElementById('owner').value || ''
        };
    } else {
        return {
            'page': 1, // Revert to first page when applying new filters
            'sort_by': getURLParameters().sort_by || '-dateOfArrival', // Either the sorting parameter from the URL or default
            'dogName': document.getElementById('searchInput').value || '',
            'breed': document.getElementById('breed').value || '',
            'gender': document.getElementById('gender').value || '',
            'furColor': document.getElementById('furColor').value || '',
            'ageFrom': Math.round(ageValues[0]) || 0,
            'ageTo': Math.round(ageValues[1]) || 20,
        };
    }
}

// Collect filter values and apply them.
function applyFilters() {
    let ageValues = ageSlider.noUiSlider.get();
    let params = applyVetFilters();

    // Update the URL and refresh the table depending on User permissions
    if (userIsVet === true) {
        updateVetURL(params.page, params.sort_by, params.dogName, params.startDateOfArrival, params.endDateOfArrival, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo, params.startDateOfVaccination, params.endDateOfVaccination, params.isNeutered, params.isDangerous, params.kongstartDateAdded, params.kongendDateAdded, params.owner);
    } else {
        updateURL(params.page, params.sort_by, params.dogName, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo);
    }

    refreshTable(params, 1);
    let closeFiltersButton = document.getElementById('closeFiltersButton');
    closeFiltersButton.click();
}


// Reset all filters to their default state.
function resetFilters() {
    document.getElementById('breed').selectedIndex = 0;
    document.getElementById('gender').selectedIndex = 0;
    document.getElementById('furColor').selectedIndex = 0;
    document.getElementById('searchInput').value = '';
    ageSlider.noUiSlider.set([0, 20]);

    // Reset filters depending on User's permissions
    if (userIsVet === true) {
        document.getElementById('startDateOfArrival').value = '';
        document.getElementById('endDateOfArrival').value = '';
        document.getElementById('startDateOfVaccination').value = '';
        document.getElementById('endDateOfVaccination').value = '';
        document.getElementById('isNeutered').selectedIndex = 0;
        document.getElementById('isDangerous').selectedIndex = 0;
        document.getElementById('kongstartDateAdded').value = '';
        document.getElementById('kongendDateAdded').value = '';
        document.getElementById('owner').selectedIndex = 0;
    }

    // Construct a new URL without query parameters and update the browser's history.
    let newurl = window.location.protocol + "//" + window.location.host + window.location.pathname;
    window.history.pushState({ path: newurl }, '', newurl);

    // Refresh the table with no filters.
    refreshTable({});
}


// Update the URL for Vets to reflect the current filter and pagination state.
function updateVetURL(page, sort_by, dogName, startDateOfArrival, endDateOfArrival, breed, gender, furColor, ageFrom, ageTo, startDateOfVaccination, endDateOfVaccination, isNeutered, isDangerous, kongstartDateAdded, kongendDateAdded, owner) {
  const url = new URL(window.location);
  url.searchParams.set('page', page || '');
  url.searchParams.set('sort_by', sort_by || '-dateOfArrival');
  url.searchParams.set('dogName', dogName || '');
  url.searchParams.set('startDateOfArrival', startDateOfArrival || '');
  url.searchParams.set('endDateOfArrival', endDateOfArrival || '');
  url.searchParams.set('breed', breed || '');
  url.searchParams.set('gender', gender || '');
  url.searchParams.set('furColor', furColor || '');
  url.searchParams.set('ageFrom', ageFrom || '');
  url.searchParams.set('ageTo', ageTo || '');
  url.searchParams.set('startDateOfVaccination', startDateOfVaccination || '');
  url.searchParams.set('endDateOfVaccination', endDateOfVaccination || '');
  url.searchParams.set('isNeutered', isNeutered || '');
  url.searchParams.set('isDangerous', isDangerous || '');
  url.searchParams.set('kongstartDateAdded', kongstartDateAdded || '');
  url.searchParams.set('kongendDateAdded', kongendDateAdded || '');
  url.searchParams.set('owner', owner || '');

  // Push the new URL state.
  window.history.pushState({ path: url.toString() }, '', url.toString());
}


// Update the URL for regular users to reflect the current filter and pagination state.
function updateURL(page, sort_by, dogName, breed, gender, furColor, ageFrom, ageTo) {
  const url = new URL(window.location);
  url.searchParams.set('page', page || '');
  url.searchParams.set('sort_by', sort_by || '-dateOfArrival');
  url.searchParams.set('dogName', dogName || '');
  url.searchParams.set('breed', breed || '');
  url.searchParams.set('gender', gender || '');
  url.searchParams.set('furColor', furColor || '');
  url.searchParams.set('ageFrom', ageFrom || '');
  url.searchParams.set('ageTo', ageTo || '');

  // Push the new URL state.
  window.history.pushState({ path: url.toString() }, '', url.toString());
}

// Retrieve parameters from the current URL.
function getURLParameters() {
  let params = {};
  const url = new URL(window.location);
  url.searchParams.forEach((value, key) => {
    params[key] = value;
  });
  return params;
}


// Handle logic for exporting/importing Dog table as JSON/Excel file.
$(document).ready(function() {
    $('#exportJsonButton').click(function() {
        $.ajax({
            url: '/get_filtered_dog_ids/',
            type: 'GET',
            success: function(response) {
                let filteredDogIDs = response.filtered_dogs_ids;
                $.ajax({
                    url: '/export_dogs_json/',
                    type: 'POST',
                    data: {'dog_ids': JSON.stringify(filteredDogIDs)},
                    headers: { 'X-CSRFToken': getCookie('csrftoken') },
                    success: async function(data, textStatus, xhr) {
                        if (xhr.status === 200) {
                            let blob = new Blob([JSON.stringify(data)], { type: 'application/json;charset=utf-8' });
                            const fileHandle = await window.showSaveFilePicker({
                                suggestedName: 'Shelter_dogs_data.json',
                                types: [{
                                    description: "JSON file",
                                    accept: {"application/json": [".json"]}
                                }]
                            });
                            const fileStream = await fileHandle.createWritable();
                            await fileStream.write(blob);
                            await fileStream.close();
                        } else {
                            // Handle non-200 responses here, such as showing an error message
                            alert("Error: Unable to export data. Please check your permissions.");
                        }
                    },
                    error: function(xhr, status, error) {
                    // Check if the response has a JSON content
                    if (xhr.responseJSON && xhr.responseJSON.error) {
                            alert(xhr.responseJSON.error);
                        } else {
                            alert("An unexpected error occurred: " + error);
                        }
                    }
                });
            }
        });
    });

    // Exporting Dog table as Excel
    $('#exportExcelButton').click(function() {
    $.ajax({
      url: '/get_filtered_dog_ids/',
      type: 'GET',
      success: function(response) {
        let filteredDogIDs = response.filtered_dogs_ids;
        let params = getURLParameters();
        let sort_by = params.sort_by || '-dateOfArrival';

        $.ajax({
            url: '/export_dogs_excel/',
            type: 'POST',
            data: JSON.stringify({'dog_ids': filteredDogIDs, 'sort_by': sort_by}),
            contentType: 'application/json; charset=utf-8',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: async function(data) {
              let blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8' });

              // File handler & file stream
              const fileHandle = await window.showSaveFilePicker({
                suggestedName: 'Shelter_dogs_data.xlsx',
                types: [{
                  description: "Excel file",
                  accept: {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"]}
                }]
              });
              const fileStream = await fileHandle.createWritable();

              // Write file
              await fileStream.write(blob);
              await fileStream.close();
            },
            error: function(response) {
                let errorMessage = response.responseJSON && response.responseJSON.message ? response.responseJSON.message : 'Unknown error occurred during export.';
                // Create error message div and append it to the message area
                var errorDiv = $('<div/>')
                    .addClass('alert alert-danger alert-dismissible fade show col-md-6 offset-md-3 text-center')
                    .text(errorMessage)
                    .append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
                $('#messageContainer').append(errorDiv);
            },
            xhrFields: {
                responseType: 'arraybuffer'
            },
        });
      },
    });
    });

    // Importing Dog entities from Excel
    $('#excelFileInput').change(function() {
        let params = getURLParameters();
        let excelFileInput = document.getElementById('excelFileInput');
        let formData = new FormData();
        formData.append('excel_file', excelFileInput.files[0]);

        $.ajax({
            url: '/import_dogs_excel/',
            type: 'POST',
            data: formData,
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success') {
                    // Create message div and append it to the message area
                    var messageDiv = $('<div/>')
                        .addClass('alert alert-success alert-dismissible fade show col-md-6 offset-md-3 text-center')
                        .text(response.message)
                        .append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
                    $('#messageContainer').append(messageDiv);

                    // Set timeout to remove the message after 5 seconds (5000 milliseconds)
                    setTimeout(function() {
                        messageDiv.alert('close');
                    }, 5000);
                }
                refreshTable(params, 1);
                $('#excelFileInput').val('');  // Reset file input

            },
            error: function(response) {
                let errorMessage = response.responseJSON && response.responseJSON.message ? response.responseJSON.message : 'Unknown error occurred during import.';
                // Create error message div and append it to the message area
                var errorDiv = $('<div/>')
                    .addClass('alert alert-danger alert-dismissible fade show col-md-6 offset-md-3 text-center')
                    .text(errorMessage)
                    .append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
                $('#messageContainer').append(errorDiv);

                $('#excelFileInput').val('');  // Reset file input
            }
        });
    });

    // Importing Dog entities from JSON
    $('#jsonFileInput').change(function() {
       let params = getURLParameters();
       let jsonFileInput = document.getElementById('jsonFileInput');
       let formData = new FormData();
       formData.append('json_file', jsonFileInput.files[0]);

       $.ajax({
           url: '/import_dogs_json/',
           type: 'POST',
           data: formData,
           headers: { 'X-CSRFToken': getCookie('csrftoken') },
           processData: false,
           contentType: false,
           success: function(response) {
               if (response.status === 'success') {
                   // Create message div and append it to the message area
                   var messageDiv = $('<div/>')
                      .addClass('alert alert-success alert-dismissible fade show col-md-6 offset-md-3 text-center')
                      .text(response.message)
                      .append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
                   $('#messageContainer').append(messageDiv);

                   // Set timeout to remove the message after 5 seconds (5000 milliseconds)
                   setTimeout(function() {
                      messageDiv.alert('close');
                   }, 5000);
               }
               refreshTable(params, 1);
               $('#jsonFileInput').val(''); // Reset file input

           },
           error: function(response) {
               let errorMessage = response.responseJSON && response.responseJSON.message ? response.responseJSON.message : 'Unknown error occurred during import.';
               // Create error message div and append it to the message area
               var errorDiv = $('<div/>')
                   .addClass('alert alert-danger alert-dismissible fade show col-md-6 offset-md-3 text-center')
                   .text(errorMessage)
                   .append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
               $('#messageContainer').append(errorDiv);

               $('#jsonFileInput').val(''); // Reset file input
           }
       });
    });

});



function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// Set a timeout to hide success message after 3 seconds
setTimeout(function() {
    $('#messageContainer .alert').fadeOut('slow');
}, 3000);
