tg = Telegram.WebApp;

document.getElementById('cancel-confirm').addEventListener('click', async function () {
    reason = document.getElementById('cancel-reason').value

    if (!reason) {
        return
    }

    fetch('/api/cancel_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            event_id: document.getElementById('event_id').value,
            reason: reason
        })
    })

    window.location.reload()
})


document.querySelectorAll('.set-remind').forEach(el => el.addEventListener('click', async function () {
    fetch('/api/set_notify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: window.Telegram.WebApp.initDataUnsafe.user.id,
            event_id: document.getElementById('event_id').value,
            notify: this.id
        })
    })
    .then (response => response.json())
    .then (data => {
        if (data['status'] == 'add') {
            this.innerHTML = '✅ ' + this.innerHTML;
        }
        else {
            this.innerHTML = this.innerHTML.slice(2);
        }
    })
}))


document.getElementById('mail-confirm').addEventListener('click', async function () {
    if (!document.getElementById('mail-message').value) {
        return
    }
    fetch('/api/make_mailing', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            event_id: document.getElementById('event_id').value,
            message: document.getElementById('mail-message').value
        })
    })
    document.getElementById('mail-confirm').style.backgroundColor = 'green'
    document.getElementById('mail-confirm').innerHTML = '✅ Отправлено'
    document.getElementById('mail-message').value = ''
    window.navigator.vibrate(50);
    setTimeout(() => {
        document.getElementById('popup').style.bottom = '-100%'
        document.getElementById('mail-popup').style.display = 'none'        
        document.getElementById('mail-confirm').style.backgroundColor = 'var(--tg-theme-button-color)'
        document.getElementById('mail-confirm').innerHTML = 'Отправить'
    }, 2000)
})


document.getElementById('finish-confirm').addEventListener('click', async function () {
    fetch('/api/complete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            event_id: document.getElementById('event_id').value,
            photo_url: document.getElementById('finish-link').value
        })
    })

    window.location.reload()
})