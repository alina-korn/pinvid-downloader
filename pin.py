import tkinter as tk
from yt_dlp import YoutubeDL
import os

def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename

def download_pinterest_video(url):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'download/%(title)s.%(ext)s',
        'quiet': True,
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
            result_label.config(text=f"✅ Скачано: {video_title}")
        except Exception as e:
            result_label.config(text=f"❌ Ошибка: {e}")

def start_download():
    url = url_entry.get()
    if url:
        download_pinterest_video(url)
    else:
        result_label.config(text="Введите URL!")

# Создание окна
root = tk.Tk()
root.title("Pinterest Video Downloader")
root.geometry("400x200")

# Элементы интерфейса
url_label = tk.Label(root, text="Введите URL видео:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Скачать", command=start_download)
download_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()




