
$(document).ready(function () {
    var maxItems = $('#plusButton').data('max');
    $('#minusButton').prop('disabled', true);
    $('#currentCount').val(1);
    $('#currentCount').on('input', function () {
        var currentCount = parseInt($('#currentCount').val());
       
        $('#addCart').show();
        $('#message-number-items').text('');

        $('#minusButton').prop('disabled', false);
        $('#plusButton').prop('disabled', false);
        if (currentCount > maxItems || currentCount < 1) {
            $('#plusButton').prop('disabled', true);
            $('#minusButton').prop('disabled', true);
            $('#addCart').hide();
            $('#message-number-items').text(`The minimum value is 1 and the maximum is ${maxItems}`);

        } else if (currentCount == 1) {
            $('#minusButton').prop('disabled', true);
            $('#addCart').show();
            $('#message-number-items').text('');


        } else if (currentCount == maxItems) {
            $('#plusButton').prop('disabled', true);
            $('#addCart').show();
            $('#message-number-items').text('');

        }

     

    });

    $('#plusButton').click(function () {
        var currentCount = parseInt($('#currentCount').val());
        if (!currentCount){
            currentCount = 2
        }
        if (currentCount < maxItems) {
            $('#currentCount').val(currentCount);
        }

        if (currentCount >= maxItems) {
            $(this).prop('disabled', true);
        }

        $('#minusButton').prop('disabled', false);
    });

    $('#minusButton').click(function () {
        var currentCount = parseInt($('#currentCount').val());
        if (currentCount == null || currentCount == 0) {
            currentCount = 1
        }
        $('#currentCount').val(currentCount)
        if (currentCount <= 1) {
            $('#minusButton').prop('disabled', true);
        }
        $('#plusButton').prop('disabled', false);





    })



    $('#form').on('submit', function (e) {
        e.preventDefault();
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken)
            },
            success: function (response) {
                var numberComments = parseInt($('#number-comments').text());
                var maxComments = $('#myComments').data('max-comments');

                var comment = `<div class="media mb-4">
                        <img src="${response.imageUrl}" alt="Image" class="img-fluid mr-3 mt-1" style="width: 45px;" />
                        <div class="media-body">
                          <h6>${response.name}<small>- <i>${response.createdAt}</i></small></h6>
                          <p>${response.message}</p>
                        </div>
                      </div>`

                $('#comments').after(comment);

                $('#number-comments').text(numberComments + 1)
                $('#message').text('The message was successfully registered.')

                if ($('#myComments').children().length == maxComments + 2) {
                    $('#myComments').children().last().remove()
                }




            },
            error: function (xhr) {
                var error = Object.values(xhr.responseJSON.error)[0]
                $('#message').text(error)

            }

        })




    })


});