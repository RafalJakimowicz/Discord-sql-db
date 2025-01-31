$(document).ready(function () {

    function loadDatabaseData(tab) {

        $.ajax({
            url: `http://127.0.0.1:5000/fetch_data?tab=${tab}`,
            type: "GET",
            dataType: "json",
            success: function (data) {
                let tableId = `#table${tab.replace("tab", "")} tbody`;
                $(tableId).empty(); // Clear old data

                data.forEach(row => {
                    let tr = "<tr>";
                    for (let key in row) {
                        tr += `<td padding="5px 5px">${row[key]}</td>`;
                    }
                    tr += "</tr>";
                    $(tableId).append(tr);
                });
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", status, error);
                alert("Failed to fetch data. Check console for details.");
            }
        });
    }

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

    $(".tab-btn").click(function () {
        let tabId = $(this).attr("data-tab");

        // Remove active class from all buttons and add to the clicked one
        $(".tab-btn").removeClass("active");
        $(this).addClass("active");

        // Hide all tab panes and show the selected one
        $(".tab-pane").removeClass("active");
        $("#" + tabId).addClass("active");
        loadDatabaseData(tabId);
    });

    loadDatabaseData("tab1");
});
