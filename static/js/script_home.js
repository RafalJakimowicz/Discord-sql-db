$(document).ready(function () {
    $("#logout-icon").load("{{ url_for('static', filename='images/cross.svg') }}", function (){
        $("#logout-icon svg").addClass("logout-icon");
    });

    $("#logout-icon").click(function () {
        window.location.href = '/logout'

        $.ajax({
            type: "POST",
            url: "/login",
            contentType: "application/json",
            data: JSON.stringify({ user_name: name, user_password: password }),
            success: function (response) {
                if(response.redirect) {
                    window.location.href = response.redirect;
                } 
            },
            error: function () {
                alert("Error processing request!");
            }
        });
    });
});
