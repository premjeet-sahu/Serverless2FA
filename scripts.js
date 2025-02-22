var API_ENDPOINT = "https://g3fnf5lxl5.execute-api.us-east-2.amazonaws.com/Production";

// AJAX POST request to generate token data
document.getElementById("generateToken").onclick = function(){
    var inputData = {
        "user_id": $('#user_id').val()
    };
    $.ajax({
        url: API_ENDPOINT,
        type: 'POST',
        data:  JSON.stringify(inputData),
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            document.getElementById("tokenSaved").innerHTML = "Token Generated!";
        },
        error: function () {
            alert("Error generating security token.");
        }
    });
}

// AJAX GET request to retrieve all tokens
document.getElementById("retrieveToken").onclick = function(){  
    $.ajax({
        url: API_ENDPOINT,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            $('#tokenData tr').slice(1).remove();
            jQuery.each(response, function(i, data) {          
                $("#tokenData").append("<tr> \
                    <td>" + data['user_id'] + "</td> \
                    <td>" + data['token'] + "</td> \
                    <td>" + data['expiry_time'] + "</td> \
                    </tr>");
            });
        },
        error: function () {
            alert("Error retrieving security token.");
        }
    });
}
