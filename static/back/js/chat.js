let users_chat = {};


 function ToBottomScroll(element){
  $(element).scrollTop($(element).prop('scrollHeight'));
 };

function СhangeElemNavig(){
    const list = document.querySelectorAll('.list');
    const list_activate = document.querySelector('#chats');
    list.forEach((item)=> item.classList.remove('active'));
    list_activate.classList.add('active');
};


function LoadCurrentUser() {
  $.ajax({
    type: 'GET',
    url: `/api/user`,
    dataType: 'json',
    cache: false,
    success: function(data) {
      sessionStorage.setItem('CurrentUser',JSON.stringify(data['data']['user']))
      },
    error: function(xhr, status, error) {
        console.log(error);
        // Handle any errors
      }
    });
};


function morph(int, array) {
    return (array = array || ['участник', 'участника', 'участников']) && array[(int % 100 > 4 && int % 100 < 20) ? 2 : [2, 0, 1, 1, 1, 2][(int % 10 < 5) ? int % 10 : 5]];
};

$(document).ready(function() {
  sessionStorage.setItem('id-open-chat', 0);
  СhangeElemNavig();
  LoadCurrentUser();
  SortChat()
  UpdateData()
})

function send_message(){
  var chat = document.querySelector('.chat-panel');
  var textarea = $('#from-textarea');
  const currentUser = JSON.parse(sessionStorage.getItem('CurrentUser'));
  const data = {
    chat_id: sessionStorage.getItem('id-open-chat'),
    text: textarea.val()
  };
  if (!textarea.val()){
    return 0;
  } else {textarea.val("")};
    $.ajax({
      method: 'POST',
      url: '/api/message',
      data: JSON.stringify(data),
      dataType: 'json',
      cache: false,
      contentType:"application/json",
      processData: false,
      success: function(response) {
        var currentMessage = response['data']['message']
        const date = new Date(currentMessage['send_time']);
        const send_time = date.toLocaleTimeString(navigator.language, { hour: '2-digit', minute: '2-digit' });
            const message = {
              id: currentMessage.id,
              message: currentMessage.text,
              time_message: send_time,
              username: currentUser.username,
              icon: currentUser.icon,
            };
            $('#template-message-sent').tmpl(message).appendTo('#chat-messages');
            set_last_massage(sessionStorage.getItem('id-open-chat'), currentMessage.id, currentMessage.text, currentMessage.send_time);
            SortChat();
            ToBottomScroll(".chat-box");
      },
      error: function(xhr, status, error) {
        console.log(error);
              // Handle any errors
      },
      complete: function() {
       
      }
    });
  };
$('#from-textarea').on('keyup', function (e) {
  console.log(e)
  if (e.key === 'Enter' || e.keyCode === 13) {
    send_message();
  };})
$('.button-send-message').on('click', send_message);

$(document).on('click','li.chat_object', function(e) {
    var chat = $('.chat-panel');
    var chat_id = e.currentTarget.id.split('_')[1];
    if (chat.is(':visible') && chat_id === sessionStorage.getItem('id-open-chat')) {
        $(this).children().removeClass('active-chat');  
        chat.animate({width: 'toggle'}, "slow");
        sessionStorage.setItem('id-open-chat', 0);
        return 0;
    }
    else if (chat.is(':visible')){
        chat.animate({width: 'toggle'}, "slow",function() {
            loadChat(chat_id);
       });
    }
    else if (!chat.is(':visible')) 
    {   
      loadChat(chat_id);
    };
    $('#from-textarea').val('');
    $('#chat_' + sessionStorage.getItem('id-open-chat')).children().removeClass('active-chat');
    sessionStorage.setItem('id-open-chat', chat_id);
    $(this).children().addClass('active-chat');   
    chat.animate({width: 'toggle'}, 400);
});

