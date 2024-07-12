$(document).ready(function() {
    const switchers = $('.switcher');
  
    switchers.on('click', function() {
      switchers.parent().removeClass('is-active');
      $(this).parent().addClass('is-active');
    });
  });