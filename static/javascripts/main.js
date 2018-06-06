let $carouselContent = null,
  carouselIsAnimate = null,
  carouselIndex = null,
  carouselContentChild = null,
  carouselLength = null,
  carouselLastItem = null,
  carouselFirstItem = null,
  autoSlide = null;

$(function () {
  hidePreload();
  let prev_s = $(window).scrollTop();
  var w_height = $(window).height();

  let $header = $('#atm-header');
  let $prlx_img1 = $('#atm-header-slogan-section .parallax-img');

  // CAROUSEL
  $carouselContent = $("#scenery-carousel .content");
  carouselIsAnimate = false;
  carouselIndex = 0;
  carouselContentChild = $carouselContent.children();
  carouselLength = carouselContentChild.length;
  carouselLastItem = carouselContentChild[carouselLength - 1];
  carouselFirstItem = $carouselContent.children()[0];

  $('.carousel-control.left').on('click', function (e) {
    slideLeft();
  });
  $('.carousel-control.right').on('click', function (e) {
    slideRight();
  });
  $('#scenery-carousel')
    .on('mouseover', function () {
      clearInterval(autoSlide);
    }).on('mouseout', function () {
      autoRotateSlide();
    });

  autoRotateSlide();

  let header_height = w_height;

  $(window).on('resize', function () {
    w_height = $(window).height();
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
  }

  function mainContentParallax(c_scroll) {
    $prlx_main.css('top', (c_scroll - header_height) + 'px');
  }

  function sliderSlide() {

  }


  ////// Plate events
  bindPlateEvents();
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

function autoRotateSlide() {
  autoSlide = setInterval(function () {
    slideRight();
  }, 2500);
}

function slideRight() {
  if (carouselIsAnimate) {
    return;
  }
  carouselIsAnimate = true;
  carouselIndex++;

  if (carouselIndex >= carouselLength) {
    carouselContentChild.each(function (i) {
      $(this).animate({
        'left': i * $(this).width()
      }, 1000, function () {
        carouselIsAnimate = false;
      });
    });
    carouselIndex = 0;
  } else {
    carouselContentChild.each(function (i) {
      $(this).animate({
        'left': $(this).position().left - $(this).width()
      }, 1000, function () {
        carouselIsAnimate = false;
      });
    });
  }
}

function slideLeft(carousel) {
  if (carouselIsAnimate) {
    return;
  }
  carouselIsAnimate = true;
  carouselIndex--;

  if (carouselIndex < 0) {
    carouselContentChild.each(function (i) {
      $(this).animate({
        'left': $(this).position().left - (carouselLength - 1) * $(this).width()
      }, 1000, function () {
        carouselIsAnimate = false;
      });
    });
    carouselIndex = carouselLength - 1;
  } else {
    carouselContentChild.each(function (i) {
      $(this).animate({
        'left': $(this).position().left + $(this).width()
      }, 1000, function () {
        carouselIsAnimate = false;
      });
    });
  }
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

function bindPlateEvents() {
  $('.plate_new')
    .each(function () {
      $(this).css({
        'min-height': '286px',
        'height': '286px',
        'max-height': '286px'
      });
    });
  // $('.plate__more-btn')
  //   .on('click', function (evt) {
  //     let $parentPlate = $(this).closest('.plate');
  //     let $plate = $parentPlate.clone();

  //     $plate
  //       .css({
  //         'top': $parentPlate.offset().top,
  //         'left': $parentPlate.offset().left,
  //         'width': $parentPlate.width()
  //       })
  //       .appendTo('body')
  //       .wrap('<div class="full-plate__content container"></div>')
  //       // .wrap('<div class="col-md"></div>')
  //       // .wrap('<div class="row"></div>')
  //       // .wrap('<div class="container"></div>')
  //       .animate({
  //         'left': 0,
  //         'right': 0,
  //         'top': $(window).scrollTop(),
  //         'bottom': 0,
  //         'borderRadius': 0,
  //         'width': $(window).width()
  //       })


  //     // let $fullPlate = null;
  //     // let plate_img = $plate.find('.plate__img-preview').clone();
  //     // let plate_header = $plate.find('.header').clone();
  //     // let plate_description = $plate.find('.description').clone();
  //     // let close_btn = $('<a class="full-plate__close-btn far fa-times-circle"></a>')
  //     //   .one('click', function (evt) {
  //     //     $fullPlate.animate({
  //     //       'top': -$($fullPlate).height()
  //     //     }, 300, function () {
  //     //       $(this).remove();
  //     //       $('body').css('overflow', 'auto');
  //     //     });
  //     //   });


  //     // let $tmpDiv = $('<div class="full-plate__content container">')

  //     // // .append(close_btn)
  //     // // .append(plate_img)
  //     // // .append(plate_header)
  //     // // .append(plate_description)
  //     // // .append(plate_description.clone())
  //     // // .append(plate_description.clone());

  //     // $fullPlate = $('<div>')
  //     //   .addClass('full-plate')
  //     //   .append($tmpDiv);

  //     // $('body').css('overflow', 'hidden');

  //     // $fullPlate
  //     //   .appendTo('body')
  //     //   .css({
  //     //     'top': $(window).scrollTop() - $(window).height(),
  //     //     'visibility': 'visible'
  //     //   })
  //     //   .animate({
  //     //     'top': $(window).scrollTop()
  //     //   }, 500);
  //   });
}