function set_count_new_message(idChat,value){
  var count_new_message = $(`#chat_${idChat} .count-new-message`);
  if (value == 0){
    count_new_message.css('background', 'inherit');
    count_new_message.text('');
  }else{
    count_new_message.css('background', 'red');
    count_new_message.text(value);
  }
};
function set_last_massage(idChat,id,massage,time){
  const date = new Date(time);
  var text_message_id = $(`#chat_${idChat} .text`);
  var text_message = $(`#chat_${idChat} .text .text-muted`);
  var time_message = $(`#chat_${idChat} .time`);
  text_message.text(massage)
  if (time){
  time_message.text(date.toLocaleTimeString(navigator.language, { hour: '2-digit', minute: '2-digit' }));
  }else{
    time_message.text(time);
  };
  text_message_id.attr("id",`last_message_in_chat_id_${id}`);
};

function SortChat(){
  $('#list-chats').find('.chat_object').sort(function(a, b) {
    const object_a = parseInt($(a).find('.text').attr('id').split('_').slice(-1)[0]) || 0;
    const object_b = parseInt($(b).find('.text').attr('id').split('_').slice(-1)[0]) || 0;
    return object_b - object_a;
  }).appendTo('#list-chats');
};

function loadChat(idChat) {
  $("#chat-messages").empty();
  const titleChat = $('#title-chat-in-frame');
  const iconChat = $('#icon-chat');
  const countParticipants = $('.text-count-participants');
  const currentUser = JSON.parse(sessionStorage.getItem('CurrentUser'));
  const data = { chat_id: idChat };
  titleChat.val('');
  countParticipants.val('');
  iconChat.attr('src','')
  $.ajax({
    type: 'GET',
    url: `/api/chat/${idChat}`,
    dataType: 'json',
    cache: false,
    success: function(data) {
      titleChat.text(data.title);
      if ('user_participant' in data) {
        countParticipants.show();
        $('._menu-chat').show();
        countParticipants.text(`${data.user_participant} ${morph(data.user_participant)}`);
      if (data.admin_chat !== currentUser.id) {
        $('#delete_chat').parent().hide();
      };}
      else {
        countParticipants.hide();
        $('._menu-chat').hide();};
      iconChat.attr('src', `data:image/png;base64,${data.icon}`);
    },
    error: function(xhr, status, error) {
      console.log(error);
    },
    complete: function() {
      $.ajax({
        type: 'GET',
        url: `/api/chatparticipants/${idChat}`,
        dataType: 'json',
        cache: false,
        success: function(data) {
          users_chat = data['data']['users'];
        },
        error: function(xhr, status, error) {
          console.log(error);
        },
        complete: function() {
          $.ajax({
            type: 'GET',
            url: '/api/messages',
            data: data,
            dataType: 'json',
            cache: false,
            success: function(data) {
              const messageList = data['data']['messages'];
              messageList.forEach(currentMessage => {
                let userMessage = null;
                if (currentMessage.user_id === currentUser['id']) {
                  const date = new Date(currentMessage['send_time']);
                  const message = {
                    id: currentMessage.id,
                    message: currentMessage.text,
                    time_message: date.toLocaleTimeString(navigator.language, { hour: '2-digit', minute: '2-digit' }),
                    username: currentUser.username,
                    icon: currentUser.icon,
                  };
                  $('#template-message-sent').tmpl(message).appendTo('#chat-messages');
                } else {
                  userMessage = users_chat[0][currentMessage.user_id];
                  const date = new Date(currentMessage['send_time']);
                  const message = {
                    id: currentMessage.id,
                    message: currentMessage.text,
                    time_message: date.toLocaleTimeString(navigator.language, { hour: '2-digit', minute: '2-digit' }),
                    username: userMessage.username || '',
                    icon: userMessage.icon || '',
                  };
                  $('#template-message-received').tmpl(message).appendTo('#chat-messages');
                }
              });
            },
            error: function(xhr, status, error) {
              console.log(error);
            },
            complete: function() {
              ToBottomScroll(".chat-box");
              set_count_new_message(idChat,0);
            }
          });
        }
      });
    }
  });
}

