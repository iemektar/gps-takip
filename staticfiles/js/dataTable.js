function correctData(data, situations) {

    for(var i = 0; i<data.length;i++)
    {
        for(var j=0; j<situations.length;j++)
        {
            var dataItem = data[i][situations[j]['column']];
            var sItem = situations[j];

            if(sItem['func'] === 'length')
                dataItem = lengthCorrection(dataItem,sItem['minLength'],sItem['correctValue']);
            else if(sItem['func'] === 'trueFalse')
                dataItem = trueFalseCorrection(dataItem,sItem['trueValue'],sItem['falseValue']);

            data[i][situations[j]['column']] = dataItem;
        }
    }

    return data;
}

function lengthCorrection(data,minLength, correctValue) {

    if(data.length < minLength)
        data = correctValue;
    return data;
}

function trueFalseCorrection(data,trueValue,falseValue) {

    if(data === true)
        data = trueValue;
    else if(data === false)
        data = falseValue;
    return data;
}


function generateButton(buttonText, buttonClass, buttonIcon,url) {
    if(buttonText.length === buttonClass.length && buttonClass.length  === url.length && url.length=== buttonIcon.length) {
        var buttons = "";
        for (var i = 0; i < buttonText.length; i++)
            buttons += "<a class='" + buttonClass[i] + "' href='" + url[i] + "' >" +"" +
                "<i class='"+buttonIcon[i]+"'></i> &nbsp;"+ buttonText[i] + "</a> &nbsp;";
        return buttons;
    }

    return "Count of lists not equal each other.";
}

function customAjax (url,data, type,dataType, successFunc) {

    $.ajax({
        'url': url,
        'data': data,
        'type': type.toLowerCase(),
        'dataType': dataType.toLowerCase(),
        success: successFunc
    });

}

function customPostAjax(url,data,successFunc) {
    customAjax(url,data,'post','json',successFunc);
}

function generateSuccessFunc(tableElement,columnList,dataSituations) {

    var successFunc = function (dataSet) {
        dataSet = correctData(dataSet.data,dataSituations);
        tableElement.DataTable(
            {
                data: dataSet,
                columns: columnList
            }
        );
    };
    return successFunc;
}
