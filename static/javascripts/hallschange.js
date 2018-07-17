jQuery(document).ready(function ($) {
    HallsChange();
    $('.view').click(HallsChange);
    function HallsChange() {
        var data_desc = $(this).attr('data-desc');
        if ($(this).attr('data-desc') == undefined){
            data_desc = 'dark';
        }
        $.ajax({
            type: "GET",
            url: "/halls/hallschange/",
            data:{
                'view': data_desc,
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