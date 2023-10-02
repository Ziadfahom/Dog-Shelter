// Initialize ageSlider for the noUiSlider
const ageSlider = document.getElementById('ageRange');

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
    params.startDateOfArrival = document.getElementById('startDateOfArrival').value;
    params.endDateOfArrival = document.getElementById('endDateOfArrival').value;
    params.breed = document.getElementById('breed').value;
    params.gender = document.getElementById('gender').value;
    params.furColor = document.getElementById('furColor').value;
    params.ageFrom = Math.round(ageSlider.noUiSlider.get()[0]);
    params.ageTo = Math.round(ageSlider.noUiSlider.get()[1]);
    params.startDateOfVaccination = document.getElementById('startDateOfVaccination').value;
    params.endDateOfVaccination = document.getElementById('endDateOfVaccination').value;
    params.isNeutered = document.getElementById('isNeutered').value;
    params.isDangerous = document.getElementById('isDangerous').value;
    params.kongstartDateAdded = document.getElementById('kongstartDateAdded').value;
    params.kongendDateAdded = document.getElementById('kongendDateAdded').value;
    params.owner = document.getElementById('owner').value;


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

    // Update the URL with the new parameter and refresh the table
    updateURL(params.page, params.sort_by, searchQuery || '', params.startDateOfArrival, params.endDateOfArrival, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo, params.startDateOfVaccination, params.endDateOfVaccination, params.isNeutered, params.isDangerous, params.kongstartDateAdded, params.kongendDateAdded, params.owner);
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

      // Update the URL to reflect the new state.
      updateURL(pageNumber, params.sort_by, params.dogName || '', params.startDateOfArrival, params.endDateOfArrival, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo, params.startDateOfVaccination, params.endDateOfVaccination, params.isNeutered, params.isDangerous, params.kongstartDateAdded, params.kongendDateAdded, params.owner);

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
    document.getElementById('startDateOfArrival').value = params.startDateOfArrival || '';
    document.getElementById('endDateOfArrival').value = params.endDateOfArrival || '';
    document.getElementById('breed').value = params.breed || '';
    document.getElementById('gender').value = params.gender || '';
    document.getElementById('furColor').value = params.furColor || '';
    ageSlider.noUiSlider.set([params.ageFrom || 0, params.ageTo || 20]);
    document.getElementById('startDateOfVaccination').value = params.startDateOfVaccination || '';
    document.getElementById('endDateOfVaccination').value = params.endDateOfVaccination || '';
    document.getElementById('isNeutered').value = params.isNeutered || '';
    document.getElementById('isDangerous').value = params.isDangerous || '';
    document.getElementById('kongstartDateAdded').value = params.kongstartDateAdded || '';
    document.getElementById('kongendDateAdded').value = params.kongendDateAdded || '';
    document.getElementById('owner').value = params.owner || '';
  }

  // Refresh the table.
  refreshTable(params, page);  // Apply the filters using the retrieved parameters
}


// Collect filter values and apply them.
function applyFilters() {
  let ageValues = ageSlider.noUiSlider.get();

  let params = {
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

  // Update the URL and refresh the table.
  updateURL(params.page, params.sort_by, params.dogName, params.startDateOfArrival, params.endDateOfArrival, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo, params.startDateOfVaccination, params.endDateOfVaccination, params.isNeutered, params.isDangerous, params.kongstartDateAdded, params.kongendDateAdded, params.owner);
  refreshTable(params, 1);
}


// Reset all filters to their default state.
function resetFilters() {
  document.getElementById('startDateOfArrival').value = '';
  document.getElementById('endDateOfArrival').value = '';
  document.getElementById('breed').selectedIndex = 0;
  document.getElementById('gender').selectedIndex = 0;
  document.getElementById('furColor').selectedIndex = 0;
  document.getElementById('searchInput').value = '';
  ageSlider.noUiSlider.set([0, 20]);
  document.getElementById('startDateOfVaccination').value = '';
  document.getElementById('endDateOfVaccination').value = '';
  document.getElementById('isNeutered').selectedIndex = 0;
  document.getElementById('isDangerous').selectedIndex = 0;
  document.getElementById('kongstartDateAdded').value = '';
  document.getElementById('kongendDateAdded').value = '';
  document.getElementById('owner').selectedIndex = 0;

  // Construct a new URL without query parameters and update the browser's history.
  let newurl = window.location.protocol + "//" + window.location.host + window.location.pathname;
  window.history.pushState({ path: newurl }, '', newurl);

  // Refresh the table with no filters.
  refreshTable({});
}


// Update the URL to reflect the current filter and pagination state.
function updateURL(page, sort_by, dogName, startDateOfArrival, endDateOfArrival, breed, gender, furColor, ageFrom, ageTo, startDateOfVaccination, endDateOfVaccination, isNeutered, isDangerous, kongstartDateAdded, kongendDateAdded, owner) {
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
    // Exporting Dog table as JSON
    $('#exportJsonButton').click(function() {
      // First, fetch the filtered dog IDs
      $.ajax({
          url: '/get_filtered_dog_ids/',
          type: 'GET',
          success: function(response) {
              // Use the filtered dog IDs for exporting
              let filteredDogIDs = response.filtered_dogs_ids;

              // Initiate the export process
              $.ajax({
                  url: '/export_dogs_json/',
                  type: 'POST',
                  data: {'dog_ids': JSON.stringify(filteredDogIDs)},
                  headers: { 'X-CSRFToken': getCookie('csrftoken') },
                  success: function(data) {
                      downloadJSON(data, 'Shelter_dogs_data.json');
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
            success: function(data) {
                let blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8' });
                let link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = 'Shelter_dogs_data.xlsx';
                link.click();
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

                refreshTable(params, 1);
                $('#excelFileInput').val('');  // Reset file input

            },
            error: function(response) {
                // Handle error
                $('#excelFileInput').val('');  // Reset file input
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


function downloadJSON(data, filename) {

    let blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
    let url = window.URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    a.click();
    window.URL.revokeObjectURL(url);
}
