$(document).ready(function () {
    var tableElement = $("#dataTable");
        columnList = [
            {
                title: 'İsim',
                width:'15%'},
            {
                title: 'Soyisim',
                width:'15%'},
            {
                title: 'Kullanıcı Adı',
                width:'15%'
            },

            {
                title: 'Email',
                width:'15%'
            },

            {
                title: 'Yetki',
                width:'20%'
            },

            {
                title: 'İşlemler',
                width:'20%',
                render: function (data) {
                    return generateButton(['Düzenle','Sil'],['btn btn-primary','btn btn-danger'],['fa fa-pencil-square-o','fa fa-trash'],data.split(','));
                }
            }
        ];
        var situations = [];
        var successFunc =  generateSuccessFunc(tableElement,columnList,situations);
        customPostAjax(tableElement.attr('data-link'),{},successFunc);
});