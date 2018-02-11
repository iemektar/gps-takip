$(document).ready(function () {

        var tableElement = $("#dataTable");
        columnList = [
            {
                title: 'Seri No',
                width:'25%'},
            {
                title: 'Plaka No',
                width:'25%'},
            {
                title: 'Aktiflik Durumu',
                width:'25%'
            },
            {
                title: 'İşlemler',
                width:'25%',
                render: function (data) {
                    return generateButton(['Düzenle','Sil'],['btn btn-primary','btn btn-danger'],
                        ['fa fa-pencil-square-o','fa fa-trash'],data.split(','));
                }
            }
        ];
        var situations = [
                {
                    'column': 1,
                    'func': 'length',
                    'minLength': 1,
                    'correctValue': '{-}'
                },
                {
                    'column': 2,
                    'func': 'trueFalse',
                    'trueValue':'Aktif',
                    'falseValue': 'Aktif Değil'
                }
            ];

        var successFunc =  generateSuccessFunc(tableElement,columnList,situations);
        customPostAjax(tableElement.attr('data-link'),{},successFunc);
});
