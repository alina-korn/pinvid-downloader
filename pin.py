


import tkinter as tk
from tkinter import ttk
import threading
import logging
import re
import os
from yt_dlp import YoutubeDL

# Настройка логирования
logging.basicConfig(
    filename='video_downloader.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Создание окна
root = tk.Tk()
root.title("Pinterest Video Downloader")
root.geometry("400x200")

# Элементы интерфейса
url_label = tk.Label(root, text="Введите URL видео:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Скачать", command=lambda: start_download())
download_button.pack(pady=10)

progress = ttk.Progressbar(root, mode='indeterminate')  # Прогресс-бар
progress.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

def get_unique_filename(filename):
    """Генерирует уникальное имя файла, если такой уже существует."""
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename

def is_valid_pinterest_url(url):
    """Проверяет, является ли URL валидным для Pinterest."""
    pattern = r'^(https?://(www\.)?pinterest\..+/.+/?)$'
    return bool(re.match(pattern, url))

def download_pinterest_video(url):
    """Скачивает видео с Pinterest и обновляет интерфейс."""
    logging.info(f"Начато скачивание видео с URL: {url}")
    progress.start()  # Запуск прогресс-бара
    download_button.config(state="disabled")  # Блокировка кнопки во время загрузки

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'download/%(title)s.%(ext)s',
        'quiet': True,
    }

    # Создание папки для загрузок, если её нет
    if not os.path.exists("download"):
        os.makedirs("download")

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            filename = f"download/{video_title}.mp4"
            unique_filename = get_unique_filename(filename)
            
            if filename != unique_filename and os.path.exists(filename):
                os.rename(filename, unique_filename)
            
            result_label.config(text=f"✅ Скачано: {video_title}")
            logging.info(f"Видео успешно скачано: {unique_filename}")
        except Exception as e:
            result_label.config(text=f"❌ Ошибка: {str(e)}")
            logging.error(f"Ошибка при скачивании {url}: {str(e)}")
        finally:
            progress.stop()  # Остановка прогресс-бара
            download_button.config(state="normal")  # Разблокировка кнопки

def start_download():
    """Запускает процесс скачивания в отдельном потоке."""
    url = url_entry.get().strip()
    
    if not url:
        result_label.config(text="Введите URL!")
        logging.warning("Попытка скачивания без URL")
        return
    
    if not is_valid_pinterest_url(url):
        result_label.config(text="Введите корректный Pinterest URL!")
        logging.warning(f"Некорректный URL: {url}")
        return
    
    result_label.config(text="⏳ Скачивание началось...")
    # Запуск скачивания в отдельном потоке
    thread = threading.Thread(target=download_pinterest_video, args=(url,))
    thread.start()

# Запуск основного цикла приложения
root.mainloop()

