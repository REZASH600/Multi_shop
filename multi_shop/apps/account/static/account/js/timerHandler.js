$(document).ready(function () {
    var expiryTime = $('#myBtn').data('expiry-time'); // seconds
    var startTime = new Date($('#myBtn').data('otp-created'));


    var timerInterval = null;

    function formatTimeUnit(time) {
        return time <= 9 ? `0${time}` : time;

    }

    function timeDifference() {
        var now = new Date();
        return Math.floor((now - startTime) / 1000)  // seconds
    }

    var timeRemaining = timeDifference();


    function updateTimerDisplay() {
        if (Math.floor(timeRemaining) >= expiryTime) {
            clearInterval(timerInterval);
            $('#myBtn').text('Send Code');
            $('#errors').text('');
            $('.wrap-input100').hide();
            $('#timer').text('');
        } else {
            timeRemaining++;
            var minutes = Math.floor((expiryTime - timeRemaining) / 60); // minutes
            var seconds = Math.floor((expiryTime - timeRemaining) % 60); // seconds
            $("#timer").text(`${formatTimeUnit(minutes)}:${formatTimeUnit(seconds)} time remaining `);
        }


    }


    timerInterval = setInterval(updateTimerDisplay, 1000);


    $('#myBtn').click(function (e) {
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            e.preventDefault();
            if ($('#myBtn').text() === 'Send Code') {
                var url = $(this).data('url');
                $.ajax({
                    type: "POST",
                    url: url,
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader('X-CSRFToken', csrftoken)
                    },
                    success: function (data) {
                        startTime = new Date(data.otpCreated);

                        timeRemaining = timeDifference();

                        $('#timer').text(`${data.response}`);
                        $('#myBtn').text('Verify');
                        $('.wrap-input100').show();

                        timerInterval = setInterval(updateTimerDisplay, 1000)
                    },
                    error: function (xhr, status, error) {
                        alert(error)
                    }

                })


            } else {
                $.ajax({
                    type: "POST",
                    data: $('#form').serialize(),
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader('X-CSRFToken', csrftoken)
                    },
                    success: function (response) {
                        if (response.redirect_url) {
                            window.location.href = response.redirect_url;
                        } else {
                            alert(response.response);
                        }


                    },
                    error: function (xhr, status, error) {
                        $('#errors').text(xhr.responseJSON.response)
                    }

                })
            }


        }
    )


})