function UpdateData(){
  $.ajax({
      type: 'GET',
      url: `/api/update`,
      dataType: 'json',
      cache: false,
      success: function(data) {
        var count_new_messages = data['data']['count_new_messages'];
        var chats_last_messages = data['data']['chats_last_messages'];
        var list_unread_chat = data['data']['list_unread_chat'];
        var chat = $('.chat-panel');
        for (var key in count_new_messages) {
          if (chat.is(':visible') && sessionStorage.getItem('id-open-chat') === key){
            if (count_new_messages[key] != 0){
              $.ajax({
                type: 'GET',
                url: `/api/new_massage/${sessionStorage.getItem('id-open-chat')}`,
                dataType: 'json',
                cache: false,
                success: function(data) {
                  const messageList = data.data.new_message;
                  const currentUser = JSON.parse(sessionStorage.getItem('CurrentUser'));
                  
                  messageList.forEach(currentMessage => {
                    const userMessage = users_chat[0][currentMessage.user_id];
                    const date = new Date(currentMessage.send_time);
                    const message = {
                      id: currentMessage.id,
                      message: currentMessage.text,
                      time_message: date.toLocaleTimeString(navigator.language, { hour: '2-digit', minute: '2-digit' }),
                      username: userMessage.username || '',
                      icon: userMessage.icon || '',
                    };
                    $('#template-message-received').tmpl(message).appendTo('#chat-messages').show('slow');
                    ToBottomScroll('.chat-box');
                    }
                  );
                },
                error: function(xhr, status, error) {
                  console.log(error);
                }
              }
              );
          };
        } else {
          const $chat = $(`#chat_${key}`);
          const inputValue = $('#search-input').val();
          const count_new_message = $chat.find('.count-new-message').text() || '0';
          if (count_new_messages[key] && !(count_new_message == count_new_messages[key]) && $chat) {
            set_count_new_message(key, count_new_messages[key]);
            const last_message = chats_last_messages[key];
            set_last_massage(key, last_message.id, last_message.text, last_message.send_time);
            if (!inputValue){
            SortChat();
            };
          };

          
        };
      };
      if (list_unread_chat.length) {
        const data = { list_chats_id: list_unread_chat.toString()};
        $.ajax({
          type: 'GET',
          url: '/api/chats',
          data: data,
          dataType: 'json',
          cache: false,
          success: function(data) 
          {
            console.log(data)
            var chats = data['data']['chats'];
            for (var key in chats) {
              var chat_dict = {
                id:chats[key].id,
                title:chats[key].title,
                icon:chats[key].icon,
              };
              $('#template-chat').tmpl(chat_dict).appendTo('#list-chats').show('slow');
            };
          },
          error: function(xhr, status, error) 
          {
              console.log(error);
          }
      }
      )
    };
      },
      error: function(xhr, status, error) {
        console.log(error);
      }
    });
setTimeout(UpdateData, 3000);
}

$(document).on('click','#exit_chat', function(e) {
  $.ajax({
    method: 'DELETE',
    url: `/api/chatparticipant/${sessionStorage.getItem('id-open-chat')}`,
    dataType: 'json',
    cache: false,
    success: function(response) {
      location.reload();
    },
    error: function(xhr, status, error) {
      console.log(error);
      // Handle any errors
    },
  });
});


$(document).on('change', '#search-input', function(event) {
  const inputValue = event.target.value;
  const data = {
    search_value: inputValue
  };
  $.ajax({
    method: 'GET',
    url: '/api/search-chats',
    data: data,
    dataType: 'json',
    cache: false,
    success: function(response) {
      $("#list-chats").empty();
      var chats = response['data']['chats'];
      for (var key in chats) {
        chat = chats[key];
        var chat_dict = {
          id: chat.id,
          title: chat.title,
          icon: chat.icon,
        };
        $('#template-chat').tmpl(chat_dict).appendTo('#list-chats').show('slow');
        set_count_new_message(chat.id, chat.count_new_message);
        set_last_massage(chat.id, chat.last_message_id, chat.last_message, chat.send_time);
        SortChat();

        var chat = $('.chat-panel');
        if (chat.is(':visible')){
          $(`#chat_${sessionStorage.getItem('id-open-chat')}`).children().addClass('active-chat'); ;
        }
      };
    },
    error: function(xhr, status, error) {
      console.log(error);
      // Handle any errors
    },
  });
});







