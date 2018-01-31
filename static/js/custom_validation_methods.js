$(document).ready(function () {
    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return /^[A-Za-zıIİÖöÜüŞşÇçĞğ]+$/i.test(value);
    }, "Sadece harflerden oluşmalıdır.");

    jQuery.validator.addMethod("startingwithnum", function (value, element) {
        return /^[A-Za-z][A-Za-z0-9]*$/i.test(value);
    }, "Sayı ile başlayamaz");

    jQuery.validator.addMethod("selectvalidation", function (value, element) {
        if (value == 'none')
            return false;
        else
            return true;
    }, "Lütfen bir seçim yapınız");
});