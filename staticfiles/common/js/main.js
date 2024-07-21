$(document).ready(function () {
  $(".custom-dropdown").on("show.bs.dropdown", function () {
    var that = $(this);
    setTimeout(function () {
      that.find(".dropdown-menu").addClass("active");
    }, 100);
  });

  $(".custom-dropdown").on("hide.bs.dropdown", function () {
    $(this).find(".dropdown-menu").removeClass("active");
  });
});

// Set timeout for alert message
document.addEventListener('DOMContentLoaded', (event) => {
    let messageElement = $('#base-message-alert');

    if (messageElement) {
        let timeout = messageElement.hasClass('alert-danger') ? 6000 : 3000;
        setTimeout(function() {
            messageElement.fadeOut('slow');
        }, timeout);
    }
});
