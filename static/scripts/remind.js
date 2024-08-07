const buttons = document.querySelectorAll('button');

fetch('/api/users_notify', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        user_id: window.Telegram.WebApp.initDataUnsafe.user.id,
        event_id: document.getElementById('event_id').textContent
    })
})
.then(response => response.json())
.then(data => {
    buttons.forEach(button => {
        if (data[button.id]) {
            button.innerHTML = '✅ ' + button.innerHTML;
        }
    })
})

buttons.forEach(button => {
  button.addEventListener('click', () => {
    fetch('/api/set_notify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: window.Telegram.WebApp.initDataUnsafe.user.id,
            event_id: document.getElementById('event_id').textContent,
            notify: button.id
        })
    })
    .then (response => response.json())
    .then (data => {
        if (data['status'] == 'add') {
            button.innerHTML = '✅ ' + button.innerHTML;
        }
        else {
            button.innerHTML = button.innerHTML.slice(2);
        }
    })
})});
