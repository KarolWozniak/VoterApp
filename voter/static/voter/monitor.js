var votes = [];

function compare(array1, array2) {
    for (var i = 0; i < array1.length; i++) {
        if (array1[i] != array2[i])
            return false;
    }
    return true;
}

function getData() {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: window.location.href,
        success: function(data) {
            var obj = JSON.parse(data);
            var values = Object.keys(obj).map(function(key) {
                return obj[key];
            });
            if (compare(values, votes)) {
                var votingValues = document.getElementsByClassName("values");
                var index = 0;
                $.each(values, function(i, field) {
                    votingValues[index++].innerHTML = field;
                });
            } else {
                votes = values;
            }
        },
    });
};
setInterval(function() {
    getData()
}, 5000);