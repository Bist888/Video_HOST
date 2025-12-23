Мини‑видеохостинг на Flask
==========================

Проект: небольшое веб‑приложение для загрузки, просмотра, комментирования и оценки (лайк/дизлайк) видео. Используется Python + Flask + SQLite.

## Возможности
- Регистрация и вход пользователей (Flask-Login).
- Загрузка видеофайлов (папка `uploads/`, проверка формата).
- Главная страница со списком видео (гостям показываются только неограниченные).
- Страница видео: просмотр, счётчик просмотров, лайк/дизлайк, комментарии.
- Удаление собственного видео автором или администратором.
- Админ-раздел (blueprint `admin`) для управления пользователями и видео (шаблоны в `templates/admin/`).

## Стек
- Python 3.10+
- Flask 2.x
- Flask-Login 0.6.x
- Flask-SQLAlchemy / SQLAlchemy 2.x
- SQLite (по умолчанию)
- (Опционально) Alembic для миграций

## Структура
- `app.py` — основное приложение, маршруты, регистрация blueprints.
- `models.py` — модели `User`, `Video`, `Comment`, `Like`.
- `templates/` — Jinja2-шаблоны (главная, видео, загрузка, логин/регистрация, админ).
- `static/` — CSS/JS и превьюшки (`static/thumbnails/`).
- `uploads/` — загруженные видеофайлы (создаётся автоматически).

## Как запустить локально
1. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Настроить переменные окружения (пример `.env`):
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=change-me
   SQLALCHEMY_DATABASE_URI=sqlite:///video_hosting.db
   ```
3. Инициализировать БД и создать админа (делается автоматически в `app.py` при первом запуске, логин/пароль admin/admin123).
4. Запустить сервер:
   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```
5. Открыть в браузере: http://localhost:5000

## Основные маршруты
- `GET /` — список видео.
- `GET /video/<id>` — просмотр видео, комментарии, лайки.
- `POST /video/<id>/comment` — добавить комментарий (требуется вход).
- `POST /video/<id>/like`, `POST /video/<id>/dislike` — реакции (требуется вход, JSON-ответ).
- `GET/POST /upload` — загрузка видео (требуется вход).
- `POST /video/<id>/delete` — удалить своё видео или админ.
- `GET /uploads/<filename>` — раздача загруженных файлов.
- `GET/POST /login`, `GET/POST /register`.

## База данных (схема вкратце)
- users (1) — (N) videos
- users (1) — (N) comments
- users (1) — (N) likes
- videos (1) — (N) comments
- videos (1) — (N) likes

Таблицы:
- `users`: id, username, email, password_hash, role, created_at
- `videos`: id, title, description, filename, thumbnail, user_id, created_at, views, is_restricted
- `comments`: id, text, user_id, video_id, created_at
- `likes`: id, user_id, video_id, is_like, created_at, UNIQUE(user_id, video_id)

## Масштабирование (хранение файлов)
- Сейчас: локальная папка `uploads/` — просто и быстро для учебного проекта.
- На рост: вынести файлы в объектное хранилище (S3-совместимое) + CDN; хранить в БД только ключи/URL; включить versioning и бэкапы бакета; фоновые задачи для генерации превью.

## Лицензия
MIT/BSD/Apache-2.0

"- �ࠢ�� 1" 
"- �ࠢ�� 2" 
"- �ࠢ�� 3" 
"- �ࠢ�� 4" 
"- �ࠢ�� 5" 
"- �ࠢ�� 6" 
"- �ࠢ�� 7" 
"- �ࠢ�� 8" 
"- �ࠢ�� 9" 
"- �ࠢ�� 10" 
