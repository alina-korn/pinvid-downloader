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
root.geometry("400x250")  # Увеличиваем окно для нового элемента

# Элементы интерфейса
url_label = tk.Label(root, text="Введите URL видео:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Добавляем выбор качества видео
quality_label = tk.Label(root, text="Выберите качество видео:")
quality_label.pack(pady=5)

quality_var = tk.StringVar(value="best")  # Значение по умолчанию
quality_options = ["best", "720p", "480p", "360p"]
quality_menu = ttk.Combobox(root, textvariable=quality_var, values=quality_options, state="readonly")
quality_menu.pack(pady=5)

download_button = tk.Button(root, text="Скачать", command=lambda: start_download())
download_button.pack(pady=10)

progress = ttk.Progressbar(root, mode='indeterminate')
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

def get_format_string(quality):
    """Возвращает строку формата для yt-dlp в зависимости от выбранного качества."""
    if quality == "best":
        return "bestvideo+bestaudio/best"
    elif quality == "720p":
        return "bestvideo[height<=720]+bestaudio/best[height<=720]"
    elif quality == "480p":
        return "bestvideo[height<=480]+bestaudio/best[height<=480]"
    elif quality == "360p":
        return "bestvideo[height<=360]+bestaudio/best[height<=360]"
    return "best"  # На случай ошибки

def download_pinterest_video(url, quality):
    """Скачивает видео с Pinterest с учетом выбранного качества."""
    logging.info(f"Начато скачивание видео с URL: {url}, качество: {quality}")
    progress.start()
    download_button.config(state="disabled")

    ydl_opts = {
        'format': get_format_string(quality),
        'outtmpl': 'download/%(title)s.%(ext)s',
        'quiet': True,
        'merge_output_format': 'mp4',  # Обеспечиваем выходной формат mp4
    }

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
            
            result_label.config(text=f"✅ Скачано: {video_title} ({quality})")
            logging.info(f"Видео успешно скачано: {unique_filename}")
        except Exception as e:
            result_label.config(text=f"❌ Ошибка: {str(e)}")
            logging.error(f"Ошибка при скачивании {url}: {str(e)}")
        finally:
            progress.stop()
            download_button.config(state="normal")

def start_download():
    """Запускает процесс скачивания в отдельном потоке."""
    url = url_entry.get().strip()
    quality = quality_var.get()
    
    if not url:
        result_label.config(text="Введите URL!")
        logging.warning("Попытка скачивания без URL")
        return
    
    if not is_valid_pinterest_url(url):
        result_label.config(text="Введите корректный Pinterest URL!")
        logging.warning(f"Некорректный URL: {url}")
        return
    
    result_label.config(text="⏳ Скачивание началось...")
    thread = threading.Thread(target=download_pinterest_video, args=(url, quality))
    thread.start()

# Запуск основного цикла приложения
root.mainloop()

