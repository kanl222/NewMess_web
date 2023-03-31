var plus = "<i class='bi bi-plus-lg'></i>"
var dash ="<i class='bi bi-dash-lg'></i>"

var stringToHTML = function (str) {
	var dom = document.createElement('div');
	dom.innerHTML = str;
	return dom;

};

var list_user_in_chat = []

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

