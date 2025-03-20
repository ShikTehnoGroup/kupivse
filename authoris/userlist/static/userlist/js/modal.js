document.addEventListener('DOMContentLoaded', function() {
    // Получаем модальное окно
    var modal = document.getElementById("registrationModal");

    // Получаем кнопку, которая открывает модальное окно
    var btn = document.getElementById("openModal");

    // Проверяем, существует ли кнопка
    if (!btn) {
        console.error('Кнопка с ID "openModal" не найдена.');
        return;
    }

    // Получаем элемент <span>, который закрывает модальное окно
    var span = document.getElementsByClassName("close")[0];

    // Получаем URL для регистрации из data-атрибута
    var registerUrl = btn.getAttribute('data-url');

    // Когда пользователь нажимает на кнопку, открывается модальное окно
    btn.onclick = function(event) {
        event.preventDefault(); // Предотвращаем переход по ссылке

        // Загружаем форму регистрации через AJAX
        fetch(registerUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                document.getElementById("modalFormContent").innerHTML = data;
                modal.style.display = "block"; // Показываем модальное окно
            })
            .catch(error => console.error('Error loading the registration form:', error));
    }

    // Когда пользователь нажимает на <span> (x), закрывается модальное окно
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Когда пользователь нажимает в любом месте вне модального окна, оно закрывается
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Обработчик отправки формы
    document.addEventListener('submit', function(event) {
        if (event.target.matches('#registrationForm')) {
            event.preventDefault(); // Предотвращаем стандартное поведение формы

            const formData = new FormData(event.target);
            const csrfToken = formData.get('csrfmiddlewaretoken'); // Извлекаем CSRF-токен из формы

            // Выводим CSRF-токен в консоль
            console.log('CSRF Token:', csrfToken);

            fetch(registerUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', // Указываем, что это AJAX-запрос
                    'X-CSRFToken': csrfToken // Добавляем CSRF-токен в заголовок
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        // Обработка ошибок валидации
                        const errors = data.errors;
                        console.log(errors);
                        // Здесь вы можете отобразить ошибки на форме
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // alert(data.message);
                    window.location.href = data.redirect_url; // Перенаправление на указанный URL
                }
            })
            .catch(error => console.error('Ошибка при регистрации:', error));
        }
    });
});