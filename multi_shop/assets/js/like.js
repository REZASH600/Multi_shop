$(document).ready(function () {

    $(document).on('click', '.btn-like', function (e) {
        e.preventDefault();
        var $this = $(this);
        var currentUlr = window.location.pathname
        var url = $this.attr('href')

        url += ($this.attr('href').includes('?') ? '&' : '?') + `current_url=${currentUlr}`;

        $.ajax({
            url: url,
            type: 'GET',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success: function (response) {
                if ('url' in  response){
                    window.location.href = response.url;
                    return ;

                }
                if (response.isLiked) {
                    $this.find('i').attr('class','fas fa-heart')
                } else {      
                    $this.find('i').attr('class','far fa-heart')
                }
                $('.number-like').text(response.numberLike)
            


            },
            error: function(xhr){
                console.log(xhr)
            }

        })

    })
})