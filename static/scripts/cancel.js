document.querySelector('.form-control-file').addEventListener('change', function(e) {
    let file = e.target.files[0];
    console.log(file.name);

    document.querySelector('.input-file-text').innerHTML = file.name;
})