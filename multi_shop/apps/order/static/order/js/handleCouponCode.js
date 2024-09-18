$(document).ready(function () {
    $("#coupon-code-form").on('submit', function (e) {
        e.preventDefault();
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $("#coupon-code-form").serialize(),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success: function (response) {
                $("#total-price").text(response.total_price);
                $("#show-message").text('Discount successfully applied.')

            },
            error: function (xhr) {
                $("#show-message").text(xhr.responseJSON.error)
     
            }


        })
    })
})