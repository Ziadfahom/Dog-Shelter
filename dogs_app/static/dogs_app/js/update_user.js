
document.getElementById('customUploadButton').addEventListener('click', function() {
    document.getElementById('id_image').click();
});

document.getElementById('id_image').addEventListener('change', function(e) {
    var file = e.target.files[0];
    var reader = new FileReader();

    reader.onloadend = function() {
        document.getElementById('profile_picture').src = reader.result;
        document.getElementById('image_change_alert').style.display = 'block';  // Show the alert
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        document.getElementById('profile_picture').src = "/static/dogs_app/img/default.jpg";
    }
});

$('#profile_picture').click(function() {
    var imgSrc = $(this).attr('src');
    console.log(imgSrc)
    $('#modal_image').attr('src', imgSrc);
    $('#imageModal').modal('show');
});

function submitUserForm() {
    const form = document.querySelector('.stylish-form');
    form.submit();
}

function goBack() {
    window.history.back();
}