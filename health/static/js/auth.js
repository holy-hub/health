$(document).ready(function () {
    const container = $('#container');
    const registerBtn = $('#register');
    const loginBtn = $('#login');

    registerBtn.click(function() {
        container.addClass("active");
    });

    loginBtn.click(function() {
        container.removeClass("active");
    });
});