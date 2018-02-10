$(document).ready(function () {

    $("form").validate({

        rules: {
            first_name: {
                required: true,
                lettersonly: true,
                rangelength: [1, 50]
            },
            last_name: {
                required: true,
                lettersonly: true,
                rangelength: [1, 50]
            },
            username: {
                required: true,
                rangelength: [4, 15],
                startingwithnum: true
            },
            password: {
                required: true,
                rangelength: [4, 50]
            },
            re_password: {
                required: true,
                equalTo: "#password"
            },
            email: {
                required: true,
                email: true
            },
            permissions: {
                selectvalidation: true
            }

        },
        messages: {

            first_name: "Ad alanı sadece harflerden oluşmalı, boş bırakılamaz ve en falza 50 karakter uzunluğunda olmalıdır.",
            last_name: "Soyad alanı sadece harflerden oluşmalı, boş bırakılamaz" +
            " ve en falza 50 karakter uzunluğunda olmalıdır.",

            username: "Kullanıcı adı boş bırakılamaz ve sayı ile başlayamaz. " +
            "Karakter uzunluğu 4-15 arasında olmalıdır.",

            password: "Parola boş bırakılamaz. Karakter uzunluğu 4-50 " +
            "arasında olmalıdır.",

            re_password: "Parolalar uyuşmuyor.",

            email: "Geçerli bir mail adresi giriniz." + "\n"

        },
        highlight: function (element) {
            $(element).addClass("error-input");
        },
        unhighlight: function (element) {
            $(element).removeClass("error-input");
        }


    });

});