var $carouselContent = null,
  carouselIsAnimate = null,
  carouselIndex = null,
  carouselContentChild = null,
  carouselLength = null,
  carouselLastItem = null,
  carouselFirstItem = null,
  autoSlide = null;

var first_submenu_load = true;

$(document).ready(function () {
  var prev_s = $(window).scrollTop();
  var w_height = $(window).height();
  var w_width = $(window).width();

  var $header = $('#atm-header');
  var $prlx_img1 = $('#atm-header-slogan-section .parallax-img');
  var $prlx_blog_img = $('.blog-header .blog-item__bg');

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

  bindTopPageBtn();
  autoRotateSlide();
  var header_height = w_height;

  $(window).on('resize', function () {
    w_height = $(window).height();
    header_height = w_height;

    // Жуткий костыль какой-то конечно
    checkMobileTopPadding();
  });

  var team_img_pos = [];
  $('.team-block-image').each(function (val) {
    team_img_pos.push([$(this), $(this).offset().top]);
  });

  $(window).scroll(function (e) {
    var cur_s = $(this).scrollTop();
    var direction = (prev_s - cur_s) < 0 ? 1 : -1;
    var $topBtn = $('.atm-toppage-btn');

    requestAnimationFrame(function () {
      if (cur_s <= header_height) {
        if (w_width > 1104) {
          headerParallax(cur_s);
          $prlx_blog_img.css('top', (cur_s * 0.5) + 'px');
        }
        $('.aeWidgetBtn').css({
          'display': 'none',
          'opacity': '0'
        });
        $topBtn.css({
          'display': 'none',
          'opacity': '0'
        });
      }
      if (cur_s > header_height) {
        $('.aeWidgetBtn').css({
          'display': 'block',
          'opacity': '1'
        });
        $topBtn.css({
          'display': 'block',
          'opacity': '.5'
        });
      }

      if (team_img_pos.length) { // Не знаю на сколько это всё оптимально сделано
        var dones = [];
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

  var $bgHeader = $('.atm-navigation__bg-img');
  if ($bgHeader) {
    $navContainer = $('.atm-nav-container');
    $bgHeader.css({
      height: $navContainer[0].offsetHeight + 20,
      width: $navContainer[0].offsetWidth + 20,
      left: -(Number($navContainer.css('padding-left').replace('px', '')) + 10),
      display: 'block'
    });
  }

  ////// Plate events
  bindPlateEvents();
  bindAjaxContentChange();
  bindAjaxReservedForm();
  $('body').on('click', function (e) {
    if ($(e.target).hasClass('.atm-overlay')) {
      $('.atm-overlay').remove();
      $('.atm-reserved-form').remove();
      $('body').css('overflow', 'auto');
      return;
    }

    if ($('.atm-nav_mobile').hasClass('active')) {
      $('.atm-nav_mobile').removeClass('active');
    }
  });

  $('.atm-menu-mobile__btn').on('click', function (e) {
    e.preventDefault();
    e.stopPropagation();

    $(this).closest('.atm-nav-container_mobile').toggleClass('active');
    $('.atm-under-menu-panel').toggleClass('active');
    $('.atm-menu-submenu-btn_mobile')
      .removeClass('active')
      .next('.atm-menu-submenu_mobile')
      .slideUp()
      .end()
      .children('i')
      .removeClass('active');
  });
  $('.atm-nav_mobile').on('click', function (e) {
    e.stopPropagation();
  });
  $('.atm-menu-submenu-btn_mobile').on('click', function (e) {
    if ($(this).hasClass('active')) {
      $(this)
        .removeClass('active')
        .next('.atm-menu-submenu_mobile')
        .slideUp()
        .end()
        .children('i')
        .removeClass('active');
    } else {
      $(this)
        .addClass('active')
        .next('.atm-menu-submenu_mobile')
        .slideDown()
        .end()
        .children('i')
        .addClass('active');
    }
  });

  checkMobileTopPadding();
});

function bindTopPageBtn() {
  var $topBtn = $('.atm-toppage-btn');
  $topBtn.on('click', function (evt) {
    $('html, body').stop().animate({
      scrollTop: 0
    }, 777);
  });
}

function checkMobileTopPadding() {
  // bindAjaxContentChange();
  var $atmMobileNav = $('#atm-navigation_mobile');
  if ($atmMobileNav.css('display') === 'block') {
    $atmMobileNav.next('section').css('margin-top', $atmMobileNav.height());
    // $( '.view' )
    //   .first()
    //   .addClass( 'active' )
    // // $( '.atm-under-menu .view' ).first().addClass( 'active' );
  } else {
    $atmMobileNav.next('section').css('margin-top', 0);
  }
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
  var item = carousel.find('.item');
  var item_count = item.length;

  item.each(function (i, e) {
    var active = $(e).hasClass('active');

    var w = carousel.width();
    var pos = $(e).position();

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
var subMenuContentAction = {
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
      // console.log(res);
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

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function bindAjaxReservedForm() {
  $('.reserved-btn-scroolled').on('click', function (evt) {
    evt.preventDefault();
    $('html, body').stop().animate({
      scrollTop: $('#signup').offset().top
    }, 777);
  });
  $('.reserved-btn').on('click', function (evt) {
    evt.preventDefault();
    var page = $('#page_name').val();
    var id_form = $(this).data("reserve");
    // console.log(page, id_form);

    $.ajax({
      type: "GET",
      url: "/reserved/form",
      data: {
        'page': page,
        'id_form': id_form
      },
      dataType: "json",
      cache: false,
      success: function (res) {
        if (res.response === "ok") {
          createOverlay();
          var $html = $(res.html);

          $html.appendTo('body');
          var height = $html.outerHeight();
          var topScroll = $(window).scrollTop();

          $html
            .css({
              'top': topScroll - height,
              'display': 'block'
            })
            .find('.fa-times')
            .one('click', function () {
              hideReservedForm();
            })
            .end()
            .find('.atm-form__phone')
            .mask("+7(999) 999-9999")
            .end()
            .animate({
              'top': topScroll
            }, 300);

          $('body')
            .css('overflow', 'hidden');

          $('.atm-reserved-form__form')
            .submit(function (evt) {
              evt.preventDefault();
              evt.stopPropagation();
              var $form = $(this);
              var $reservForm = $('.atm-reserved-form');

              var ajaxObj = $(this).serialize();
              ajaxObj += "&page=" + page;
              ajaxObj += "&id_form=" + id_form;
              $(this).empty()
                .append('<div class="atm-reserved-spinner"><i class="fas fa-spinner fa-spin"></i></div>');

              $.ajax({
                type: "POST",
                url: "/reserve/", ///// INSERT URL HERE
                dataType: "json",
                cache: false,
                data: ajaxObj,
                success: function (res) {
                  if (res.response == 200) {
                    $reservForm.find('.atm-reserved-name').text('Сасибо!\nВы записаны');
                    $reservForm.append('<div class="atm-reserved-notification"><label>Наш Администратор вам перезвонит в ближайшее время и направит счёт на оплату на ваш e-mail</label></div>');
                    $form.remove();
                    setTimeout(function () {
                      hideReservedForm();
                    }, 4500);
                  }
                }
              });
              return false;
            });
        }
      }
    });
  });
}

function hideReservedForm() {
  var topScroll = $(window).scrollTop();
  var height = $('.atm-reserved-form').outerHeight();

  $('.atm-overlay')
    .fadeOut(300, function () {
      $(this).remove();
    });
  $('.atm-reserved-form')
    .animate({
      'top': topScroll - height
    }, function () {
      $(this).remove();
    });
  $('body').css('overflow', 'auto');
}

function createOverlay() {
  $('<div></div>')
    .addClass('atm-overlay')
    .appendTo('body')
    .fadeIn(300);
}

function changeSubMenuContent(data_desc) {
  var page = window.location.pathname.replace(/\//g, '');

  data_desc = data_desc || $(this).attr('data-desc');
  if (data_desc && page in subMenuContentAction) {
    $(this).addClass('active');
    var subMenuObj = subMenuContentAction[page];
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

          if (first_submenu_load) {
            first_submenu_load = false;
          } else {
            // ANIMATE SCROLL
            $('html').animate({
              scrollTop: $('.atm-under-menu').offset().top
            }, 500);
          }
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
        $('#desc_image').attr('src', response.image_src);
        $('#title').html(response.title);
        $('#main_text').html(response.main_text);
      }
    }
  });
});