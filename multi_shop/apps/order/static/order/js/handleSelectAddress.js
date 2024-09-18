$(document).ready(function () {


    $('#select-address').on('change', function () {
        var url = $('#my-form').attr('action')
        var addressId = $(this).val();
        var orderId = $(this).data('order-id');
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: "POST",
            data: { "order_id": orderId, "address_id": addressId },
            url:url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success:function(){
                $('#message-address').text("The address has been registered successfully.")
            }

        })
    })
})