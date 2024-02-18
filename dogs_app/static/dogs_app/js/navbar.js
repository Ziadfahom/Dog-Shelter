document.addEventListener("DOMContentLoaded", function() {
    const branchToggle = document.getElementById('branch-toggle');
    if (branchToggle) {
        branchToggle.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = toggleBranchUrl;
        });
    }
});
