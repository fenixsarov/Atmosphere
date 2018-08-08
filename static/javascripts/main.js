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
  $carouselContent.css({
    'height': $carouselContent.width() / 3
  });
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

  var team_img_pos = []
  $('.team-block-image').each(function (val) {
    team_img_pos.push([$(this), $(this).offset().top]);
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

      if (team_img_pos.length) { // Не знаю на сколько это всё оптимально сделано
        let dones = [];
        team_img_pos.forEach(function (value, index) {
          if ((cur_s + w_height / 2) > value[1]) {
            value[0].animate({
              'opacity': 1
            }, 600);
            dones.push(index);
          }
        });
        dones.forEach(function (value) {
          team_img_pos.splice(value, 1);
        });
      }
    });

    prev_s = cur_s;

    // BG Header
  });

  function headerParallax(c_scroll) {
    $prlx_img1.css('top', (c_scroll * 0.5) + 'px');
  }

  function mainContentParallax(c_scroll) {
    $prlx_main.css('top', (c_scroll - header_height) + 'px');
  }

  function sliderSlide() {

  }

  let $bgHeader = $('.atm-navigation__bg-img');
  if ($bgHeader) {
    $navContainer = $('.atm-nav-container');
    $bgHeader.css({
      height: $navContainer[0].offsetHeight + 20,
      width: $navContainer[0].offsetWidth + 20,
      left: -(Number($navContainer.css('padding-left').replace('px', '')) + 10),
      display: 'block'
    })
  }
  ////// Plate events
  bindPlateEvents();
  bindAjaxContentChange();
  bindAjaxReservedForm();

  $('body').on('click', '.atm-overlay', function () {
    $('.atm-overlay').remove();
    $('.atm-reserved-form').remove();
    $('body').css('overflow', 'auto');
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
}

//// AJAX
let subMenuContentAction = {
  'graduations': {
    'url': '/graduations/graduationschange/',
    'default': 'school', // DEFAULT VALUE... remove later
    'success': function (res) {
      $('#graduations_images').html(res.html);
    }
  },
  'sessions': {
    'url': '/halls/sessionschange/',
    'default': 'family', // DEFAULT VALUE... remove later
    'success': function (res) {
      $('#session').html(res.html);
      $('#title').html(res.title);
      $('#desc').html(res.desc);
    }
  },
  'halls': {
    'url': '/halls/hallschange/',
    'default': 'dark', // DEFAULT VALUE... remove later
    'success': function (res) {
      console.log(res);
      $('#hall').html(res.html);
      $('#title').html(res.title);
      $('#desc').html(res.desc);
      $('#hallsize').html('Размер зала: ' + res.hallsize + ' кв.м.');
      $('#price').html('Стоимость аренды зала: <br>' + res.price + 'руб./час');
    }
  }
};

function bindAjaxContentChange() {
  var page = window.location.pathname.replace(/\//g, '');
  if (page in subMenuContentAction) {
    changeSubMenuContent(subMenuContentAction[page].default); // SET DEFAULT VALUE ON PAGE LOAD
    $('.view')
      .first()
      .addClass('active')
      .end()
      .on('click', function (evt) {
        evt.preventDefault();

        $('.view').removeClass('active');

        changeSubMenuContent.call(this);
      });
  }
}

function bindAjaxReservedForm() {
  $('.reserved-btn').on('click', function (evt) {
    evt.preventDefault();
    $.ajax({
      type: "GET",
      url: "/reserved/form",
      dataType: "json",
      cache: false,
      success: function (res) {
        if (res.response === "ok") {
          createOverlay();
          let $html = $(res.html);
          $html
            .css({
              'top': $(window).scrollTop() + 20
            })
            .find('.fa-times')
            .on('click', function () {
              $('.atm-overlay').remove();
              $('.atm-reserved-form').remove();
              $('body').css('overflow', 'auto');
            })
            .end()
            .find('.atm-form__phone')
            .mask("+7(999) 999-9999");

          $('body')
            .css('overflow', 'hidden')
            .append($html);
        }
      }
    });
  })
}

function createOverlay() {
  $('<div></div>')
    .addClass('atm-overlay')
    .appendTo('body');
}

function changeSubMenuContent(data_desc) {
  var page = window.location.pathname.replace(/\//g, '');

  data_desc = data_desc || $(this).attr('data-desc');
  if (data_desc && page in subMenuContentAction) {
    $(this).addClass('active');
    let subMenuObj = subMenuContentAction[page];
    $.ajax({
      type: "GET",
      url: subMenuObj.url,
      data: {
        'view': data_desc,
      },
      dataType: "json",
      cache: false,
      success: function (response) {
        if (response.response == 'ok') {
          subMenuObj.success(response);

          // // ANIMATE SCROLL
          // $('html').animate({
          //   scrollTop: $('.atm-under-menu').offset().top
          // }, 500);
        }
      }
    });
  }
}

jQuery(document).ready(function ($) {
  var partOfPath = document.location.href.split('://')[1].split('/')[1];
  $.ajax({
    type: "GET",
    url: "/" + partOfPath + "/",
    data: {
      'view': partOfPath,
    },
    dataType: "json",
    cache: false,
    success: function (response) {
      if (response.response == 'ok') {
        $('#desc_image').attr('src', '/' + response.image_src);
        $('#title').html(response.title);
        $('#main_text').html(response.main_text);
      }
    }
  });
});