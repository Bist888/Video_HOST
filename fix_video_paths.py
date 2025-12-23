"""
Скрипт для исправления путей к видео в базе данных
Запустите: python fix_video_paths.py
"""

from app import app
from models import db, Video
import os

with app.app_context():
    videos = Video.query.all()
    fixed_count = 0
    
    for video in videos:
        # Получаем имя файла из пути
        original_filename = video.filename
        
        # Обрабатываем путь (работает и с / и с \)
        filename = original_filename.replace('\\', '/').split('/')[-1]
        
        # Проверяем, существует ли файл
        filepath = os.path.join('uploads', filename)
        
        if os.path.exists(filepath) and original_filename != filename:
            print(f"Исправляю: {original_filename} -> {filename}")
            video.filename = filename
            fixed_count += 1
        elif not os.path.exists(filepath):
            print(f"ВНИМАНИЕ: Файл не найден для видео '{video.title}': {filename}")
    
    if fixed_count > 0:
        db.session.commit()
        print(f"\n✓ Исправлено {fixed_count} записей в базе данных")
    else:
        print("\n✓ Все пути уже корректны или файлы не найдены")

