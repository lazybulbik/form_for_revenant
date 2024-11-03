tg = window.Telegram.WebApp;

tg.BackButton.show();
tg.BackButton.onClick(() => {
    window.history.back()
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
        el.style.display = 'flex';
    }, 300);
    setTimeout(() => {
        el.style.opacity = '1';
    }, 10);
}


document.getElementById('basic-tab').addEventListener('click', function () {
    document.getElementById('basic-tab').classList.add('selected')
    document.getElementById('personal-tab').classList.remove('selected')

    hide_el(document.getElementById('personal'))
    show_el(document.getElementById('basic'))
})

document.getElementById('personal-tab').addEventListener('click', function () {
    document.getElementById('basic-tab').classList.remove('selected')
    document.getElementById('personal-tab').classList.add('selected')

    hide_el(document.getElementById('basic'))
    show_el(document.getElementById('personal'))
})