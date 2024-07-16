let tg = window.Telegram.WebApp;

let btn_show = document.getElementById('show_users');
let admin_btns = document.querySelector('.admin');
let user_btns = document.querySelector('.user');

btn_show.addEventListener('click', function() {
    let users_list = document.querySelector('.users_info');
    let user_columns = document.querySelectorAll('.user_column');

    if (users_list.classList.contains('show')) {
        users_list.classList.remove('show');
        btn_show.textContent = '👀 Посмотреть участников';

        return
    } else {
        users_list.classList.add('show');
        btn_show.textContent = '❌ Скрыть участников';

        return
    }
});

fetch('api/is_admin', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        user_id: tg.initDataUnsafe.user.id
    })
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
})
.then(data => {
    console.log(data);
    if (data.status === true) {
        admin_btns.style.display = 'block';
        user_btns.style.display = 'none';
    }
    else {
        admin_btns.style.display = 'none';
        user_btns.style.display = 'block';
    }
})