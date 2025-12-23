from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Модель пользователя"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # guest, user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    videos = db.relationship('Video', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    
    def set_password(self, password):
        """Установка пароля с хешированием"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Проверка, является ли пользователь администратором"""
        return self.role == 'admin'

class Video(db.Model):
    """Модель видеоролика"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(255))  # Путь к превью
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    is_restricted = db.Column(db.Boolean, default=False)  # Ограничение от администратора
    
    # Связи
    comments = db.relationship('Comment', backref='video', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='video', lazy=True, cascade='all, delete-orphan')
    
    def get_likes_count(self):
        """Получить количество лайков"""
        return Like.query.filter_by(video_id=self.id, is_like=True).count()
    
    def get_dislikes_count(self):
        """Получить количество дизлайков"""
        return Like.query.filter_by(video_id=self.id, is_like=False).count()

class Comment(db.Model):
    """Модель комментария"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Like(db.Model):
    """Модель лайка/дизлайка"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    is_like = db.Column(db.Boolean, nullable=False)  # True - лайк, False - дизлайк
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Уникальность: один пользователь может поставить только один лайк/дизлайк на видео
    __table_args__ = (db.UniqueConstraint('user_id', 'video_id'),)

