let tg = window.Telegram.WebApp;

tg.expand();

tg.BackButton.show();
tg.BackButton.onClick(() => {
    window.location.href = '/events';
})

async function is_admin() {
    data = await fetch('/api/is_admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: tg.initDataUnsafe.user.id,
            event_id: document.getElementById('event_id').value
        })
    }).then(response => response.json())

    return data['status']
}

async function get_event_data() {
    data = await fetch('/api/get_event_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            event_id: document.getElementById('event_id').value,
            user_id: tg.initDataUnsafe.user.id
        })
    }).then(response => response.json())
    return data
}

document.querySelectorAll('.vote').forEach(btn => {
    btn.addEventListener('click', async function () {
        document.querySelectorAll('.vote').forEach(el => {el.classList.remove('active');el.disabled = false})
        this.classList.toggle('active')
        this.disabled = true
        
        data = await fetch('/api/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                event_id: document.getElementById('event_id').value,
                user_id: tg.initDataUnsafe.user.id,
                vote: this.id
            })
        }).then(response => response.json())

        fill_list(data);
    })
})


document.addEventListener('click', (event) => {
    popup = document.getElementById('popup');
    remindBtn = document.getElementById('remind-btn');
    deleteBtn = document.getElementById('kick-btn');
    mailBtn = document.getElementById('mail-btn');

    // finishBtn = document.getElementById('finish-btn');
    cancelBtn = document.getElementById('cancel-btn');

    const isFinalBtn = cancelBtn.contains(event.target);
    // if (finishBtn) {
    //     console.log('finish')
    //     isFinalBtn = finishBtn.contains(event.target);
    // }

    const isClickInsidePopup = popup.contains(event.target);
    const isRemindBtn = remindBtn.contains(event.target);
    const isDeleteBtn = deleteBtn.contains(event.target);
    const isMailBtn = mailBtn.contains(event.target);

    // Если клик вне попапа и не на хэдере, то скрываем попап
    if (!isClickInsidePopup && !isRemindBtn && !isDeleteBtn && !isMailBtn && !isFinalBtn) {
        popup.style.bottom = '-100%';
        document.querySelectorAll('.popup-content').forEach(el => el.style.display = 'none')
    }
});


async function cancel_btn () {
    document.getElementById('popup').style.bottom = 0
    document.getElementById('cancel-popup').style.display = 'flex'
}


async function finish_btn() {
    document.getElementById('popup').style.bottom = 0
    document.getElementById('finish-popup').style.display = 'flex'
}

document.getElementById('remind-btn').addEventListener('click', async function () {
    buttons = document.querySelectorAll('.set-remind');
    fetch('/api/users_notify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: window.Telegram.WebApp.initDataUnsafe.user.id,
            event_id: document.getElementById('event_id').value
        })
    })
    .then(response => response.json())
    .then(data => {
        buttons.forEach(button => {
            if (data[button.id]) {
                if (button.innerHTML.indexOf('✅') == -1) {
                    button.innerHTML = '✅ ' + button.innerHTML;                
                }
            }
        })
    })

    document.getElementById('popup').style.bottom = 0
    document.getElementById('remind-popup').style.display = 'flex'
})

document.getElementById('kick-btn').addEventListener('click', async function () {
    document.querySelectorAll('.kick-user').forEach(el => el.remove())
    fetch('/api/users_list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            event_id: document.getElementById('event_id').value
        })
    })
    .then(response => response.json())
    .then(data => {
        let users_list = document.getElementById('kick-users-list');
    
        for (let i = 0; i < data.length; i++) {
            let user_btn = document.createElement('div');        
            user_btn.classList.add('space-around', 'margin-top');
    
            users_list.appendChild(user_btn); // Append the created div to the users_list
    
            let btn = document.createElement('button');
            btn.classList.add('kick-user');
            btn.id = data[i]['id'];
            btn.addEventListener('click', () => {kick(btn)});
    
            if (data[i]['kick']) {
                btn.textContent = '❌ ' + data[i]['name'];
            }
            else {
                btn.textContent = '✅ ' + data[i]['name'];
            }
    
            user_btn.appendChild(btn); // Append the created button to the div
        }
    })

    document.getElementById('popup').style.bottom = 0
    document.getElementById('kick-popup').style.display = 'flex'
})

