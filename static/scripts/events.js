tg = window.Telegram.WebApp;

tg.BackButton.show();
tg.BackButton.onClick(() => {
    window.location.href = '/';
})

tg.MainButton.setParams({
    'color': '#9159ff',
    'text': "Создать мероприятие"
})
tg.MainButton.show();

function fill_list(data) {
    document.getElementById('preloader').style.display = 'none';
    data.forEach(el => {
        let list = document.getElementById('events-list');
        let eventBlock = document.createElement('div');
        let eventHeader = document.createElement('div');
        let eventInfo = document.createElement('div');
    
        let eventTitle = document.createElement('h3');
        let eventDate = document.createElement('p');
    
        let creator = document.createElement('p');
        let address = document.createElement('p');
        let time = document.createElement('p');
    
        let button = document.createElement('button');
    
        // ---
    
        eventBlock.classList.add('event-block');
        eventHeader.classList.add('event-header');
        eventInfo.classList.add('event-info');
        eventTitle.classList.add('event-title');
        eventDate.classList.add('event-date');
    
        creator_link = document.createElement('a');
        creator_link.href = `https://t.me/${el['creator_username']}`;
        creator_link.textContent = `@${el['creator_username']}`;
    
        // ---
    
        eventTitle.textContent = `${el['emoji']} ${el['plan'].length > 20 ? el['plan'].slice(0, 17) + '...' : el['plan']}`;
        eventDate.textContent = `📅 ${el['human_date']}`;
    
        creator.textContent = `👩‍💻 Создатель: `;
        creator.appendChild(creator_link);
    
        address.textContent = `📍 Адрес: ${el['address']}`;
    
        time.textContent = `⏰ ${el['time']}`;
    
        button.textContent = 'Подробнее';
        button.classList.add('btn');
        button.addEventListener('click', () => {
            window.location.href = `/new_event/${el['id']}`;
        });
    
        // ----
        
        eventBlock.style.backgroundImage = `url(${el['cover_url']})`;
    
        eventBlock.appendChild(eventHeader);
        eventBlock.appendChild(eventInfo);
        eventBlock.appendChild(button);
    
        eventHeader.appendChild(eventTitle);
        eventHeader.appendChild(eventDate);
    
        eventInfo.appendChild(creator);
        eventInfo.appendChild(address);
        eventInfo.appendChild(time);
    
        list.appendChild(eventBlock);        
    });

    document.getElementById('events-list').style.opacity = 1;
}


document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/get_events_list', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => response.json())
    .then(data => {
        // console.log(data);

        fill_list(data);
    })

    fetch('/api/get_bot_username', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => response.json())
    .then(data => {
        tg.MainButton.onClick(() => {
            tg.openTelegramLink(`https://t.me/${data['username']}?start=new_event`);
            tg.close();
        })
    })
})