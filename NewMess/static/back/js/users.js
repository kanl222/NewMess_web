const plus = "<i class='bi bi-plus-lg'></i>";
const dash ="<i class='bi bi-dash-lg'></i>";
const chat_dots ="<i class='bi bi-chat-dots-fill'></i>";
var list_user_in_chat = [];
var is_open_create_menu_chat = false;

function changeElemNavig() {
  const list = document.querySelectorAll('.list');
  const list_activate = document.querySelector('#users');
  list.forEach((item) => item.classList.remove('active'));
  list_activate.classList.add('active');
}

const stringToHTML = (str) => {
  const dom = document.createElement('div');
  dom.innerHTML = str;
  return dom;
};

function clearList(lst) {
  return lst.filter(num => num !== null).filter(function(){return true;});;
};


$(document).ready(() => { const list = document.querySelectorAll('.list');
    const list_activate = document.querySelector('#users');
    list.forEach((item) => item.classList.remove('active'));
    list_activate.classList.add('active');
    const text_tittle = $('#form-chat-name');
    text_tittle.prop('disabled', true);
});

$(document).on('click', 'div .button-add-user-in-chat', function(e) {
    const parentEl = $(this).parent().parent();
    if (list_user_in_chat.includes(`${parentEl.attr('id')}`)) {
      parentEl.remove();
    };
    const dom = stringToHTML(dash);
    dom.className = 'button-delete-user-from-chat';
    this.replaceWith(dom);
    list_user_in_chat.push(parentEl.attr('id'));
    parentEl.appendTo($('#chat-participants'));
    const text_tittle = $('#form-chat-name');
    console.log(list_user_in_chat.length,list_user_in_chat)
    if (list_user_in_chat.length >= 2 && text_tittle.attr('disabled')) {
      text_tittle.prop('disabled', false);
    };
});

$(document).on('click', 'div .button-delete-user-from-chat', function(e) {
    const parentEl = $(this).parent().parent();
    const dom = stringToHTML(plus);
    dom.className = 'button-add-user-in-chat';
    this.replaceWith(dom);
    list_user_in_chat.splice(list_user_in_chat.indexOf(parentEl.attr('id')), 1);
    parentEl.appendTo($('#list-users'));
    const text_tittle = $('#form-chat-name');
    if (list_user_in_chat.length < 2 && !text_tittle.prop('disabled')) {
      text_tittle.prop('disabled', true);
    };
});

$(document).on('click', 'div .open-menu-create-chat', function(e) {
  const time_ = 'slow';
  const chat_create_panel = $('.create-chat-panel');
  const open_menu_create_chat = $('.open-menu-create-chat');
  open_menu_create_chat.hide();
  chat_create_panel.animate({width: 'toggle'}, time_);
  is_open_create_menu_chat = true;

  $('.user_object .button-send-to-user').each((index, element) => {
    const parentEl = $(element).parent().parent();
    const dom = stringToHTML(plus);
    $(element).fadeOut('fast', function() {
      dom.className = 'button-add-user-in-chat';
      $(this).replaceWith(dom);
      $(dom).hide().removeClass('flip-out-y').addClass('flip-in-y').fadeIn('slow');
    });
    parentEl.appendTo($('#list-users'));
  }); 
   
});

$(document).on('click', 'div .button-close-chat', function(e) {
  const time_ = 'slow';
  const chat_create_panel = $('.create-chat-panel');
  const open_menu_create_chat = $('.open-menu-create-chat');
  is_open_create_menu_chat = false;
  chat_create_panel.animate({width: 'toggle'}, time_, () => {
    open_menu_create_chat.show();
  });
  $('.user_object .button-add-user-in-chat').each((index, element) => {
    const parentEl = $(element).parent().parent();
    const dom = stringToHTML(chat_dots);
   $(element).fadeOut('fast', function() {
      dom.className = 'button-send-to-user';
      $(this).replaceWith(dom);
      $(dom).hide().removeClass('flip-out-y').addClass('flip-in-y').fadeIn('slow');
    });
    list_user_in_chat = [];
    parentEl.appendTo($('#list-users'));   
  });
});

$(document).on('click', '.button-send-to-user', function(e) {
  const parentEl = $(this).parent().parent();
  console.log(parentEl.attr('id'))
  $.ajax({
    method: 'GET',
    url: `/api/create-private-chat/${parentEl.attr('id')}`,
    cache: false,
    success: function(response) {
    console.log(response,response.statusCode,response.statusCode == 200 , response.statusCode == 202)
    if ( response.statusCode === 200 || response.statusCode === 202){
      url=`/mes?chat_id=${response.data.chat_id}`
      window.location.replace(url);
    };
    },
    error: function(xhr, status, error) {
      console.log(error);
      // Handle any errors
    },
  });
});


$(document).on('click', 'div.button-load-icon-chat', function(event) {
  var load_icon = $("div.button-load-icon-chat");
    const input = document.createElement('input');
    input.type = 'file';
 
 
    input.onchange = function() {
       const file = this.files[0];
       const reader = new FileReader();
       reader.onload = function() {
          const img_in = document.querySelector('.button-load-icon-chat');
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
                img_in.setAttribute('style', `background-image: url(data:image/png;base64,${data['data']})`);
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


 $(document).on('click', 'div.button-create-chat', (e) => {
    const error_mes = $('#error-text');
    const title_chat = $('#form-chat-name').val();
    console.log(list_user_in_chat)
    if (list_user_in_chat.length <=1) {
      _error('Необходимо добавить минимум 2 пользователей в чат');
      return 0;
    }
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
        url=`/mes?chat_id=${response.data.id}`
      window.location.replace(url);
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


$(document).on('change', '#search-input', (event) => {
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
      for (var i = 0; i < users.length; i++) {
        var user = users[i];
        if (!list_user_in_chat.includes(`${user.id}`)) { 
          console.log(user)
          var dataItems = {
            id: user.id,
            username: user.username,
            icon: user.icon
          };
          if (!is_open_create_menu_chat){
            $('#template-user-button-send-to-user').tmpl(dataItems).appendTo('#list-users');
          } else {
            $('#template-user-button-add-user-in-chat').tmpl(dataItems).appendTo('#list-users');
          }
        }
      }
    },
    error: function(xhr, status, error) {
      console.log(error);
      // Handle any errors
    },
  });
  
});


window.onunload = changeElemNavig;