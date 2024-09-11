$(document).ready(function () {


    var previousCount = 0;


    $('.removeProduct').on('click', function () {
        var url = $(this).data('url');
        var urlParts = url.split('/');

        // Slug separation
        var name = urlParts[urlParts.length - 2];

        $.ajax({
            type: 'GET',
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success: function (response) {
                $(`#${name}`).remove();
                $('#total-cart').text(response.totalCart);

            },
            error: function (xhr) {
                alert(xhr)

            }
        })
    })



    function ajaxRequest(currentCount, nameProduct, tdPrice) {
        var baseUrl = '/carts/change/quantity';
        var finalUrl = `${baseUrl}/${nameProduct}/${currentCount}/`;


        $.ajax({
            type: 'GET',
            url: finalUrl,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success: function (response) {
                $('#total-cart').text(response.totalCart);
                tdPrice.text(response.totalPrice)

            },
            error: function (xhr) {
                console.log(xhr)
            }

        })
    }

    $('.input-quantity').on('focus', function () {
        number = parseInt($(this).val());
        if (number) {
            previousCount = number;
        }


    })

    $('.input-quantity').on('input', function () {
        var currentCount = parseInt($(this).val());
        var nameProduct = $(this).data('name');
        var tdPrice = $(`#${nameProduct}`).find('.price-product');
    
        var plusButton = $(this).closest('.quantity').find('.btn-plus');
        var minusButton = $(this).closest('.quantity').find('.btn-minus');
        var maxQuantity = plusButton.data('max');
        var orderButton = $('#order-button');
    
        function updateButtons(plusDisabled, minusDisabled, showOrder) {
            plusButton.prop('disabled', plusDisabled);
            minusButton.prop('disabled', minusDisabled);
            orderButton.toggle(showOrder);
        }
    
        if (currentCount > maxQuantity || currentCount < 1 || !currentCount) {
            updateButtons(true, true, false); 
        } else {
            var plusDisabled = (currentCount == maxQuantity);
            var minusDisabled = (currentCount == 1);
            updateButtons(plusDisabled, minusDisabled, true); 
    
            if (currentCount !== previousCount) {
                ajaxRequest(currentCount - previousCount, nameProduct, tdPrice);
                previousCount = currentCount; 
            }
        }
    });
    


    $('.plusButton').on('click', function () {
        var input = $(this).closest('.quantity').find('input');
        var currentCount = parseInt(input.val());
        var nameProduct = $(input).data('name');
        var tdPrice = $(`#${nameProduct}`).find('.price-product');
        var maxQuantity = $(this).data('max');
        var minusButton = $(this).closest('.quantity').find('.btn-minus');


        // If currentCount is undefined or 0, set it to 2 as the default value.
        // Note: The value of currentCount is modified when a user clicks the plus/minus buttons in the $('.quantity button') handler in main.js.
        if (!currentCount) {
            currentCount = 2
        }
        if (currentCount < maxQuantity) {
            input.val(currentCount);
        }

        if (currentCount >= maxQuantity) {
            $(this).prop('disabled', true);
        }
        ajaxRequest(1, nameProduct, tdPrice)

        minusButton.prop('disabled', false);


    })



    $('.minusButton').on('click', function () {

        var input = $(this).closest('.quantity').find('input');
        var currentCount = parseInt(input.val());
        var nameProduct = $(input).data('name');
        var tdPrice = $(`#${nameProduct}`).find('.price-product');
        var plusButton = $(this).closest('.quantity').find('.btn-plus');

        if (!currentCount) {
            currentCount = 1
        }
        input.val(currentCount)
        if (currentCount <= 1) {
            $(this).prop('disabled', true);
        }

        ajaxRequest(-1, nameProduct, tdPrice)
        plusButton.prop('disabled', false);

    })


})