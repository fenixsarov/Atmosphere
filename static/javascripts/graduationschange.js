jQuery(document).ready(function ($) {
    $('.view').click(GraduationsChange);
    function GraduationsChange() {
        $.ajax({
            type: "GET",
            url: "/graduations/graduationschange/",
            data:{
                'view':$(this).attr('data-descc'),
            },
            dataType: "html",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    location.reload();
                }
            }
       });
    }
});