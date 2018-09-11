jQuery(document).ready(function ($) {
    $.ajax({
        type: "GET",
        url: "/about/aboutchange/",
        data: {
            'view': 'about',
        },
        dataType: "json",
        cache: false,
        success: function (response) {
            if (response.response == 'ok') {
                // document.body.appendChild(response.html);
                $('#teamperson_plates').append(response.html);
                bindPlateEvents();
                main();
            }
        }
    });
});