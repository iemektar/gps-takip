$(document).ready(function () {

    $("form").validate({

        rules:{
            serial_no: {
                required: true,
                rangelength: [1, 50]
            },
            plate_no: {
                required: false,
                rangelength: [7,9]
            }
        },
        messages: {
            serial_no : "Seri No alanı zorunlu bir alandır ve 1-50 karakter arasında olmalıdır.",
            plate_no: "Plaka No alanı 7 veya 8 karakter uzunluğunda olmalıdır."
        },
        highlight: function (element) {
            $(element).addClass("error-input");
        },
        unhighlight: function (element) {
            $(element).removeClass("error-input");
        }
    });

});