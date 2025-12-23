// Основной JavaScript файл

document.addEventListener('DOMContentLoaded', function() {
    // Автоматическое скрытие flash сообщений через 5 секунд
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
    
    // Получение длительности видео для превью
    const videoThumbnails = document.querySelectorAll('.video-thumbnail video');
    videoThumbnails.forEach(function(video) {
        video.addEventListener('loadedmetadata', function() {
            const duration = video.duration;
            const minutes = Math.floor(duration / 60);
            const seconds = Math.floor(duration % 60);
            const durationText = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            
            const durationElement = video.parentElement.querySelector('.video-duration');
            if (durationElement) {
                durationElement.textContent = durationText;
            }
        });
    });
    
    // Валидация формы регистрации
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        
        if (password && confirmPassword) {
            confirmPassword.addEventListener('input', function() {
                if (password.value !== confirmPassword.value) {
                    confirmPassword.setCustomValidity('Пароли не совпадают');
                } else {
                    confirmPassword.setCustomValidity('');
                }
            });
        }
    }
});

