$(document).ready(function () {
    $('#myBtn').click(function (e) {
        e.preventDefault();
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            data: $('#form').serialize(),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken)
            },
            success: function (response) {
                $('#form').hide();
                var link = $('<a>', {href: response.url, text: 'login', color: 'black', class: 'login100-form-btn'})

                $('#link-form').append(link);

            },
            error: function (xhr, status, err) {
                 $('#error').text(xhr.responseJSON.nonFieldError);
                 $('#password1').text(xhr.responseJSON.password1Error);
                 $('#password2').text(xhr.responseJSON.password2Error);
            }


        })
    })
})