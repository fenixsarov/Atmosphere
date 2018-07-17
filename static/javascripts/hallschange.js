jQuery(document).ready(function ($) {
    $.ajax({
        type: "GET",
        url: "/halls/hallschange/",
        data: {
            'view': 'dark',
        },
        dataType: "json",
        cache: false,
        success: function (response) {
            if (response.response == 'ok') {
                $('#hall').html(response.html);
                $('#title').html(response.title);
                $('#desc').html(response.desc);
                $('#hallsize').html('Размер зала: ' + response.hallsize + ' кв.м.');
            }
        }
    });
    $('.view').click(HallsChange);
    function HallsChange() {
        $.ajax({
            type: "GET",
            url: "/halls/hallschange/",
            data:{
                'view':$(this).attr('data-desc'),
            },
            dataType: "json",
            cache: false,
            success: function (response) {
                if (response.response == 'ok') {
                    $('#hall').html(response.html);
                    $('#title').html(response.title);
                    $('#desc').html(response.desc);
                    $('#hallsize').html('Размер зала: ' + response.hallsize + ' кв.м.');
                }
            }
       });
    }
});