// This script is run when the document is fully loaded.
$(document).ready(function() {
    // Initialize tooltips with a custom configuration.
    // The tooltip trigger is set to 'hover', so the tooltip will be shown when the mouse hovers over the element.
    // The tooltip boundary is set to 'window', so the tooltip will not overflow the window.
    // The tooltip's HTML is enabled, so you can use HTML tags in the tooltip.
    // The tooltip animation is disabled for performance reasons.
    // The tooltip is added to the 'body' container to ensure that it is not confined by the layout of the page.
    // The placement function is used to determine the position of the tooltip based on the position of the mouse.
    $('[data-bs-toggle="tooltip"]').tooltip({
        trigger: 'hover',
        boundary: 'window',
        html: true,
        animation: false,
        container: 'body',
        placement: function(context, source){
            var position = $(source).offset();
            if (position.left < 515){
                return "right";
            }
            if (position.left > 515){
                return "left";
            }
            if (position.top < 110){
                return "bottom";
            }
            return "top";
        }
    });

    // When a row with the class 'dog-row' is clicked, the user is redirected to the URL specified in the 'data-href' attribute of the row.
    $(".dog-row").click(function() {
        window.location = $(this).data("href");
    });
});