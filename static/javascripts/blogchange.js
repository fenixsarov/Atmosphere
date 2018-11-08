jQuery(document).ready(function ($) {
    $.ajax({
        type: "GET",
        url: "/blog/blogchange/",
        data: {
            'view': 'blog',
        },
        dataType: "json",
        cache: false,
        success: function (response) {
            if (response.response == 'ok') {
               $('#blog_plates').html(response.html);
               bindPlateEvents();
            }
        }
    });
});