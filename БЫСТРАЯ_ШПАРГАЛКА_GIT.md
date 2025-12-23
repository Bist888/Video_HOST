# ⚡ Быстрая шпаргалка: Загрузка на GitHub

## 🚀 Быстрый старт (5 минут)

### 1. Установите Git (если нет)
Скачайте: https://git-scm.com/download/win

### 2. Настройте Git (первый раз)
```bash
git config --global user.name "Ваше Имя"
git config --global user.email "ваш.email@example.com"
```

### 3. Создайте репозиторий на GitHub
- Зайдите на https://github.com
- Нажмите "+" → "New repository"
- Название: `video-hosting`
- Нажмите "Create repository"

### 4. Инициализируйте Git в проекте
```bash
cd C:\Users\studentColl\Desktop\XXS
git init
```

### 5. Создайте историю коммитов

**Вариант А (автоматически):**
```bash
# Запустите скрипт (Windows)
create_git_history.bat
```

**Вариант Б (вручную):**
```bash
git add .
git commit -m "feat: начальный коммит проекта видеохостинга"
```

### 6. Подключите к GitHub
```bash
# Замените URL на ваш репозиторий!
git remote add origin https://github.com/ваш-username/video-hosting.git
git branch -M main
git push -u origin main
```

## 📋 Минимальный набор команд

```bash
# 1. Инициализация
git init

# 2. Добавить все файлы
git add .

# 3. Создать коммит
git commit -m "описание изменений"

# 4. Подключить GitHub (один раз)
git remote add origin https://github.com/ваш-username/название.git

# 5. Отправить на GitHub
git push -u origin main
```

## 🔑 Авторизация на GitHub

GitHub больше не принимает пароли. Используйте **Personal Access Token**:

1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Выберите `repo` (полный доступ)
5. Скопируйте токен
6. Используйте токен вместо пароля при `git push`

## ✅ Чек-лист перед отправкой

- [ ] Git инициализирован (`git init`)
- [ ] Все файлы добавлены (`git add .`)
- [ ] Создан коммит (`git commit`)
- [ ] Репозиторий создан на GitHub
- [ ] Подключен remote (`git remote add origin`)
- [ ] Код отправлен (`git push`)

## 🆘 Частые проблемы

**"fatal: not a git repository"**
→ Выполните `git init`

**"fatal: remote origin already exists"**
→ `git remote remove origin` затем `git remote add origin URL`

**"Permission denied"**
→ Используйте Personal Access Token вместо пароля

**"Large files detected"**
→ Убедитесь, что `uploads/` в `.gitignore`

## 📚 Подробная инструкция

См. файл: `КАК_ЗАГРУЗИТЬ_НА_GITHUB.md`

---

**Готово! 🎉**

