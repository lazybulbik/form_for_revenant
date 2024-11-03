tg = window.Telegram.WebApp;

tg.BackButton.show();
tg.BackButton.onClick(() => {
    window.location.href = '/';
})

async function hide_el(el) {
    el.style.opacity = 0

    setTimeout(() => {
        el.style.display = 'none'
    }, 300)
}
async function show_el(el) {
    el.style.display = 'block'
    el.style.opacity = 1
}

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/is_admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: tg.initDataUnsafe.user.id,
        })
    }).then(response => response.json())
    .then(data => {
        if (data['status']) {
            tg.MainButton.show();
            tg.MainButton.setParams({
                'color': '#9159ff',
                'text': "Создать чат"
            })        
        }
    })
})

tg.MainButton.onClick(() => {
    let chats = document.getElementById('chats')
    let create = document.getElementById('create')

    if (chats.style.display == 'none') {
        hide_el(create)
        setTimeout(() => {
            show_el(chats)
        }, 300)

        tg.MainButton.setParams({
            'color': '#9159ff',
            'text': "Создать чат"
        })        
    } else {
        hide_el(chats)
        setTimeout(() => {
            show_el(create)
        }, 300)

        tg.MainButton.setParams({
            'color': '#9159ff',
            'text': "< Вернуться"
        })
    }
})

document.querySelectorAll('.chat').forEach(el => {
    let timer = null
    
    el.addEventListener('contextmenu', e => {
        e.preventDefault();
        tg.showPopup({
            'message': 'Вы уверены, что хотите удалить этот чат?',
            'buttons': [
                {
                    'id': 'delete',
                    'text': 'Удалить',
                    'type': 'destructive'
                }
            ]
        })
        navigator.vibrate(50);
    })
    el.addEventListener('touchstart', e => {
        timer = setTimeout(() => {
            tg.showPopup({
                'message': 'Вы уверены, что хотите удалить этот чат?',
                'buttons': [
                    {
                        'id': 'delete',
                        'text': 'Удалить',
                        'type': 'destructive'
                    }
                ]
            })
            navigator.vibrate(50);
        }, 800)
    })
    el.addEventListener('touchend', () => {
        clearTimeout(timer)
    })

})

tg.onEvent('popupClosed', async function(eventData) {})