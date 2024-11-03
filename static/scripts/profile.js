tg = window.Telegram.WebApp;

tg.BackButton.show();
tg.BackButton.onClick(() => {
    // window.location.href = '/';
    if (window.history.length > 1) {
        window.history.back()
    } else {
        window.location.href = '/';
    }
})

function hide_el(el) {
    el.style.opacity = '0';
    setTimeout(() => {
        el.style.display = 'none';
    }, 300);
}

function show_el(el) {
    el.style.opacity = '0';
    setTimeout(() => {
        el.style.display = 'block';
    }, 300);
    setTimeout(() => {
        el.style.opacity = '1';
    }, 10);
}

let user_id = document.getElementById('user_id').value

document.getElementById('about').addEventListener('click', async function () {
    if (user_id != tg.initDataUnsafe.user.id) {
        return
    }

    this.setAttribute('contenteditable', 'true')

    this.onblur = function() {
        this.setAttribute('contenteditable', 'false')
        if (this.innerHTML == '') {
            this.innerHTML = 'О себе';
        }

        fetch('/api/edit_about', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: window.Telegram.WebApp.initDataUnsafe.user.id,
                about: this.innerHTML
            })
        })
    };
})

document.getElementById('birthday').addEventListener('click', function () {
    if (user_id != tg.initDataUnsafe.user.id) {
        return
    }

    // this.style.display = 'none';
    // document.getElementById('birthday-edit').style.display = 'flex';

    // hide_el(this)
    // show_el(document.getElementById('birthday-edit'))

    console.log('click')
    document.getElementById('birthdayInput').focus();
    document.getElementById('birthdayInput').click();
    document.getElementById('birthdayInput').showPicker();
})

document.getElementById('birthdayInput').addEventListener('input', function () {
    console.log('input')
    console.log(this.value)

    fetch('/api/edit_birthday', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: window.Telegram.WebApp.initDataUnsafe.user.id,
            birthday: document.getElementById('birthdayInput').value
        })
    }).then(response => response.json())
    .then(data => {
        if (data['status']) {
            if (data['birthday']) {
                document.getElementById('birthday').innerHTML = `🎂 ${data['birthday']} (${data['age']}, ${data['zodiac']})`
            } else {
                document.getElementById('birthday').innerHTML = '🎂 Нажмите чтобы указать дату рождения'
            }
        }
    })
})

// document.getElementById('saveBirthday').addEventListener('click', function () {
//     if (document.getElementById('birthdayInput').value.length != 10) {
//         return
//     }
//     fetch('/api/edit_birthday', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             user_id: window.Telegram.WebApp.initDataUnsafe.user.id,
//             birthday: document.getElementById('birthdayInput').value
//         })
//     }).then(response => response.json())
//     .then(data => {
//         if (data['status']) {
//             document.getElementById('birthday').innerHTML = `🎂 ${data['birthday']} (${data['age']}, ${data['zodiac']})`
//         }
//     })
//     hide_el(document.getElementById('birthday-edit'))
//     show_el(document.getElementById('birthday'))
// })

document.getElementById('neuro-block').addEventListener('click', async function () {
    text = document.getElementById('neuro-comment')
    text.style.maxHeight = text.style.maxHeight === '1000vh' ? '100px' : '1000vh';
})


document.addEventListener('DOMContentLoaded', function () {
    fetch(`/api/get_profile_data?user_id=${user_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => response.json())
    .then(data => {
        document.getElementById('about').innerHTML = data['about']
        document.getElementById('name').innerHTML = data['name']
        const img = document.getElementById('avatar');

        if (data['birthday']) {
            document.getElementById('birthday').innerHTML = `🎂 ${data['birthday']} (${data['age']}, ${data['zodiac']})`
        } else {
            if (data['id'] == tg.initDataUnsafe.user.id) {
                document.getElementById('birthday').innerHTML = '🎂 Нажмите чтобы указать дату рождения'
            } else {
                document.getElementById('birthday').innerHTML = '🎂 Дата рождения не указана'
            }
        }

        document.getElementById('rank').innerHTML = `🏅 Ранг: ${data['rank']}`
        // document.getElementById('rating').innerHTML = `⭐️ Рейтинг: ${data['rating']}`
        document.getElementById('create').innerHTML = `🦖 В новотропске с: ${data['create_date']} (${data['days_from_create']})`
        document.getElementById('messages').innerHTML = `💬 Всего сообщений: ${data['stats']['total_msg']}`
        document.getElementById('polls').innerHTML = `🗳 Голосов в Опросах:: ${data['stats']['total_votes']}`
        document.getElementById('skiped-polls').innerHTML = `😔 Пропущено голосований: ${data['stats']['skip_procent']}%`

        img.onload = function() {
            document.getElementById('inner').style.opacity = '1'
        }
        img.onerror = function() {
            document.getElementById('inner').style.opacity = '1'
        }
        img.setAttribute('src', data['photo']);
    })

    fetch('/api/analyze_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: user_id
        })
    }).then(response => response.json())
    .then(data => {
            const culture_index = (data['culture_index'] / 10) * 100
            const friendly_index = (data['friendly_index'] / 10) * 100
            const respons_index = (data['respons_index'] / 10) * 100

        document.getElementById('culture-index').style.width = `${culture_index}%`
        document.getElementById('friendly-index').style.width = `${friendly_index}%`
        document.getElementById('respons-index').style.width = `${respons_index}%`
    })

    fetch('/api/analyze_user_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: user_id
        })
    }).then(response => response.json())
    .then(data => {
        document.getElementById('neuro-comment').innerHTML = data['result'].replace(/\n/g, '<br>')
    })
})