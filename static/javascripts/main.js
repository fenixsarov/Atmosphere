$(function () {
  hidePreload();
  let prev_s = $(window).scrollTop();
  var w_height = $(window).height();

  let $header = $('#atm-header');
  let $prlx_img1 = $('#atm-header .parallax-img');
  let $prlx_slogan = $('#atm-header .atm-slogan');
  let $prlx_main = $('#main-content .parallax-img');

  let $carousel = $("#scenery-carousel");

  setInterval(function () {
    slideTo($carousel);
  }, 1500);

  let slogan_start = $prlx_slogan[0].offsetTop;
  let header_height = w_height;

  // $header.height(w_height);

  $(window).on('resize', function () {
    w_height = $(window).height();
    // $header.height(w_height);
    header_height = w_height;
  });

  $(window).scroll(function (e) {
    var cur_s = $(this).scrollTop();
    let direction = (prev_s - cur_s) < 0 ? 1 : -1;

    requestAnimationFrame(function () {
      if (cur_s <= header_height) {
        headerParallax(cur_s);
        // $prlx_main.css('position', 'absolute');
      }
      if (cur_s > header_height) {
        // mainContentParallax( cur_s );
        // $prlx_main.css('position', 'fixed');
      }
    });

    prev_s = cur_s;
  });

  function headerParallax(c_scroll) {
    $prlx_img1.css('top', (c_scroll * 0.5) + 'px');
    // $prlx_slogan.css('top', (slogan_start + c_scroll * 0.3) + 'px');
  }
  function mainContentParallax(c_scroll) {
    $prlx_main.css('top', (c_scroll - header_height) + 'px');
  }
  function sliderSlide() {

  }
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
function slideTo(carousel, number) {
  let item = carousel.find('.item');
  let item_count = item.length;

  item.each(function (i, e) {
    let active = $(e).hasClass('active');

    let w = carousel.width();
    let pos = $(e).position();

    // if (active && (item_count - 1) == i) {
    //   $(e).animate({
    //     'left': `${i * 100}%`
    //   }, 500);
    // } else {
    //   $(e).animate({
    //     'left': `-${}`
    //   }, 500);
    // }
  });
  // console.log(item.position());
}