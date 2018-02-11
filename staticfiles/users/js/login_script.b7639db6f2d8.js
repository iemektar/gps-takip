$(document).ready(function () {
    
    $("form").validate({
        rules: {

            username: {
                required: true,
                rangelength: [4, 15],
                startingwithnum: true
            },
            password: {
                required: true,
                rangelength: [4, 50]
            }
        },
        messages: {
            username: "Boş bırakılamaz ve sayı ile başlayamaz. 4-15 Karakter aralığında olmalıdır.",
            password: "Boş bırakılamaz. 4-50 Karakter aralığında olmalıdır."
        },
        highlight: function (element) {
            $(element).addClass("error-input");
        },
        unhighlight: function (element) {
            $(element).removeClass("error-input");
        }
    });
});
