$(document).ready(function () {

  $('#id_province').change(function () {
    var provinceId = $(this).val()
    if (provinceId) {
      $.ajax({
        url: $("#form").data("get-cities-url"),
        data: {
          province_id: provinceId
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        },
        success: function (data) {
          var citySelect = $('#id_city');
          citySelect.empty();

          if (data.length > 0) {
            $.each(data, function (key, value) {
              var option = $('<option></option>')
                .attr('value', value.id)
                .text(value.name);

              if (key === 0) {
                option.prop('selected', true);
              }

              citySelect.append(option);
            });
          } else {
            citySelect.append('<option value="">No cities available</option>');
          }
        }

      })
    }

  });

})
