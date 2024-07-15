let tg = window.Telegram.WebApp;

function chec_sub() {
    tg.checkChatMember('-10012382913').then(isMember => {
        if (isMember) {
            document.write('Вы подписаны');
            return;
        }
    });
}

tg.MainButton.render();

chec_sub();