$(document).ready(function(){
    var allContainers = [
        '#treatments_container',
        '#examinations_container',
        '#observations_container',
        '#placements_container'
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
});

function goBack() {
    window.history.back();
}