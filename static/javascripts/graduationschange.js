jQuery(document).ready(function ($) {
    GraduationsChange();
    $('.view').click(GraduationsChange);
    function GraduationsChange() {
        var data_desc = $(this).attr('data-desc');
        if ($(this).attr('data-desc') == undefined){
            data_desc = 'school';
        }
        $.ajax({
            type: "GET",
            url: "/graduations/graduationschange/",
            data:{
                'view': data_desc,
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