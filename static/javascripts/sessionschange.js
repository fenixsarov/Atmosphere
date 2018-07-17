jQuery(document).ready(function ($) {
        $.ajax({
        type: "GET",
        url: "/halls/sessionschange/",
        data: {
            'view': 'family',
        },
        dataType: "json",
        cache: false,
        success: function (response) {
            if (response.response == 'ok') {
                $('#session').html(response.html);
                $('#title').html(response.title);
                $('#desc').html(response.desc);
            }
        }
    });
    $('.view').click(HallsChange);
    function HallsChange() {
        $.ajax({
            type: "GET",
            url: "/halls/sessionschange/",
            data:{
                'view':$(this).attr('data-desc'),
            },
            dataType: "json",
            cache: false,
            success: function (response) {
            if (response.response == 'ok') {
                $('#session').html(response.html);
                $('#title').html(response.title);
                $('#desc').html(response.desc);
            }
        }
       });
    }
});