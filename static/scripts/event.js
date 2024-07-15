let tg = window.Telegram.WebApp;



let field = document.getElementById('input');
let field_2 = document.getElementById('output');

try {
    var tg_data = tg.initDataUnsafe;
    document.getElementById('input').value = tg_data;
    document.getElementById('output').value = 'ok';
    
} catch (error) {

    document.getElementById('input').value = error;
    
}

document.getElementById('test').addEventListener('click', function() {
    document.getElementById('output').value = 'ok';
})