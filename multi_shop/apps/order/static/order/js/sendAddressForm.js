$(document).ready(function(){

    $('#form').on('submit', function (e) {

        e.preventDefault();
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $form = $('#form');
    
        $.ajax({
          type: 'POST',
          url: $form.attr('action'),
          beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
          },
          data: $form.serialize(),
          success: function (res=null) {
            if (res){
              window.location.href = res.url
            }else{

              $('#success').html("<div class='alert alert-success'>");
              $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                .append("</button>");
              $('#success > .alert-success')
                .append("<strong>The address has been registered successfully. <a href=></a></strong>");
              $('#success > .alert-success')
                .append('</div>');
              $('#contactForm').trigger("reset");


            }
            
         
          },
          error: function () {
            $('#success').html("<div class='alert alert-danger'>");
            $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
              .append("</button>");
            $('#success > .alert-danger').append($("<strong>").text("Please fill out the form correctly."));
            $('#success > .alert-danger').append('</div>');
            $('#form').trigger("reset");
          },
    
    
    
    
    
        })
    
    
    
    
      });
    
      $('#recipient-name, #street').focus(function () {
        $('#success').html('');
    });
})