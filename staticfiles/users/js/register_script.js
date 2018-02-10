$(document).ready(function () {
    username_validated = true;
    $("#username").keyup(function () {
        var username = $("#username");
        $.ajax({

            url: username.attr("validation"),
            data: {
                'username': username.val()
            },
            type: "post",
            dataType: 'json',
            success: function (data) {
                if (data.error_message) {

                    if (username_validated) {
                        username.after('<i id="validationMessage" class="error">Bu kullanıcı adı alındı</i>');
                        username_validated = false;
                    }
                }
                else {
                    username_validated = true;
                    $("#validationMessage").remove();
                }
            }

        });
    });

    $("form").submit(function (e) {
        if (username_validated === false) {
            e.preventDefault();
        }
    });

});