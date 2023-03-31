

function СhangeElemNavig(){
    const list = document.querySelectorAll('.list');
    const list_activate = document.querySelector('#chats');
    list.forEach((item)=> item.classList.remove('active'));
    list_activate.classList.add('active');
    $(".chat-panel").hide();
};

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
                localStorage['myKey'] = 'somestring';
            }
        });
    }

})

$('.button-send-message').on('click',function(e){
        var chat = document.querySelector('.chat-panel');
        console.log(chat.id)
        $.ajax({
            type: "Get",
            url: "/api/jobs",
            dataType: "json",
            type: 'Get',
            cache: false,
            success: function(data) {
                AddChat()
                console.log(data['jobs'][0])
                
            }
        });
        })

$('.chat_object').on('click',function(e) {
    if ( $(".chat-panel").is(':visible')){
        $(".chat-panel").hide("slow");
    }
    var chat = document.querySelector('.chat-panel');
    chat.setAttribute("id", e.currentTarget.id);


    $(".chat-panel").show("normal");
    $(".chat-box").scrollTop($(".chat-box").prop('scrollHeight'));
})

window.onload = СhangeElemNavig;



function AddChat() {
    var dataItems = [{
        id:1,
        time_message:'12.20',
        username:"Robo Cop22",
        message: $('#from-textarea').val(),
    }];
    $('#template-message-sent').tmpl(dataItems).appendTo('#chat-messages');
}

