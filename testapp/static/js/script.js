$(document).ready(function() {
    $('#registerForm').submit(function(event) {
        event.preventDefault(); // Ngừng hành động mặc định của form (không reload trang)

        const username = $('#username').val();
        const password = $('#password').val();
        const email = $('#email').val();

        $.ajax({
            url: 'http://127.0.0.1:5000/register', // URL API của Flask
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password,
                email: email
            }),
            success: function(response) {
                $('#message').text(response.message).css('color', 'green');
            },
            error: function(error) {
                $('#message').text(error.responseJSON.error).css('color', 'red');
            }
        });
    });
});
