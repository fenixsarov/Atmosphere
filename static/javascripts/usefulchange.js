jQuery(document).ready(function ($) {
    $.ajax({
        type: "GET",
        url: "/useful/usefulchange/",
        data: {
            'view': 'useful',
        },
        dataType: "json",
        cache: false,
        success: function (response) {
            if (response.response == 'ok') {
                $('#useful_plates').html(response.html);
                bindPlateEvents();
            }
        }
    });
});