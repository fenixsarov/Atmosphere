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
               $('#masterclass_plates').html(response.html);
               bindPlateEvents();
            }
        }
    });
});