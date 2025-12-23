from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_login import LoginManager, login_required, current_user
import os
from werkzeug.utils import secure_filename
from datetime import datetime

from models import db, User, Video, Comment, Like
from auth import auth_bp
from admin import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video_hosting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB максимум

# Создание папок
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/thumbnails', exist_ok=True)

# Инициализация расширений
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Регистрация Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# Разрешенные расширения видео
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Главная страница - список видеороликов"""
    # Гости видят только неограниченные видео
    if not current_user.is_authenticated:
        videos = Video.query.filter_by(is_restricted=False).order_by(Video.created_at.desc()).all()
    # Пользователи видят все видео
    else:
        videos = Video.query.order_by(Video.created_at.desc()).all()
    
    return render_template('index.html', videos=videos)

@app.route('/video/<int:video_id>')
def video_detail(video_id):
    """Страница просмотра видео"""
    video = Video.query.get_or_404(video_id)
    
    # Проверка ограничений для гостей
    if not current_user.is_authenticated and video.is_restricted:
        flash('Это видео доступно только зарегистрированным пользователям', 'error')
        return redirect(url_for('index'))
    
    # Увеличение счетчика просмотров
    video.views += 1
    db.session.commit()
    
    # Получение комментариев
    comments = Comment.query.filter_by(video_id=video_id).order_by(Comment.created_at.desc()).all()
    
    # Проверка лайка/дизлайка текущего пользователя
    user_like = None
    if current_user.is_authenticated:
        user_like = Like.query.filter_by(user_id=current_user.id, video_id=video_id).first()
    
    likes_count = video.get_likes_count()
    dislikes_count = video.get_dislikes_count()
    
    return render_template('video_detail.html', 
                         video=video, 
                         comments=comments,
                         user_like=user_like,
                         likes_count=likes_count,
                         dislikes_count=dislikes_count)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Загрузка видеоролика"""
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('Файл не выбран', 'error')
            return redirect(request.url)
        
        file = request.files['video']
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        if file.filename == '':
            flash('Файл не выбран', 'error')
            return redirect(request.url)
        
        if not title:
            flash('Введите название видео', 'error')
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash('Недопустимый формат файла. Разрешены: mp4, avi, mov, wmv, flv, webm, mkv', 'error')
            return redirect(request.url)
        
        # Сохранение файла
        original_filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Сохраняем только имя файла, а не полный путь
        # Это обеспечит кроссплатформенность (Windows/Linux)
        
        # Создание записи в БД
        video = Video(
            title=title,
            description=description,
            filename=filename,  # Только имя файла, без пути
            user_id=current_user.id
        )
        
        db.session.add(video)
        db.session.commit()
        
        flash('Видео успешно загружено!', 'success')
        return redirect(url_for('video_detail', video_id=video.id))
    
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Отдача загруженных видео файлов"""
    # Безопасная обработка имени файла
    filename = secure_filename(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/video/<int:video_id>/like', methods=['POST'])
@login_required
def like_video(video_id):
    """Лайк видеоролика"""
    video = Video.query.get_or_404(video_id)
    
    # Проверка существующего лайка/дизлайка
    existing_like = Like.query.filter_by(user_id=current_user.id, video_id=video_id).first()
    
    if existing_like:
        if existing_like.is_like:
            # Если уже лайкнуто, убираем лайк
            db.session.delete(existing_like)
            action = 'removed'
        else:
            # Если был дизлайк, меняем на лайк
            existing_like.is_like = True
            action = 'liked'
    else:
        # Создаем новый лайк
        like = Like(user_id=current_user.id, video_id=video_id, is_like=True)
        db.session.add(like)
        action = 'liked'
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'action': action,
        'likes': video.get_likes_count(),
        'dislikes': video.get_dislikes_count()
    })

@app.route('/video/<int:video_id>/dislike', methods=['POST'])
@login_required
def dislike_video(video_id):
    """Дизлайк видеоролика"""
    video = Video.query.get_or_404(video_id)
    
    # Проверка существующего лайка/дизлайка
    existing_like = Like.query.filter_by(user_id=current_user.id, video_id=video_id).first()
    
    if existing_like:
        if not existing_like.is_like:
            # Если уже дизлайкнуто, убираем дизлайк
            db.session.delete(existing_like)
            action = 'removed'
        else:
            # Если был лайк, меняем на дизлайк
            existing_like.is_like = False
            action = 'disliked'
    else:
        # Создаем новый дизлайк
        dislike = Like(user_id=current_user.id, video_id=video_id, is_like=False)
        db.session.add(dislike)
        action = 'disliked'
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'action': action,
        'likes': video.get_likes_count(),
        'dislikes': video.get_dislikes_count()
    })

@app.route('/video/<int:video_id>/comment', methods=['POST'])
@login_required
def add_comment(video_id):
    """Добавление комментария к видео"""
    video = Video.query.get_or_404(video_id)
    text = request.form.get('text', '').strip()
    
    if not text:
        flash('Комментарий не может быть пустым', 'error')
        return redirect(url_for('video_detail', video_id=video_id))
    
    comment = Comment(
        text=text,
        user_id=current_user.id,
        video_id=video_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Комментарий добавлен', 'success')
    return redirect(url_for('video_detail', video_id=video_id))

@app.route('/video/<int:video_id>/delete', methods=['POST'])
@login_required
def delete_video(video_id):
    """Удаление собственного видео пользователем"""
    video = Video.query.get_or_404(video_id)
    
    # Только автор или администратор может удалить
    if video.user_id != current_user.id and not current_user.is_admin():
        flash('У вас нет прав для удаления этого видео', 'error')
        return redirect(url_for('video_detail', video_id=video_id))
    
    # Удаление файла
    if os.path.exists(video.filename):
        try:
            os.remove(video.filename)
        except:
            pass
    
    db.session.delete(video)
    db.session.commit()
    
    flash('Видео удалено', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Создание администратора по умолчанию
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@admin.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Создан администратор: username='admin', password='admin123'")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

