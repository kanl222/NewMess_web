var plus = "<i class='bi bi-plus-lg'></i>"
var dash ="<i class='bi bi-dash-lg'></i>"

function СhangeElemNavig(){
  const list = document.querySelectorAll('.list');
  const list_activate = document.querySelector('#users');
  list.forEach((item)=> item.classList.remove('active'));
  list_activate.classList.add('active');
};


var stringToHTML = function (str) {
	var dom = document.createElement('div');
	dom.innerHTML = str;
	return dom;

};

var list_user_in_chat = [];

$(document).ready(function() {
    const list = document.querySelectorAll('.list');
    const list_activate = document.querySelector('#users');
    list.forEach((item)=> item.classList.remove('active'));
    list_activate.classList.add('active');
});

$(document).on('click', 'div .button-add-user-in-chat', function(e) {
    const parentEl = $(this).parent().parent();
    var dom = stringToHTML(dash)
    dom.className = 'button-delete-user-from-chat';
    this.replaceWith(dom)
    list_user_in_chat.push(parentEl.attr('id'))
    parentEl.appendTo($('#chat-participants'));
});

$(document).on('click', 'div .button-delete-user-from-chat', function(e) {
    const parentEl = $(this).parent().parent();
    var dom = stringToHTML(plus)
    dom.className = 'button-add-user-in-chat';
    this.replaceWith(dom)
    delete list_user_in_chat[list_user_in_chat.indexOf(parentEl.attr('id'))]
    console.log(list_user_in_chat)
    parentEl.appendTo($('#list-users'));
});

$(document).on('click', 'div.button-load-icon-chat', function(event) {
    const input = document.createElement('input');
    input.type = 'file';
 
 
    input.onchange = function() {
       const file = this.files[0];
       const reader = new FileReader();
       reader.onload = function() {
          const img_in = document.querySelector('.icon-chat-create');
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
                sessionStorage.setItem('IconChat',data['data'])
                img_in.setAttribute('src', `data:image/png;base64,${data['data']}`);
                img_in.setAttribute('style', 'display:block');
             },
             error: function(xhr, status, error) {
                console.log(error);
                // Handle any errors
             }
             
          });
       };
       reader.readAsDataURL(file);
    };
    input.click();
 }) 


 $(document).on('click', 'div.button-create-chat', function(event) {
    const error_mes = $('#error-text');
    const title_chat = $('#form-chat-name').val();
  
    if (!title_chat) {
      _error('Не указано название чата');
      return 0;
    } else if (!list_user_in_chat.toString()) {
      _error('Нет участников чата');
      return 0;
    }
  
    const data = {
      title: title_chat,
      list_user_in_chat: list_user_in_chat.toString(),
      icon_base64: sessionStorage['IconChat'],
    };
  
    $.ajax({
      method: 'POST',
      url: '/api/chat',
      data: JSON.stringify(data),
      dataType: 'json',
      cache: false,
      contentType:"application/json",
      processData: false,
      success: function(response) {
        location.reload();
      },
      error: function(xhr, status, error) {
        console.log(error);
              // Handle any errors
      },
    });
  });
  
function _error(error) {
    const error_mes = $('#error-text');
    error_mes.text(error);
    error_mes.attr('style', 'display:block');
}


$(document).on('change', '#search-input', function(event) {
  const inputValue = event.target.value;
  console.log(inputValue)
  const data = {
    search_value: inputValue
  };


  $.ajax({
    method: 'GET',
    url: '/api/search-users',
    data: data,
    dataType: 'json',
    cache: false,
    success: function(response) {
      $("#list-users").empty();
      var users = response.data.users;
      if (users && users.length) {

        for (var i = 0; i < users.length; i++) {
          var users = users[i];
          if (!(users.id in list_user_in_chat)){
          var dataItems = {
            id: users.id,
            username: users.username,
            icon: users.icon
          };
          $('#template-user').tmpl(dataItems).appendTo('#list-users');
        };
      };
      };
    },
    error: function(xhr, status, error) {
      console.log(error);
      // Handle any errors
    },
  });
});


window.onunload = СhangeElemNavig