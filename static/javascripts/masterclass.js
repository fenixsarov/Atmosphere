jQuery(document).ready(function ($) {
    $.ajax({
        type: "GET",
        url: "/masterclass/masterclasschange/",
        data: {
            'view': 'masterclass',
        },
        dataType: "json",
        cache: false,
        success: function (response) {
            if (response.response == 'ok') {
                console.log(response.html);
               $('#masterclass_plates').html(response.html);
               bindPlateEvents();
            }
        }
    });
});