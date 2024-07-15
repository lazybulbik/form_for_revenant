let tg = window.Telegram.WebApp;

function chec_sub() {
    tg.checkChatMember('10012382913').then(isMember => {
        if (!isMember) {
            tg.sendMessage('10012382913', 'Вы не являетесь участником группы Тропчики. Обратитесь к администраторам группы, чтобы присоединиться к нам.');
            return;
        }
    });
}
