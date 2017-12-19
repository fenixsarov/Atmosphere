// Preloader
$(document).ready(function($) {
  $(window).load(function() {
    setTimeout(function() {
      $('#preloader').fadeOut('slow', function() {});
    }, 300);
      setTimeout(function(){
        startPage()
    }, 0);
  });
});
