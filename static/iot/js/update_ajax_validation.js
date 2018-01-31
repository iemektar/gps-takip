$(document).ready(function () {

    plate_no_validated = true;
    $("#plate_no").keyup(function () {
        var plate_no = $("#plate_no");
        if (plate_no.val().length <= 0)
            return;
        $.ajax({

            url: plate_no.attr("validation"),
            data: {
                'type': 'update',
                'plate_no': plate_no.val(),
                'serial_no': $("#serial_no").val()
            },
            type: "post",
            dataType: 'json',
            success: function (data) {
                if (data.error_message) {

                    if (plate_no_validated) {
                        plate_no.after('<i id="plateNoValidationMessage" class="error">' + data.error_message + '</i>');
                        plate_no_validated = false;
                    }
                }
                else {
                    plate_no_validated = true;
                    $("#plateNoValidationMessage").remove();
                }
            }

        });
    });

    $("form").submit(function (e) {
        if (plate_no_validated === false) {
            e.preventDefault();
        }
    });
});