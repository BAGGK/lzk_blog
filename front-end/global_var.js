let url = 'http://182.254.228.53/API'
// let url = 'http://127.0.0.1:5000'
function get_data(api) {
  let ret_val = 0;

  $.get({
    url: url + api,
    async: false,
    success: function (data, status) {
      data = jQuery.parseJSON(data)
      ret_val = data

      if (status == 400) {
        alert(data)
      }

    }
  })
  return ret_val

}

function post_data(api, form_data) {

  $.post(
    {
      url: url + api,
      data: form_data,
      processData: false,
      contentType: false,
      success: function (data, status) {
        location.reload();
        if (status == 400) {
          alert(data)
        }
      }
    })

}