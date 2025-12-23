from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Video, User

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Декоратор для проверки прав администратора"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Доступ запрещен. Требуются права администратора.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/videos')
@login_required
@admin_required
def video_list():
    """Список всех видеороликов для администратора"""
    videos = Video.query.order_by(Video.created_at.desc()).all()
    return render_template('admin/video_list.html', videos=videos)

@admin_bp.route('/admin/video/<int:video_id>/toggle_restriction', methods=['POST'])
@login_required
@admin_required
def toggle_restriction(video_id):
    """Включение/выключение ограничения на видео"""
    video = Video.query.get_or_404(video_id)
    video.is_restricted = not video.is_restricted
    db.session.commit()
    
    status = 'ограничено' if video.is_restricted else 'разрешено'
    flash(f'Видео "{video.title}" теперь {status}', 'success')
    return redirect(url_for('admin.video_list'))

@admin_bp.route('/admin/video/<int:video_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_video(video_id):
    """Удаление видео администратором"""
    video = Video.query.get_or_404(video_id)
    title = video.title
    
    # Удаление файла видео
    import os
    if os.path.exists(video.filename):
        try:
            os.remove(video.filename)
        except:
            pass
    
    db.session.delete(video)
    db.session.commit()
    
    flash(f'Видео "{title}" удалено', 'success')
    return redirect(url_for('admin.video_list'))

@admin_bp.route('/admin/users')
@login_required
@admin_required
def user_list():
    """Список всех пользователей для администратора"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/user_list.html', users=users)

