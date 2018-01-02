$(function () {
  hidePreload();
  var prev_s = $(document).scrollTop();
  var w_height = $(window).height();

  let paralax_background = $('.background-paralax');
  var paralax_sl = $('.background-paralax .slogan');

  let def_sl_spos = Number(paralax_sl.css('top').slice(0, -2));

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

    if (cur_s < paralax_background.height()) {
      requestAnimationFrame(function () {
        // paralax_background.css('background-position-y', (0 - (cur_s * 0.3)) + 'px');
        // paralax_background.css('height', (0 - (cur_s * 0.3)) + 'px');
      });
    }
    if (cur_s < sl_y_range.max) {
      requestAnimationFrame(function () {
        paralax_sl.css('top', (def_sl_spos + (cur_s * 0.5)) + 'px');

        if (prev_s > cur_s && sl_y < sl_y_range.min) paralax_sl.css('top', `${sl_y_range.min}px`);
        if (prev_s < cur_s && sl_y > sl_y_range.max) paralax_sl.css('top', `${sl_y_range.max}px`);
      });
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