function validateForm(event) {
    const checkboxes_interests = document.querySelectorAll('.form-check-input.interests');
    const checkboxes_finds = document.querySelectorAll('.form-check-input.finds');
    
    const isInterestChecked = Array.from(checkboxes_interests).some(checkbox => checkbox.checked);
    const isFindChecked = Array.from(checkboxes_finds).some(checkbox => checkbox.checked);

    const alertBox = document.createElement('div');
    alertBox.classList.add('alert');
    alertBox.textContent = 'Вы заполнили не все поля';
    
    if (!isInterestChecked || !isFindChecked) {
      document.body.appendChild(alertBox);
      event.preventDefault();
      event.stopPropagation();

      return false;
    }

    // setTimeout(function() {
    //   alertBox.remove();
    // }, 1000);      
    
    return true;
  }

document.addEventListener('DOMContentLoaded', function() {
// Находим форму и добавляем обработчик события submit
const form = document.querySelector('form');
form.addEventListener('submit', validateForm);
});