jQuery(document).ready(function ($) {
    SessionChange();
    $('.view').click(SessionChange);
    function SessionChange() {
        var data_desc = $(this).attr('data-desc');
        if ($(this).attr('data-desc') == undefined){
            data_desc = 'family';
        }
        $.ajax({
            type: "GET",
            url: "/halls/sessionschange/",
            data:{
                'view': data_desc,
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