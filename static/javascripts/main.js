$(function () {
  hidePreload();
  var prev_s = $(document).scrollTop();
  var w_height = $(window).height();

  var paralax_sl = $('.background-paralax .slogan');

  var sl_y_range = {
    min: Number(paralax_sl.css('top').slice(0, -2)),
    max: w_height - paralax_sl.height() - 5
  };

  $('.background-paralax').height(w_height);

  $(window).on('resize', function () {
    w_height = $(window).height();
    $('.background-paralax').height(w_height);
  });

  $(window).scroll(function (e) {
    var cur_s = $(this).scrollTop();
    var delta = prev_s - cur_s;

    if (cur_s < sl_y_range.max) {
      var sl_y = Number(paralax_sl.css('top').slice(0, -2));
      sl_y -= delta / 2;
      paralax_sl.css({
        'top': `${sl_y}px`
      });

      if (prev_s > cur_s && sl_y < sl_y_range.min) paralax_sl.css('top', `${sl_y_range.min}px`);
      if (prev_s < cur_s && sl_y > sl_y_range.max) paralax_sl.css('top', `${sl_y_range.max}px`);
    }
    prev_s = cur_s;
  });
});

function hidePreload() {
  $('#preloader').fadeOut('slow', function () {
    $('body').css({
      'overflow': 'visible'
    });
    startPage();
  });
}
function startPage() {
  $('.background-paralax .slogan').animate({
    opacity: '1'
  }, 700);
}