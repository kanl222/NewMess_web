function СhangeElemNavig(){
    const list = document.querySelectorAll('.list');
    const list_activate = document.querySelector('#sittings');
    list.forEach((item)=> item.classList.remove('active'));
    list_activate.classList.add('active');
  };
  

$(document).ready(function() {
    СhangeElemNavig();
  })
  

$('#new-icon-user').on('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
       reader.onload = function() {
          const img_in = document.querySelector('.element-img .image_in_navig');
          const formData = new FormData();
          formData.append('image_base64', reader.result.split(',')[1]);
          $.ajax({
             method: 'POST',
             url: '/resize_image',
             data: formData,
             dataType: 'json',
             cache: false,
             contentType: false,
             processData: false,
             success: function(data) {
                img_in.setAttribute('src', `data:image/png;base64,${data['data']}`);
             },
             error: function(xhr, status, error) {
                console.log(error);
                // Handle any errors
             }
             
          });
       };
       reader.readAsDataURL(file);
  });

  $('.submit').on('click', function(event) {
    const username = $('#username').val();
    const email = $('#email').val();
    const icon = $('.element-img .image_in_navig').attr('src').split(',')[1];
    console.log(username,email,icon)

    const formData = {
    'username':username || '',
    'email': email || '',
    'icon':icon || ''
  };

    $.ajax({
             method: 'PUT',
             url: '/api/user',
             data: JSON.stringify(formData),
             dataType: 'json',
             cache: false,
             contentType:"application/json",
             processData: false,
             success: function(data) {
                img_in.setAttribute('src', `data:image/png;base64,${data['data']}`);
             },
             error: function(xhr, status, error) {
                console.log(error);
                // Handle any errors
             }
             
  })
});
  