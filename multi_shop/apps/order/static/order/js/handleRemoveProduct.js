$(document).ready(function(){
    $('.btn-danger').on('click',function(){
        $this = $(this)
        url = $this.data('url')
        $.ajax({
            type:"GET",
            url:url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success:function(response){
                $this.parent().parent().remove()
                $('#total-price').text(response.total_price)
            }
        })
    })
})