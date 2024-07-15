(function ($) {
    "use strict";
    
    if ($('.typed-text-output').length == 1) {
        var typed_strings = $('.typed-text').text();
        var typed = new Typed('.typed-text-output', {
            strings: typed_strings.split(', '),
            typeSpeed: 100,
            backSpeed: 20,
            smartBackspace: false,
            loop: true
        });
    }

    $(document).ready(function() {
        $('#voir-plus').click(function(e) {
            e.preventDefault();
            setTimeout(() => {
                $('.hidden-content').slideDown();
                $(this).hide();
            }, 3000);
        });
    });

})(jQuery);