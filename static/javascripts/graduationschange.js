jQuery(document).ready(function ($) {
    $.ajax({
        type: "GET",
        url: "/graduations/graduationschange/",
        data: {
            'view': 'school',
        },
        dataType: "json",
        cache: false,
        success: function (response) {
            if (response.response == 'ok') {
                $('#graduations_images').html(response.html);
            }
        }
    });
    $('.view').click(GraduationsChange);
    function GraduationsChange() {
        $.ajax({
            type: "GET",
            url: "/graduations/graduationschange/",
            data:{
                'view':$(this).attr('data-desc'),
            },
            dataType: "json",
            cache: false,
            success: function(response){
                if (response.response == 'ok'){
                    $('#graduations_images').html(response.html);
                }
            }
       });
    }
});