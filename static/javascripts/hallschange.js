jQuery(document).ready(function ($) {
    $('.view').click(HallsChange);
    function HallsChange() {
        $.ajax({
            type: "GET",
            url: "/halls/hallschange/",
            data:{
                'view':$(this).attr('data-desc'),
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