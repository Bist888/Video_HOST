@echo off
REM Скрипт для создания истории коммитов Git
REM Запустите этот файл после git init

echo ========================================
echo Создание истории коммитов Git
echo ========================================
echo.

REM Проверка инициализации Git
if not exist .git (
    echo Ошибка: Git репозиторий не инициализирован!
    echo Выполните: git init
    pause
    exit /b 1
)

echo [1/10] Базовая структура проекта...
git add README.md requirements.txt .gitignore
git commit -m "feat: добавлена базовая структура проекта и зависимости"
echo ✓

echo [2/10] Модели базы данных...
git add models.py
git commit -m "feat: созданы модели базы данных (User, Video, Comment, Like)"
echo ✓

echo [3/10] Система авторизации...
git add auth.py templates/login.html templates/register.html
git commit -m "feat: реализована система регистрации и авторизации пользователей"
echo ✓

echo [4/10] Главная страница и шаблоны...
git add templates/base.html templates/index.html static/css/style.css static/js/main.js
git commit -m "feat: создан базовый интерфейс и главная страница"
echo ✓

echo [5/10] Функционал загрузки видео...
git add templates/upload.html
git commit -m "feat: добавлена страница загрузки видеороликов"
echo ✓

echo [6/10] Просмотр видео...
git add templates/video_detail.html
git commit -m "feat: реализована страница просмотра видео с плеером"
echo ✓

echo [7/10] Лайки и комментарии...
git add app.py
git commit -m "feat: добавлен функционал лайков, дизлайков и комментариев"
echo ✓

echo [8/10] Админ-панель...
git add admin.py templates/admin/
git commit -m "feat: создана административная панель для управления контентом"
echo ✓

echo [9/10] Документация...
git add ОБЪЯСНЕНИЕ_ПРОЕКТА.md ПРЕЗЕНТАЦИЯ.md ИНСТРУКЦИЯ_ПО_ЗАПУСКУ.md КАК_ЗАГРУЗИТЬ_НА_GITHUB.md
git commit -m "docs: добавлена документация проекта и инструкции"
echo ✓

echo [10/10] Финальные правки...
git add .
git commit -m "fix: финальные правки и улучшения"
echo ✓

echo.
echo ========================================
echo История коммитов создана успешно!
echo ========================================
echo.
echo Теперь выполните:
echo   1. git remote add origin https://github.com/ваш-username/название-репозитория.git
echo   2. git branch -M main
echo   3. git push -u origin main
echo.
pause

