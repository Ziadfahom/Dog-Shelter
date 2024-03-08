$(document).ready(function() {
    // Capture the height of the User Profile div
    var userProfileHeight = $("#user-profile").height();

    // Set the height of the news section
    $("#news-section").css("max-height", userProfileHeight*0.84);

    // Make the news section scrollable
    $("#news-section").css("overflow-y", "auto");

    document.getElementById("voteForm").addEventListener("submit", function(event) {
        var selectedChoice = document.querySelector('input[name="choice"]:checked');
        
        if (!selectedChoice) {
            alert("Please select an option before voting.");
            event.preventDefault();
        }
    });

});
