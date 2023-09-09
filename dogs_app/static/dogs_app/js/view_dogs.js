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
    params.startDate = document.getElementById('startDate').value;
    params.endDate = document.getElementById('endDate').value;
    params.breed = document.getElementById('breed').value;
    params.gender = document.getElementById('gender').value;
    params.furColor = document.getElementById('furColor').value;
    params.ageFrom = Math.round(ageSlider.noUiSlider.get()[0]);
    params.ageTo = Math.round(ageSlider.noUiSlider.get()[1]);
    params.vacStartDate = document.getElementById('vacStartDate').value;
    params.vacEndDate = document.getElementById('vacEndDate').value;
    params.isNeutered = document.getElementById('isNeutered').value;
    params.isDangerous = document.getElementById('isDangerous').value;
    params.kongStartDate = document.getElementById('kongStartDate').value;
    params.kongEndDate = document.getElementById('kongEndDate').value;
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
    updateURL(params.page, params.sort_by, searchQuery || '', params.startDate, params.endDate, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo, params.vacStartDate, params.vacEndDate, params.isNeutered, params.isDangerous, params.kongStartDate, params.kongEndDate, params.owner);
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
      updateURL(pageNumber, params.sort_by, params.dogName || '', params.startDate, params.endDate, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo, params.vacStartDate, params.vacEndDate, params.isNeutered, params.isDangerous, params.kongStartDate, params.kongEndDate, params.owner);

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
    document.getElementById('startDate').value = params.startDate || '';
    document.getElementById('endDate').value = params.endDate || '';
    document.getElementById('breed').value = params.breed || '';
    document.getElementById('gender').value = params.gender || '';
    document.getElementById('furColor').value = params.furColor || '';
    ageSlider.noUiSlider.set([params.ageFrom || 0, params.ageTo || 20]);
    document.getElementById('vacStartDate').value = params.vacStartDate || '';
    document.getElementById('vacEndDate').value = params.vacEndDate || '';
    document.getElementById('isNeutered').value = params.isNeutered || '';
    document.getElementById('isDangerous').value = params.isDangerous || '';
    document.getElementById('kongStartDate').value = params.kongStartDate || '';
    document.getElementById('kongEndDate').value = params.kongEndDate || '';
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
    'startDate': document.getElementById('startDate').value || '',
    'endDate': document.getElementById('endDate').value || '',
    'breed': document.getElementById('breed').value || '',
    'gender': document.getElementById('gender').value || '',
    'furColor': document.getElementById('furColor').value || '',
    'ageFrom': Math.round(ageValues[0]) || 0,
    'ageTo': Math.round(ageValues[1]) || 20,
    'vacStartDate': document.getElementById('vacStartDate').value || '',
    'vacEndDate': document.getElementById('vacEndDate').value || '',
    'isNeutered': document.getElementById('isNeutered').value || '',
    'isDangerous': document.getElementById('isDangerous').value || '',
    'kongStartDate': document.getElementById('kongStartDate').value || '',
    'kongEndDate': document.getElementById('kongEndDate').value || '',
    'owner': document.getElementById('owner').value || ''
  };

  // Update the URL and refresh the table.
  updateURL(params.page, params.sort_by, params.dogName, params.startDate, params.endDate, params.breed, params.gender, params.furColor, params.ageFrom, params.ageTo, params.vacStartDate, params.vacEndDate, params.isNeutered, params.isDangerous, params.kongStartDate, params.kongEndDate, params.owner);
  refreshTable(params, 1);
}


// Reset all filters to their default state.
function resetFilters() {
  document.getElementById('startDate').value = '';
  document.getElementById('endDate').value = '';
  document.getElementById('breed').selectedIndex = 0;
  document.getElementById('gender').selectedIndex = 0;
  document.getElementById('furColor').selectedIndex = 0;
  document.getElementById('searchInput').value = '';
  ageSlider.noUiSlider.set([0, 20]);
  document.getElementById('vacStartDate').value = '';
  document.getElementById('vacEndDate').value = '';
  document.getElementById('isNeutered').selectedIndex = 0;
  document.getElementById('isDangerous').selectedIndex = 0;
  document.getElementById('kongStartDate').value = '';
  document.getElementById('kongEndDate').value = '';
  document.getElementById('owner').selectedIndex = 0;

  // Construct a new URL without query parameters and update the browser's history.
  let newurl = window.location.protocol + "//" + window.location.host + window.location.pathname;
  window.history.pushState({ path: newurl }, '', newurl);

  // Refresh the table with no filters.
  refreshTable({});
}


// Update the URL to reflect the current filter and pagination state.
function updateURL(page, sort_by, dogName, startDate, endDate, breed, gender, furColor, ageFrom, ageTo, vacStartDate, vacEndDate, isNeutered, isDangerous, kongStartDate, kongEndDate, owner) {
  const url = new URL(window.location);
  url.searchParams.set('page', page || '');
  url.searchParams.set('sort_by', sort_by || '-dateOfArrival');
  url.searchParams.set('dogName', dogName || '');
  url.searchParams.set('startDate', startDate || '');
  url.searchParams.set('endDate', endDate || '');
  url.searchParams.set('breed', breed || '');
  url.searchParams.set('gender', gender || '');
  url.searchParams.set('furColor', furColor || '');
  url.searchParams.set('ageFrom', ageFrom || '');
  url.searchParams.set('ageTo', ageTo || '');
  url.searchParams.set('vacStartDate', vacStartDate || '');
  url.searchParams.set('vacEndDate', vacEndDate || '');
  url.searchParams.set('isNeutered', isNeutered || '');
  url.searchParams.set('isDangerous', isDangerous || '');
  url.searchParams.set('kongStartDate', kongStartDate || '');
  url.searchParams.set('kongEndDate', kongEndDate || '');
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