document.getElementById('mail-btn').addEventListener('click', async function () {
    document.getElementById('popup').style.bottom = 0
    document.getElementById('mail-popup').style.display = 'flex'
})


function kick(button) {
    fetch('/api/kick_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: button.id,
            event_id: document.getElementById('event_id').value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data['status'] == 'kick') {
            button.innerHTML = '❌ ' + data['name'];
        }
        else {
            button.innerHTML = '✅ ' + data['name'];
        }
        document.getElementById('type').innerHTML = `🔐 Тип мероприятия: ${data['type']}`
    })
  }


function fill_list(data) {
    document.querySelectorAll('.user').forEach(el => el.remove())

    ready_count = data['ready_users'].length + data['maybe_users'].length
    no_count = data['no_users'].length
    total_count = ready_count + no_count

    document.getElementById('count-ready').innerHTML = `✅ Иду (${ready_count})`
    document.getElementById('count-no').innerHTML = `❌ Не иду (${no_count})`
    document.getElementById('total-count').innerHTML = `Участников проголосовало: ${total_count}`

    data['ready_users'].forEach(user => {
        let list = document.getElementById('ready-users')
        let user_text = document.createElement('div')
        user_text.innerHTML = `✅ `
        user_text.classList.add('base-text', 'user')
        user_text.id = user['name']

        user_link = document.createElement('a')
        user_link.href = `/profile/${user['id']}`  
        user_link.innerHTML = `${user['name']}`

        user_text.appendChild(user_link)

        list.appendChild(user_text)
    })
    data['maybe_users'].forEach(user => {
        let list = document.getElementById('ready-users')
        let user_text = document.createElement('div')
        user_text.classList.add('base-text', 'user')
        user_text.id = user
        user_text.innerHTML = `☑️ `

        user_link = document.createElement('a')
        user_link.href = `/profile/${user['id']}`  
        user_link.innerHTML = `${user['name']}`

        user_text.appendChild(user_link)

        list.appendChild(user_text)
    })
    data['no_users'].forEach(user => {
        let list = document.getElementById('no-users')
        let user_text = document.createElement('div')
        user_text.classList.add('base-text', 'user')
        user_text.id = user
        user_text.innerHTML = `❌ `

        user_link = document.createElement('a')
        user_link.href = `/profile/${user['id']}`  
        user_link.innerHTML = `${user['name']}`

        user_text.appendChild(user_link)

        list.appendChild(user_text)
    })
}


document.addEventListener('DOMContentLoaded', async function() {
    if (await is_admin()) {
        document.getElementById('admin-btns').style.display = 'flex'
    }
    data = await get_event_data()

    document.getElementById('title').innerHTML = `${data['emoji']}  ${data['plan']}`
    document.getElementById('date').innerHTML = `📅 Дата: ${data['date']}`
    document.getElementById('time').innerHTML = `⏰ Время: ${data['time']}`
    document.getElementById('adress').innerHTML = data['adress']
    document.getElementById('adress').href = data['map_link']
    if(data['note']) {
        document.getElementById('note').innerHTML = `📄 Примечание: ${data['note']}`
    } else {
        document.getElementById('note').style.display = 'none'
    }
    document.getElementById('type').innerHTML = `🔐 Тип мероприятия: ${data['event_type']}`
    document.getElementById('creator').innerHTML = `@${data['creator']}`
    document.getElementById('creator').href = `https://t.me/${data['creator']}`

    if(data['user_vote']) {
        document.getElementById(data['user_vote']).classList.add('active')
        document.getElementById(data['user_vote']).disabled = true
    }
    if(data['is_expired']) {
        document.getElementById('cancel-btn').innerHTML = '✅ Завершить меропритие'
        document.getElementById('cancel-btn').addEventListener('click', finish_btn)
        // document.getElementById('cancel-btn').id = 'finish-btn'
    } else {
        document.getElementById('cancel-btn').addEventListener('click', cancel_btn)
    }
    if (data['event_status'] != 'new') {
        document.getElementById(data['event_status']).style.display = 'flex'
        document.getElementById('vote').style.display = 'none'
        document.getElementById('btns').style.display = 'none'
    }
    if (data['photo_url']) {
        document.getElementById('photos').display = 'flex'
        document.getElementById('photos-btn').href = data['photo_url']
    }

    fill_list(data)
    
    document.getElementById('preloader-check').style.display = 'none'
})