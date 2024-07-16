let tg = window.Telegram.WebApp;

let btn_show = document.getElementById('show_users');
let admin_btns = document.querySelector('.admin');
let user_btns = document.querySelector('.user');

btn_show.addEventListener('click', function() {
    let users_list = document.querySelector('.users_info');

    if (users_list.classList.contains('show')) {
        users_list.classList.remove('show');
        btn_show.textContent = '👀 Посмотреть участников';
        
        users_list.addEventListener('transitionend', function() {
            users_list.style.display = 'none';
        });
    } else {
        users_list.style.display = 'flex';
        setTimeout(function() {
            users_list.classList.add('show');
            btn_show.textContent = '❌ Скрыть участников';
        }, 0);
    }
});


tg.getMe().then(function(me) {
  return tg.getChatMember({
    chat_id: -1002165833102,
    user_id: me.id
  });
}).then(function(chatMember) {
  if (chatMember.status === 'administrator' || chatMember.status === 'creator' || chatMember.status === 'member') {
    admin_btns.style.display = 'flex';
    user_btns.style.display = 'none';

  } else {
    admin_btns.style.display = 'none';
    user_btns.style.display = 'flex';
  }
}).catch(function(err) {
  console.log(err);
});