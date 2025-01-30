$(document).ready(function () {
    $("#submitBtn").click(function () {
        $("#submitBtn").css("border", "2px solid #ffffff");

        setTimeout(function () {
            $("#submitBtn").css("border", "2px solid #cccccc");
        }, 100);

        event.preventDefault();
        var name = $("#usenameInput").val(); 
        var password = $("#passwordInput").val();

        $.ajax({
            type: "POST",
            url: "/login",
            contentType: "application/json",
            data: JSON.stringify({ user_name: name, user_password: password }),
            success: function (response) {
                if(response.redirect) {
                    window.location.href = response.redirect;
                } else {
                    $("#responseMessage").text(response.error);
                }
            },
            error: function () {
                alert("Error processing request!");
            }
        });
    });
});
