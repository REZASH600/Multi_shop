(function ($) {
    "use strict";

    // Dropdown on mouse hover
    $(document).ready(function () {
        if ($(window).width() > 992) {
            $('.navbar .dropdown > .dropdown-toggle').off('click').on('click', function (e) {
                e.preventDefault();

                var $this = $(this);
                var $dropdownMenu = $this.next('.dropdown-menu');
                if ($dropdownMenu.is(':visible')) {
                    $dropdownMenu.slideUp();

                }else{

                    $('.dropdown-menu').each(function () {
                        var $menu = $(this);
    
                        if ($this.closest($menu).length > 0) {
                            return;
                        }
    
                        $menu.slideUp();
                    });

                    
                    $dropdownMenu.slideToggle();

                }    

            

            });
        } else {
            $('.navbar .dropdown-toggle').off('click');
        }
    });


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 2
            },
            576: {
                items: 3
            },
            768: {
                items: 4
            },
            992: {
                items: 5
            },
            1200: {
                items: 6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 2
            },
            768: {
                items: 3
            },
            992: {
                items: 4
            }
        }
    });


    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });


})(jQuery);


