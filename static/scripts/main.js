tg = window.Telegram.WebApp;

tg.expand();
tg.BackButton.hide();

function show_dev_popup() {
    tg.showPopup({
        'title': 'Этот раздел пока в разработке',
        'message': 'Вы можете ускорить его выход, поддержав проект ❤',
    })
}


document.getElementById('events').addEventListener('click', function () {
    window.location.href = '/events';
})

document.getElementById('profile').addEventListener('click', function () {
    window.location.href = `/profile/${tg.initDataUnsafe.user.id}`;
})

document.getElementById('chat').addEventListener('click', function () {
    // show_dev_popup()
    window.location.href = '/chats';
})

document.getElementById('store').addEventListener('click', function () {
    show_dev_popup()
})

document.getElementById('photos').addEventListener('click', function () {
    tg.openTelegramLink('https://t.me/+DuBqBtAQVj00YmMy')
})

document.getElementById('donate').addEventListener('click', function () {
    show_dev_popup()
})

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/get_bot_username', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => response.json())
    .then(data => {
        document.getElementById('write').addEventListener('click', function () {
            // window.location.href = `https://t.me/${data['username']}?start=write`;
            tg.openTelegramLink(`https://t.me/${data['username']}?start=write`)
            tg.close();
        })
    })
})

console.log(tg.initDataUnsafe.user);