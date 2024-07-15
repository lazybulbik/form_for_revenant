let tg = window.Telegram.WebApp;

function chec_sub() {
    var tg_id = tg.initDataUnsafe.user.id;
    var tg_data = tg.initDataUnsafe
    document.write(tg_id);
    // tg.checkChatMember('-10012382913').then(isMember => {
    //     if (isMember) {
    //         document.write('Вы подписаны');
    //         return;
    //     }

    //     document.write('Вы не подписаны');
    // });
}

let field = document.getElementById('input');
let field_2 = document.getElementById('output');

try {
    var tg_data = tg.initDataUnsafe;
    document.getElementById('input').value = tg_data;
    document.getElementById('output').value = 'ok';
    
} catch (error) {

    document.getElementById('input').value = error;
    
}