function kick(button) {
    fetch('/api/kick_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: button.id,
            event_id: document.getElementById('event_id').textContent
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
    })
  }

fetch('/api/users_list', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        event_id: document.getElementById('event_id').textContent
    })
})
.then(response => response.json())
.then(data => {
    let users_list = document.querySelector('.btns_group');

    for (let i = 0; i < data.length; i++) {
        let user_btn = document.createElement('div');        
        user_btn.classList.add('single_block');

        users_list.appendChild(user_btn); // Append the created div to the users_list

        let btn = document.createElement('button');
        btn.classList.add('btn');
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