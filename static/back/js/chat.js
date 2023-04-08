

function СhangeElemNavig(){
    const list = document.querySelectorAll('.list');
    const list_activate = document.querySelector('#chats');
    list.forEach((item)=> item.classList.remove('active'));
    list_activate.classList.add('active');
};

function morph(int, array) {
    return (array = array || ['участник', 'участника', 'участников']) && array[(int % 100 > 4 && int % 100 < 20) ? 2 : [2, 0, 1, 1, 1, 2][(int % 10 < 5) ? int % 10 : 5]];
}

$(document).ready(function() {

    show();

    function show() {
        $.ajax({
            type: "Get",
            url: "/api/jobs",
            dataType: "json",
            type: 'Get',
            cache: false,
            success: function(data) {
                console.log(data['jobs'][0])
                setTimeout(function() {show();}, 5000);
            }
        });
    }

})

$('.button-send-message').on('click',function(e){
        var chat = document.querySelector('.chat-panel');
        const data = {
            chat_id: sessionStorage.getItem('id-open-chat'),
            text: $('#from-textarea').val()
          };
        
          $.ajax({
            method: 'POST',
            url: '/api/message',
            data: JSON.stringify(data),
            dataType: 'json',
            cache: false,
            contentType:"application/json",
            processData: false,
            success: function(response) {
              console.log(response)
            },
            error: function(xhr, status, error) {
              console.log(error);
                    // Handle any errors
            },
          });
        });

$('.chat_object').on('click', function(e) {
    var chat = $('.chat-panel');
    if (chat.is(':visible') && e.currentTarget.id === sessionStorage.getItem('id-open-chat')) {
        $(this).children().removeClass('active-chat');  
        chat.animate({width: 'toggle'}, "slow");
        return 0;
    }
    else if (chat.is(':visible')){
        chat.animate({width: 'toggle'}, "slow",function() {
            loadChat(e.currentTarget.id);
       });
    }
    else if (!chat.is(':visible')) 
    {
        loadChat(e.currentTarget.id);
    };
    $('#' + sessionStorage.getItem('id-open-chat')).children().removeClass('active-chat');
    sessionStorage.setItem('id-open-chat', e.currentTarget.id);
    $(this).children().addClass('active-chat');   
    chat.animate({width: 'toggle'}, 400);
    $(".chat-box").scrollTop($(".chat-box").prop('scrollHeight'));   
});

function loadChat(idChat) {
    const titleChat = $('#title-chat-in-frame');
    const iconChat = $('#icon-chat');
    const countParticipants = $('.text-count-participants');
    const data = {
        chat_id: idChat
      };
  
    $.ajax({
    type: 'GET',
      url: `/api/chat/${idChat}`,
      dataType: 'json',
      cache: false,
      success: function(data) {
        console.log(`${data.user_participant} ${morph(data.user_participant)}`);
        titleChat.text(data.title);
        countParticipants.text(`${data.user_participant} ${morph(data.user_participant)}`);
        iconChat.attr('src', `data:image/png;base64,${data.icon}`);
      }
    });

    $.ajax({
        type: 'GET',
        url: `/api/messages`,
        data: data,
        dataType: 'json',
        cache: false,
        success: function(data) {
            console.log(data);
          }
        });
  }




window.onunload = СhangeElemNavig

