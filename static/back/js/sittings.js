let changeIcon = false;


function changeElemNavig() {
  const list = document.querySelectorAll('.list');
  const listActivate = document.querySelector('#sittings');
  list.forEach((item) => item.classList.remove('active'));
  listActivate.classList.add('active');
}


$(document).ready(() => {
  changeElemNavig();
});


$('#new-icon-user').on('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = function () {
    const imgInNavig = document.querySelector('.element-img .image_in_navig');
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
      success: (data) => {
        changeIcon = true;
        imgInNavig.setAttribute('src', `data:image/png;base64,${data['data']}`);
      },
      error: (xhr, status, error) => {
        console.log(error);
      },
    });
  };
  reader.readAsDataURL(file);
});


$('.submit').on('click', (event) => {
  const username = $('#username').val();
  const email = $('#email').val();
  const icon = $('.element-img .image_in_navig').attr('src').split(',')[1];
  const currentUser = JSON.parse(sessionStorage.getItem('CurrentUser'));


  if (!username || !email) {
    $('.error').text('Пустая строки');
    return 0;
  }


  const formData = {
    username,
    email,
    icon: changeIcon ? icon : '',
  };


  if (changeIcon || !(username === currentUser.username) || !(email === currentUser.email)) {
    $.ajax({
      method: 'PUT',
      url: '/api/user',
      data: JSON.stringify(formData),
      dataType: 'json',
      cache: false,
      contentType: 'application/json',
      processData: false,
      success: () => {
        location.reload();
      },
      error: (xhr, status, error) => {
        console.log(xhr, error);
        if (xhr.responseText === 'Email already exists') {
          $('.error').text('Электронная почта уже занята');
        } else if (xhr.responseText === 'Username already exists') {
            $('.error').text('Имя пользователя уже занято');
        } else {
          console.log(xhr, error);
        }
      },
    });
  }
});